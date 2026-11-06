SELECT
    CASE
        WHEN a.balance IS NULL THEN 'Missing balance'
        ELSE 'Recorded balance'
    END AS balance_status,
    COUNT(*) AS total_customers,
    SUM(d.churned) AS churned_customers,
    ROUND(
        100.0 * SUM(d.churned) / COUNT(*),
        2
    ) AS churn_rate_pct
FROM public.demographic d
JOIN public.account a
    ON a.customer_id = d.customer_id
GROUP BY
    CASE
        WHEN a.balance IS NULL THEN 'Missing balance'
        ELSE 'Recorded balance'
    END
ORDER BY churn_rate_pct DESC;

-- Recorded balance: 24.08% churn; missing balance: 13.82%.
-- Observed gap: 10.26 percentage points.
-- Preserve missingness information for later model evaluation.
-- Missing balances have not been established as zero balances.