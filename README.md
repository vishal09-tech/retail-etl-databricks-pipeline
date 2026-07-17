# Retail Data Engineering Pipeline

## Overview
End-to-end ETL pipeline built on Databricks using PySpark and SQL — 
no cloud services (AWS/Azure/GCP) used.

## Architecture
Medallion Architecture: Bronze -> Silver -> Gold

- **Bronze**: Raw ingestion via Databricks Auto Loader (incremental, 
  schema-tracked)
- **Silver**: Data cleaning (parsing nested product lists, timestamp 
  conversion, null handling, deduplication)
- **Gold**: Star schema (1 fact table + 4 dimension tables + 1 bridge 
  table for many-to-many product relationship)
- **Analytics**: SQL queries answering business questions (revenue 
  trends, top products, customer segmentation)

## Tech Stack
PySpark, SQL, Delta Lake, Databricks Workflows, Databricks Auto Loader

## Orchestration
4-task Databricks Workflow job, chained with dependencies, scheduled 
daily.

## Project Screenshots

### Bronze Layer
![Bronze Layer](screenshots/bronze_layer.png)

### Silver Layer
![Silver Layer](screenshots/silver_layer.png)

### Gold Layer
![Gold Layer](screenshots/gold_layer.png)

### Analytics
![Analytics](screenshots/analytics.png)

### Jobs & Scheduling
![Workflow](screenshots/workflow_job_run.png.png)
![Workflow](screenshots/workflow_schedule.png.png)

## Dataset
Retail transactions dataset (~1M rows), 2020-2024.
