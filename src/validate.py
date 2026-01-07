import sqlite3
import pandas as pd


def counts(db_path: str) -> dict:
    conn = sqlite3.connect(db_path)
    c = pd.read_sql_query(
        """
        SELECT 
          (SELECT COUNT(*) FROM sqlite_master WHERE name='staging' AND type='table') as has_staging,
          (SELECT COUNT(*) FROM staging) as staging_rows,
          (SELECT COUNT(*) FROM dim_date) as dim_date_rows,
          (SELECT COUNT(*) FROM dim_property) as dim_property_rows,
          (SELECT COUNT(*) FROM fact_sales) as fact_sales_rows
        """, conn)
    conn.close()
    return c.iloc[0].to_dict()


def no_null_house_id(db_path: str) -> int:
    conn = sqlite3.connect(db_path)
    r = pd.read_sql_query("SELECT COUNT(*) as n FROM fact_sales WHERE house_id IS NULL OR TRIM(house_id) = ''", conn)
    conn.close()
    return int(r['n'].iloc[0])


def numeric_issues(db_path: str) -> dict:
    conn = sqlite3.connect(db_path)
    issues = {}
    # purchase_price should be > 0
    r = pd.read_sql_query("SELECT COUNT(*) as n FROM fact_sales WHERE purchase_price IS NULL OR purchase_price <= 0", conn)
    issues['bad_purchase_price'] = int(r['n'].iloc[0])
    # sqm_price should be >= 0
    r = pd.read_sql_query("SELECT COUNT(*) as n FROM fact_sales WHERE sqm_price IS NULL OR sqm_price < 0", conn)
    issues['bad_sqm_price'] = int(r['n'].iloc[0])
    conn.close()
    return issues


def run_all(db_path: str) -> None:
    c = counts(db_path)
    if c.get('has_staging', 0) == 0:
        raise AssertionError("staging table not found in DB")
    assert c['staging_rows'] > 0, 'staging has 0 rows'
    assert c['fact_sales_rows'] > 0, 'fact_sales has 0 rows (transform may have failed)'
    assert c['dim_property_rows'] > 0, 'dim_property has 0 rows'
    null_houses = no_null_house_id(db_path)
    assert null_houses == 0, f"Found {null_houses} rows in fact_sales with NULL or empty house_id"
    issues = numeric_issues(db_path)
    assert issues['bad_purchase_price'] == 0, f"Found {issues['bad_purchase_price']} invalid purchase_price values"
    assert issues['bad_sqm_price'] == 0, f"Found {issues['bad_sqm_price']} invalid sqm_price values"
    return None
