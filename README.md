# SalesPulse: Retail Sales Analysis

**Tools:** Python (pandas, matplotlib), SQL (SQLite)

## Problem
A retail business wants to know: which months, categories, cities and products
drive revenue and profit, and does discounting actually help?

## What I did
1. **Data:** 2,500 orders (2024-2025) across 5 categories and 6 cities (sample dataset made with `generate_data.py`).
2. **Cleaning (pandas):** removed 15 duplicate orders, filled 25 missing cities as "Unknown", converted dates, created `revenue` and `profit` columns.
3. **SQL analysis:** 7 queries in `queries.sql` (KPIs, monthly trend, category/city performance, top products, top customers, discount impact).
4. **Charts:** saved in `charts/`.

## Key findings
- Total revenue Rs 56.4 lakh, profit Rs 19.7 lakh, margin 34.9%.
- Electronics earns the most revenue, but Clothing has the best margin (43.6%).
- Delhi, Mumbai and Bengaluru together bring most of the revenue.
- A 20% discount drops the margin from 39.6% to 23.7%, while average quantity per order barely rises (1.66 to 1.77). Heavy discounts hurt profit.
- Smart Watch is the top product by revenue.

## Recommendations
- Reduce 20% discounts, or use them only on slow-moving items.
- Push high-margin Clothing and Books more in marketing.
- Focus on Delhi, Mumbai and Bengaluru, and test campaigns in Lucknow and Jaipur.

## How to run
```bash
pip install -r requirements.txt
python generate_data.py
python analysis.py
```

## Project structure
```
generate_data.py   # creates data/sales_data.csv
queries.sql        # all SQL queries
analysis.py        # cleaning + SQL + charts + summary
charts/            # output charts
output/summary.md  # auto-generated findings
```
