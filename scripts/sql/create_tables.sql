CREATE TABLE public.location (
    location_id INTEGER PRIMARY KEY,
    geography TEXT NOT NULL
);

CREATE TABLE public.demographic (
    customer_id INTEGER PRIMARY KEY,
    gender TEXT NOT NULL,
    age INTEGER NOT NULL,
    salary NUMERIC(12, 2) NOT NULL,
    location_id INTEGER NOT NULL
        REFERENCES public.location(location_id),
    churned SMALLINT NOT NULL CHECK (churned IN (0, 1))
);

CREATE TABLE public.account (
    account_id TEXT PRIMARY KEY,
    customer_id INTEGER NOT NULL UNIQUE
        REFERENCES public.demographic(customer_id),
    tenure INTEGER NOT NULL,
    balance NUMERIC(12, 2),
    num_products INTEGER NOT NULL,
    has_credit_card SMALLINT NOT NULL
        CHECK (has_credit_card IN (0, 1)),
    is_active SMALLINT NOT NULL
        CHECK (is_active IN (0, 1))
);