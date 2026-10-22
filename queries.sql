-- name: kpis
SELECT COUNT(DISTINCT order_id) AS orders,
       ROUND(SUM(revenue), 0) AS revenue,
       ROUND(SUM(profit), 0) AS profit,
       ROUND(100.0 * SUM(profit) / SUM(revenue), 1) AS margin_pct
FROM sales;

-- name: monthly_revenue
SELECT strftime('%Y-%m', order_date) AS month,
       ROUND(SUM(revenue), 0) AS revenue
FROM sales
GROUP BY month
ORDER BY month;

-- name: category_performance
SELECT category,
       ROUND(SUM(revenue), 0) AS revenue,
       ROUND(SUM(profit), 0) AS profit,
       ROUND(100.0 * SUM(profit) / SUM(revenue), 1) AS margin_pct
FROM sales
GROUP BY category
ORDER BY revenue DESC;

-- name: city_revenue
SELECT city, ROUND(SUM(revenue), 0) AS revenue
FROM sales
GROUP BY city
ORDER BY revenue DESC;

-- name: top_products
SELECT product, category, SUM(quantity) AS units_sold,
       ROUND(SUM(revenue), 0) AS revenue
FROM sales
GROUP BY product, category
ORDER BY revenue DESC
LIMIT 5;

-- name: top_customers
SELECT customer_id, COUNT(*) AS orders, ROUND(SUM(revenue), 0) AS total_spent
FROM sales
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;

-- name: discount_impact
SELECT discount,
       COUNT(*) AS orders,
       ROUND(AVG(quantity), 2) AS avg_quantity,
       ROUND(100.0 * SUM(profit) / SUM(revenue), 1) AS margin_pct
FROM sales
GROUP BY discount
ORDER BY discount;
