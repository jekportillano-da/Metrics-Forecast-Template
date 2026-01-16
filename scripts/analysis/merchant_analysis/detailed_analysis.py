"""
Merchant_A and Merchant_B Offer Pause Impact Analysis - DETAILED VERSION
============================================================

Comprehensive analysis including:
- Variant-level performance breakdown
- User behavior patterns
- Transaction patterns and spend analysis
- Growth trends and seasonality
- Risk assessment and recommendations
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

# Analysis period: May - October 2025
analysis_months = ['2025-05', '2025-06', '2025-07', '2025-08', '2025-09', '2025-10']

print("=" * 100)
print("Merchant_A AND PETBARN OFFER PAUSE IMPACT ANALYSIS - COMPREHENSIVE REPORT")
print("=" * 100)
print(f"\nReport Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Analysis Period: May 2025 - October 2025 (6 months)")
print(f"Projection Target: November 2025")
print("\n" + "=" * 100)

# ============================================================================
# SECTION 1: DATA COLLECTION AND MERCHANT VARIANT IDENTIFICATION
# ============================================================================
print("\n" + "█" * 100)
print("SECTION 1: MERCHANT VARIANT IDENTIFICATION & DATA COLLECTION")
print("█" * 100)

# Collect all merchant data to identify variants
all_merchants = set()
for month in analysis_months:
    month_data = data.get_merchant_performance(month)
    all_merchants.update(month_data['Merchant'].tolist())

bws_variants = sorted([m for m in all_merchants if 'Merchant_A' in m.upper()])
petbarn_variants = sorted([m for m in all_merchants if 'PETBARN' in m.upper()])

print(f"\n📋 Merchant_A VARIANTS IDENTIFIED ({len(bws_variants)}):")
for i, variant in enumerate(bws_variants, 1):
    print(f"   {i}. {variant}")

print(f"\n📋 PETBARN VARIANTS IDENTIFIED ({len(petbarn_variants)}):")
for i, variant in enumerate(petbarn_variants, 1):
    print(f"   {i}. {variant}")

# ============================================================================
# SECTION 2: Merchant_A DETAILED ANALYSIS
# ============================================================================
print("\n\n" + "█" * 100)
print("SECTION 2: Merchant_A COMPREHENSIVE ANALYSIS")
print("█" * 100)

# Collect Merchant_A data by variant and month
bws_detailed_data = []
bws_monthly_totals = []

for month in analysis_months:
    month_data = data.get_merchant_performance(month)
    bws_data = month_data[month_data['Merchant'].str.contains('Merchant_A', case=False, na=False)]
    
    if not bws_data.empty:
        # Monthly totals
        bws_monthly_totals.append({
            'month': month,
            'total_users': bws_data['unique_users'].sum(),
            'total_transactions': bws_data['transaction_count'].sum(),
            'total_spend': bws_data['total_spend'].sum(),
            'avg_transaction_value': bws_data['total_spend'].sum() / bws_data['transaction_count'].sum(),
            'avg_transactions_per_user': bws_data['transaction_count'].sum() / bws_data['unique_users'].sum(),
            'variant_count': len(bws_data)
        })
        
        # Variant-level details
        for _, row in bws_data.iterrows():
            bws_detailed_data.append({
                'month': month,
                'variant': row['Merchant'],
                'unique_users': row['unique_users'],
                'transaction_count': row['transaction_count'],
                'total_spend': row['total_spend'],
                'avg_spend_per_user': row['total_spend'] / row['unique_users'] if row['unique_users'] > 0 else 0,
                'avg_transaction_value': row['total_spend'] / row['transaction_count'] if row['transaction_count'] > 0 else 0
            })

bws_monthly_df = pd.DataFrame(bws_monthly_totals)
bws_detailed_df = pd.DataFrame(bws_detailed_data)

print("\n" + "─" * 100)
print("2.1 Merchant_A MONTHLY PERFORMANCE SUMMARY")
print("─" * 100)
print("\n" + bws_monthly_df.to_string(index=False))

# Calculate key metrics
print("\n" + "─" * 100)
print("2.2 Merchant_A KEY PERFORMANCE INDICATORS")
print("─" * 100)

total_bws_users = bws_monthly_df['total_users'].sum()
avg_monthly_users = bws_monthly_df['total_users'].mean()
total_bws_spend = bws_monthly_df['total_spend'].sum()
total_bws_transactions = bws_monthly_df['total_transactions'].sum()

print(f"\n📊 Overall Metrics (May-Oct 2025):")
print(f"   • Total Unique Users (cumulative): {total_bws_users:,}")
print(f"   • Average Monthly Active Users: {avg_monthly_users:,.0f}")
print(f"   • Total Transaction Volume: {total_bws_transactions:,}")
print(f"   • Total Spend: ${total_bws_spend:,.2f}")
print(f"   • Average Transaction Value: ${bws_monthly_df['avg_transaction_value'].mean():.2f}")
print(f"   • Average Transactions per User: {bws_monthly_df['avg_transactions_per_user'].mean():.2f}")

# Trend analysis
print(f"\n📈 Growth & Trend Analysis:")
first_month = bws_monthly_df.iloc[0]
last_month = bws_monthly_df.iloc[-1]
user_growth = ((last_month['total_users'] - first_month['total_users']) / first_month['total_users'] * 100)
spend_growth = ((last_month['total_spend'] - first_month['total_spend']) / first_month['total_spend'] * 100)

print(f"   • User Growth (Jul to Oct): {user_growth:+.1f}%")
print(f"   • Spend Growth (Jul to Oct): {spend_growth:+.1f}%")
print(f"   • Peak Month: {bws_monthly_df.loc[bws_monthly_df['total_users'].idxmax(), 'month']} with {bws_monthly_df['total_users'].max():,} users")
print(f"   • Lowest Month: {bws_monthly_df.loc[bws_monthly_df['total_users'].idxmin(), 'month']} with {bws_monthly_df['total_users'].min():,} users")

# Variance analysis
print(f"\n📊 Volatility Analysis:")
user_std = bws_monthly_df['total_users'].std()
user_cv = (user_std / avg_monthly_users) * 100
print(f"   • Standard Deviation: {user_std:,.0f} users")
print(f"   • Coefficient of Variation: {user_cv:.1f}%")
print(f"   • Interpretation: {'High volatility' if user_cv > 20 else 'Moderate volatility' if user_cv > 10 else 'Low volatility'}")

# Pre-pause vs Gradual-pause period analysis
pre_pause = bws_monthly_df[bws_monthly_df['month'] <= '2025-08']
gradual_pause = bws_monthly_df[bws_monthly_df['month'] >= '2025-09']

print(f"\n⚠️  Pre-Pause vs Gradual Pause Period Comparison:")
print(f"   Pre-Pause Period (May-Aug):")
print(f"      • Average Users: {pre_pause['total_users'].mean():,.0f}")
print(f"      • Average Spend: ${pre_pause['total_spend'].mean():,.2f}")
print(f"   Gradual Pause Period (Sept-Oct):")
print(f"      • Average Users: {gradual_pause['total_users'].mean():,.0f}")
print(f"      • Average Spend: ${gradual_pause['total_spend'].mean():,.2f}")

user_change = gradual_pause['total_users'].mean() - pre_pause['total_users'].mean()
spend_change = gradual_pause['total_spend'].mean() - pre_pause['total_spend'].mean()

print(f"   Change:")
print(f"      • Users: {user_change:+,.0f} ({(user_change/pre_pause['total_users'].mean()*100):+.1f}%)")
print(f"      • Spend: ${spend_change:+,.2f} ({(spend_change/pre_pause['total_spend'].mean()*100):+.1f}%)")
print(f"\n   💡 Insight: {'UNEXPECTED - Users increased during supposed gradual pause' if user_change > 0 else 'As expected - Users decreased during gradual pause'}")

# Variant-level performance
print("\n" + "─" * 100)
print("2.3 Merchant_A VARIANT-LEVEL PERFORMANCE BREAKDOWN")
print("─" * 100)

variant_summary = bws_detailed_df.groupby('variant').agg({
    'unique_users': 'sum',
    'transaction_count': 'sum',
    'total_spend': 'sum'
}).reset_index()

variant_summary['avg_spend_per_user'] = variant_summary['total_spend'] / variant_summary['unique_users']
variant_summary = variant_summary.sort_values('total_spend', ascending=False)

print("\n" + variant_summary.to_string(index=False))

print(f"\n📊 Variant Insights:")
top_variant = variant_summary.iloc[0]
print(f"   • Top Performing Variant: {top_variant['variant']}")
print(f"      - Total Spend: ${top_variant['total_spend']:,.2f} ({top_variant['total_spend']/variant_summary['total_spend'].sum()*100:.1f}% of total)")
print(f"      - Users: {top_variant['unique_users']:,.0f} ({top_variant['unique_users']/variant_summary['unique_users'].sum()*100:.1f}% of total)")

# ============================================================================
# SECTION 3: PETBARN DETAILED ANALYSIS
# ============================================================================
print("\n\n" + "█" * 100)
print("SECTION 3: PETBARN COMPREHENSIVE ANALYSIS")
print("█" * 100)

# Collect Merchant_B data by variant and month
petbarn_detailed_data = []
petbarn_monthly_totals = []

for month in analysis_months:
    month_data = data.get_merchant_performance(month)
    petbarn_data = month_data[month_data['Merchant'].str.contains('Merchant_B', case=False, na=False)]
    
    if not petbarn_data.empty:
        # Monthly totals
        petbarn_monthly_totals.append({
            'month': month,
            'total_users': petbarn_data['unique_users'].sum(),
            'total_transactions': petbarn_data['transaction_count'].sum(),
            'total_spend': petbarn_data['total_spend'].sum(),
            'avg_transaction_value': petbarn_data['total_spend'].sum() / petbarn_data['transaction_count'].sum(),
            'avg_transactions_per_user': petbarn_data['transaction_count'].sum() / petbarn_data['unique_users'].sum(),
            'variant_count': len(petbarn_data)
        })
        
        # Variant-level details
        for _, row in petbarn_data.iterrows():
            petbarn_detailed_data.append({
                'month': month,
                'variant': row['Merchant'],
                'unique_users': row['unique_users'],
                'transaction_count': row['transaction_count'],
                'total_spend': row['total_spend'],
                'avg_spend_per_user': row['total_spend'] / row['unique_users'] if row['unique_users'] > 0 else 0,
                'avg_transaction_value': row['total_spend'] / row['transaction_count'] if row['transaction_count'] > 0 else 0
            })

petbarn_monthly_df = pd.DataFrame(petbarn_monthly_totals)
petbarn_detailed_df = pd.DataFrame(petbarn_detailed_data)

print("\n" + "─" * 100)
print("3.1 PETBARN MONTHLY PERFORMANCE SUMMARY")
print("─" * 100)
print("\n" + petbarn_monthly_df.to_string(index=False))

# Calculate key metrics
print("\n" + "─" * 100)
print("3.2 PETBARN KEY PERFORMANCE INDICATORS")
print("─" * 100)

total_petbarn_users = petbarn_monthly_df['total_users'].sum()
avg_monthly_users_pb = petbarn_monthly_df['total_users'].mean()
total_petbarn_spend = petbarn_monthly_df['total_spend'].sum()
total_petbarn_transactions = petbarn_monthly_df['total_transactions'].sum()

print(f"\n📊 Overall Metrics (May-Oct 2025):")
print(f"   • Total Unique Users (cumulative): {total_petbarn_users:,}")
print(f"   • Average Monthly Active Users: {avg_monthly_users_pb:,.0f}")
print(f"   • Total Transaction Volume: {total_petbarn_transactions:,}")
print(f"   • Total Spend: ${total_petbarn_spend:,.2f}")
print(f"   • Average Transaction Value: ${petbarn_monthly_df['avg_transaction_value'].mean():.2f}")
print(f"   • Average Transactions per User: {petbarn_monthly_df['avg_transactions_per_user'].mean():.2f}")

# Trend analysis
print(f"\n📈 Growth & Trend Analysis:")
first_month_pb = petbarn_monthly_df.iloc[0]
last_month_pb = petbarn_monthly_df.iloc[-1]
user_growth_pb = ((last_month_pb['total_users'] - first_month_pb['total_users']) / first_month_pb['total_users'] * 100)
spend_growth_pb = ((last_month_pb['total_spend'] - first_month_pb['total_spend']) / first_month_pb['total_spend'] * 100)

print(f"   • User Growth (Jul to Oct): {user_growth_pb:+.1f}%")
print(f"   • Spend Growth (Jul to Oct): {spend_growth_pb:+.1f}%")
print(f"   • Peak Month: {petbarn_monthly_df.loc[petbarn_monthly_df['total_users'].idxmax(), 'month']} with {petbarn_monthly_df['total_users'].max():,} users")
print(f"   • Lowest Month: {petbarn_monthly_df.loc[petbarn_monthly_df['total_users'].idxmin(), 'month']} with {petbarn_monthly_df['total_users'].min():,} users")

# Variance analysis
print(f"\n📊 Volatility Analysis:")
user_std_pb = petbarn_monthly_df['total_users'].std()
user_cv_pb = (user_std_pb / avg_monthly_users_pb) * 100
print(f"   • Standard Deviation: {user_std_pb:,.0f} users")
print(f"   • Coefficient of Variation: {user_cv_pb:.1f}%")
print(f"   • Interpretation: {'HIGH volatility - significant fluctuations' if user_cv_pb > 50 else 'Moderate volatility' if user_cv_pb > 20 else 'Low volatility'}")

# Variant-level performance
print("\n" + "─" * 100)
print("3.3 PETBARN VARIANT-LEVEL PERFORMANCE BREAKDOWN")
print("─" * 100)

variant_summary_pb = petbarn_detailed_df.groupby('variant').agg({
    'unique_users': 'sum',
    'transaction_count': 'sum',
    'total_spend': 'sum'
}).reset_index()

variant_summary_pb['avg_spend_per_user'] = variant_summary_pb['total_spend'] / variant_summary_pb['unique_users']
variant_summary_pb = variant_summary_pb.sort_values('total_spend', ascending=False)

print("\n" + variant_summary_pb.to_string(index=False))

print(f"\n📊 Variant Insights:")
top_variant_pb = variant_summary_pb.iloc[0]
print(f"   • Top Performing Variant: {top_variant_pb['variant']}")
print(f"      - Total Spend: ${top_variant_pb['total_spend']:,.2f} ({top_variant_pb['total_spend']/variant_summary_pb['total_spend'].sum()*100:.1f}% of total)")
print(f"      - Users: {top_variant_pb['unique_users']:,.0f} ({top_variant_pb['unique_users']/variant_summary_pb['unique_users'].sum()*100:.1f}% of total)")

# ============================================================================
# SECTION 4: NOVEMBER PROJECTION & FORECASTING
# ============================================================================
print("\n\n" + "█" * 100)
print("SECTION 4: NOVEMBER 2025 PROJECTION & IMPACT ANALYSIS")
print("█" * 100)

print("\n" + "─" * 100)
print("4.1 Merchant_A NOVEMBER PROJECTION")
print("─" * 100)

# Multiple projection methods for Merchant_A
print("\nProjection Methodology:")

# Method 1: Pre-pause average (conservative)
pre_pause_avg_bws = pre_pause['total_users'].mean()
print(f"\n   Method 1 - Pre-Pause Baseline (May-Aug Average):")
print(f"      • Projected Users: {pre_pause_avg_bws:,.0f}")
print(f"      • Rationale: Conservative estimate using pre-pause performance")

# Method 2: Linear regression on pre-pause period
if len(pre_pause) >= 3:
    x = np.arange(len(pre_pause))
    y = pre_pause['total_users'].values
    z = np.polyfit(x, y, 1)
    growth_rate_bws = z[0]
    intercept = z[1]
    months_ahead = 3  # From August to November
    bws_linear_projection = intercept + growth_rate_bws * (len(pre_pause) + months_ahead - 1)
    
    print(f"\n   Method 2 - Linear Trend (Pre-Pause Period):")
    print(f"      • Monthly Growth Rate: {growth_rate_bws:+.0f} users/month")
    print(f"      • Projected Users: {bws_linear_projection:,.0f}")
    print(f"      • Rationale: Extends pre-pause trend into November")

# Method 3: Recent average (last 3 months)
recent_avg_bws = bws_monthly_df.tail(3)['total_users'].mean()
print(f"\n   Method 3 - Recent Period Average (Aug-Oct):")
print(f"      • Projected Users: {recent_avg_bws:,.0f}")
print(f"      • Rationale: Most recent performance indicator")

# Selected projection
bws_projected = pre_pause_avg_bws  # Using conservative estimate
print(f"\n   ✅ SELECTED PROJECTION: {bws_projected:,.0f} users")
print(f"      (Using Method 1 - Conservative pre-pause baseline)")

print("\n" + "─" * 100)
print("4.2 PETBARN NOVEMBER PROJECTION")
print("─" * 100)

print("\nProjection Methodology:")

# Method 1: Overall average
overall_avg_pb = petbarn_monthly_df['total_users'].mean()
print(f"\n   Method 1 - 6-Month Average (May-Oct):")
print(f"      • Projected Users: {overall_avg_pb:,.0f}")
print(f"      • Rationale: Average of full analysis period")

# Method 2: Linear regression
x_pb = np.arange(len(petbarn_monthly_df))
y_pb = petbarn_monthly_df['total_users'].values
z_pb = np.polyfit(x_pb, y_pb, 1)
growth_rate_pb = z_pb[0]
intercept_pb = z_pb[1]
petbarn_linear_projection = intercept_pb + growth_rate_pb * len(petbarn_monthly_df)

print(f"\n   Method 2 - Linear Trend Extrapolation:")
print(f"      • Monthly Growth Rate: {growth_rate_pb:+.0f} users/month")
print(f"      • Projected Users: {petbarn_linear_projection:,.0f}")
print(f"      • Rationale: Extends observed trend")

# Method 3: Median (less sensitive to outliers)
median_pb = petbarn_monthly_df['total_users'].median()
print(f"\n   Method 3 - Median (Outlier-Resistant):")
print(f"      • Projected Users: {median_pb:,.0f}")
print(f"      • Rationale: Accounts for September spike outlier")

# Selected projection
petbarn_projected = petbarn_linear_projection
print(f"\n   ✅ SELECTED PROJECTION: {petbarn_projected:,.0f} users")
print(f"      (Using Method 2 - Linear trend from October baseline)")

# ============================================================================
# SECTION 5: TOTAL IMPACT ASSESSMENT
# ============================================================================
print("\n\n" + "█" * 100)
print("SECTION 5: TOTAL IMPACT ASSESSMENT & BUSINESS IMPLICATIONS")
print("█" * 100)

total_projected_users = bws_projected + petbarn_projected
total_projected_spend = (bws_projected * (total_bws_spend / total_bws_users)) + \
                        (petbarn_projected * (total_petbarn_spend / total_petbarn_users))

print("\n" + "─" * 100)
print("5.1 CONSOLIDATED NOVEMBER PROJECTIONS")
print("─" * 100)

print(f"\n{'Merchant':<15} {'Projected Users':>20} {'Est. Monthly Spend':>25} {'% of Total':>15}")
print("─" * 80)
print(f"{'Merchant_A':<15} {bws_projected:>20,.0f} ${(bws_projected * (total_bws_spend / total_bws_users)):>23,.2f} {(bws_projected/total_projected_users*100):>14.1f}%")
print(f"{'Merchant_B':<15} {petbarn_projected:>20,.0f} ${(petbarn_projected * (total_petbarn_spend / total_petbarn_users)):>23,.2f} {(petbarn_projected/total_projected_users*100):>14.1f}%")
print("─" * 80)
print(f"{'TOTAL':<15} {total_projected_users:>20,.0f} ${total_projected_spend:>23,.2f} {'100.0%':>14}")

print("\n" + "─" * 100)
print("5.2 FINANCIAL IMPACT ANALYSIS")
print("─" * 100)

avg_spend_per_user_bws = total_bws_spend / total_bws_users
avg_spend_per_user_pb = total_petbarn_spend / total_petbarn_users

print(f"\n💰 Per-User Economics:")
print(f"   Merchant_A:")
print(f"      • Average Spend per User (6-month): ${avg_spend_per_user_bws:,.2f}")
print(f"      • Estimated November Revenue Loss: ${bws_projected * avg_spend_per_user_bws:,.2f}")
print(f"\n   Merchant_B:")
print(f"      • Average Spend per User (6-month): ${avg_spend_per_user_pb:,.2f}")
print(f"      • Estimated November Revenue Loss: ${petbarn_projected * avg_spend_per_user_pb:,.2f}")
print(f"\n   Combined:")
print(f"      • Total Estimated Revenue Loss: ${total_projected_spend:,.2f}")

print("\n" + "─" * 100)
print("5.3 COMPARATIVE ANALYSIS")
print("─" * 100)

print(f"\n📊 Merchant_A vs Merchant_B Comparison:")
print(f"\n{'Metric':<40} {'Merchant_A':>20} {'Merchant_B':>20}")
print("─" * 80)
print(f"{'Projected November Users':<40} {bws_projected:>20,.0f} {petbarn_projected:>20,.0f}")
print(f"{'Avg Monthly Users (May-Oct)':<40} {avg_monthly_users:>20,.0f} {avg_monthly_users_pb:>20,.0f}")
print(f"{'User Volatility (CV%)':<40} {user_cv:>20.1f}% {user_cv_pb:>20.1f}%")
print(f"{'Total Transactions (May-Oct)':<40} {total_bws_transactions:>20,} {total_petbarn_transactions:>20,}")
print(f"{'Total Spend (May-Oct)':<40} ${total_bws_spend:>19,.0f} ${total_petbarn_spend:>19,.0f}")
print(f"{'Avg Transaction Value':<40} ${bws_monthly_df['avg_transaction_value'].mean():>19.2f} ${petbarn_monthly_df['avg_transaction_value'].mean():>19.2f}")
print(f"{'Avg Transactions per User':<40} {bws_monthly_df['avg_transactions_per_user'].mean():>20.2f} {petbarn_monthly_df['avg_transactions_per_user'].mean():>20.2f}")

# ============================================================================
# SECTION 6: KEY FINDINGS & RECOMMENDATIONS
# ============================================================================
print("\n\n" + "█" * 100)
print("SECTION 6: KEY FINDINGS, INSIGHTS & STRATEGIC RECOMMENDATIONS")
print("█" * 100)

print("\n" + "─" * 100)
print("6.1 CRITICAL FINDINGS")
print("─" * 100)

print(f"""
1. 📊 SCALE OF IMPACT
   • Total projected user loss: {total_projected_users:,.0f} active users in November
   • Estimated revenue impact: ${total_projected_spend:,.2f}
   • Merchant_A represents {(bws_projected/total_projected_users*100):.1f}% of impact
   • Merchant_B represents {(petbarn_projected/total_projected_users*100):.1f}% of impact

2. ⚠️  Merchant_A GRADUAL PAUSE CONTRADICTION
   • Data shows INCREASE from {pre_pause['total_users'].mean():,.0f} (pre-pause) to {gradual_pause['total_users'].mean():,.0f} (Sept-Oct)
   • This suggests the "gradual pause" may have been:
     a) More sudden than reported
     b) Started in November, not September
     c) Offset by promotional activities during Sept-Oct
   
3. 📈 PETBARN VOLATILITY
   • Extremely high volatility (CV: {user_cv_pb:.1f}%)
   • September spike of {petbarn_monthly_df['total_users'].max():,} users (4x baseline)
   • Suggests campaign-driven or seasonal behavior
   • Difficult to predict baseline without understanding spike drivers

4. 💰 REVENUE CONCENTRATION
   • Merchant_A total spend: ${total_bws_spend:,.2f} ({(total_bws_spend/(total_bws_spend+total_petbarn_spend)*100):.1f}%)
   • Merchant_B total spend: ${total_petbarn_spend:,.2f} ({(total_petbarn_spend/(total_bws_spend+total_petbarn_spend)*100):.1f}%)
   • Combined 6-month spend: ${total_bws_spend + total_petbarn_spend:,.2f}

5. 🎯 VARIANT DISTRIBUTION
   • Merchant_A operates {len(bws_variants)} variants
   • Merchant_B operates {len(petbarn_variants)} variants
   • Top Merchant_A variant: {variant_summary.iloc[0]['variant']} ({variant_summary.iloc[0]['total_spend']/variant_summary['total_spend'].sum()*100:.1f}% of spend)
   • Top Merchant_B variant: {variant_summary_pb.iloc[0]['variant']} ({variant_summary_pb.iloc[0]['total_spend']/variant_summary_pb['total_spend'].sum()*100:.1f}% of spend)
""")

print("\n" + "─" * 100)
print("6.2 STRATEGIC RECOMMENDATIONS")
print("─" * 100)

print("""
🎯 IMMEDIATE ACTIONS:

1. INVESTIGATE Merchant_A SEPTEMBER-OCTOBER PERFORMANCE
   • Conduct deep-dive into what drove user increase during "pause" period
   • Identify if specific variants or campaigns offset pause impact
   • Understand actual timing of offer reduction

2. ANALYZE PETBARN SEPTEMBER SPIKE
   • Determine root cause of 4x user surge in September
   • Assess if replicable for future campaigns
   • Understand October decline (campaign end? seasonal?)

3. VALIDATE DATA COMPLETENESS
   • Confirm all merchant variants captured
   • Verify transaction data completeness for May-June
   • Cross-reference with other data sources

📊 ANALYTICAL PRIORITIES:

4. USER COHORT ANALYSIS
   • Track user retention before/after pause
   • Identify if users migrated to other merchants
   • Measure re-activation rates if offers resume

5. COMPETITIVE IMPACT
   • Assess if users shifted to competitor merchants
   • Analyze wallet share changes across portfolio
   • Identify substitution patterns

6. SEASONALITY BASELINE
   • Establish true baseline without promotional spikes
   • Account for seasonal patterns (holidays, back-to-school, etc.)
   • Build more robust forecasting models

💡 STRATEGIC CONSIDERATIONS:

7. OFFER OPTIMIZATION
   • Rather than full pause, consider:
     - Reduced offer percentages
     - Targeted offers to high-value segments
     - Time-limited promotions
   
8. PORTFOLIO REBALANCING
   • Use pause period to test other merchant categories
   • Diversify user engagement across portfolio
   • Reduce dependency on single merchants

9. RE-ACTIVATION STRATEGY
   • Plan for controlled offer restart
   • Test different offer levels for optimal ROI
   • Measure incremental lift vs. baseline
""")

print("\n" + "─" * 100)
print("6.3 DATA QUALITY & ASSUMPTIONS")
print("─" * 100)

print("""
📋 ASSUMPTIONS USED IN ANALYSIS:
   • All merchant variants accurately captured via keyword matching
   • Transaction data is complete and accurate for analysis period
   • User uniqueness maintained across variants and months
   • Linear trends are reasonable predictors for short-term projection
   • No major external factors (market changes, competitor actions) assumed

⚠️  LIMITATIONS:
   • Limited to 6-month historical window (May-Oct 2025)
   • Cannot account for:
     - Seasonal patterns beyond analysis period
     - Marketing campaign impacts
     - Competitive dynamics
     - Macro-economic factors
   • High volatility (especially Merchant_B) reduces forecast confidence
   • May-June data appears limited for some variants

✅ CONFIDENCE LEVELS:
   • Merchant_A Projection: MODERATE (data shows unexpected patterns)
   • Merchant_B Projection: LOW-MODERATE (high volatility, outlier spike)
   • Overall Impact: MODERATE (directionally correct, magnitude uncertain)
""")

# ============================================================================
# SAVE COMPREHENSIVE RESULTS
# ============================================================================
print("\n\n" + "█" * 100)
print("SECTION 7: OUTPUT FILES GENERATED")
print("█" * 100)

# Save summary
summary_data = {
    'Merchant': ['Merchant_A', 'Merchant_B', 'TOTAL'],
    'Projected_November_Users': [int(bws_projected), int(petbarn_projected), int(total_projected_users)],
    'Estimated_November_Spend': [
        bws_projected * avg_spend_per_user_bws,
        petbarn_projected * avg_spend_per_user_pb,
        total_projected_spend
    ],
    'Avg_Monthly_Users_May_Oct': [int(avg_monthly_users), int(avg_monthly_users_pb), int(avg_monthly_users + avg_monthly_users_pb)],
    'Total_Spend_May_Oct': [total_bws_spend, total_petbarn_spend, total_bws_spend + total_petbarn_spend],
    'Volatility_CV': [round(user_cv, 1), round(user_cv_pb, 1), '-']
}

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv('bws_petbarn_analysis_summary.csv', index=False)
print("\n✅ Saved: bws_petbarn_analysis_summary.csv")

# Save monthly details
bws_monthly_df.to_csv('bws_monthly_performance.csv', index=False)
print("✅ Saved: bws_monthly_performance.csv")

petbarn_monthly_df.to_csv('petbarn_monthly_performance.csv', index=False)
print("✅ Saved: petbarn_monthly_performance.csv")

# Save variant details
variant_summary.to_csv('bws_variant_breakdown.csv', index=False)
print("✅ Saved: bws_variant_breakdown.csv")

variant_summary_pb.to_csv('petbarn_variant_breakdown.csv', index=False)
print("✅ Saved: petbarn_variant_breakdown.csv")

print("\n" + "=" * 100)
print("ANALYSIS COMPLETE")
print("=" * 100)
print(f"\nTotal Projected User Impact: {total_projected_users:,.0f} users")
print(f"Estimated Revenue Impact: ${total_projected_spend:,.2f}")
print(f"\nAll detailed results have been saved to CSV files for further analysis.")
print("=" * 100)
