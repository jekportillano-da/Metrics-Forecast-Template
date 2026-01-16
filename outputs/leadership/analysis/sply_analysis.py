"""Calculate SPLY insights for Nov-Dec projections"""

# Historical data
sply_2024 = [2.56, 2.47, 2.73, 4.07, 4.28]  # Aug-Dec 2024
sply_2025_organic = [3.85, 4.45, 4.44, 4.40, 4.50]  # Aug-Dec 2025 (excl VOX-ING)
sply_2025_vox = [1.71, 5.45, 3.98, 4.20, 4.50]  # VOX-ING contribution
sply_2025_total = [o + v for o, v in zip(sply_2025_organic, sply_2025_vox)]

months = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec']

print("\n" + "="*70)
print("GMV SPLY Analysis: 2024 vs 2025 (Aug-Dec)")
print("="*70)

for i, month in enumerate(months):
    gmv_2024 = sply_2024[i]
    gmv_2025 = sply_2025_total[i]
    growth = ((gmv_2025 / gmv_2024) - 1) * 100
    vox_contrib = (sply_2025_vox[i] / gmv_2025) * 100
    
    print(f"\n{month} 2024: ${gmv_2024:.2f}M → {month} 2025: ${gmv_2025:.2f}M")
    print(f"  YoY Growth: +{growth:.1f}%")
    print(f"  VOX-ING: ${sply_2025_vox[i]:.2f}M ({vox_contrib:.0f}% of total)")
    print(f"  Organic: ${sply_2025_organic[i]:.2f}M ({100-vox_contrib:.0f}% of total)")

print("\n" + "="*70)
print("Q4 2024 vs Q4 2025 Projection (Nov-Dec Focus)")
print("="*70)

# Nov-Dec averages
nov_dec_2024 = (4.07 + 4.28) / 2
nov_dec_2025 = (8.60 + 9.00) / 2
nov_dec_growth = ((nov_dec_2025 / nov_dec_2024) - 1) * 100

print(f"\nNov-Dec 2024 Average: ${nov_dec_2024:.2f}M")
print(f"Nov-Dec 2025 Forecast: ${nov_dec_2025:.2f}M")
print(f"YoY Growth: +{nov_dec_growth:.1f}%")

# Volume implications
print("\n" + "="*70)
print("Transaction Volume Implications (assuming constant AOV)")
print("="*70)

# Assuming Oct 2025 had 77,084 transactions for $4.44M organic + $3.98M VOX = $8.42M
oct_2025_txns = 77084
oct_2025_gmv = 8.42
aov_2025 = oct_2025_gmv * 1000000 / oct_2025_txns

print(f"\nOct 2025 baseline: {oct_2025_txns:,} transactions, ${oct_2025_gmv:.2f}M GMV")
print(f"Average Order Value: ${aov_2025:.2f}")

# Nov-Dec volume projections
nov_2025_gmv = 8.60
dec_2025_gmv = 9.00
nov_2025_txns = int((nov_2025_gmv * 1000000) / aov_2025)
dec_2025_txns = int((dec_2025_gmv * 1000000) / aov_2025)

print(f"\nNov 2025 projection: {nov_2025_txns:,} transactions (+{((nov_2025_txns/oct_2025_txns)-1)*100:.1f}% MoM)")
print(f"Dec 2025 projection: {dec_2025_txns:,} transactions (+{((dec_2025_txns/nov_2025_txns)-1)*100:.1f}% MoM)")

# User growth context
print("\n" + "="*70)
print("User Growth Context")
print("="*70)
users_2024 = [24.50, 21.89, 24.38, 32.84, 34.64]  # Aug-Dec 2024
users_2025_organic = [27.85, 26.62, 25.37, 27.60, 28.15]  # Aug-Dec 2025 (excl VOX)
users_2025_vox = [0, 0, 0, 0.72, 1.57]  # VOX-ING users
users_2025_total = [o + v for o, v in zip(users_2025_organic, users_2025_vox)]

nov_dec_users_2024 = (32.84 + 34.64) / 2
nov_dec_users_2025 = (28.32 + 29.72) / 2  # Nov-Dec 2025 forecast

print(f"\nNov-Dec 2024 Avg Users: {nov_dec_users_2024:.1f}K")
print(f"Nov-Dec 2025 Forecast: {nov_dec_users_2025:.1f}K")
print(f"Change: {((nov_dec_users_2025/nov_dec_users_2024)-1)*100:.1f}%")

print("\n" + "="*70)
print("Key Insights for Leadership")
print("="*70)
print("""
1. GMV SURGE: Nov-Dec 2025 projected at ~$8.8M average (+111% YoY)
   - This is MORE THAN DOUBLE last year's holiday performance
   - VOX-ING partnership contributing ~50% of growth

2. VOLUME SPIKE: Expecting ~78K-82K transactions per month
   - Up from 77K in October (+2-7% monthly growth)
   - System capacity and merchant support must scale accordingly

3. USER DYNAMICS: Despite GMV growth, user base is DOWN -14% YoY
   - Higher spending per user (GMV/User increased significantly)
   - Focus on retention and reactivation critical for sustainability

4. OPERATIONAL READINESS:
   - Payment processing capacity: Ensure infrastructure handles 80K+ txns
   - Merchant support: Top merchants will see 2x volume vs last year
   - Customer service: Plan for proportional inquiry volume increase
   - Network partnerships: VOX-ING relationship critical to Q4 success

5. RISK FACTORS:
   - High dependency on VOX-ING (50% of Q4 GMV)
   - User decline trend must reverse for long-term health
   - Holiday seasonality makes Jan 2026 drop-off likely
""")
