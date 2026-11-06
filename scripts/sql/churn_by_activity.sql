SELECT
    a.is_active,
    COUNT(*) AS total_customers,
    SUM(d.churned) AS churned_customers,
    ROUND(
        100.0 * SUM(d.churned) / COUNT(*),
        2
    ) AS churn_rate_pct
FROM public.demographic d
JOIN public.account a
    ON a.customer_id = d.customer_id
GROUP BY a.is_active
ORDER BY churn_rate_pct DESC;

-- Inactive customers: 26.85% churn; active customers: 14.27%.
-- Observed gap: 12.58 percentage points.
-- This association does not establish that inactivity causes churn.