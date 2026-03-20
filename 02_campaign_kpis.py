# ============================================
# PROJECT 1: Campaign Analytics Dashboard
# File 2: Campaign KPIs
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ── Load clean data ──
print("Loading clean data...")
df = pd.read_csv('../data/bank_clean.csv')
print(f"Rows loaded: {len(df)}")

# ══════════════════════════════════════════
# KPI 1 — Overall Conversion Rate
# ══════════════════════════════════════════
total = len(df)
converted = df['subscribed_binary'].sum()
conversion_rate = (converted / total) * 100
print(f"\nKPI 1 — Conversion Rate: {conversion_rate:.2f}%")

# ══════════════════════════════════════════
# KPI 2 — Conversion Rate by Channel
# ══════════════════════════════════════════
channel = df.groupby('contact')['subscribed_binary'].mean() * 100
channel = channel.sort_values(ascending=False)
print(f"\nKPI 2 — Conversion by Channel:\n{channel.round(2)}")

# ══════════════════════════════════════════
# KPI 3 — Monthly Conversion Trend
# ══════════════════════════════════════════
month_order = ['jan','feb','mar','apr','may','jun',
               'jul','aug','sep','oct','nov','dec']
monthly = df.groupby('month')['subscribed_binary'].mean() * 100
monthly = monthly.reindex(month_order).dropna()
print(f"\nKPI 3 — Monthly Conversion:\n{monthly.round(2)}")

# ══════════════════════════════════════════
# KPI 4 — Call Duration vs Conversion
# ══════════════════════════════════════════
bins = [0, 60, 180, 600, 99999]
labels = ['<1 min', '1-3 min', '3-10 min', '10+ min']
df['duration_bucket'] = pd.cut(df['duration'], bins=bins, labels=labels)
duration = df.groupby('duration_bucket', observed=True)['subscribed_binary'].mean() * 100
print(f"\nKPI 4 — Conversion by Call Duration:\n{duration.round(2)}")

# ══════════════════════════════════════════
# KPI 5 — Campaign Fatigue
# ══════════════════════════════════════════
df['campaign_bucket'] = df['campaign'].clip(upper=6)
df['campaign_bucket'] = df['campaign_bucket'].astype(str)
df.loc[df['campaign'] >= 6, 'campaign_bucket'] = '6+'
fatigue = df.groupby('campaign_bucket', observed=True)['subscribed_binary'].mean() * 100
fatigue.index = fatigue.index.astype(str)
fatigue = fatigue.reindex(sorted(fatigue.index, key=lambda x: int(x.replace('+','99'))))
print(f"\nKPI 5 — Campaign Fatigue:\n{fatigue.round(2)}")

# ══════════════════════════════════════════
# KPI 6 — Previous Campaign Effect
# ══════════════════════════════════════════
df['had_previous'] = (df['previous'] > 0).map({True: 'Had prior contact', False: 'No prior contact'})
prev = df.groupby('had_previous')['subscribed_binary'].mean() * 100
print(f"\nKPI 6 — Previous Campaign Effect:\n{prev.round(2)}")

# ══════════════════════════════════════════
# BUILD THE 6-PANEL DASHBOARD
# ══════════════════════════════════════════
print("\nBuilding dashboard chart...")
fig = plt.figure(figsize=(18, 12))
fig.suptitle('Campaign Performance KPI Dashboard', fontsize=18, fontweight='bold', y=0.98)
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

# Panel 1 — Conversion Rate (big number)
ax1 = fig.add_subplot(gs[0, 0])
ax1.text(0.5, 0.55, f"{conversion_rate:.1f}%", ha='center', va='center',
         fontsize=52, fontweight='bold', color='#2ecc71', transform=ax1.transAxes)
ax1.text(0.5, 0.2, 'Overall Conversion Rate', ha='center', va='center',
         fontsize=12, color='gray', transform=ax1.transAxes)
ax1.axis('off')
ax1.set_title('KPI 1 — Conversion Rate', fontweight='bold')

# Panel 2 — Channel Performance
ax2 = fig.add_subplot(gs[0, 1])
bars = ax2.bar(channel.index, channel.values, color=['#3498db','#e74c3c','#95a5a6'])
ax2.set_title('KPI 2 — Conversion by Channel', fontweight='bold')
ax2.set_ylabel('Conversion Rate (%)')
ax2.set_ylim(0, channel.max() * 1.3)
for bar, val in zip(bars, channel.values):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f'{val:.1f}%', ha='center', fontsize=10, fontweight='bold')

# Panel 3 — Monthly Trend
ax3 = fig.add_subplot(gs[0, 2])
ax3.plot(monthly.index, monthly.values, marker='o', color='#9b59b6', linewidth=2)
ax3.set_title('KPI 3 — Monthly Conversion Trend', fontweight='bold')
ax3.set_ylabel('Conversion Rate (%)')
ax3.tick_params(axis='x', rotation=45)
ax3.grid(axis='y', alpha=0.3)

# Panel 4 — Call Duration
ax4 = fig.add_subplot(gs[1, 0])
bars4 = ax4.bar(duration.index, duration.values, color=['#e74c3c','#f39c12','#2ecc71','#27ae60'])
ax4.set_title('KPI 4 — Call Duration vs Conversion', fontweight='bold')
ax4.set_ylabel('Conversion Rate (%)')
ax4.set_ylim(0, duration.max() * 1.3)
for bar, val in zip(bars4, duration.values):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f'{val:.1f}%', ha='center', fontsize=10, fontweight='bold')

# Panel 5 — Campaign Fatigue
ax5 = fig.add_subplot(gs[1, 1])
ax5.plot(fatigue.index, fatigue.values, marker='o', color='#e74c3c', linewidth=2)
ax5.set_title('KPI 5 — Campaign Fatigue', fontweight='bold')
ax5.set_xlabel('Number of Contacts')
ax5.set_ylabel('Conversion Rate (%)')
ax5.grid(axis='y', alpha=0.3)

# Panel 6 — Previous Campaign Effect
ax6 = fig.add_subplot(gs[1, 2])
bars6 = ax6.bar(prev.index, prev.values, color=['#3498db','#bdc3c7'])
ax6.set_title('KPI 6 — Previous Campaign Effect', fontweight='bold')
ax6.set_ylabel('Conversion Rate (%)')
ax6.set_ylim(0, prev.max() * 1.3)
for bar, val in zip(bars6, prev.values):
    ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f'{val:.1f}%', ha='center', fontsize=10, fontweight='bold')

plt.savefig('../outputs/kpi_dashboard.png', dpi=150, bbox_inches='tight')
print("✅ Dashboard saved to outputs/kpi_dashboard.png")
plt.show()
