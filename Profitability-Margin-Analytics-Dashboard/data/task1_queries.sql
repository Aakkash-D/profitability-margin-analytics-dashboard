SELECT
    customer_id,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(cost), 2) AS total_cost,
    ROUND(SUM(sales) - SUM(cost), 2) AS contribution_margin
FROM sales_orders
GROUP BY customer_id
ORDER BY total_revenue DESC;

WITH customer_revenue AS (
    SELECT
        customer_id,
        SUM(sales) AS revenue
    FROM sales_orders
    GROUP BY customer_id
)
SELECT
    ROUND(SUM(revenue), 2) AS customer_total_revenue
FROM customer_revenue;


SELECT
    ROUND(SUM(sales), 2) AS overall_revenue
FROM sales_orders;

WITH customer_region_revenue AS (
    SELECT
        region,
        customer_id,
        SUM(sales) AS revenue
    FROM sales_orders
    GROUP BY region, customer_id
),
ranked_customers AS (
    SELECT
        region,
        customer_id,
        revenue,
        ROW_NUMBER() OVER (
            PARTITION BY region
            ORDER BY revenue DESC
        ) AS revenue_rank
    FROM customer_region_revenue
)
SELECT
    region,
    customer_id,
    ROUND(revenue,2) AS revenue,
    revenue_rank
FROM ranked_customers
WHERE revenue_rank <= 3
ORDER BY region, revenue_rank;


WITH monthly_revenue AS (
    SELECT
        strftime('%Y-%m', order_date) AS month,
        SUM(sales) AS revenue
    FROM sales_orders
    GROUP BY month
)
SELECT
    month,
    ROUND(revenue,2) AS revenue,

    ROUND(
        revenue -
        LAG(revenue) OVER (
            ORDER BY month
        ),
        2
    ) AS mom_change,

    ROUND(
        (
            revenue -
            LAG(revenue) OVER (
                ORDER BY month
            )
        ) * 100.0 /
        LAG(revenue) OVER (
            ORDER BY month
        ),
        2
    ) AS mom_growth_pct

FROM monthly_revenue
ORDER BY month;

WITH customer_margin AS (
    SELECT
        customer_id,
        SUM(sales) AS revenue,
        SUM(cost) AS cost,
        SUM(sales) - SUM(cost) AS margin
    FROM sales_orders
    GROUP BY customer_id
),

lowest_margin_customers AS (
    SELECT *
    FROM customer_margin
    ORDER BY margin ASC
    LIMIT 10
)

SELECT
    l.customer_id,
    ROUND(l.margin,2) AS customer_margin,
    s.product,
    ROUND(
        SUM(s.sales - s.cost),
        2
    ) AS product_margin
FROM lowest_margin_customers l
JOIN sales_orders s
    ON l.customer_id = s.customer_id
GROUP BY
    l.customer_id,
    s.product
ORDER BY
    l.margin,
    product_margin;

    