SELECT
    a.num_products,
    COUNT(*) AS total_customers,
    SUM(d.churned) AS churned_customers,
    ROUND(
        100.0 * SUM(d.churned) / COUNT(*),
        2
    ) AS churn_rate_pct
FROM public.demographic d
JOIN public.account a
    ON a.customer_id = d.customer_id
GROUP BY a.num_products
ORDER BY a.num_products;

-- Two-product customers have the lowest observed churn: 7.58%.
-- Three-product customers: 82.71% churn (220 of 266).
-- Four-product customers: 100% churn (60 of 60).
-- The three-product and four-product groups are much smaller.
-- These comparisons do not establish causation.