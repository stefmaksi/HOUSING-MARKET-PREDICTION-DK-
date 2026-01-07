#!/usr/bin/env python3
"""
Minimal transform: staging -> dim_date, dim_property, fact_sales

This version is intentionally small and easy to read for learning/demo purposes.
Usage:
  python src/transform.py --db Data/warehouse.db
"""

import argparse
import sqlite3
import sys
import pandas as pd


def transform(db_path: str):
    conn = sqlite3.connect(db_path)

    # Read staging
    try:
        staging = pd.read_sql('SELECT * FROM staging', conn)
    except Exception:
        print("ERROR: Could not read 'staging' table. Run src/etl.py first.", file=sys.stderr)
        conn.close()
        sys.exit(1)

    if staging.empty:
        print("Staging table is empty. Nothing to transform.")
        conn.close()
        return

    # Minimal column normalization
    staging.columns = [c.strip() for c in staging.columns]

    # Parse date and add derived fields
    staging['date'] = pd.to_datetime(staging['date'], errors='coerce')
    staging = staging.dropna(subset=['date'])
    staging['date'] = staging['date'].dt.strftime('%Y-%m-%d')
    staging['year'] = pd.to_datetime(staging['date']).dt.year
    staging['month'] = pd.to_datetime(staging['date']).dt.month
    staging['quarter'] = pd.to_datetime(staging['date']).dt.quarter

    # Build dim_date
    dim_date = staging[['date', 'year', 'month', 'quarter']].drop_duplicates()

    # Build dim_property (keep a few useful columns)
    prop_cols = ['house_id', 'house_type', 'address', 'zip_code', 'city', 'area', 'region', 'year_build', 'sqm', 'no_rooms']
    prop_present = [c for c in prop_cols if c in staging.columns]
    dim_property = staging[prop_present].drop_duplicates(subset=['house_id']) if 'house_id' in prop_present else pd.DataFrame()

    # Build fact_sales (select only relevant sale columns)
    fact_cols = ['house_id', 'date', 'sales_type', 'purchase_price', '%_change_between_offer_and_purchase', 'sqm_price']
    fact_present = [c for c in fact_cols if c in staging.columns]
    fact = staging[fact_present].copy()

    # Rename long pct column to a safe name
    if '%_change_between_offer_and_purchase' in fact.columns:
        fact = fact.rename(columns={'%_change_between_offer_and_purchase': 'pct_change'})

    # Make numeric conversions for common numeric fields
    for c in ['purchase_price', 'pct_change', 'sqm_price']:
        if c in fact.columns:
            fact[c] = pd.to_numeric(fact[c], errors='coerce')

    # Write tables back to DB
    dim_date.to_sql('dim_date', conn, if_exists='replace', index=False)
    if not dim_property.empty:
        dim_property.to_sql('dim_property', conn, if_exists='replace', index=False)
    fact.to_sql('fact_sales', conn, if_exists='replace', index=False)

    # Print summary
    print(f"Wrote dim_date: {len(dim_date)} rows")
    print(f"Wrote dim_property: {len(dim_property)} rows")
    print(f"Wrote fact_sales: {len(fact)} rows")

    conn.close()

    # Run validations to enforce data quality; raise on failure so the pipeline fails fast
    import importlib
    try:
        validate = importlib.import_module('src.validate')
    except Exception:
        validate = importlib.import_module('validate')

    try:
        validate.run_all(db_path)
        print('Validation passed ✅')
    except AssertionError as e:
        print('Validation failed ❌:', e)
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', default='Data/warehouse.db')
    args = parser.parse_args()
    transform(args.db)


# Confirm counts:
# sqlite3 Data/warehouse.db "SELECT count(*) FROM staging;"
# sqlite3 -header -column Data/warehouse.db "SELECT * FROM staging LIMIT 5;"