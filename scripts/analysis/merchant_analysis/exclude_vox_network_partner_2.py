"""
Merchant_A and Merchant_B Offer Pause Impact Analysis - EXCLUDING VOX-Network_Partner_2 USER NETWORK
=============================================================================

This analysis compares:
1. Full analysis (all user networks including VOX-Network_Partner_2)
2. Analysis EXCLUDING VOX-Network_Partner_2 user network
3. Shows the true impact for non-VOX-Network_Partner_2 users
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

print("=" * 130)
print("Merchant_A AND PETBARN OFFER PAUSE IMPACT ANALYSIS - EXCLUDING VOX-Network_Partner_2 USER NETWORK")
print("=" * 130)
print(f"\nReport Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Analysis Period: May 2025 - October 2025 (6 months)")
print(f"Enhancement: Separate analysis excluding VOX-Network_Partner_2 user network")
print("\n" + "=" * 130)

def analyze_by_network(months, exclude_vox_ing=False):
    """Analyze Merchant_A and Merchant_B transactions with option to exclude VOX-Network_Partner_2 network users"""
    
    bws_monthly_data = []
    petbarn_monthly_data = []
    
    for month in months:
        # Get all transactions for the month
        if exclude_vox_ing:
            # Get transactions excluding VOX-Network_Partner_2 network
            # Note: We need to filter at transaction level by User Network
            month_start = month + '-01'
            month_end = month + '-31'
            all_txn = data.get_transactions(start_date=month_start, end_date=month_end)
            
            # Exclude VOX-Network_Partner_2 networks
            all_txn = all_txn[~all_txn['User Network'].str.contains('VOX', case=False, na=False)]
            
            # Merchant_A transactions
            bws_txn = all_txn[all_txn['Merchant'].str.contains('Merchant_A', case=False, na=False)]
            if not bws_txn.empty:
                bws_monthly_data.append({
                    'month': month,
                    'unique_users': bws_txn['Email'].nunique(),
                    'transaction_count': len(bws_txn),
                    'total_spend': bws_txn['Amount'].sum()
                })
            
            # Merchant_B transactions
            petbarn_txn = all_txn[all_txn['Merchant'].str.contains('Merchant_B', case=False, na=False)]
            if not petbarn_txn.empty:
                petbarn_monthly_data.append({
                    'month': month,
                    'unique_users': petbarn_txn['Email'].nunique(),
                    'transaction_count': len(petbarn_txn),
                    'total_spend': petbarn_txn['Amount'].sum()
                })
        else:
            # Full analysis - use merchant performance (includes all networks)
            month_perf = data.get_merchant_performance(month)
            
            # Merchant_A
            bws_data = month_perf[month_perf['Merchant'].str.contains('Merchant_A', case=False, na=False)]
            if not bws_data.empty:
                bws_monthly_data.append({
                    'month': month,
                    'unique_users': bws_data['unique_users'].sum(),
                    'transaction_count': bws_data['transaction_count'].sum(),
                    'total_spend': bws_data['total_spend'].sum()
                })
            
            # Merchant_B
            petbarn_data = month_perf[month_perf['Merchant'].str.contains('Merchant_B', case=False, na=False)]
            if not petbarn_data.empty:
                petbarn_monthly_data.append({
                    'month': month,
                    'unique_users': petbarn_data['unique_users'].sum(),
                    'transaction_count': petbarn_data['transaction_count'].sum(),
                    'total_spend': petbarn_data['total_spend'].sum()
                })
    
    return pd.DataFrame(bws_monthly_data), pd.DataFrame(petbarn_monthly_data)

# ============================================================================
# SECTION 1: FULL ANALYSIS (ALL USER NETWORKS INCLUDING VOX-Network_Partner_2)
# ============================================================================
print("\n" + "█" * 130)
print("SECTION 1: FULL ANALYSIS - ALL USER NETWORKS (INCLUDING VOX-Network_Partner_2)")
print("█" * 130)

bws_full_df, petbarn_full_df = analyze_by_network(analysis_months, exclude_vox_ing=False)

print("\n" + "─" * 130)
print("1.1 Merchant_A MONTHLY PERFORMANCE (All Networks)")
print("─" * 130)
if not bws_full_df.empty:
    print("\n" + bws_full_df.to_string(index=False))
else:
    print("No data available")

print("\n" + "─" * 130)
print("1.2 PETBARN MONTHLY PERFORMANCE (All Networks)")
print("─" * 130)
if not petbarn_full_df.empty:
    print("\n" + petbarn_full_df.to_string(index=False))
else:
    print("No data available")

# Calculate projections for full analysis
if len(bws_full_df) >= 3:
    pre_pause_bws = bws_full_df[bws_full_df['month'] <= '2025-08']
    bws_full_projected = pre_pause_bws['unique_users'].mean() if len(pre_pause_bws) > 0 else bws_full_df['unique_users'].mean()
else:
    bws_full_projected = bws_full_df['unique_users'].mean() if not bws_full_df.empty else 0

if len(petbarn_full_df) >= 3:
    x_pb = np.arange(len(petbarn_full_df))
    y_pb = petbarn_full_df['unique_users'].values
    z_pb = np.polyfit(x_pb, y_pb, 1)
    petbarn_full_projected = z_pb[1] + z_pb[0] * len(petbarn_full_df)
else:
    petbarn_full_projected = petbarn_full_df['unique_users'].mean() if not petbarn_full_df.empty else 0

total_full_projected = bws_full_projected + petbarn_full_projected

# Full analysis metrics
bws_full_total_users = bws_full_df['unique_users'].sum() if not bws_full_df.empty else 0
bws_full_total_spend = bws_full_df['total_spend'].sum() if not bws_full_df.empty else 0
bws_full_avg_spend_per_user = bws_full_total_spend / bws_full_total_users if bws_full_total_users > 0 else 0

petbarn_full_total_users = petbarn_full_df['unique_users'].sum() if not petbarn_full_df.empty else 0
petbarn_full_total_spend = petbarn_full_df['total_spend'].sum() if not petbarn_full_df.empty else 0
petbarn_full_avg_spend_per_user = petbarn_full_total_spend / petbarn_full_total_users if petbarn_full_total_users > 0 else 0

total_full_projected_spend = (bws_full_projected * bws_full_avg_spend_per_user) + (petbarn_full_projected * petbarn_full_avg_spend_per_user)

print("\n" + "─" * 130)
print("1.3 PROJECTIONS (November 2025) - ALL NETWORKS")
print("─" * 130)
print(f"\n{'Merchant':<15} {'Projected Users':>20} {'Est. Spend':>25} {'% of Total':>15}")
print("─" * 85)
print(f"{'Merchant_A':<15} {bws_full_projected:>20,.0f} ${(bws_full_projected * bws_full_avg_spend_per_user):>23,.2f} {(bws_full_projected/total_full_projected*100) if total_full_projected > 0 else 0:>14.1f}%")
print(f"{'Merchant_B':<15} {petbarn_full_projected:>20,.0f} ${(petbarn_full_projected * petbarn_full_avg_spend_per_user):>23,.2f} {(petbarn_full_projected/total_full_projected*100) if total_full_projected > 0 else 0:>14.1f}%")
print("─" * 85)
print(f"{'TOTAL':<15} {total_full_projected:>20,.0f} ${total_full_projected_spend:>23,.2f} {'100.0%':>14}")

# ============================================================================
# SECTION 2: ANALYSIS EXCLUDING VOX-Network_Partner_2 USER NETWORK
# ============================================================================
print("\n\n" + "█" * 130)
print("SECTION 2: ANALYSIS EXCLUDING VOX-Network_Partner_2 USER NETWORK")
print("█" * 130)

print("\n⏳ Processing transaction-level data to exclude VOX-Network_Partner_2 network users...")
bws_no_vox_df, petbarn_no_vox_df = analyze_by_network(analysis_months, exclude_vox_ing=True)

print("\n" + "─" * 130)
print("2.1 Merchant_A MONTHLY PERFORMANCE (Excluding VOX-Network_Partner_2 Network)")
print("─" * 130)
if not bws_no_vox_df.empty:
    print("\n" + bws_no_vox_df.to_string(index=False))
else:
    print("No data available")

print("\n" + "─" * 130)
print("2.2 PETBARN MONTHLY PERFORMANCE (Excluding VOX-Network_Partner_2 Network)")
print("─" * 130)
if not petbarn_no_vox_df.empty:
    print("\n" + petbarn_no_vox_df.to_string(index=False))
else:
    print("No data available")

# Calculate projections excluding VOX-Network_Partner_2
if len(bws_no_vox_df) >= 3:
    pre_pause_bws_no_vox = bws_no_vox_df[bws_no_vox_df['month'] <= '2025-08']
    bws_no_vox_projected = pre_pause_bws_no_vox['unique_users'].mean() if len(pre_pause_bws_no_vox) > 0 else bws_no_vox_df['unique_users'].mean()
else:
    bws_no_vox_projected = bws_no_vox_df['unique_users'].mean() if not bws_no_vox_df.empty else 0

if len(petbarn_no_vox_df) >= 3:
    x_pb_nv = np.arange(len(petbarn_no_vox_df))
    y_pb_nv = petbarn_no_vox_df['unique_users'].values
    z_pb_nv = np.polyfit(x_pb_nv, y_pb_nv, 1)
    petbarn_no_vox_projected = z_pb_nv[1] + z_pb_nv[0] * len(petbarn_no_vox_df)
else:
    petbarn_no_vox_projected = petbarn_no_vox_df['unique_users'].mean() if not petbarn_no_vox_df.empty else 0

total_no_vox_projected = bws_no_vox_projected + petbarn_no_vox_projected

# No-VOX analysis metrics
bws_no_vox_total_users = bws_no_vox_df['unique_users'].sum() if not bws_no_vox_df.empty else 0
bws_no_vox_total_spend = bws_no_vox_df['total_spend'].sum() if not bws_no_vox_df.empty else 0
bws_no_vox_avg_spend_per_user = bws_no_vox_total_spend / bws_no_vox_total_users if bws_no_vox_total_users > 0 else 0

petbarn_no_vox_total_users = petbarn_no_vox_df['unique_users'].sum() if not petbarn_no_vox_df.empty else 0
petbarn_no_vox_total_spend = petbarn_no_vox_df['total_spend'].sum() if not petbarn_no_vox_df.empty else 0
petbarn_no_vox_avg_spend_per_user = petbarn_no_vox_total_spend / petbarn_no_vox_total_users if petbarn_no_vox_total_users > 0 else 0

total_no_vox_projected_spend = (bws_no_vox_projected * bws_no_vox_avg_spend_per_user) + (petbarn_no_vox_projected * petbarn_no_vox_avg_spend_per_user)

print("\n" + "─" * 130)
print("2.3 PROJECTIONS (November 2025) - EXCLUDING VOX-Network_Partner_2 NETWORK")
print("─" * 130)
print(f"\n{'Merchant':<15} {'Projected Users':>20} {'Est. Spend':>25} {'% of Total':>15}")
print("─" * 85)
print(f"{'Merchant_A':<15} {bws_no_vox_projected:>20,.0f} ${(bws_no_vox_projected * bws_no_vox_avg_spend_per_user):>23,.2f} {(bws_no_vox_projected/total_no_vox_projected*100) if total_no_vox_projected > 0 else 0:>14.1f}%")
print(f"{'Merchant_B':<15} {petbarn_no_vox_projected:>20,.0f} ${(petbarn_no_vox_projected * petbarn_no_vox_avg_spend_per_user):>23,.2f} {(petbarn_no_vox_projected/total_no_vox_projected*100) if total_no_vox_projected > 0 else 0:>14.1f}%")
print("─" * 85)
print(f"{'TOTAL':<15} {total_no_vox_projected:>20,.0f} ${total_no_vox_projected_spend:>23,.2f} {'100.0%':>14}")

# ============================================================================
# SECTION 3: COMPARATIVE ANALYSIS - VOX-Network_Partner_2 NETWORK IMPACT
# ============================================================================
print("\n\n" + "█" * 130)
print("SECTION 3: COMPARATIVE ANALYSIS - VOX-Network_Partner_2 USER NETWORK IMPACT")
print("█" * 130)

print("\n" + "─" * 130)
print("3.1 SIDE-BY-SIDE COMPARISON")
print("─" * 130)

print(f"\n{'Metric':<50} {'With VOX-Network_Partner_2':>25} {'Without VOX-Network_Partner_2':>25} {'Difference':>20}")
print("─" * 130)

# Merchant_A Comparison
bws_user_diff = bws_full_projected - bws_no_vox_projected
bws_spend_diff = (bws_full_projected * bws_full_avg_spend_per_user) - (bws_no_vox_projected * bws_no_vox_avg_spend_per_user)

print(f"{'Merchant_A - Projected November Users':<50} {bws_full_projected:>25,.0f} {bws_no_vox_projected:>25,.0f} {bws_user_diff:>20,.0f}")
print(f"{'Merchant_A - Projected November Spend':<50} ${(bws_full_projected * bws_full_avg_spend_per_user):>24,.2f} ${(bws_no_vox_projected * bws_no_vox_avg_spend_per_user):>24,.2f} ${bws_spend_diff:>19,.2f}")
print(f"{'Merchant_A - Avg Spend per User':<50} ${bws_full_avg_spend_per_user:>24,.2f} ${bws_no_vox_avg_spend_per_user:>24,.2f} ${(bws_full_avg_spend_per_user - bws_no_vox_avg_spend_per_user):>19,.2f}")
print(f"{'Merchant_A - Total Historic Users (May-Oct)':<50} {bws_full_total_users:>25,.0f} {bws_no_vox_total_users:>25,.0f} {(bws_full_total_users - bws_no_vox_total_users):>20,.0f}")
print(f"{'Merchant_A - Total Historic Spend (May-Oct)':<50} ${bws_full_total_spend:>24,.2f} ${bws_no_vox_total_spend:>24,.2f} ${(bws_full_total_spend - bws_no_vox_total_spend):>19,.2f}")

print()

# Merchant_B Comparison
petbarn_user_diff = petbarn_full_projected - petbarn_no_vox_projected
petbarn_spend_diff = (petbarn_full_projected * petbarn_full_avg_spend_per_user) - (petbarn_no_vox_projected * petbarn_no_vox_avg_spend_per_user)

print(f"{'Merchant_B - Projected November Users':<50} {petbarn_full_projected:>25,.0f} {petbarn_no_vox_projected:>25,.0f} {petbarn_user_diff:>20,.0f}")
print(f"{'Merchant_B - Projected November Spend':<50} ${(petbarn_full_projected * petbarn_full_avg_spend_per_user):>24,.2f} ${(petbarn_no_vox_projected * petbarn_no_vox_avg_spend_per_user):>24,.2f} ${petbarn_spend_diff:>19,.2f}")
print(f"{'Merchant_B - Avg Spend per User':<50} ${petbarn_full_avg_spend_per_user:>24,.2f} ${petbarn_no_vox_avg_spend_per_user:>24,.2f} ${(petbarn_full_avg_spend_per_user - petbarn_no_vox_avg_spend_per_user):>19,.2f}")
print(f"{'Merchant_B - Total Historic Users (May-Oct)':<50} {petbarn_full_total_users:>25,.0f} {petbarn_no_vox_total_users:>25,.0f} {(petbarn_full_total_users - petbarn_no_vox_total_users):>20,.0f}")
print(f"{'Merchant_B - Total Historic Spend (May-Oct)':<50} ${petbarn_full_total_spend:>24,.2f} ${petbarn_no_vox_total_spend:>24,.2f} ${(petbarn_full_total_spend - petbarn_no_vox_total_spend):>19,.2f}")

print()
print("─" * 130)

# Total Comparison
total_user_diff = total_full_projected - total_no_vox_projected
total_spend_diff = total_full_projected_spend - total_no_vox_projected_spend

print(f"{'TOTAL - Projected November Users':<50} {total_full_projected:>25,.0f} {total_no_vox_projected:>25,.0f} {total_user_diff:>20,.0f}")
print(f"{'TOTAL - Projected November Spend':<50} ${total_full_projected_spend:>24,.2f} ${total_no_vox_projected_spend:>24,.2f} ${total_spend_diff:>19,.2f}")
print(f"{'TOTAL - Total Historic Spend (May-Oct)':<50} ${(bws_full_total_spend + petbarn_full_total_spend):>24,.2f} ${(bws_no_vox_total_spend + petbarn_no_vox_total_spend):>24,.2f} ${((bws_full_total_spend + petbarn_full_total_spend) - (bws_no_vox_total_spend + petbarn_no_vox_total_spend)):>19,.2f}")

print("\n" + "─" * 130)
print("3.2 VOX-Network_Partner_2 USER NETWORK CONTRIBUTION ANALYSIS")
print("─" * 130)

vox_user_contribution_pct = (total_user_diff / total_full_projected * 100) if total_full_projected > 0 else 0
vox_spend_contribution_pct = (total_spend_diff / total_full_projected_spend * 100) if total_full_projected_spend > 0 else 0

print(f"\n💡 VOX-Network_Partner_2 User Network Impact on Merchant_A/Merchant_B:")
print(f"   • Projected User Contribution: {total_user_diff:,.0f} users ({vox_user_contribution_pct:.1f}% of total)")
print(f"   • Projected Spend Contribution: ${total_spend_diff:,.2f} ({vox_spend_contribution_pct:.1f}% of total)")
print(f"   • Historic Merchant_A VOX-Network_Partner_2 User Spend: ${(bws_full_total_spend - bws_no_vox_total_spend):,.2f}")
print(f"   • Historic Merchant_B VOX-Network_Partner_2 User Spend: ${(petbarn_full_total_spend - petbarn_no_vox_total_spend):,.2f}")
print(f"   • Total Historic VOX-Network_Partner_2 Impact: ${((bws_full_total_spend - bws_no_vox_total_spend) + (petbarn_full_total_spend - petbarn_no_vox_total_spend)):,.2f}")

# ============================================================================
# SAVE RESULTS
# ============================================================================
print("\n\n" + "█" * 130)
print("SECTION 4: OUTPUT FILES")
print("█" * 130)

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
    'With_VOX_ING_Network': [
        int(bws_full_projected),
        bws_full_projected * bws_full_avg_spend_per_user,
        int(petbarn_full_projected),
        petbarn_full_projected * petbarn_full_avg_spend_per_user,
        int(total_full_projected),
        total_full_projected_spend
    ],
    'Without_VOX_ING_Network': [
        int(bws_no_vox_projected),
        bws_no_vox_projected * bws_no_vox_avg_spend_per_user,
        int(petbarn_no_vox_projected),
        petbarn_no_vox_projected * petbarn_no_vox_avg_spend_per_user,
        int(total_no_vox_projected),
        total_no_vox_projected_spend
    ],
    'VOX_ING_Contribution': [
        int(bws_user_diff),
        bws_spend_diff,
        int(petbarn_user_diff),
        petbarn_spend_diff,
        int(total_user_diff),
        total_spend_diff
    ],
    'VOX_ING_Percent': [
        (bws_user_diff/bws_full_projected*100) if bws_full_projected > 0 else 0,
        (bws_spend_diff/(bws_full_projected * bws_full_avg_spend_per_user)*100) if (bws_full_projected * bws_full_avg_spend_per_user) > 0 else 0,
        (petbarn_user_diff/petbarn_full_projected*100) if petbarn_full_projected > 0 else 0,
        (petbarn_spend_diff/(petbarn_full_projected * petbarn_full_avg_spend_per_user)*100) if (petbarn_full_projected * petbarn_full_avg_spend_per_user) > 0 else 0,
        vox_user_contribution_pct,
        vox_spend_contribution_pct
    ]
})

comparison_summary.to_csv('bws_petbarn_vox_ing_network_comparison.csv', index=False)
print("\n✅ Saved: bws_petbarn_vox_ing_network_comparison.csv")

# Monthly comparison
bws_full_df['scenario'] = 'With VOX-Network_Partner_2 Network'
bws_no_vox_df['scenario'] = 'Without VOX-Network_Partner_2 Network'
bws_comparison = pd.concat([bws_full_df, bws_no_vox_df])
bws_comparison.to_csv('bws_monthly_vox_ing_network_comparison.csv', index=False)
print("✅ Saved: bws_monthly_vox_ing_network_comparison.csv")

petbarn_full_df['scenario'] = 'With VOX-Network_Partner_2 Network'
petbarn_no_vox_df['scenario'] = 'Without VOX-Network_Partner_2 Network'
petbarn_comparison = pd.concat([petbarn_full_df, petbarn_no_vox_df])
petbarn_comparison.to_csv('petbarn_monthly_vox_ing_network_comparison.csv', index=False)
print("✅ Saved: petbarn_monthly_vox_ing_network_comparison.csv")

print("\n" + "=" * 130)
print("ANALYSIS COMPLETE")
print("=" * 130)
print(f"\n📊 EXECUTIVE SUMMARY:")
print(f"\n   WITH VOX-Network_Partner_2 NETWORK:")
print(f"      Users:  {total_full_projected:>10,.0f} | Spend: ${total_full_projected_spend:>15,.2f}")
print(f"\n   WITHOUT VOX-Network_Partner_2 NETWORK:")
print(f"      Users:  {total_no_vox_projected:>10,.0f} | Spend: ${total_no_vox_projected_spend:>15,.2f}")
print(f"\n   VOX-Network_Partner_2 NETWORK CONTRIBUTION:")
print(f"      Users:  {total_user_diff:>10,.0f} ({vox_user_contribution_pct:>5.1f}%) | Spend: ${total_spend_diff:>15,.2f} ({vox_spend_contribution_pct:>5.1f}%)")
print("\n" + "=" * 130)
