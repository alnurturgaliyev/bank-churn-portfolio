# Data dictionary

One customer has one demographic row and one account row in this dataset. Many customers reference one location. Source names are converted to snake_case when loading PostgreSQL.

| PostgreSQL field | Source field | Meaning / handling |
|---|---|---|
| `customer_id` | CustomerId | Existing customer identifier; join and audit key; excluded from model inputs. |
| `account_id` | AccountId | Existing account identifier; excluded from model inputs. |
| `gender` | Gender | Recorded category: Female or Male. |
| `age` | Age | Recorded customer age; observed range 18–92. |
| `salary` | Salary | Recorded salary amount; currency, period, and measurement timing unverified. |
| `location_id` | LocationId | Foreign key linking demographic to location. |
| `geography` | Geography | Germany, France, Spain, UK, Canada, USA. |
| `churned` | Churned | Target: 1 = left, 0 = retained; outcome window unverified. |
| `tenure` | Tenure | Recorded relationship tenure, observed range 0–10; time unit unverified. |
| `balance` | Balance | Recorded amount; 3,617 missing values retained as SQL NULL. Currency unverified. |
| `num_products` | NumProducts | Recorded product count, 1–4; one-hot encoded for modeling. |
| `has_credit_card` | HasCreditCard | Recorded binary flag, 0/1. |
| `is_active` | IsActive | Recorded binary activity flag, 0/1; activity definition and timing unverified. |
| — | Name | Removed from processed demographic table; unused for modeling. |

## Modeling transformations

Age, salary, tenure, and balance use median imputation and standard scaling. Missing-value indicators are added where missingness occurs in a fitting fold. Gender, geography, and product count use one-hot encoding with unknown categories ignored. The two binary flags pass through unchanged. All learned transformations are fitted inside training folds during cross-validation and on training rows for final fitting. IDs and the target are never input features.

## Provenance

The download script records the source revision and checksum. Real-bank provenance, representativeness, and feature timing have not been established. No real-world retention impact is claimed.
