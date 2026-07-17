# Databricks notebook source
df_silver = spark.table("workspace.retail_project.silver_transactions")

# COMMAND ----------

from pyspark.sql.functions import col, year, month, dayofmonth, dayofweek, date_format

dim_date = (
       df_silver.select(col("Date"))
       .distinct()
       .withColumn("Date_Key", date_format(col("Date"), "yyyyMMdd").cast("int"))
       .withColumn("Year", year(col("Date")))
       .withColumn("Month", month(col("Date")))
       .withColumn("Day", dayofmonth(col("Date")))
       .withColumn("DayOfWeek", dayofweek(col("Date")))
   )
dim_date.write.format("delta").mode("overwrite").saveAsTable("workspace.retail_project.dim_date")

# COMMAND ----------

from pyspark.sql.functions import monotonically_increasing_id

dim_customer = (
       df_silver.select("Customer_Name", "Customer_Category")
       .distinct()
       .withColumn("Customer_Key", monotonically_increasing_id())
   )
dim_customer.write.format("delta").mode("overwrite").saveAsTable("workspace.retail_project.dim_customer")

# COMMAND ----------

dim_store = (
       df_silver.select("City", "Store_Type")
       .distinct()
       .withColumn("Store_Key", monotonically_increasing_id())
   )
dim_store.write.format("delta").mode("overwrite").saveAsTable("workspace.retail_project.dim_store")

# COMMAND ----------

from pyspark.sql.functions import explode

dim_product = (
       df_silver.select(explode(col("Product")).alias("Product_Name"))
       .distinct()
       .withColumn("Product_Key", monotonically_increasing_id())
   )
dim_product.write.format("delta").mode("overwrite").saveAsTable("workspace.retail_project.dim_product")

# COMMAND ----------

fact_transactions = (
       df_silver
       .withColumn("Date_Key", date_format(col("Date"), "yyyyMMdd").cast("int"))
       .join(dim_customer, ["Customer_Name", "Customer_Category"], "left")
       .join(dim_store, ["City", "Store_Type"], "left")
       .select(
           "Transaction_ID", "Date_Key", "Customer_Key", "Store_Key",
           "Total_Items", "Total_Cost", "Payment_Method",
           "Discount_Applied", "Season", "Promotion"
       )
   )
(
    fact_transactions.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("workspace.retail_project.fact_transactions")
)

# COMMAND ----------

for t in ["dim_date", "dim_customer", "dim_store", "dim_product", "fact_transactions"]:
       print(t, spark.table(f"workspace.retail_project.{t}").count())

# COMMAND ----------

from pyspark.sql.functions import explode, col

# Transaction_ID ke saath product ko explode karo
fact_transaction_products = (
    df_silver.select("Transaction_ID", explode(col("Product")).alias("Product_Name"))
    .join(dim_product, on="Product_Name", how="left")
    .select("Transaction_ID", "Product_Key")
)

(
    fact_transactions.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("workspace.retail_project.fact_transactions")
)

# COMMAND ----------

spark.table("workspace.retail_project.fact_transaction_products").count()
display(spark.table("workspace.retail_project.fact_transaction_products").limit(10))

# COMMAND ----------

