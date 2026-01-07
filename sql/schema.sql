-- Simple schema for the demo warehouse
-- dim_date: one row per date
CREATE TABLE IF NOT EXISTS dim_date (
  date TEXT PRIMARY KEY,
  year INTEGER,
  month INTEGER,
  quarter TEXT
);

-- dim_property: one row per property (house_id)
CREATE TABLE IF NOT EXISTS dim_property (
  house_id TEXT PRIMARY KEY,
  house_type TEXT,
  address TEXT,
  zip_code TEXT,
  city TEXT,
  area TEXT,
  region TEXT,
  year_build INTEGER,
  sqm REAL,
  no_rooms INTEGER
);

-- fact_sales: one row per sale
CREATE TABLE IF NOT EXISTS fact_sales (
  sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
  house_id TEXT,
  date TEXT,
  sales_type TEXT,
  purchase_price REAL,
  pct_change REAL,
  sqm_price REAL,
  nom_interest_rate REAL,
  dk_ann_infl_rate REAL,
  yield_on_mortgage_credit_bonds REAL
);
