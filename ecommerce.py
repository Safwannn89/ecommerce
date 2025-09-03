# %%
%pip install faker pandas sqlalchemy psycopg2 pymysql
import random
import datetime
from faker import Faker
import pandas as pd
from sqlalchemy import create_engine

fake = Faker()

# -----------------------
# DATABASE CONNECTION
# -----------------------
# MySQL example:
engine = create_engine("mysql+pymysql://root:Safwan%40123@localhost/ecommerce")
# -----------------------
# PARAMETERS
# -----------------------
num_rows = 100000             # total rows you want
start_date = datetime.date(2022, 1, 1)

num_customers = 5000          # unique customers
num_products = 500            # unique products
num_stores = 50               # store locations

# -----------------------
# CUSTOMERS TABLE
# -----------------------
customers = [
    {
        "customer_id": i,
        "name": fake.name(),
        "email": fake.email(),
        "gender": random.choice(["Male", "Female", "Other"]),
        "age": random.randint(18, 65),
        "location": fake.city(),
        "join_date": fake.date_between(start_date="-2y", end_date="today")
    }
    for i in range(1, num_customers + 1)
]
pd.DataFrame(customers).to_sql("customers", engine, if_exists="replace", index=False)

# -----------------------
# PRODUCTS TABLE
# -----------------------
# -----------------------
# PRODUCTS TABLE (REALISTIC)
# -----------------------
import random

categories = {
    "Groceries": ["Maggie Noodles", "Basmati Rice", "Refined Oil", "Potato Chips", "Tea Powder"],
    "Electronics": ["Smartphone", "Laptop", "Earphones", "Power Bank", "Smartwatch"],
    "Beauty": ["Lipstick", "Face Cream", "Perfume", "Nail Polish", "Shampoo"],
    "Fashion": ["T-Shirt", "Jeans", "Sneakers", "Handbag", "Jacket"],
    "Home & Kitchen": ["Mixer Grinder", "Pressure Cooker", "Chair", "Table Lamp", "Water Bottle"]
}

products = []
sku_id = 1

for category, items in categories.items():
    for item in items:
        products.append({
            "sku_id": sku_id,
            "product_id": f"P{sku_id:05d}",
            "product_code": f"{category[:2].upper()}-{sku_id:05d}",
            "price": round(random.uniform(50, 5000), 2),
            "product_name": item,
            "description": f"{item} from {category}, high quality and best price."
        })
        sku_id += 1

pd.DataFrame(products).to_sql("products", engine, if_exists="replace", index=False)


# -----------------------
# STORES TABLE
# -----------------------
stores = [
    {
        "store_id": i,
        "location": fake.city()
    }
    for i in range(1, num_stores + 1)
]
pd.DataFrame(stores).to_sql("stores", engine, if_exists="replace", index=False)

# -----------------------
# TRANSACTIONS TABLE (1 Lakh Rows)
# -----------------------
transactions = []
for transaction_id in range(1, num_rows + 1):
    cust = random.choice(customers)
    prod = random.choice(products)
    store = random.choice(stores)

    quantity = random.randint(1, 5)
    total_amount = round(prod["price"] * quantity, 2)

    transactions.append({
        "transaction_id": transaction_id,
        "order_number": f"ORD{transaction_id:07d}",
        "customer_id": cust["customer_id"],
        "store_id": store["store_id"],
        "product_id": prod["product_id"],
        "sku_id": prod["sku_id"],
        "quantity": quantity,
        "date": fake.date_between(start_date=start_date, end_date="today"),
        "time": fake.time(),
        "total_amount": total_amount
    })

pd.DataFrame(transactions).to_sql("transactions", engine, if_exists="replace", index=False)

print("✅ Inserted 1 lakh rows successfully into database!")




