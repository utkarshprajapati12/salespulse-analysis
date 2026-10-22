"""Step 1: Create a sample retail sales dataset (data/sales_data.csv)."""
import random
from datetime import date, timedelta
import pandas as pd

random.seed(42)

CITIES = ["Lucknow", "Delhi", "Mumbai", "Bengaluru", "Kolkata", "Jaipur"]
# category -> {product: (price, cost)}
CATALOG = {
    "Electronics": {"Earphones": (1500, 900), "Power Bank": (1200, 750), "Smart Watch": (3500, 2400)},
    "Clothing": {"T-Shirt": (600, 280), "Jeans": (1800, 950), "Jacket": (2800, 1500)},
    "Home": {"Mixer Grinder": (2500, 1700), "Bedsheet": (900, 450), "Lamp": (700, 350)},
    "Books": {"Python Guide": (550, 300), "SQL Handbook": (500, 280), "Novel": (350, 180)},
    "Grocery": {"Dry Fruits": (800, 560), "Tea Pack": (300, 190), "Spices Combo": (450, 280)},
}

start = date(2024, 1, 1)
rows = []
for i in range(1, 2501):
    d = start + timedelta(days=random.randint(0, 729))
    # festive months (Oct-Nov) get extra orders
    if d.month in (10, 11) and random.random() < 0.4:
        d = d.replace(day=random.randint(1, 28))
    cat = random.choices(list(CATALOG), weights=[30, 25, 18, 10, 17])[0]
    prod, (price, cost) = random.choice(list(CATALOG[cat].items()))
    rows.append({
        "order_id": 1000 + i,
        "order_date": d.isoformat(),
        "customer_id": f"C{random.randint(1, 400):03d}",
        "city": random.choices(CITIES, weights=[10, 25, 25, 20, 10, 10])[0],
        "category": cat,
        "product": prod,
        "quantity": random.choices([1, 2, 3, 4], weights=[55, 25, 12, 8])[0],
        "unit_price": price,
        "discount": random.choice([0, 0, 0.05, 0.10, 0.20]),
        "unit_cost": cost,
    })

df = pd.DataFrame(rows)
# add a few messy rows so the cleaning step is real
df.loc[df.sample(25, random_state=1).index, "city"] = None
df = pd.concat([df, df.sample(15, random_state=2)])  # duplicates
df.to_csv("data/sales_data.csv", index=False)
print(f"Saved {len(df)} rows to data/sales_data.csv")
