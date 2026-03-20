import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ── Load clean data ──
print("Loading clean data...")
df = pd.read_csv('../data/bank_clean.csv')
print(f"Rows loaded: {len(df)}")

# ══════════════════════════════════════════
# CREATE 4 AGE COHORTS
# ══════════════════════════════════════════
bins = [0, 30, 45, 60, 999]
labels = ['Young (Under 30)', 'Mid-Career (30-45)', 'Established (45-60)', 'Pre-Retirement (60+)']
df['cohort'] = pd.cut(df['age'], bins=bins, labels=labels)

print("\n--- COHORT SIZES ---")
print(df['cohort'].value_counts().sort_index())

# ══════════════════════════════════════════
# COHORT METRICS
# ══════════════════════════════════════════

# Conversion rate per cohort
cohort_conversion = df.groupby('cohort', observed=True)['subscribed_binary'].mean() * 100

# Average balance per cohort
cohort_balance = df.groupby('cohort', observed=True)['balance'].mean()

# Average call duration per cohort
cohort_duration = df.groupby('cohort', observed=True)['duration'].mean()

# Share of total contacts per cohort
cohort_share = df['cohort'].value_counts(normalize=True).sort_index() * 100

print("\n--- COHORT CONVERSION RATES ---")
print(cohort_conversion.round(2))

print("\n--- AVERAGE BALANCE PER COHORT ---")
print(cohort_balance.round(2))

print("\n--- AVERAGE CALL DURATION (seconds) ---")
print(cohort_duration.round(2))

print("\n--- SHARE OF TOTAL CONTACTS ---")
print(cohort_share.round(2))

# ══════════════════════════════════════════
# BUILD COHORT DASHBOARD (4 panels)
# ══════════════════════════════════════════
print("\nBuilding cohort chart...")

colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']
short_labels = ['Young\n(<30)', 'Mid-Career\n(30-45)', 'Established\n(45-60)', 'Pre-Retire\n(60+)']

fig = plt.figure(figsize=(16, 10))
fig.suptitle('Customer Cohort Analysis', fontsize=16, fontweight='bold', y=0.98)
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

# Panel 1 — Conversion Rate by Cohort
ax1 = fig.add_subplot(gs[0, 0])
bars1 = ax1.bar(short_labels, cohort_conversion.values, color=colors)
ax1.set_title('Conversion Rate by Cohort', fontweight='bold')
ax1.set_ylabel('Conversion Rate (%)')
ax1.set_ylim(0, cohort_conversion.max() * 1.3)
for bar, val in zip(bars1, cohort_conversion.values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f'{val:.1f}%', ha='center', fontsize=10, fontweight='bold')

# Panel 2 — Average Balance by Cohort
ax2 = fig.add_subplot(gs[0, 1])
bars2 = ax2.bar(short_labels, cohort_balance.values, color=colors)
ax2.set_title('Average Account Balance by Cohort', fontweight='bold')
ax2.set_ylabel('Average Balance (£)')
ax2.set_ylim(0, cohort_balance.max() * 1.3)
for bar, val in zip(bars2, cohort_balance.values):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
             f'£{val:,.0f}', ha='center', fontsize=10, fontweight='bold')

# Panel 3 — Share of Contacts
ax3 = fig.add_subplot(gs[1, 0])
ax3.pie(cohort_share.values, labels=short_labels, colors=colors,
        autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10})
ax3.set_title('Share of Total Contacts', fontweight='bold')

# Panel 4 — Avg Call Duration
ax4 = fig.add_subplot(gs[1, 1])
bars4 = ax4.bar(short_labels, cohort_duration.values, color=colors)
ax4.set_title('Average Call Duration by Cohort', fontweight='bold')
ax4.set_ylabel('Duration (seconds)')
ax4.set_ylim(0, cohort_duration.max() * 1.3)
for bar, val in zip(bars4, cohort_duration.values):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
             f'{val:.0f}s', ha='center', fontsize=10, fontweight='bold')

plt.savefig('../outputs/cohort_analysis.png', dpi=150, bbox_inches='tight')
print("✅ Cohort chart saved to outputs/cohort_analysis.png")
plt.show()