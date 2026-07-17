# Databricks notebook source
df_silver = spark.table("workspace.retail_project.bronze_transactions")

# COMMAND ----------

from pyspark.sql.functions import col, regexp_replace, split, trim

df_silver = df_silver.withColumn(
       "Product_Clean",
       split(
           regexp_replace(col("Product"), r"[\[\]']", ""),
           ",\s*"
       )
   )

# COMMAND ----------

from pyspark.sql.functions import to_timestamp

df_silver = df_silver.withColumn(
       "Date_Clean",
       to_timestamp(col("Date"), "yyyy-MM-dd HH:mm:ss")
   )

# COMMAND ----------

from pyspark.sql.functions import when, isnull, lit

df_silver = df_silver.withColumn(
       "Promotion_Clean",
       when(isnull(col("Promotion")), lit("No Promotion")).otherwise(col("Promotion"))
   )

# COMMAND ----------

df_silver_final = (
       df_silver
       .drop("Product", "Date", "Promotion")
       .withColumnRenamed("Product_Clean", "Product")
       .withColumnRenamed("Date_Clean", "Date")
       .withColumnRenamed("Promotion_Clean", "Promotion")
   )

# COMMAND ----------

df_silver_final = df_silver_final.dropDuplicates(["Transaction_ID"])

# COMMAND ----------

(
       df_silver_final.write
       .format("delta")
       .mode("overwrite")
       .option("overwriteSchema", "true")
       .saveAsTable("workspace.retail_project.silver_transactions")
   )

# COMMAND ----------

display(spark.table("workspace.retail_project.silver_transactions").limit(10))
spark.table("workspace.retail_project.silver_transactions").count()

# COMMAND ----------

