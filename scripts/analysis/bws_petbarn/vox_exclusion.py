"""
BWS and Petbarn Offer Pause Impact Analysis - ENHANCED WITH VOX-ING EXCLUSION
============================================================================

Enhanced analysis that includes:
1. Full analysis (all merchants including VOX-ING variants)
2. Separate analysis EXCLUDING VOX-ING to show pure BWS/Petbarn impact
3. Comparative section showing the difference
"""

import pandas as pd
import numpy as np
from pokitpal_data import PokitPalData
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Initialize data access
data = PokitPalData()

# Analysis period: May - October 2025
analysis_months = ['2025-05', '2025-06', '2025-07', '2025-08', '2025-09', '2025-10']

print("=" * 120)
print("BWS AND PETBARN OFFER PAUSE IMPACT ANALYSIS - ENHANCED WITH VOX-ING EXCLUSION")
print("=" * 120)
print(f"\nReport Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Analysis Period: May 2025 - October 2025 (6 months)")
print(f"Enhancement: Separate analysis excluding VOX-ING related merchants")
print("\n" + "=" * 120)

# ============================================================================
# SECTION 1: FULL ANALYSIS (INCLUDING VOX-ING)
# ============================================================================
print("\n" + "█" * 120)
print("SECTION 1: FULL ANALYSIS - BWS & PETBARN (INCLUDING ALL VARIANTS)")
print("█" * 120)

def analyze_merchants(months, exclude_vox=False):
    """Analyze BWS and Petbarn with option to exclude VOX-ING"""
    
    # BWS Analysis
    bws_monthly_data = []
    for month in months:
        month_data = data.get_merchant_performance(month)
        bws_data = month_data[month_data['Merchant'].str.contains('BWS', case=False, na=False)]
        
        if exclude_vox:
            # Exclude any VOX or ING related BWS variants
            bws_data = bws_data[~bws_data['Merchant'].str.contains('VOX|ING', case=False, na=False)]
        
        if not bws_data.empty:
            bws_monthly_data.append({
                'month': month,
                'unique_users': bws_data['unique_users'].sum(),
                'transaction_count': bws_data['transaction_count'].sum(),
                'total_spend': bws_data['total_spend'].sum(),
                'variant_count': len(bws_data)
            })
    
    # Petbarn Analysis
    petbarn_monthly_data = []
    for month in months:
        month_data = data.get_merchant_performance(month)
        petbarn_data = month_data[month_data['Merchant'].str.contains('Petbarn', case=False, na=False)]
        
        if exclude_vox:
            # Exclude any VOX or ING related Petbarn variants
            petbarn_data = petbarn_data[~petbarn_data['Merchant'].str.contains('VOX|ING', case=False, na=False)]
        
        if not petbarn_data.empty:
            petbarn_monthly_data.append({
                'month': month,
                'unique_users': petbarn_data['unique_users'].sum(),
                'transaction_count': petbarn_data['transaction_count'].sum(),
                'total_spend': petbarn_data['total_spend'].sum(),
                'variant_count': len(petbarn_data)
            })
    
    return pd.DataFrame(bws_monthly_data), pd.DataFrame(petbarn_monthly_data)

# Full analysis
bws_full_df, petbarn_full_df = analyze_merchants(analysis_months, exclude_vox=False)

print("\n" + "─" * 120)
print("1.1 BWS MONTHLY PERFORMANCE (All Variants)")
print("─" * 120)
print("\n" + bws_full_df.to_string(index=False))

print("\n" + "─" * 120)
print("1.2 PETBARN MONTHLY PERFORMANCE (All Variants)")
print("─" * 120)
print("\n" + petbarn_full_df.to_string(index=False))

# Calculate projections for full analysis
if len(bws_full_df) >= 3:
    pre_pause_bws = bws_full_df[bws_full_df['month'] <= '2025-08']
    bws_full_projected = pre_pause_bws['unique_users'].mean()
else:
    bws_full_projected = bws_full_df['unique_users'].mean()

if len(petbarn_full_df) >= 3:
    x_pb = np.arange(len(petbarn_full_df))
    y_pb = petbarn_full_df['unique_users'].values
    z_pb = np.polyfit(x_pb, y_pb, 1)
    petbarn_full_projected = z_pb[1] + z_pb[0] * len(petbarn_full_df)
else:
    petbarn_full_projected = petbarn_full_df['unique_users'].mean()

total_full_projected = bws_full_projected + petbarn_full_projected

# Full analysis metrics
bws_full_avg_spend_per_user = bws_full_df['total_spend'].sum() / bws_full_df['unique_users'].sum()
petbarn_full_avg_spend_per_user = petbarn_full_df['total_spend'].sum() / petbarn_full_df['unique_users'].sum()
total_full_projected_spend = (bws_full_projected * bws_full_avg_spend_per_user) + (petbarn_full_projected * petbarn_full_avg_spend_per_user)

print("\n" + "─" * 120)
print("1.3 FULL ANALYSIS PROJECTIONS (November 2025)")
print("─" * 120)
print(f"\n{'Merchant':<15} {'Projected Users':>20} {'Est. Spend':>25} {'% of Total':>15}")
print("─" * 80)
print(f"{'BWS':<15} {bws_full_projected:>20,.0f} ${(bws_full_projected * bws_full_avg_spend_per_user):>23,.2f} {(bws_full_projected/total_full_projected*100):>14.1f}%")
print(f"{'Petbarn':<15} {petbarn_full_projected:>20,.0f} ${(petbarn_full_projected * petbarn_full_avg_spend_per_user):>23,.2f} {(petbarn_full_projected/total_full_projected*100):>14.1f}%")
print("─" * 80)
print(f"{'TOTAL':<15} {total_full_projected:>20,.0f} ${total_full_projected_spend:>23,.2f} {'100.0%':>14}")

# ============================================================================
# SECTION 2: ANALYSIS EXCLUDING VOX-ING
# ============================================================================
print("\n\n" + "█" * 120)
print("SECTION 2: ANALYSIS EXCLUDING VOX-ING VARIANTS")
print("█" * 120)

# Analysis excluding VOX-ING
bws_no_vox_df, petbarn_no_vox_df = analyze_merchants(analysis_months, exclude_vox=True)

print("\n" + "─" * 120)
print("2.1 BWS MONTHLY PERFORMANCE (Excluding VOX/ING)")
print("─" * 120)
print("\n" + bws_no_vox_df.to_string(index=False))

print("\n" + "─" * 120)
print("2.2 PETBARN MONTHLY PERFORMANCE (Excluding VOX/ING)")
print("─" * 120)
print("\n" + petbarn_no_vox_df.to_string(index=False))

# Calculate projections excluding VOX-ING
if len(bws_no_vox_df) >= 3:
    pre_pause_bws_no_vox = bws_no_vox_df[bws_no_vox_df['month'] <= '2025-08']
    bws_no_vox_projected = pre_pause_bws_no_vox['unique_users'].mean()
else:
    bws_no_vox_projected = bws_no_vox_df['unique_users'].mean()

if len(petbarn_no_vox_df) >= 3:
    x_pb_nv = np.arange(len(petbarn_no_vox_df))
    y_pb_nv = petbarn_no_vox_df['unique_users'].values
    z_pb_nv = np.polyfit(x_pb_nv, y_pb_nv, 1)
    petbarn_no_vox_projected = z_pb_nv[1] + z_pb_nv[0] * len(petbarn_no_vox_df)
else:
    petbarn_no_vox_projected = petbarn_no_vox_df['unique_users'].mean()

total_no_vox_projected = bws_no_vox_projected + petbarn_no_vox_projected

# No-VOX analysis metrics
bws_no_vox_avg_spend_per_user = bws_no_vox_df['total_spend'].sum() / bws_no_vox_df['unique_users'].sum()
petbarn_no_vox_avg_spend_per_user = petbarn_no_vox_df['total_spend'].sum() / petbarn_no_vox_df['unique_users'].sum()
total_no_vox_projected_spend = (bws_no_vox_projected * bws_no_vox_avg_spend_per_user) + (petbarn_no_vox_projected * petbarn_no_vox_avg_spend_per_user)

print("\n" + "─" * 120)
print("2.3 PROJECTIONS EXCLUDING VOX-ING (November 2025)")
print("─" * 120)
print(f"\n{'Merchant':<15} {'Projected Users':>20} {'Est. Spend':>25} {'% of Total':>15}")
print("─" * 80)
print(f"{'BWS':<15} {bws_no_vox_projected:>20,.0f} ${(bws_no_vox_projected * bws_no_vox_avg_spend_per_user):>23,.2f} {(bws_no_vox_projected/total_no_vox_projected*100):>14.1f}%")
print(f"{'Petbarn':<15} {petbarn_no_vox_projected:>20,.0f} ${(petbarn_no_vox_projected * petbarn_no_vox_avg_spend_per_user):>23,.2f} {(petbarn_no_vox_projected/total_no_vox_projected*100):>14.1f}%")
print("─" * 80)
print(f"{'TOTAL':<15} {total_no_vox_projected:>20,.0f} ${total_no_vox_projected_spend:>23,.2f} {'100.0%':>14}")

# ============================================================================
# SECTION 3: COMPARATIVE ANALYSIS - IMPACT OF VOX-ING EXCLUSION
# ============================================================================
print("\n\n" + "█" * 120)
print("SECTION 3: COMPARATIVE ANALYSIS - VOX-ING IMPACT")
print("█" * 120)

print("\n" + "─" * 120)
print("3.1 SIDE-BY-SIDE COMPARISON")
print("─" * 120)

print(f"\n{'Metric':<45} {'With VOX-ING':>25} {'Without VOX-ING':>25} {'Difference':>20}")
print("─" * 120)

# BWS Comparison
bws_user_diff = bws_full_projected - bws_no_vox_projected
bws_spend_diff = (bws_full_projected * bws_full_avg_spend_per_user) - (bws_no_vox_projected * bws_no_vox_avg_spend_per_user)

print(f"{'BWS - Projected Users':<45} {bws_full_projected:>25,.0f} {bws_no_vox_projected:>25,.0f} {bws_user_diff:>20,.0f}")
print(f"{'BWS - Projected Spend':<45} ${(bws_full_projected * bws_full_avg_spend_per_user):>24,.2f} ${(bws_no_vox_projected * bws_no_vox_avg_spend_per_user):>24,.2f} ${bws_spend_diff:>19,.2f}")
print(f"{'BWS - Avg Spend per User':<45} ${bws_full_avg_spend_per_user:>24,.2f} ${bws_no_vox_avg_spend_per_user:>24,.2f} ${(bws_full_avg_spend_per_user - bws_no_vox_avg_spend_per_user):>19,.2f}")
print(f"{'BWS - Total Historic Spend (May-Oct)':<45} ${bws_full_df['total_spend'].sum():>24,.2f} ${bws_no_vox_df['total_spend'].sum():>24,.2f} ${(bws_full_df['total_spend'].sum() - bws_no_vox_df['total_spend'].sum()):>19,.2f}")

print()

# Petbarn Comparison
petbarn_user_diff = petbarn_full_projected - petbarn_no_vox_projected
petbarn_spend_diff = (petbarn_full_projected * petbarn_full_avg_spend_per_user) - (petbarn_no_vox_projected * petbarn_no_vox_avg_spend_per_user)

print(f"{'Petbarn - Projected Users':<45} {petbarn_full_projected:>25,.0f} {petbarn_no_vox_projected:>25,.0f} {petbarn_user_diff:>20,.0f}")
print(f"{'Petbarn - Projected Spend':<45} ${(petbarn_full_projected * petbarn_full_avg_spend_per_user):>24,.2f} ${(petbarn_no_vox_projected * petbarn_no_vox_avg_spend_per_user):>24,.2f} ${petbarn_spend_diff:>19,.2f}")
print(f"{'Petbarn - Avg Spend per User':<45} ${petbarn_full_avg_spend_per_user:>24,.2f} ${petbarn_no_vox_avg_spend_per_user:>24,.2f} ${(petbarn_full_avg_spend_per_user - petbarn_no_vox_avg_spend_per_user):>19,.2f}")
print(f"{'Petbarn - Total Historic Spend (May-Oct)':<45} ${petbarn_full_df['total_spend'].sum():>24,.2f} ${petbarn_no_vox_df['total_spend'].sum():>24,.2f} ${(petbarn_full_df['total_spend'].sum() - petbarn_no_vox_df['total_spend'].sum()):>19,.2f}")

print()
print("─" * 120)

# Total Comparison
total_user_diff = total_full_projected - total_no_vox_projected
total_spend_diff = total_full_projected_spend - total_no_vox_projected_spend

print(f"{'TOTAL - Projected Users':<45} {total_full_projected:>25,.0f} {total_no_vox_projected:>25,.0f} {total_user_diff:>20,.0f}")
print(f"{'TOTAL - Projected Spend':<45} ${total_full_projected_spend:>24,.2f} ${total_no_vox_projected_spend:>24,.2f} ${total_spend_diff:>19,.2f}")
print(f"{'TOTAL - Total Historic Spend (May-Oct)':<45} ${(bws_full_df['total_spend'].sum() + petbarn_full_df['total_spend'].sum()):>24,.2f} ${(bws_no_vox_df['total_spend'].sum() + petbarn_no_vox_df['total_spend'].sum()):>24,.2f} ${((bws_full_df['total_spend'].sum() + petbarn_full_df['total_spend'].sum()) - (bws_no_vox_df['total_spend'].sum() + petbarn_no_vox_df['total_spend'].sum())):>19,.2f}")

print("\n" + "─" * 120)
print("3.2 VOX-ING CONTRIBUTION ANALYSIS")
print("─" * 120)

vox_user_contribution_pct = (total_user_diff / total_full_projected * 100) if total_full_projected > 0 else 0
vox_spend_contribution_pct = (total_spend_diff / total_full_projected_spend * 100) if total_full_projected_spend > 0 else 0

print(f"\n💡 VOX-ING Related Impact:")
print(f"   • Projected User Contribution: {total_user_diff:,.0f} users ({vox_user_contribution_pct:.1f}% of total)")
print(f"   • Projected Spend Contribution: ${total_spend_diff:,.2f} ({vox_spend_contribution_pct:.1f}% of total)")
print(f"   • Historic BWS VOX-ING Spend: ${(bws_full_df['total_spend'].sum() - bws_no_vox_df['total_spend'].sum()):,.2f}")
print(f"   • Historic Petbarn VOX-ING Spend: ${(petbarn_full_df['total_spend'].sum() - petbarn_no_vox_df['total_spend'].sum()):,.2f}")

# ============================================================================
# SECTION 4: KEY INSIGHTS & RECOMMENDATIONS
# ============================================================================
print("\n\n" + "█" * 120)
print("SECTION 4: KEY INSIGHTS FROM VOX-ING COMPARISON")
print("█" * 120)

print(f"""
🔍 CRITICAL FINDINGS:

1. PURE BWS/PETBARN IMPACT (Excluding VOX-ING):
   • Total projected user loss: {total_no_vox_projected:,.0f} users
   • Estimated revenue impact: ${total_no_vox_projected_spend:,.2f}
   • This represents the "core" BWS/Petbarn offer pause impact

2. VOX-ING CONTRIBUTION:
   • VOX-ING adds {total_user_diff:,.0f} users to the total impact ({vox_user_contribution_pct:.1f}%)
   • VOX-ING adds ${total_spend_diff:,.2f} to revenue impact ({vox_spend_contribution_pct:.1f}%)
   • Historic VOX-ING spend: ${((bws_full_df['total_spend'].sum() - bws_no_vox_df['total_spend'].sum()) + (petbarn_full_df['total_spend'].sum() - petbarn_no_vox_df['total_spend'].sum())):,.2f}

3. STRATEGIC IMPLICATIONS:
   • If VOX-ING offers remain active: Focus on core {total_no_vox_projected:,.0f} user impact
   • If VOX-ING also paused: Total impact is {total_full_projected:,.0f} users
   • VOX-ING represents {'a significant' if vox_user_contribution_pct > 10 else 'a minor'} portion of overall impact

4. MERCHANT-SPECIFIC VOX-ING IMPACT:
   BWS:
      • With VOX-ING: {bws_full_projected:,.0f} users, ${(bws_full_projected * bws_full_avg_spend_per_user):,.2f}
      • Without VOX-ING: {bws_no_vox_projected:,.0f} users, ${(bws_no_vox_projected * bws_no_vox_avg_spend_per_user):,.2f}
      • VOX-ING contribution: {bws_user_diff:,.0f} users ({(bws_user_diff/bws_full_projected*100):.1f}%)
   
   Petbarn:
      • With VOX-ING: {petbarn_full_projected:,.0f} users, ${(petbarn_full_projected * petbarn_full_avg_spend_per_user):,.2f}
      • Without VOX-ING: {petbarn_no_vox_projected:,.0f} users, ${(petbarn_no_vox_projected * petbarn_no_vox_avg_spend_per_user):,.2f}
      • VOX-ING contribution: {petbarn_user_diff:,.0f} users ({(petbarn_user_diff/petbarn_full_projected*100):.1f}%)
""")

print("\n" + "─" * 120)
print("RECOMMENDATIONS BASED ON VOX-ING ANALYSIS:")
print("─" * 120)

print("""
📊 SEGMENTATION STRATEGY:

1. TRACK VOX-ING SEPARATELY
   • VOX-ING likely represents partnership/bank-specific offers
   • Different user behavior and economics vs core offers
   • Should be analyzed and managed separately

2. SCENARIO PLANNING:
   Scenario A - VOX-ING Remains Active:
      • Core impact: {0:,} users, ${1:,.2f}
      • Focus reactivation on pure BWS/Petbarn channels
   
   Scenario B - VOX-ING Also Paused:
      • Full impact: {2:,} users, ${3:,.2f}
      • Broader reactivation strategy needed

3. OFFER OPTIMIZATION:
   • Test different offers for VOX-ING vs core channels
   • VOX-ING may have different ROI profile
   • Consider partner-specific negotiations

4. REPORTING CLARITY:
   • Always separate VOX-ING in future reports
   • Helps stakeholders understand true vs partnership impact
   • Enables better decision-making on offer strategy
""".format(
    int(total_no_vox_projected), 
    total_no_vox_projected_spend,
    int(total_full_projected),
    total_full_projected_spend
))

# ============================================================================
# SAVE RESULTS
# ============================================================================
print("\n\n" + "█" * 120)
print("SECTION 5: OUTPUT FILES")
print("█" * 120)

# Comprehensive comparison summary
comparison_summary = pd.DataFrame({
    'Metric': [
        'BWS - Projected Users',
        'BWS - Projected Spend',
        'Petbarn - Projected Users',
        'Petbarn - Projected Spend',
        'TOTAL - Projected Users',
        'TOTAL - Projected Spend'
    ],
    'With_VOX_ING': [
        int(bws_full_projected),
        bws_full_projected * bws_full_avg_spend_per_user,
        int(petbarn_full_projected),
        petbarn_full_projected * petbarn_full_avg_spend_per_user,
        int(total_full_projected),
        total_full_projected_spend
    ],
    'Without_VOX_ING': [
        int(bws_no_vox_projected),
        bws_no_vox_projected * bws_no_vox_avg_spend_per_user,
        int(petbarn_no_vox_projected),
        petbarn_no_vox_projected * petbarn_no_vox_avg_spend_per_user,
        int(total_no_vox_projected),
        total_no_vox_projected_spend
    ],
    'Difference': [
        int(bws_user_diff),
        bws_spend_diff,
        int(petbarn_user_diff),
        petbarn_spend_diff,
        int(total_user_diff),
        total_spend_diff
    ]
})

comparison_summary.to_csv('bws_petbarn_vox_comparison.csv', index=False)
print("\n✅ Saved: bws_petbarn_vox_comparison.csv")

# Monthly comparison
bws_full_df['scenario'] = 'With VOX-ING'
bws_no_vox_df['scenario'] = 'Without VOX-ING'
bws_comparison = pd.concat([bws_full_df, bws_no_vox_df])
bws_comparison.to_csv('bws_monthly_vox_comparison.csv', index=False)
print("✅ Saved: bws_monthly_vox_comparison.csv")

petbarn_full_df['scenario'] = 'With VOX-ING'
petbarn_no_vox_df['scenario'] = 'Without VOX-ING'
petbarn_comparison = pd.concat([petbarn_full_df, petbarn_no_vox_df])
petbarn_comparison.to_csv('petbarn_monthly_vox_comparison.csv', index=False)
print("✅ Saved: petbarn_monthly_vox_comparison.csv")

print("\n" + "=" * 120)
print("ENHANCED ANALYSIS COMPLETE")
print("=" * 120)
print(f"\n📊 SUMMARY:")
print(f"   With VOX-ING:    {total_full_projected:>10,.0f} users | ${total_full_projected_spend:>15,.2f}")
print(f"   Without VOX-ING: {total_no_vox_projected:>10,.0f} users | ${total_no_vox_projected_spend:>15,.2f}")
print(f"   VOX-ING Impact:  {total_user_diff:>10,.0f} users | ${total_spend_diff:>15,.2f} ({vox_user_contribution_pct:.1f}%)")
print("=" * 120)
