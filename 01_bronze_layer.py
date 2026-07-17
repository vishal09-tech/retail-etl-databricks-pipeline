# Databricks notebook source
spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.retail_project")

# COMMAND ----------

df_bronze = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "csv")
    .option("cloudFiles.schemaLocation", "/Volumes/workspace/default/retail_data/_schema")
    .option("header", "true")
    .load("/Volumes/workspace/default/retail_data/")
)

(
    df_bronze.writeStream
    .format("delta")
    .option("checkpointLocation", "/Volumes/workspace/default/retail_data/_checkpoint")
    .trigger(availableNow=True)
    .toTable("workspace.retail_project.bronze_transactions")
)

# COMMAND ----------

df_bronze.printSchema()
spark.table("workspace.retail_project.bronze_transactions").count()


# COMMAND ----------

display(spark.table("workspace.retail_project.bronze_transactions").limit(10))

# COMMAND ----------

