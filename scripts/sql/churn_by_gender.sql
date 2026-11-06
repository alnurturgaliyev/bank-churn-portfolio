SELECT
    gender,
    COUNT(*) AS total_customers,
    SUM(churned) AS churned_customers,
    ROUND(
        100.0 * SUM(churned) / COUNT(*),
        2
    ) AS churn_rate_pct
FROM public.demographic
GROUP BY gender
ORDER BY churn_rate_pct DESC;

-- Female churn rate: 25.07%; male churn rate: 16.46%.
-- Observed gap: 8.61 percentage points.
-- This comparison does not establish causation.