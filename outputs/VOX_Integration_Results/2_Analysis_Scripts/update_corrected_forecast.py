import pandas as pd
import numpy as np

print("=== UPDATING MAIN FORECAST FILE WITH CORRECTED TARGETS ===")
print()

# Load the current forecast file
df = pd.read_csv('pokitpal_forecast_updated_with_vox.csv')

# Clean currency function
def clean_currency(col):
    if col.dtype == 'object':
        return pd.to_numeric(col.str.replace(r'[\$,]', '', regex=True), errors='coerce')
    return col

# Clean the data
currency_cols = ['Spend', 'Spend_Target', 'Users_Target']
for col in currency_cols:
    if col in df.columns:
        df[col] = clean_currency(df[col])

df['Date'] = pd.to_datetime(df['Month'], format='%y-%b', errors='coerce')

print("Current data loaded")

# Our corrected forecasts and targets
corrected_data = {
    '2025-10-01': {
        'forecast_spend': 7869408.22,
        'target_spend': 9443289.86,
        'forecast_users': 48789,
        'target_users': 58547
    },
    '2025-11-01': {
        'forecast_spend': 8057376.21,
        'target_spend': 9668851.45,
        'forecast_users': 48185,
        'target_users': 57822
    },
    '2025-12-01': {
        'forecast_spend': 8286612.74,
        'target_spend': 9943935.29,
        'forecast_users': 48079,
        'target_users': 57695
    }
}

# Update the dataframe with corrected values
for date_str, values in corrected_data.items():
    date_filter = df['Date'] == date_str
    if date_filter.any():
        # Update forecasts (what we expect to happen)
        df.loc[date_filter, 'Spend'] = values['forecast_spend']
        df.loc[date_filter, 'Users'] = values['forecast_users']
        
        # Update targets (stretch goals above forecast)
        df.loc[date_filter, 'Spend_Target'] = values['target_spend']
        df.loc[date_filter, 'Users_Target'] = values['target_users']
        
        print(f"Updated {date_str}: Forecast ${values['forecast_spend']:,.0f}, Target ${values['target_spend']:,.0f} (+20%)")

# Recalculate growth rates
for i in range(1, len(df)):
    current_spend = df.iloc[i]['Spend']
    prev_spend = df.iloc[i-1]['Spend']
    if prev_spend > 0 and not pd.isna(current_spend) and not pd.isna(prev_spend):
        growth = (current_spend - prev_spend) / prev_spend
        df.iloc[i, df.columns.get_loc('Spend Growth')] = growth
    
    current_users = df.iloc[i]['Users']
    prev_users = df.iloc[i-1]['Users']
    if prev_users > 0 and not pd.isna(current_users) and not pd.isna(prev_users):
        growth = (current_users - prev_users) / prev_users
        df.iloc[i, df.columns.get_loc('User Growth')] = growth

# Save the corrected file
df_export = df.drop(['Date'], axis=1, errors='ignore')
df_export.to_csv('pokitpal_forecast_CORRECTED_with_vox.csv', index=False)

print()
print("=== CORRECTED FORECAST FILE SAVED ===")
print("File: pokitpal_forecast_CORRECTED_with_vox.csv")
print()

print("=== VERIFICATION: FORECAST vs TARGET RELATIONSHIP ===")
target_dates = ['2025-10-01', '2025-11-01', '2025-12-01']
for date_str in target_dates:
    date_filter = df['Date'] == date_str
    if date_filter.any():
        row = df[date_filter].iloc[0]
        forecast_spend = row['Spend']
        target_spend = row['Spend_Target']
        target_uplift = (target_spend / forecast_spend - 1) * 100 if forecast_spend > 0 else 0
        
        month_name = row['Month']
        print(f"{month_name}: Forecast ${forecast_spend:,.0f} → Target ${target_spend:,.0f} (+{target_uplift:.0f}%)")

print()
print("✅ CORRECTED: All targets are now properly set ABOVE forecasts")
print("✅ This creates appropriate stretch goals to drive team performance")
print("✅ Forecasts represent realistic expectations using exponential smoothing")
print("✅ Targets represent aspirational goals 20% above forecasts")

# Create summary table
summary_data = []
for date_str in target_dates:
    values = corrected_data[date_str]
    month = pd.to_datetime(date_str).strftime('%b %Y')
    summary_data.append({
        'Month': month,
        'Forecast_Spend_M': round(values['forecast_spend']/1e6, 2),
        'Target_Spend_M': round(values['target_spend']/1e6, 2),
        'Forecast_Users_K': round(values['forecast_users']/1e3, 1),
        'Target_Users_K': round(values['target_users']/1e3, 1),
        'Spend_Uplift': '20%',
        'Users_Uplift': '20%'
    })

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv('forecast_vs_target_summary.csv', index=False)
print()
print("Summary table saved to 'forecast_vs_target_summary.csv'")

print()
print("=== IMPACT ANALYSIS ===")
print("With VOX-Network_Partner_2 integration and corrected target methodology:")
print(f"December 2025:")
print(f"- Forecast: $8.29M spend, 48k users (realistic expectation)")
print(f"- Target: $9.94M spend, 58k users (stretch goal)")
print(f"- Gap to close: $1.65M spend, 10k users")
print()
print("This provides clear stretch goals while maintaining realistic forecasting.")