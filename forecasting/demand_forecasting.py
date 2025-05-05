from prophet import Prophet
import psycopg2
import pandas as pd

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="sales",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Load sales data
query = "SELECT order_date, sales FROM sales_data;"
df = pd.read_sql(query, conn)
df.rename(columns={"order_date": "ds", "sales": "y"}, inplace=True)

# Train forecasting model
model = Prophet()
model.fit(df)

# Predict next 30 days
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# Save predictions
for index, row in forecast.iterrows():
    cursor.execute("INSERT INTO forecasted_sales (forecast_date, predicted_sales) VALUES (%s, %s)", 
                   (row['ds'], row['yhat']))
    conn.commit()

cursor.close()
conn.close()
