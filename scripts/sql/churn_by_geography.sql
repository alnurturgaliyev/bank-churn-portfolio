SELECT
    l.geography,
    COUNT(*) AS total_customers,
    SUM(d.churned) AS churned_customers,
    ROUND(
        100.0 * SUM(d.churned) / COUNT(*),
        2
    ) AS churn_rate_pct
FROM public.demographic d
JOIN public.location l
    ON l.location_id = d.location_id
GROUP BY l.geography
ORDER BY churn_rate_pct DESC;

-- Country churn rates range from 19.37% to 21.13%.
-- Highest: Spain; lowest: Germany.
-- Observed spread: 1.76 percentage points.
-- Statistical significance has not been tested.