"""Step 2: Clean the data, run SQL queries, make charts, write a summary."""
import re
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------- 1. Load & clean (pandas) ----------
df = pd.read_csv("data/sales_data.csv")
print("Raw rows:", len(df))

df = df.drop_duplicates()                       # remove duplicate orders
df["city"] = df["city"].fillna("Unknown")       # fill missing cities
df["order_date"] = pd.to_datetime(df["order_date"])

df["revenue"] = df["quantity"] * df["unit_price"] * (1 - df["discount"])
df["profit"] = df["revenue"] - df["quantity"] * df["unit_cost"]
print("Clean rows:", len(df))

# ---------- 2. Load into SQLite ----------
conn = sqlite3.connect("output/sales.db")
df.assign(order_date=df["order_date"].dt.strftime("%Y-%m-%d")).to_sql(
    "sales", conn, if_exists="replace", index=False
)

# ---------- 3. Run SQL queries from queries.sql ----------
sql_text = open("queries.sql").read()
blocks = re.split(r"-- name:\s*(\w+)\n", sql_text)[1:]
results = {name: pd.read_sql(q.strip().rstrip(";"), conn)
           for name, q in zip(blocks[::2], blocks[1::2])}
for name, res in results.items():
    print(f"\n=== {name} ===\n{res.to_string(index=False)}")

# ---------- 4. Charts ----------
plt.rcParams.update({"figure.figsize": (9, 5), "axes.spines.top": False,
                     "axes.spines.right": False})

m = results["monthly_revenue"]
plt.plot(m["month"], m["revenue"], marker="o", color="#1f77b4")
plt.xticks(rotation=60); plt.title("Monthly Revenue"); plt.ylabel("Revenue (INR)")
plt.tight_layout(); plt.savefig("charts/monthly_revenue.png", dpi=150); plt.close()

c = results["category_performance"]
plt.bar(c["category"], c["revenue"], color="#2ca02c")
plt.title("Revenue by Category"); plt.ylabel("Revenue (INR)")
plt.tight_layout(); plt.savefig("charts/category_revenue.png", dpi=150); plt.close()

ci = results["city_revenue"]
plt.bar(ci["city"], ci["revenue"], color="#ff7f0e")
plt.title("Revenue by City"); plt.ylabel("Revenue (INR)")
plt.tight_layout(); plt.savefig("charts/city_revenue.png", dpi=150); plt.close()

p = results["top_products"].iloc[::-1]
plt.barh(p["product"], p["revenue"], color="#9467bd")
plt.title("Top 5 Products by Revenue"); plt.xlabel("Revenue (INR)")
plt.tight_layout(); plt.savefig("charts/top_products.png", dpi=150); plt.close()

# ---------- 5. Auto summary ----------
k = results["kpis"].iloc[0]
best_month = m.loc[m["revenue"].idxmax()]
best_cat = c.iloc[0]
best_margin = c.loc[c["margin_pct"].idxmax()]
best_city = ci.iloc[0]
summary = f"""# Key Findings

- Total orders: {int(k.orders):,} | Revenue: Rs {int(k.revenue):,} | Profit: Rs {int(k.profit):,} | Margin: {k.margin_pct}%
- Best month: {best_month.month} (Rs {int(best_month.revenue):,})
- Top category by revenue: {best_cat.category} (Rs {int(best_cat.revenue):,})
- Highest-margin category: {best_margin.category} ({best_margin.margin_pct}%)
- Top city: {best_city.city} (Rs {int(best_city.revenue):,})
"""
open("output/summary.md", "w").write(summary)
print("\n" + summary)
conn.close()
