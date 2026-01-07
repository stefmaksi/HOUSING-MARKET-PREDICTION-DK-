#!/usr/bin/env python3
"""Simple ETL extractor: read CSV and write to a staging table in SQLite.

Usage examples:
  python3 src/etl.py            # uses default CSV and DB paths
  python3 src/etl.py --sample 100
  python3 src/etl.py --csv data/sample.csv --db data/warehouse.db --table staging

"""

import argparse
import os
import sqlite3
import sys
import pandas as pd


def stage(csv_path, db_path, table='staging', sample=None):
    # Checks CSV exists; prints an error and exits if not found.
    if not os.path.exists(csv_path):
        print(f"ERROR: CSV not found: {csv_path}", file=sys.stderr)
        sys.exit(1)

    # Read CSV (optionally only first N rows for quick test)
    df = pd.read_csv(csv_path, nrows=sample) if sample else pd.read_csv(csv_path)

    # Ensure DB directory exists
    os.makedirs(os.path.dirname(db_path) or '.', exist_ok=True)

    # Write to SQLite
    conn = sqlite3.connect(db_path)
    df.to_sql(table, conn, if_exists='replace', index=False)
    conn.close()

    print(f"Staged {len(df)} rows into '{table}' in {db_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', default='/Users/sm/Developer/Projects/Danish Residential Housing EDA/Data/DKHousingPricesSample100k.csv')
    parser.add_argument('--db', default='/Users/sm/Developer/Projects/Danish Residential Housing EDA/Data/warehouse.db')
    parser.add_argument('--table', default='staging')
    parser.add_argument('--sample', type=int, help='If set, read only first N rows')
    args = parser.parse_args()

    stage(args.csv, args.db, args.table, args.sample)


if __name__ == '__main__':
    main()
