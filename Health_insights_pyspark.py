# Making connection to Spark Cluster 

# Note - 1 [ creating dedicated spark session is Not required in the notebook , but to run job in dataproc, this is needed ]


from pyspark.sql import SparkSession

spark = SparkSession.builder \
                    .appName("HealthcareDataProcessing") \
                    .getOrCreate()


#Importing important functions

from pyspark.sql.types import StructType, StructField, StringType, IntegerType,DoubleType
from pyspark.sql.functions import *
import google.cloud.logging
import logging

# Initialize Google Cloud Logging
logging_client = google.cloud.logging.Client()
logging_client.setup_logging()
logger = logging.getLogger('healthcare-data-pipeline')

def log_pipeline_step(step, message, level='INFO'):
    
    if level == 'INFO':
        logger.info(f"Step: {step}, Message: {message}")
    elif level == 'ERROR':
        logger.error(f"Step: {step}, Error: {message}")
    elif level == 'WARNING':
        logger.warning(f"Step: {step}, Warning: {message}")

# Defining important variables

gcs_source_file='gs://project-health-data/patients_data/*.json'
gcs_invalid_path='gs://project-health-data/patients_data/invalid/json_data'
BQ_table_id = "temp-prashant.health_data.patients_insights"
gcs_temp_bucket='gs://project-health-data/temp'





# Defining Schema for the json Data

schema = StructType([
    StructField("patient_id", StringType(), True),
    StructField("heart_rate", IntegerType(), True),
    StructField("blood_pressure", IntegerType(), True),
    StructField("temperature", DoubleType(), True),
    StructField("timestamp", StringType(), True)
])


# Validating Data 


def validate_data(df):    # it will take dataframe as input and give 2 dataframe as output, Valid and Invalid DataFrame
    
    log_pipeline_step("Data Validation", "Starting data validation.")
    
    df1=df.withColumn("is_valid", when((col("heart_rate") > 40) & (col("heart_rate") < 200) & 
                                                  (col("blood_pressure") > 50) & (col("blood_pressure") < 200) & 
                                                  (col("temperature") > 35.0) & (col("temperature") < 42.0), True).otherwise(False))
    valid_records=df1.filter(col("is_valid") == True)
    Invalid_records=df1.filter(col("is_valid") == False)
    
    log_pipeline_step("Data Validation", f"Valid records: {valid_records.count()}, Invalid records: {Invalid_records.count()}")
    
    return valid_records,Invalid_records


# Main Processing Function

def process_data():
    
    # Step 1: Read raw data from GCS
    
    log_pipeline_step("Data Ingestion", "Reading raw data from GCS.")
    
    df = spark.read \
    .format("json") \
    .schema(schema) \
    .load(gcs_source_file)
    
    # Step 2: Validate data
    
    valid_df,invalid_df=validate_data(df)
    
    # Step 3: Log invalid records (for auditing)
    
    if invalid_df.count() > 0:
        
        log_pipeline_step("Invalid Data", "Found invalid records.", level='WARNING')
        invalid_df.write \
        .mode("append") \
        .format("json") \
        .save(gcs_invalid_path)
        

        
    
     # Step 4: Data Transformation - Aggregate by patient_id
        
    df_agg = valid_df.groupBy("patient_id").agg(
                                                    round(avg("heart_rate"), 2).alias("avg_heart_rate"),
                                                    round(avg("blood_pressure"), 2).alias("avg_blood_pressure"),
                                                    round(avg("temperature"), 2).alias("avg_temperature")
                                                ) 
    # Step 5: Calculate standard deviation for heart rate and blood pressure for each patient
    
    log_pipeline_step("Data Transformation", "Calculating standard deviation for heart rate and blood pressure.")
    
    df_stddev = valid_df.groupBy("patient_id").agg(
                                                        stddev("heart_rate").alias("stddev_heart_rate"),
                                                        stddev("blood_pressure").alias("stddev_blood_pressure"),
                                                        stddev("temperature").alias("stddev_temperature")
                                                    )
    # Step 6: Join the aggregated data with standard deviation metrics
    
    log_pipeline_step("Data Transformation", "Joining aggregated data with standard deviation metrics.")
    
    df_joined = df_agg.join(df_stddev, on="patient_id")
    
    # Step 8: Flag patients with high average heart rate or high heart rate variation
    
    log_pipeline_step("Data Transformation", "Flagging high-risk patients.")
    
    df_joined = df_joined.withColumn("risk_category", 
                                                        when(col("avg_heart_rate") > 100, "High Risk")
                                                        .when(col("stddev_heart_rate") > 15, "Moderate Risk")
                                                        .otherwise("Low Risk"))
    
    
     # Step 9: Write the aggregated data with risk categorization to BigQuery
      
    log_pipeline_step("Data Write", "Writing aggregated and transformed data to BigQuery.")
    df_joined.write \
    .format("bigquery") \
    .option("table", BQ_table_id) \
    .option("temporaryGcsBucket", gcs_temp_bucket) \
    .mode("overwrite") \
    .save()
    
    

if __name__ == "__main__":
    log_pipeline_step("Pipeline Start", "Healthcare data processing pipeline initiated.")
    process_data()
    log_pipeline_step("Pipeline End", "Healthcare data processing pipeline completed.")
    
    