from kafka import KafkaConsumer
import json
import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="sales",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

consumer = KafkaConsumer(
    'sales_data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    data = message.value
    cursor.execute("""
        INSERT INTO sales_data (product, order_date, sales, quantity_sold, warehouse_location)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (order_id, product) DO NOTHING;
    """, (data["Product"], data["Order Date"], data["Sales"], data["Quantity Sold"], data["Warehouse Location"]))
    
    conn.commit()

cursor.close()
conn.close()
