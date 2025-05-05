import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
np.random.seed(42)

# Generate 1000 synthetic sales records
num_records = 1000
products = ["Shoes", "Laptop", "Phone", "T-Shirt", "Watch", "Headphones", "Backpack", "Sunglasses", "Book", "Camera"]
locations = ["New York", "Los Angeles", "Chicago", "Houston", "Miami", "Lagos", "London", "Tokyo", "Beijing", "Sydney","Paris"]

data = {
    "Order ID": np.arange(1, num_records + 1),
    "Product": np.random.choice(products, num_records),
    "Order Date": pd.date_range(start="2023-01-01", periods=num_records, freq='D'),
    "Sales": np.random.randint(20, 500, num_records),
    "Quantity Sold": np.random.randint(1, 10, num_records),
    "Warehouse Location": np.random.choice(locations, num_records)
}

sales_df = pd.DataFrame(data)
sales_df.to_csv("synthetic_sales.csv", index=False)
