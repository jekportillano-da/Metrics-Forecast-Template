"""
Merchant_A and Merchant_B Offer Pause Impact Analysis - ENHANCED WITH VOX-Network_Partner_2 EXCLUSION
============================================================================

Enhanced analysis that includes:
1. Full analysis (all merchants including VOX-Network_Partner_2 variants)
2. Separate analysis EXCLUDING VOX-Network_Partner_2 to show pure Merchant_A/Merchant_B impact
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
print("Merchant_A AND PETBARN OFFER PAUSE IMPACT ANALYSIS - ENHANCED WITH VOX-Network_Partner_2 EXCLUSION")
print("=" * 120)
print(f"\nReport Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Analysis Period: May 2025 - October 2025 (6 months)")
print(f"Enhancement: Separate analysis excluding VOX-Network_Partner_2 related merchants")
print("\n" + "=" * 120)

# ============================================================================
# SECTION 1: FULL ANALYSIS (INCLUDING VOX-Network_Partner_2)
# ============================================================================
print("\n" + "█" * 120)
print("SECTION 1: FULL ANALYSIS - Merchant_A & PETBARN (INCLUDING ALL VARIANTS)")
print("█" * 120)

def analyze_merchants(months, exclude_vox=False):
    """Analyze Merchant_A and Merchant_B with option to exclude VOX-Network_Partner_2"""
    
    # Merchant_A Analysis
    bws_monthly_data = []
    for month in months:
        month_data = data.get_merchant_performance(month)
        bws_data = month_data[month_data['Merchant'].str.contains('Merchant_A', case=False, na=False)]
        
        if exclude_vox:
            # Exclude any VOX or Network_Partner_2 related Merchant_A variants
            bws_data = bws_data[~bws_data['Merchant'].str.contains('VOX|Network_Partner_2', case=False, na=False)]
        
        if not bws_data.empty:
            bws_monthly_data.append({
                'month': month,
                'unique_users': bws_data['unique_users'].sum(),
                'transaction_count': bws_data['transaction_count'].sum(),
                'total_spend': bws_data['total_spend'].sum(),
                'variant_count': len(bws_data)
            })
    
    # Merchant_B Analysis
    petbarn_monthly_data = []
    for month in months:
        month_data = data.get_merchant_performance(month)
        petbarn_data = month_data[month_data['Merchant'].str.contains('Merchant_B', case=False, na=False)]
        
        if exclude_vox:
            # Exclude any VOX or Network_Partner_2 related Merchant_B variants
            petbarn_data = petbarn_data[~petbarn_data['Merchant'].str.contains('VOX|Network_Partner_2', case=False, na=False)]
        
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
print("1.1 Merchant_A MONTHLY PERFORMANCE (All Variants)")
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
print(f"{'Merchant_A':<15} {bws_full_projected:>20,.0f} ${(bws_full_projected * bws_full_avg_spend_per_user):>23,.2f} {(bws_full_projected/total_full_projected*100):>14.1f}%")
print(f"{'Merchant_B':<15} {petbarn_full_projected:>20,.0f} ${(petbarn_full_projected * petbarn_full_avg_spend_per_user):>23,.2f} {(petbarn_full_projected/total_full_projected*100):>14.1f}%")
print("─" * 80)
print(f"{'TOTAL':<15} {total_full_projected:>20,.0f} ${total_full_projected_spend:>23,.2f} {'100.0%':>14}")

# ============================================================================
# SECTION 2: ANALYSIS EXCLUDING VOX-Network_Partner_2
# ============================================================================
print("\n\n" + "█" * 120)
print("SECTION 2: ANALYSIS EXCLUDING VOX-Network_Partner_2 VARIANTS")
print("█" * 120)

# Analysis excluding VOX-Network_Partner_2
bws_no_vox_df, petbarn_no_vox_df = analyze_merchants(analysis_months, exclude_vox=True)

print("\n" + "─" * 120)
print("2.1 Merchant_A MONTHLY PERFORMANCE (Excluding VOX/Network_Partner_2)")
print("─" * 120)
print("\n" + bws_no_vox_df.to_string(index=False))

print("\n" + "─" * 120)
print("2.2 PETBARN MONTHLY PERFORMANCE (Excluding VOX/Network_Partner_2)")
print("─" * 120)
print("\n" + petbarn_no_vox_df.to_string(index=False))

# Calculate projections excluding VOX-Network_Partner_2
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
print("2.3 PROJECTIONS EXCLUDING VOX-Network_Partner_2 (November 2025)")
print("─" * 120)
print(f"\n{'Merchant':<15} {'Projected Users':>20} {'Est. Spend':>25} {'% of Total':>15}")
print("─" * 80)
print(f"{'Merchant_A':<15} {bws_no_vox_projected:>20,.0f} ${(bws_no_vox_projected * bws_no_vox_avg_spend_per_user):>23,.2f} {(bws_no_vox_projected/total_no_vox_projected*100):>14.1f}%")
print(f"{'Merchant_B':<15} {petbarn_no_vox_projected:>20,.0f} ${(petbarn_no_vox_projected * petbarn_no_vox_avg_spend_per_user):>23,.2f} {(petbarn_no_vox_projected/total_no_vox_projected*100):>14.1f}%")
print("─" * 80)
print(f"{'TOTAL':<15} {total_no_vox_projected:>20,.0f} ${total_no_vox_projected_spend:>23,.2f} {'100.0%':>14}")

# ============================================================================
# SECTION 3: COMPARATIVE ANALYSIS - IMPACT OF VOX-Network_Partner_2 EXCLUSION
# ============================================================================
print("\n\n" + "█" * 120)
print("SECTION 3: COMPARATIVE ANALYSIS - VOX-Network_Partner_2 IMPACT")
print("█" * 120)

print("\n" + "─" * 120)
print("3.1 SIDE-BY-SIDE COMPARISON")
print("─" * 120)

print(f"\n{'Metric':<45} {'With VOX-Network_Partner_2':>25} {'Without VOX-Network_Partner_2':>25} {'Difference':>20}")
print("─" * 120)

# Merchant_A Comparison
bws_user_diff = bws_full_projected - bws_no_vox_projected
bws_spend_diff = (bws_full_projected * bws_full_avg_spend_per_user) - (bws_no_vox_projected * bws_no_vox_avg_spend_per_user)

print(f"{'Merchant_A - Projected Users':<45} {bws_full_projected:>25,.0f} {bws_no_vox_projected:>25,.0f} {bws_user_diff:>20,.0f}")
print(f"{'Merchant_A - Projected Spend':<45} ${(bws_full_projected * bws_full_avg_spend_per_user):>24,.2f} ${(bws_no_vox_projected * bws_no_vox_avg_spend_per_user):>24,.2f} ${bws_spend_diff:>19,.2f}")
print(f"{'Merchant_A - Avg Spend per User':<45} ${bws_full_avg_spend_per_user:>24,.2f} ${bws_no_vox_avg_spend_per_user:>24,.2f} ${(bws_full_avg_spend_per_user - bws_no_vox_avg_spend_per_user):>19,.2f}")
print(f"{'Merchant_A - Total Historic Spend (May-Oct)':<45} ${bws_full_df['total_spend'].sum():>24,.2f} ${bws_no_vox_df['total_spend'].sum():>24,.2f} ${(bws_full_df['total_spend'].sum() - bws_no_vox_df['total_spend'].sum()):>19,.2f}")

print()

# Merchant_B Comparison
petbarn_user_diff = petbarn_full_projected - petbarn_no_vox_projected
petbarn_spend_diff = (petbarn_full_projected * petbarn_full_avg_spend_per_user) - (petbarn_no_vox_projected * petbarn_no_vox_avg_spend_per_user)

print(f"{'Merchant_B - Projected Users':<45} {petbarn_full_projected:>25,.0f} {petbarn_no_vox_projected:>25,.0f} {petbarn_user_diff:>20,.0f}")
print(f"{'Merchant_B - Projected Spend':<45} ${(petbarn_full_projected * petbarn_full_avg_spend_per_user):>24,.2f} ${(petbarn_no_vox_projected * petbarn_no_vox_avg_spend_per_user):>24,.2f} ${petbarn_spend_diff:>19,.2f}")
print(f"{'Merchant_B - Avg Spend per User':<45} ${petbarn_full_avg_spend_per_user:>24,.2f} ${petbarn_no_vox_avg_spend_per_user:>24,.2f} ${(petbarn_full_avg_spend_per_user - petbarn_no_vox_avg_spend_per_user):>19,.2f}")
print(f"{'Merchant_B - Total Historic Spend (May-Oct)':<45} ${petbarn_full_df['total_spend'].sum():>24,.2f} ${petbarn_no_vox_df['total_spend'].sum():>24,.2f} ${(petbarn_full_df['total_spend'].sum() - petbarn_no_vox_df['total_spend'].sum()):>19,.2f}")

print()
print("─" * 120)

# Total Comparison
total_user_diff = total_full_projected - total_no_vox_projected
total_spend_diff = total_full_projected_spend - total_no_vox_projected_spend

print(f"{'TOTAL - Projected Users':<45} {total_full_projected:>25,.0f} {total_no_vox_projected:>25,.0f} {total_user_diff:>20,.0f}")
print(f"{'TOTAL - Projected Spend':<45} ${total_full_projected_spend:>24,.2f} ${total_no_vox_projected_spend:>24,.2f} ${total_spend_diff:>19,.2f}")
print(f"{'TOTAL - Total Historic Spend (May-Oct)':<45} ${(bws_full_df['total_spend'].sum() + petbarn_full_df['total_spend'].sum()):>24,.2f} ${(bws_no_vox_df['total_spend'].sum() + petbarn_no_vox_df['total_spend'].sum()):>24,.2f} ${((bws_full_df['total_spend'].sum() + petbarn_full_df['total_spend'].sum()) - (bws_no_vox_df['total_spend'].sum() + petbarn_no_vox_df['total_spend'].sum())):>19,.2f}")

print("\n" + "─" * 120)
print("3.2 VOX-Network_Partner_2 CONTRIBUTION ANALYSIS")
print("─" * 120)

vox_user_contribution_pct = (total_user_diff / total_full_projected * 100) if total_full_projected > 0 else 0
vox_spend_contribution_pct = (total_spend_diff / total_full_projected_spend * 100) if total_full_projected_spend > 0 else 0

print(f"\n💡 VOX-Network_Partner_2 Related Impact:")
print(f"   • Projected User Contribution: {total_user_diff:,.0f} users ({vox_user_contribution_pct:.1f}% of total)")
print(f"   • Projected Spend Contribution: ${total_spend_diff:,.2f} ({vox_spend_contribution_pct:.1f}% of total)")
print(f"   • Historic Merchant_A VOX-Network_Partner_2 Spend: ${(bws_full_df['total_spend'].sum() - bws_no_vox_df['total_spend'].sum()):,.2f}")
print(f"   • Historic Merchant_B VOX-Network_Partner_2 Spend: ${(petbarn_full_df['total_spend'].sum() - petbarn_no_vox_df['total_spend'].sum()):,.2f}")

# ============================================================================
# SECTION 4: KEY INSIGHTS & RECOMMENDATIONS
# ============================================================================
print("\n\n" + "█" * 120)
print("SECTION 4: KEY INSIGHTS FROM VOX-Network_Partner_2 COMPARISON")
print("█" * 120)

print(f"""
🔍 CRITICAL FINDINGS:

1. PURE Merchant_A/PETBARN IMPACT (Excluding VOX-Network_Partner_2):
   • Total projected user loss: {total_no_vox_projected:,.0f} users
   • Estimated revenue impact: ${total_no_vox_projected_spend:,.2f}
   • This represents the "core" Merchant_A/Merchant_B offer pause impact

2. VOX-Network_Partner_2 CONTRIBUTION:
   • VOX-Network_Partner_2 adds {total_user_diff:,.0f} users to the total impact ({vox_user_contribution_pct:.1f}%)
   • VOX-Network_Partner_2 adds ${total_spend_diff:,.2f} to revenue impact ({vox_spend_contribution_pct:.1f}%)
   • Historic VOX-Network_Partner_2 spend: ${((bws_full_df['total_spend'].sum() - bws_no_vox_df['total_spend'].sum()) + (petbarn_full_df['total_spend'].sum() - petbarn_no_vox_df['total_spend'].sum())):,.2f}

3. STRATEGIC IMPLICATIONS:
   • If VOX-Network_Partner_2 offers remain active: Focus on core {total_no_vox_projected:,.0f} user impact
   • If VOX-Network_Partner_2 also paused: Total impact is {total_full_projected:,.0f} users
   • VOX-Network_Partner_2 represents {'a significant' if vox_user_contribution_pct > 10 else 'a minor'} portion of overall impact

4. MERCHANT-SPECIFIC VOX-Network_Partner_2 IMPACT:
   Merchant_A:
      • With VOX-Network_Partner_2: {bws_full_projected:,.0f} users, ${(bws_full_projected * bws_full_avg_spend_per_user):,.2f}
      • Without VOX-Network_Partner_2: {bws_no_vox_projected:,.0f} users, ${(bws_no_vox_projected * bws_no_vox_avg_spend_per_user):,.2f}
      • VOX-Network_Partner_2 contribution: {bws_user_diff:,.0f} users ({(bws_user_diff/bws_full_projected*100):.1f}%)
   
   Merchant_B:
      • With VOX-Network_Partner_2: {petbarn_full_projected:,.0f} users, ${(petbarn_full_projected * petbarn_full_avg_spend_per_user):,.2f}
      • Without VOX-Network_Partner_2: {petbarn_no_vox_projected:,.0f} users, ${(petbarn_no_vox_projected * petbarn_no_vox_avg_spend_per_user):,.2f}
      • VOX-Network_Partner_2 contribution: {petbarn_user_diff:,.0f} users ({(petbarn_user_diff/petbarn_full_projected*100):.1f}%)
""")

print("\n" + "─" * 120)
print("RECOMMENDATIONS BASED ON VOX-Network_Partner_2 ANALYSIS:")
print("─" * 120)

print("""
📊 SEGMENTATION STRATEGY:

1. TRACK VOX-Network_Partner_2 SEPARATELY
   • VOX-Network_Partner_2 likely represents partnership/bank-specific offers
   • Different user behavior and economics vs core offers
   • Should be analyzed and managed separately

2. SCENARIO PLANNING:
   Scenario A - VOX-Network_Partner_2 Remains Active:
      • Core impact: {0:,} users, ${1:,.2f}
      • Focus reactivation on pure Merchant_A/Merchant_B channels
   
   Scenario B - VOX-Network_Partner_2 Also Paused:
      • Full impact: {2:,} users, ${3:,.2f}
      • Broader reactivation strategy needed

3. OFFER OPTIMIZATION:
   • Test different offers for VOX-Network_Partner_2 vs core channels
   • VOX-Network_Partner_2 may have different ROI profile
   • Consider partner-specific negotiations

4. REPORTING CLARITY:
   • Always separate VOX-Network_Partner_2 in future reports
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
        'Merchant_A - Projected Users',
        'Merchant_A - Projected Spend',
        'Merchant_B - Projected Users',
        'Merchant_B - Projected Spend',
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
bws_full_df['scenario'] = 'With VOX-Network_Partner_2'
bws_no_vox_df['scenario'] = 'Without VOX-Network_Partner_2'
bws_comparison = pd.concat([bws_full_df, bws_no_vox_df])
bws_comparison.to_csv('bws_monthly_vox_comparison.csv', index=False)
print("✅ Saved: bws_monthly_vox_comparison.csv")

petbarn_full_df['scenario'] = 'With VOX-Network_Partner_2'
petbarn_no_vox_df['scenario'] = 'Without VOX-Network_Partner_2'
petbarn_comparison = pd.concat([petbarn_full_df, petbarn_no_vox_df])
petbarn_comparison.to_csv('petbarn_monthly_vox_comparison.csv', index=False)
print("✅ Saved: petbarn_monthly_vox_comparison.csv")

print("\n" + "=" * 120)
print("ENHANCED ANALYSIS COMPLETE")
print("=" * 120)
print(f"\n📊 SUMMARY:")
print(f"   With VOX-Network_Partner_2:    {total_full_projected:>10,.0f} users | ${total_full_projected_spend:>15,.2f}")
print(f"   Without VOX-Network_Partner_2: {total_no_vox_projected:>10,.0f} users | ${total_no_vox_projected_spend:>15,.2f}")
print(f"   VOX-Network_Partner_2 Impact:  {total_user_diff:>10,.0f} users | ${total_spend_diff:>15,.2f} ({vox_user_contribution_pct:.1f}%)")
print("=" * 120)
