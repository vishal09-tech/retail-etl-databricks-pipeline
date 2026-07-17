# Databricks notebook source
# MAGIC  %sql
# MAGIC USE CATALOG workspace;
# MAGIC USE SCHEMA retail_project; -- Set schema on default so we dont need to write workspace.retail_project.

# COMMAND ----------

# MAGIC
# MAGIC %sql
# MAGIC -- Query 1 — Monthly Revenue Trend
# MAGIC SELECT d.Year, d.Month, ROUND(SUM(f.Total_Cost), 2) AS Total_Revenue
# MAGIC    FROM fact_transactions f
# MAGIC    JOIN dim_date d ON f.Date_Key = d.Date_Key
# MAGIC    GROUP BY d.Year, d.Month
# MAGIC    ORDER BY d.Year, d.Month;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Query 2 — Top 10 Selling Products
# MAGIC SELECT p.Product_Name, COUNT(*) AS Times_Sold
# MAGIC    FROM fact_transaction_products ftp
# MAGIC    JOIN dim_product p ON ftp.Product_Key = p.Product_Key
# MAGIC    GROUP BY p.Product_Name
# MAGIC    ORDER BY Times_Sold DESC
# MAGIC    LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Query 3 — Customer Category-wise Spending
# MAGIC SELECT c.Customer_Category, ROUND(SUM(f.Total_Cost), 2) AS Total_Spend, COUNT(*) AS Total_Transactions
# MAGIC    FROM fact_transactions f
# MAGIC    JOIN dim_customer c ON f.Customer_Key = c.Customer_Key
# MAGIC    GROUP BY c.Customer_Category
# MAGIC    ORDER BY Total_Spend DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Query 4 — City/Store-Type wise Performance
# MAGIC SELECT s.City, s.Store_Type, ROUND(SUM(f.Total_Cost), 2) AS Revenue
# MAGIC    FROM fact_transactions f
# MAGIC    JOIN dim_store s ON f.Store_Key = s.Store_Key
# MAGIC    GROUP BY s.City, s.Store_Type
# MAGIC    ORDER BY Revenue DESC
# MAGIC    LIMIT 15;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Query 5 — Season-wise Sales Pattern
# MAGIC SELECT Season, ROUND(AVG(Total_Cost), 2) AS Avg_Order_Value, COUNT(*) AS Transactions
# MAGIC    FROM fact_transactions
# MAGIC    GROUP BY Season
# MAGIC    ORDER BY Avg_Order_Value DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Query 6 — Promotion Impact
# MAGIC SELECT Promotion, ROUND(AVG(Total_Cost), 2) AS Avg_Order_Value
# MAGIC    FROM fact_transactions
# MAGIC    GROUP BY Promotion
# MAGIC    ORDER BY Avg_Order_Value DESC;

# COMMAND ----------

