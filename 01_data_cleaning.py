# ============================================
# PROJECT 1: Campaign Analytics Dashboard
# File 1: Data Cleaning
# ============================================

import pandas as pd
import numpy as np

# ── STEP 1: Load the data ──
# YOUR dataset uses commas, so we use sep=','
print("Loading data...")
df = pd.read_csv('../data/bank.csv', sep=',')

# ── STEP 2: See the basic info ──
print("\n--- BASIC INFO ---")
print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"\nColumn names: {list(df.columns)}")

# ── STEP 3: See first 5 rows ──
print("\n--- FIRST 5 ROWS ---")
print(df.head())

# ── STEP 4: Check for missing values ──
print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

# ── STEP 5: Check 'unknown' values ──
print("\n--- UNKNOWN VALUES PER COLUMN ---")
for col in df.columns:
    unknown_count = (df[col] == 'unknown').sum()
    if unknown_count > 0:
        print(f"{col}: {unknown_count} unknown values")

# ── STEP 6: Rename columns for clarity ──
print("\nRenaming columns...")
df.rename(columns={
    'deposit': 'subscribed'   # your file uses 'deposit' not 'y'
}, inplace=True)

# ── STEP 7: Replace 'unknown' with NaN ──
df.replace('unknown', np.nan, inplace=True)

# ── STEP 8: Create a binary column for subscribed ──
# 1 = subscribed (yes), 0 = did not subscribe (no)
df['subscribed_binary'] = (df['subscribed'] == 'yes').astype(int)

# ── STEP 9: Drop rows where key columns are missing ──
before = len(df)
df.dropna(subset=['job', 'education'], inplace=True)
after = len(df)
print(f"\nRows removed due to missing job/education: {before - after}")
print(f"Clean dataset size: {after} rows")

# ── STEP 10: Check the overall conversion rate ──
total = len(df)
converted = df['subscribed_binary'].sum()
rate = (converted / total) * 100
print(f"\n--- HEADLINE METRIC ---")
print(f"Total customers contacted: {total}")
print(f"Total subscriptions (conversions): {converted}")
print(f"Overall Conversion Rate: {rate:.2f}%")

# ── STEP 11: Save the clean file ──
df.to_csv('../data/bank_clean.csv', index=False)
print("\n✅ Clean data saved to data/bank_clean.csv")