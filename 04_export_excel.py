# ============================================
# PROJECT 1: Export KPIs to Excel for Power BI
# ============================================

import pandas as pd
import numpy as np

df = pd.read_csv('../data/bank_clean.csv')

# Monthly performance table
month_order = ['jan','feb','mar','apr','may','jun',
               'jul','aug','sep','oct','nov','dec']
monthly = df.groupby('month').agg(
    total_contacts=('subscribed_binary','count'),
    conversions=('subscribed_binary','sum')
).reindex(month_order).dropna()
monthly['conversion_rate'] = (monthly['conversions'] / monthly['total_contacts'] * 100).round(2)
monthly.reset_index(inplace=True)

# Channel performance table
channel = df.groupby('contact').agg(
    total_contacts=('subscribed_binary','count'),
    conversions=('subscribed_binary','sum')
)
channel['conversion_rate'] = (channel['conversions'] / channel['total_contacts'] * 100).round(2)
channel.reset_index(inplace=True)

# Cohort table
bins = [0, 30, 45, 60, 999]
labels = ['Young (Under 30)', 'Mid-Career (30-45)', 'Established (45-60)', 'Pre-Retirement (60+)']
df['cohort'] = pd.cut(df['age'], bins=bins, labels=labels)
cohort = df.groupby('cohort', observed=True).agg(
    total_contacts=('subscribed_binary','count'),
    conversions=('subscribed_binary','sum'),
    avg_balance=('balance','mean'),
    avg_duration=('duration','mean')
)
cohort['conversion_rate'] = (cohort['conversions'] / cohort['total_contacts'] * 100).round(2)
cohort['avg_balance'] = cohort['avg_balance'].round(2)
cohort['avg_duration'] = cohort['avg_duration'].round(2)
cohort.reset_index(inplace=True)

# Write to Excel with 4 sheets
with pd.ExcelWriter('../outputs/campaign_kpis.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Full_Clean_Data', index=False)
    monthly.to_excel(writer, sheet_name='Monthly_Performance', index=False)
    channel.to_excel(writer, sheet_name='Channel_Performance', index=False)
    cohort.to_excel(writer, sheet_name='Cohort_Analysis', index=False)

print("✅ Excel file saved to outputs/campaign_kpis.xlsx")
print("   Sheets: Full_Clean_Data, Monthly_Performance, Channel_Performance, Cohort_Analysis")
