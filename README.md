
### ✅   GCP Health Insights Project


## 📌 Project Overview

This project focuses on processing patient health data, including vital signs such as heart rate, blood pressure, and body temperature, to generate meaningful insights for proactive monitoring. Leveraging Google Cloud Dataproc and PySpark, the pipeline ingests, transforms, and analyzes streaming health metrics at scale. The final insights are stored in BigQuery for reporting, visualization, and anomaly detection in patient vitals — enabling better clinical decision-making and health outcome tracking.

Below are some more details :
 

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

## 🛠️ Tech Stack

- **Google Cloud Storage (GCS)** – Raw data staging & temporary processing outputs
- **Dataproc (PySpark on Hadoop/YARN)** – Distributed data computation.
- **BigQuery** – Final data warehouse for visualization.

---

## 🔄 Data Pipeline Flow

![image](https://github.com/user-attachments/assets/bee1298e-b27a-438f-8f03-351958f6e65e)



---

## 📂 Project Structure

```

health-insights/
│
├── README.md                ← Project documentation
├── pipeline.py         ← Main PySpark code for Dataproc job
├── Input_data/Health_data.json            ←  input data [ Json File ]

````

---

## 📄 File Description

| File | Description |
|------|-------------|
| `main_pipeline.py` | Core PySpark script used in Dataproc to read from GCS, process data, compute aggregations and standard deviations, and write the result to BigQuery |
| `README.md` | Documentation for understanding and running the project |
| `sample_data/` | Contains mock or real input data used in the pipeline |
| `output/` | Holds intermediate output for validation or debugging |

---

## 📌 GCP Resources

| Resource | Name/Link |
|----------|-----------|
| GCS Bucket | `gs://your-bucket-name/health-insights/` |
| Dataproc Cluster | `health-insights-cluster` (Region: `us-central1`) |
| BigQuery Table | `your_project.health_dataset.final_insights` |

---

## 🚀 How to Run

### 🔁 Step 1: Upload input data to GCS
```bash
gsutil cp local_file.csv gs://your-bucket-name/health-insights/input/
````

### 🔁 Step 2: Submit the PySpark job to Dataproc

```bash
gcloud dataproc jobs submit pyspark main_pipeline.py \
    --cluster=health-insights-cluster \
    --region=us-central1 \
    --jars=gs://spark-lib/bigquery/spark-bigquery-latest.jar
```

### 🔁 Step 3: Verify in BigQuery

Go to BigQuery and query:

```sql
SELECT * FROM `your_project.health_dataset.final_insights`
```

---

## 📊 Example Use Case

Compute standard deviation of lab test results per patient and flag anomalies:

* Patients with unusually high/low test results
* Time-series trends for health monitoring

---

## 👨‍💻 Author

**Prashant Tripathi**
*Data Analyst & Cloud Enthusiast*
📧 [prashant@example.com](mailto:prashant@example.com)
🔗 [LinkedIn](https://linkedin.com/in/your-profile)

---

## 📃 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```

---

### 📝 Tips:
- Replace placeholders like `your_project`, `your-bucket-name`, `your-profile` with your actual project details.
- You can add badges (like GCP, PySpark, BigQuery) at the top if you're uploading to GitHub.

Let me know if you'd like me to generate a logo, add GitHub Actions for CI/CD, or include a `.json` schema validator example!
```
