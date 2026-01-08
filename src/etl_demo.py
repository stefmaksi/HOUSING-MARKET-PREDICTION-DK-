"""Notebook-like demo script to run the ETL, run the transform, show queries and plots.
Run this as: python notebooks/etl_demo.py
"""

import subprocess
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def show_counts_and_preview(db_path):
    if not os.path.exists(db_path):
        raise FileNotFoundError(
            f"DB file not found: {db_path}. Run src/etl.py first or set the correct db_path."
        )
    con = sqlite3.connect(db_path)
    counts = pd.read_sql_query(
        """
SELECT 
 (SELECT COUNT(*) FROM staging) AS staging_rows,
 (SELECT COUNT(*) FROM dim_date) AS dim_date_rows,
 (SELECT COUNT(*) FROM dim_property) AS dim_property_rows,
 (SELECT COUNT(*) FROM fact_sales) AS fact_sales_rows
""",
        con,
    )
    print(counts)
    print("\nSample rows from fact_sales:")
    print(pd.read_sql_query("SELECT * FROM fact_sales LIMIT 10", con))
    con.close()


def plot_avg_price_by_year(db_path):
    if not os.path.exists(db_path):
        raise FileNotFoundError(
            f"DB file not found: {db_path}. Run src/etl.py first or set the correct db_path."
        )
    con = sqlite3.connect(db_path)
    avg_by_year = pd.read_sql_query(
        """SELECT d.year, AVG(f.purchase_price) AS avg_price
FROM fact_sales f
JOIN dim_date d ON f.date = d.date
GROUP BY d.year
ORDER BY d.year""",
        con,
    )
    con.close()
    ax = avg_by_year.plot.bar(x="year", y="avg_price", legend=False, figsize=(8, 4))
    ax.set_ylabel("Average purchase price (DKK)")
    ax.set_title("Average purchase price by year")
    plt.tight_layout()
    plt.show()


def plot_top_regions(db_path):
    if not os.path.exists(db_path):
        raise FileNotFoundError(
            f"DB file not found: {db_path}. Run src/etl.py first or set the correct db_path."
        )
    con = sqlite3.connect(db_path)
    sales_by_region = pd.read_sql_query(
        """SELECT p.region, COUNT(*) AS sales_count
FROM fact_sales f
JOIN dim_property p ON f.house_id = p.house_id
GROUP BY p.region
ORDER BY sales_count DESC
LIMIT 10""",
        con,
    )
    con.close()
    ax = sales_by_region.plot.bar(
        x="region", y="sales_count", legend=False, figsize=(10, 4)
    )
    ax.set_ylabel("Number of sales")
    ax.set_title("Top 10 regions by sales")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def plot_price_distribution(db_path):
    if not os.path.exists(db_path):
        raise FileNotFoundError(
            f"DB file not found: {db_path}. Run src/etl.py first or set the correct db_path."
        )
    con = sqlite3.connect(db_path)
    prices = pd.read_sql_query(
        "SELECT purchase_price FROM fact_sales WHERE purchase_price IS NOT NULL", con
    )
    con.close()
    plt.figure(figsize=(8, 4))
    sns.histplot(prices["purchase_price"], bins=50, kde=False)
    plt.xscale("log")
    plt.title("Purchase price distribution (log scale)")
    plt.xlabel("Price (DKK)")
    plt.tight_layout()
    plt.show()
