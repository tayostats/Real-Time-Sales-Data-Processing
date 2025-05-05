CREATE TABLE sales_data (
    order_id SERIAL PRIMARY KEY,
    product VARCHAR(100),
    order_date TIMESTAMP,
    sales NUMERIC,
    quantity_sold INT,
    warehouse_location VARCHAR(50),
	UNIQUE(order_id, product)
);

CREATE TABLE forecasted_sales (
    forecast_date TIMESTAMP PRIMARY KEY,
    predicted_sales NUMERIC
);
