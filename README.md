# Campaign Performance Analytics Dashboard

End-to-end campaign analytics pipeline built using the
UCI Bank Marketing dataset (10,634 records).

## What This Project Does
- Cleans and prepares 10,000+ rows of bank CRM campaign data
- Computes 6 campaign KPIs: conversion rate, channel performance,
  monthly trends, call duration analysis, contact fatigue, and
  previous campaign effect
- Performs cohort analysis across 4 customer age segments
- Visualises findings in a 6-panel matplotlib dashboard
- Delivers a structured insights report with 5 recommendations

## Tools Used
Python | pandas | numpy | matplotlib | seaborn | Power BI | Excel

## Key Findings
- Overall conversion rate: 47.22%
- Cellular channel outperforms telephone by 4.2 percentage points
- Campaign fatigue: conversion drops from 53% to 29% after 6+ contacts
- Pre-Retirement (60+) cohort converts at 82.8% but gets only 5.2% 
  of contacts — the most underserved high-value segment

## Files
| File | Description |
|------|-------------|
| 01_data_cleaning.py | Load, clean, and validate raw data |
| 02_campaign_kpis.py | Compute 6 KPIs and generate dashboard |
| 03_cohort_analysis.py | Segment customers and compare cohorts |
| 04_export_excel.py | Export data to Excel for Power BI |
| outputs/kpi_dashboard.png | 6-panel KPI visualisation |
| outputs/cohort_analysis.png | Cohort comparison charts |
| outputs/insights_report.pdf | Stakeholder-ready findings report |

## Dataset
UCI Bank Marketing Dataset via Kaggle:
https://www.kaggle.com/datasets/janiobachmann/bank-marketing-dataset
