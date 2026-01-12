# Databricks notebook source
# Databricks notebook source
# MAGIC %md
# MAGIC # Unfixable Error Test - Jira Integration
# MAGIC 
# MAGIC This notebook intentionally fails with an error that CANNOT be auto-fixed.
# MAGIC The healer agent should create a [System] Incident in Jira.
# MAGIC
# MAGIC **Error Type**: Missing production table (requires manual intervention)

# COMMAND ----------

from pyspark.sql import functions as F

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 1: Load Critical Production Data
# MAGIC 
# MAGIC This step tries to load a table that doesn't exist.
# MAGIC The agent CANNOT fix this because:
# MAGIC 1. It cannot create production tables
# MAGIC 2. It doesn't know where the data should come from
# MAGIC 3. This requires human intervention to identify the correct data source

# COMMAND ----------

# This table intentionally does not exist
# The agent cannot create it because it requires knowing the actual data source
try:
    critical_data = spark.table("production_analytics.finance.quarterly_revenue_2024_q4")
    critical_data_count = critical_data.count()
    if critical_data_count == 0:
        print("Warning: Table 'production_analytics.finance.quarterly_revenue_2024_q4' is empty")
except Exception as e:
    print(f"Error loading table: {str(e)}")
    critical_data = None

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 2: Process the data (will never reach here)

# COMMAND ----------

# This code will never execute because the table doesn't exist
if critical_data is not None:
    processed = critical_data.groupBy("region", "business_unit").agg(
        F.sum("revenue").alias("total_revenue"),
        F.avg("margin_pct").alias("avg_margin"),
        F.count("transaction_id").alias("transaction_count")
    )
    display(processed)
else:
    print("Skipping data processing due to missing input data")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 3: Write to reporting table

# COMMAND ----------

# This will also never execute
if 'processed' in locals():
    processed.write.mode("overwrite").saveAsTable("reporting.finance.q4_summary")
    print("Report generated successfully!")
else:
    print("Skipping report generation due to missing processed data")