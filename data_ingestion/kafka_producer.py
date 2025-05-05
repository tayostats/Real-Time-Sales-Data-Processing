from kafka import KafkaProducer
import json
import pandas as pd
import time

# Step 1: Set up the Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # Connecting to your Kafka server
    value_serializer=lambda x: json.dumps(x).encode('utf-8')  # Serialize the data as JSON
)

# Step 2: Load your synthetic sales data from CSV
df = pd.read_csv("synthetic_sales.csv")

# Step 3: Iterate through each row of the DataFrame and send to Kafka
for _, row in df.iterrows():
    producer.send('sales_data', value=row.to_dict())  # Send each row as a message
    time.sleep(1)  # Simulate real-time stream by waiting 1 second between each message

# Step 4: Ensure all messages are sent before closing
producer.flush()
