import pandas as pd
import numpy as np

print("=== CORRECTING FORECAST vs TARGET METHODOLOGY ===")
print()
print("CRITICAL CORRECTION:")
print("- FORECAST = Realistic prediction using exponential smoothing")
print("- TARGET = Stretch goal set ABOVE forecast to drive performance")
print()

# Load our current forecast results
forecast_data = {
    'Oct 2025': {'forecast_spend': 7869408.22, 'forecast_users': 48789},
    'Nov 2025': {'forecast_spend': 8057376.21, 'forecast_users': 48185},
    'Dec 2025': {'forecast_spend': 8286612.74, 'forecast_users': 48079}
}

print("=== CURRENT FORECASTS (WITH VOX-Network_Partner_2) ===")
for month, data in forecast_data.items():
    print(f"{month}: ${data['forecast_spend']:,.2f} spend, {data['forecast_users']:,} users")
print()

# Calculate appropriate targets (10-15% above forecast)
target_uplift_spend = 0.12  # 12% above forecast for spend targets
target_uplift_users = 0.15  # 15% above forecast for users targets

print(f"TARGET METHODOLOGY:")
print(f"- Spend Targets: {target_uplift_spend:.0%} above forecast")
print(f"- Users Targets: {target_uplift_users:.0%} above forecast")
print()

updated_targets = {}
for month, data in forecast_data.items():
    target_spend = data['forecast_spend'] * (1 + target_uplift_spend)
    target_users = data['forecast_users'] * (1 + target_uplift_users)
    
    updated_targets[month] = {
        'forecast_spend': data['forecast_spend'],
        'forecast_users': data['forecast_users'],
        'target_spend': target_spend,
        'target_users': target_users,
        'spend_gap': target_spend - data['forecast_spend'],
        'users_gap': target_users - data['forecast_users']
    }

print("=== CORRECTED FORECAST vs TARGET RELATIONSHIP ===")
for month, data in updated_targets.items():
    print(f"{month}:")
    print(f"  Forecast: ${data['forecast_spend']:,.2f} spend, {data['forecast_users']:,} users")
    print(f"  Target:   ${data['target_spend']:,.2f} spend, {data['target_users']:,.0f} users")
    print(f"  Gap:      ${data['spend_gap']:,.2f} spend (+{target_uplift_spend:.0%}), {data['users_gap']:,.0f} users (+{target_uplift_users:.0%})")
    print()

print("=== ORIGINAL FILE TARGET ANALYSIS ===")
# Let's check how the original file set targets vs forecasts
original_data = [
    {'month': 'Jul 2025', 'forecast': 4543866.62, 'target': 4543866.62},  # Same
    {'month': 'Aug 2025', 'forecast': 4858964.79, 'target': 4816498.62},  # Target lower (unusual)
    {'month': 'Sep 2025', 'forecast': 4846007.50, 'target': 5105488.54},  # Target higher (+5.4%)
    {'month': 'Oct 2025', 'forecast': 4873929.03, 'target': 5411817.85},  # Target higher (+11.0%)
    {'month': 'Nov 2025', 'forecast': 4837215.33, 'target': 5736526.92},  # Target higher (+18.6%)
    {'month': 'Dec 2025', 'forecast': 4470707.84, 'target': 6080718.54}   # Target higher (+36.0%)
]

print("Original file Target vs Forecast analysis:")
for data in original_data:
    if data['target'] > 0 and data['forecast'] > 0:
        uplift = (data['target'] / data['forecast'] - 1) * 100
        print(f"{data['month']}: Target {uplift:+.1f}% vs Forecast")
print()

print("INSIGHT: Original file shows targets should be 10-35% ABOVE forecasts")
print()

# Calculate what our December target should be with appropriate uplift
original_dec_target_uplift = (6080718.54 / 4470707.84 - 1)  # +36% in original
print(f"Original December target was {original_dec_target_uplift:.0%} above forecast")

# Apply similar aggressive uplift to our updated forecast
aggressive_target_uplift = 0.20  # 20% above forecast (more reasonable than 36%)

final_targets = {}
for month, data in forecast_data.items():
    target_spend = data['forecast_spend'] * (1 + aggressive_target_uplift)
    target_users = data['forecast_users'] * (1 + aggressive_target_uplift)
    
    final_targets[month] = {
        'forecast_spend': data['forecast_spend'],
        'target_spend': target_spend,
        'forecast_users': data['forecast_users'],
        'target_users': target_users
    }

print("=== FINAL CORRECTED TARGETS (20% above forecast) ===")
for month, data in final_targets.items():
    print(f"{month}:")
    print(f"  Forecast: ${data['forecast_spend']:,.2f} spend, {data['forecast_users']:,} users")
    print(f"  Target:   ${data['target_spend']:,.2f} spend, {data['target_users']:,.0f} users")
    print(f"  Stretch:  +20% above forecast")
    print()

# Export corrected data
corrected_forecast_data = []
months = ['Oct 2025', 'Nov 2025', 'Dec 2025']
for month in months:
    data = final_targets[month]
    corrected_forecast_data.append({
        'Month': month,
        'Forecast_Spend': data['forecast_spend'],
        'Target_Spend': data['target_spend'],
        'Forecast_Users': data['forecast_users'],
        'Target_Users': data['target_users'],
        'Target_Uplift': '20%'
    })

corrected_df = pd.DataFrame(corrected_forecast_data)
corrected_df.to_csv('corrected_forecast_vs_targets.csv', index=False)

print("=== SUMMARY ===")
print("✅ CORRECTED: Targets are now properly set ABOVE forecasts")
print("✅ December 2025:")
print(f"   - Forecast: ${final_targets['Dec 2025']['forecast_spend']:,.2f}")
print(f"   - Target:   ${final_targets['Dec 2025']['target_spend']:,.2f} (+20%)")
print("✅ This creates appropriate stretch goals to drive performance")
print()
print("Corrected data exported to 'corrected_forecast_vs_targets.csv'")

print()
print("NEXT: Need to update the main forecast file with corrected targets")