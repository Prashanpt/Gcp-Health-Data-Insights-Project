
# GCP Health Insights Project


## 1) Project Overview :

This project focuses on processing patient health data, including vital signs such as heart rate, blood pressure, and body temperature, to generate meaningful insights for proactive monitoring. Leveraging Google Cloud Dataproc and PySpark, the pipeline ingests, transforms, and analyzes  health metrics at scale. The final insights are stored in BigQuery for reporting, visualization, and anomaly detection in patient vitals — enabling better clinical decision-making and health outcome tracking.

---

## 2) Project Details :
 

Objective: Build a scalable, real-time data pipeline for validating, transforming, and analyzing patient data, then storing results in BigQuery. <br>
Data Source: JSON files containing patient data streamed from Google Cloud Storage (GCS). <br>
Data Validation: Validate incoming records (heart rate, blood pressure, temperature) to ensure data quality and filter out invalid data. <br>
Data Transformation: Calculate average and standard deviation metrics, detect abnormal trends using moving windows, and categorize patients based on risk levels. <br>
Architecture: GCS (raw data) → Dataproc (processing) → BigQuery (storage). <br>
Logging & Monitoring: Use Google Cloud Logging for tracking pipeline steps, errors, and performance. <br>
Error Handling: Capture and log exceptions to ensure robust pipeline operation and to easily debug issues. <br>
Output: Write transformed and validated data, along with patient risk categorization, to BigQuery for further analysis. <br>
Business Value: Enables real-time monitoring of patient health metrics, aids in detecting critical trends, and supports healthcare providers with actionable insights. <br>

---

## 3) Tech Stack

- **Google Cloud Storage (GCS)** – Raw data staging & temporary processing outputs
- **Dataproc (PySpark on Hadoop/YARN)** – Distributed data computation.
- **BigQuery** – Final data warehouse for visualization.

---

## 4) Sample Patient Data [ Json File ]

![image](https://github.com/user-attachments/assets/81f1b5a1-e3b5-400d-a242-a874a39bd1de)


---

## 5) Data Pipeline Flow

![image](https://github.com/user-attachments/assets/bee1298e-b27a-438f-8f03-351958f6e65e)


---

## 6) All steps in detail

###  Step 1: Upload input data to GCS.

###  Step 2: Submit the PySpark job to Dataproc.

###  Step 3: Verify in BigQuery.

Go to BigQuery and query:

```sql
SELECT * FROM `your_project.health_dataset.final_insights`
```

---

## Biquery Output

![Output](https://github.com/user-attachments/assets/86f7471e-9e45-48f3-8b32-c6a14268eef7)

---

## Author

**Prashant Tripathi**
📧 [prashanttripathi2k24@gmail.com](mailto:prashanttripathi2k24@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/prashanttripathi786/)

