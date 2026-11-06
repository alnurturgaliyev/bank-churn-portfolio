WITH customer_segments AS (
    SELECT
        l.geography,
        CASE
            WHEN d.age < 30 THEN 'Under 30'
            WHEN d.age <= 50 THEN '30–50'
            ELSE 'Over 50'
        END AS age_group,
        d.churned
    FROM public.demographic d
    JOIN public.location l
        ON l.location_id = d.location_id
)
SELECT
    geography,
    age_group,
    COUNT(*) AS total_customers,
    SUM(churned) AS churned_customers,
    ROUND(
        100.0 * SUM(churned) / COUNT(*),
        2
    ) AS churn_rate_pct
FROM customer_segments
GROUP BY geography, age_group
ORDER BY geography, churn_rate_pct DESC;

-- In every country, the Over 50 group has the highest observed
-- churn rate, followed by 30–50, then Under 30.
-- Over 50 churn rates range from 40.74% to 49.27%.
-- These results describe associations, not causes.