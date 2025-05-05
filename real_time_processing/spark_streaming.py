from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, sum, expr
from pyspark.sql.types import StructType, StringType, IntegerType, DoubleType, TimestampType


# Initialize Spark session
spark = SparkSession.builder.appName("SalesProcessing").getOrCreate()

# Define the schema for the incoming JSON

schema = StructType() \
    .add("product", StringType()) \
    .add("order_date", TimestampType()) \
    .add("sales", DoubleType()) \
    .add("quantity_sold", IntegerType()) \
    .add("warehouse_location", StringType())
# Read the Kafka stream
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sales_data") \
    .load()

# Parse the value column as JSON using the schema
df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# **Ensure 'sales' column is a numerical type before aggregation**
df = df.withColumn("sales", col("sales").cast("string"))
# Filter out rows with null product before aggregation
df = df.filter(col("product").isNotNull())

# Now aggregate the sales per product
df_agg = df.groupBy("product").agg(sum("sales").alias("total_sales"))


'''
# Define the function to write to PostgreSQL in batch
def write_to_postgres(batch_df, batch_id):
    print("----- Batch ID:", batch_id, "-----")
    batch_df.show()
    print("Schema of batch_df:", batch_df.schema)
    # Write the batch DataFrame to PostgreSQL
    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/sales") \
        .option("dbtable", "aggregated_sales") \
        .option("user", "postgres") \
        .option("password", "admin") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

# Write the streaming DataFrame to PostgreSQL in micro-batches
df_agg.writeStream \
    .outputMode("complete") \
    .foreachBatch(write_to_postgres) \
    .start() \
    .awaitTermination()
'''
def write_to_csv(batch_df, batch_id):
    print("----- Batch ID:", batch_id, "-----")
    batch_df.show()
    print("Schema of batch_df:", batch_df.schema)
    
    # Write the batch DataFrame to CSV (you can specify the path you want)
    batch_df.write \
        .format("csv") \
        .option("header", "true") \
        .mode("append") \
        .save("aggregated_sales.csv")

# Write the streaming DataFrame to CSV in micro-batches
df_agg.writeStream \
    .outputMode("complete") \
    .foreachBatch(write_to_csv) \
    .start() \
    .awaitTermination()