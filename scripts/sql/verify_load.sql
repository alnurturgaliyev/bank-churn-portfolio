SELECT
    (SELECT COUNT(*) FROM public.location) AS locations,
    (SELECT COUNT(*) FROM public.demographic) AS customers,
    (SELECT COUNT(*) FROM public.account) AS accounts,
    (SELECT COUNT(*) FROM public.account
     WHERE balance IS NULL) AS missing_balances,
    (SELECT SUM(churned) FROM public.demographic) AS churned_customers,
    (
        SELECT COUNT(*)
        FROM public.demographic d
        JOIN public.account a ON a.customer_id = d.customer_id
        JOIN public.location l ON l.location_id = d.location_id
    ) AS joined_rows;