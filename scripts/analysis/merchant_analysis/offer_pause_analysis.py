"""
Merchant_A and Merchant_B Offer Pause Impact Analysis
==========================================

This script analyzes the potential active users that could have been added
if Merchant_A and Merchant_B had not paused their offers in November 2025.

Analysis Period: May 2025 - October 2025 (6 months)
Key Insights:
- Merchant_A gradually paused offers in Sept-Oct 2025
- Merchant_B fully paused in November 2025
- Both merchants had active offers before September 2025
"""

import pandas as pd
import numpy as np
from pokitpal_data import PokitPalData
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Initialize data access
data = PokitPalData()

# Analysis period: May - October 2025 (6 months before November)
analysis_months = [
    '2025-05', '2025-06', '2025-07', 
    '2025-08', '2025-09', '2025-10'
]

print("=" * 80)
print("Merchant_A AND PETBARN OFFER PAUSE IMPACT ANALYSIS")
print("=" * 80)
print(f"\nAnalysis Date: {datetime.now().strftime('%Y-%m-%d')}")
print(f"Period Analyzed: May 2025 - October 2025")
print(f"Merchants: Merchant_A, Merchant_B")
print("\n" + "=" * 80)

# Get transaction data for both merchants
print("\n📊 Loading transaction data...")

# Merchant_A Analysis (including all Merchant_A variants: online, instore, etc.)
print("\n" + "-" * 80)
print("Merchant_A ANALYSIS (All Variants)")
print("-" * 80)

bws_monthly_data = []
for month in analysis_months:
    month_data = data.get_merchant_performance(month)
    # Filter for all merchants containing "Merchant_A" (case-insensitive)
    bws_data = month_data[month_data['Merchant'].str.contains('Merchant_A', case=False, na=False)]
    if not bws_data.empty:
        # Aggregate all Merchant_A variants for the month
        bws_monthly_data.append({
            'month': month,
            'unique_users': bws_data['unique_users'].sum(),
            'transaction_count': bws_data['transaction_count'].sum(),
            'total_spend': bws_data['total_spend'].sum(),
            'variants': ', '.join(bws_data['Merchant'].tolist())
        })

# Show all Merchant_A variants found
if bws_monthly_data:
    all_variants = set()
    for month_record in bws_monthly_data:
        all_variants.update(month_record['variants'].split(', '))
    print(f"\nBWS Variants Found: {', '.join(sorted(all_variants))}")

bws_df = pd.DataFrame(bws_monthly_data)
print("\nBWS Monthly Active Users:")
print(bws_df.to_string(index=False))

# Calculate Merchant_A trends
if len(bws_df) >= 3:
    # Pre-pause period (May-Aug)
    pre_pause_months = bws_df[bws_df['month'] <= '2025-08']
    # Gradual pause period (Sept-Oct)
    pause_months = bws_df[bws_df['month'] >= '2025-09']
    
    print(f"\n📈 Pre-Pause Period (May-Aug) Average Active Users: {pre_pause_months['unique_users'].mean():.0f}")
    print(f"📉 Gradual Pause Period (Sept-Oct) Average Active Users: {pause_months['unique_users'].mean():.0f}")
    
    decline = pre_pause_months['unique_users'].mean() - pause_months['unique_users'].mean()
    if decline > 0:
        print(f"⚠️  Decline during gradual pause: {decline:.0f} users ({(decline / pre_pause_months['unique_users'].mean() * 100):.1f}%)")
    else:
        print(f"⚠️  Change during gradual pause: {decline:+.0f} users (Note: Increase observed, pause may have started later)")

# Merchant_B Analysis (including all Merchant_B variants: online, instore, etc.)
print("\n" + "-" * 80)
print("PETBARN ANALYSIS (All Variants)")
print("-" * 80)

petbarn_monthly_data = []
for month in analysis_months:
    month_data = data.get_merchant_performance(month)
    # Filter for all merchants containing "Merchant_B" (case-insensitive)
    petbarn_data = month_data[month_data['Merchant'].str.contains('Merchant_B', case=False, na=False)]
    if not petbarn_data.empty:
        # Aggregate all Merchant_B variants for the month
        petbarn_monthly_data.append({
            'month': month,
            'unique_users': petbarn_data['unique_users'].sum(),
            'transaction_count': petbarn_data['transaction_count'].sum(),
            'total_spend': petbarn_data['total_spend'].sum(),
            'variants': ', '.join(petbarn_data['Merchant'].tolist())
        })

# Show all Merchant_B variants found
if petbarn_monthly_data:
    all_variants = set()
    for month_record in petbarn_monthly_data:
        all_variants.update(month_record['variants'].split(', '))
    print(f"\nPetbarn Variants Found: {', '.join(sorted(all_variants))}")

petbarn_df = pd.DataFrame(petbarn_monthly_data)
print("\nPetbarn Monthly Active Users:")
print(petbarn_df.to_string(index=False))

# Calculate Merchant_B trends
if len(petbarn_df) >= 3:
    # Full period (May-Oct) - all active before November pause
    print(f"\n📈 Average Active Users (May-Oct): {petbarn_df['unique_users'].mean():.0f}")
    print(f"📊 Median Active Users (May-Oct): {petbarn_df['unique_users'].median():.0f}")
    print(f"📈 Trend: {petbarn_df['unique_users'].iloc[-1] - petbarn_df['unique_users'].iloc[0]:+.0f} users from May to Oct")

# PROJECTION FOR NOVEMBER 2025
print("\n" + "=" * 80)
print("NOVEMBER 2025 PROJECTION (IF OFFERS CONTINUED)")
print("=" * 80)

# Merchant_A Projection
print("\n🔮 Merchant_A Projection:")
if len(bws_df) >= 4:
    # Use pre-pause average (May-Aug) as baseline for projection
    pre_pause_avg = bws_df[bws_df['month'] <= '2025-08']['unique_users'].mean()
    
    # Calculate growth trend from pre-pause period
    pre_pause_data = bws_df[bws_df['month'] <= '2025-08'].copy()
    if len(pre_pause_data) >= 3:
        # Linear regression for trend
        x = np.arange(len(pre_pause_data))
        y = pre_pause_data['unique_users'].values
        z = np.polyfit(x, y, 1)
        growth_rate = z[0]  # monthly growth/decline
        
        print(f"   • Pre-pause baseline (May-Aug avg): {pre_pause_avg:.0f} users")
        print(f"   • Monthly growth trend: {growth_rate:+.0f} users/month")
        print(f"   • Projected November active users: {pre_pause_avg + growth_rate * 3:.0f} users")
        
        bws_projected = pre_pause_avg + growth_rate * 3
    else:
        bws_projected = pre_pause_avg
        print(f"   • Projected November active users (using pre-pause avg): {bws_projected:.0f} users")
else:
    bws_projected = bws_df['unique_users'].mean()
    print(f"   • Projected November active users (using overall avg): {bws_projected:.0f} users")

# Merchant_B Projection
print("\n🔮 Merchant_B Projection:")
if len(petbarn_df) >= 4:
    # Calculate trend from full 6-month period
    x = np.arange(len(petbarn_df))
    y = petbarn_df['unique_users'].values
    z = np.polyfit(x, y, 1)
    growth_rate = z[0]
    
    # Project for November (next month after October)
    petbarn_projected = petbarn_df['unique_users'].iloc[-1] + growth_rate
    
    print(f"   • October 2025 active users: {petbarn_df['unique_users'].iloc[-1]:.0f} users")
    print(f"   • Monthly growth trend: {growth_rate:+.0f} users/month")
    print(f"   • Projected November active users: {petbarn_projected:.0f} users")
else:
    petbarn_projected = petbarn_df['unique_users'].mean()
    print(f"   • Projected November active users (using avg): {petbarn_projected:.0f} users")

# TOTAL IMPACT
print("\n" + "=" * 80)
print("💡 TOTAL POTENTIAL ACTIVE USERS LOST IN NOVEMBER")
print("=" * 80)

total_projected = bws_projected + petbarn_projected
print(f"\n   Merchant_A:     {bws_projected:>8,.0f} projected active users")
print(f"   Merchant_B: {petbarn_projected:>8,.0f} projected active users")
print(f"   " + "-" * 40)
print(f"   TOTAL:   {total_projected:>8,.0f} potential active users")

print("\n" + "=" * 80)
print("KEY FINDINGS")
print("=" * 80)

print("""
1. Analysis includes ALL Merchant_A and Merchant_B variants (online, instore, etc.)
2. Merchant_A showed gradual offer reduction in Sept-Oct 2025
3. Merchant_B maintained consistent offer activity through October 2025
4. Both merchant groups paused/reduced offers in November 2025
5. Projections based on historical trends from May-October 2025

ASSUMPTIONS:
- Merchant_A projection uses pre-pause period (May-Aug) as baseline where available
- Merchant_B projection uses full 6-month trend through October
- Linear trend analysis applied for projections
- Aggregates all merchant variants (online, instore, etc.)
- No external market factors considered
""")

# Save results
output_data = {
    'Merchant': ['Merchant_A', 'Merchant_B', 'TOTAL'],
    'Projected_November_Active_Users': [
        int(bws_projected),
        int(petbarn_projected),
        int(total_projected)
    ]
}

results_df = pd.DataFrame(output_data)
results_df.to_csv('bws_petbarn_offer_pause_analysis.csv', index=False)

print("\n✅ Analysis complete! Results saved to 'bws_petbarn_offer_pause_analysis.csv'")
print("=" * 80)
