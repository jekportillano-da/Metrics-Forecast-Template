"""
Create forecast_2026 table with actual Jul-Dec 2025 data and exponential smoothing forecast
Considering Australian seasonality
"""
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Get database path relative to script location
SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR.parent / 'data' / 'processed' / 'pokitpal_historical_data.db'

# Connect to database
conn = sqlite3.connect(DB_PATH)

# Load existing forecast_data
print("Loading existing forecast_data table...")
forecast_df = pd.read_sql_query('SELECT * FROM forecast_data', conn)
print(f"Loaded {len(forecast_df)} rows from forecast_data")
print(f"Columns: {forecast_df.columns.tolist()}")

# Get actual transaction data for Jul-Dec 2025
print("\nCalculating actual metrics from transactions...")
print("Logic: SUM all states (Cancelled amounts are already negative)")

# Aggregate in SQL for better performance - handles both date formats
# Strip $ signs from Amount, Cashback, Fee fields
# SUM all transaction states (Cancelled is already negative)
query = """
SELECT 
    CASE 
        WHEN [Transaction Date] LIKE '%-%' THEN substr([Transaction Date], 1, 7)
        ELSE substr([Transaction Date], 7, 4) || '-' || substr([Transaction Date], 4, 2)
    END as month,
    SUM(CAST(REPLACE(Amount, '$', '') AS REAL)) as total_spend,
    SUM(CAST(REPLACE(Cashback, '$', '') AS REAL)) as total_cashback,
    SUM(CAST(REPLACE(Fee, '$', '') AS REAL)) as total_fee,
    COUNT(DISTINCT Email) as unique_users,
    COUNT(*) as transaction_count
FROM transactions
GROUP BY month
ORDER BY month
"""
actuals = pd.read_sql_query(query, conn)
actuals['month'] = pd.to_datetime(actuals['month'])
actuals = actuals.sort_values('month')

print(f"\nActuals data from {actuals['month'].min()} to {actuals['month'].max()}")
print(actuals)

# Calculate derived metrics
actuals['cashback_pct'] = (actuals['total_cashback'] / actuals['total_spend'] * 100).round(2)
actuals['fee_pct'] = (actuals['total_fee'] / actuals['total_spend'] * 100).round(2)
actuals['arpu'] = (actuals['total_spend'] / actuals['unique_users']).round(2)

# Format month for display
actuals['Month'] = actuals['month'].dt.strftime('%y-%b')

# Calculate growth rates
actuals = actuals.sort_values('month')
actuals['Spend Growth'] = actuals['total_spend'].pct_change()
actuals['Cashback Growth'] = actuals['total_cashback'].pct_change()
actuals['Fee Growth'] = actuals['total_fee'].pct_change()
actuals['User Growth'] = actuals['unique_users'].pct_change()
actuals['ARPU Growth'] = actuals['arpu'].pct_change()

# Prepare the base forecast dataframe - copy structure from forecast_data
forecast_2026 = forecast_df.copy()

# Update Jul-Dec 2025 with actual data (without growth rates first)
for idx, row in actuals.iterrows():
    month_str = row['Month']
    
    # Find matching row in forecast_2026
    mask = forecast_2026['Month'] == month_str
    
    if mask.any():
        print(f"\nUpdating {month_str} with actual data...")
        forecast_2026.loc[mask, 'Spend'] = row['total_spend']
        forecast_2026.loc[mask, 'Cashback'] = row['total_cashback']
        forecast_2026.loc[mask, 'Cashback %'] = f"{row['cashback_pct']:.2f}%"
        forecast_2026.loc[mask, 'Fee'] = row['total_fee']
        forecast_2026.loc[mask, 'Fee %'] = f"{row['fee_pct']:.2f}%"
        forecast_2026.loc[mask, 'Users'] = row['unique_users']
        forecast_2026.loc[mask, 'ARPU'] = row['arpu']

print("\n" + "="*80)
print("Creating forecasts for 2026 using Exponential Smoothing...")
print("="*80)

# Parse months and sort chronologically
forecast_2026['month_date'] = pd.to_datetime(forecast_2026['Month'], format='%y-%b')
forecast_2026 = forecast_2026.sort_values('month_date')

# Add 2026 months (Jan-Dec)
months_2026 = pd.date_range('2026-01-01', '2026-12-31', freq='MS')
new_rows = []
for month in months_2026:
    new_row = forecast_2026.iloc[-1].copy()  # Copy structure from last row
    new_row['Month'] = month.strftime('%y-%b')
    new_row['month_date'] = month
    # Reset values that will be forecasted
    for col in ['Spend', 'Cashback', 'Fee', 'Users', 'ARPU', 'Spend Growth', 
                'Cashback Growth', 'Fee Growth', 'User Growth', 'ARPU Growth']:
        new_row[col] = 0
    new_rows.append(new_row)

# Append 2026 rows
forecast_2026 = pd.concat([forecast_2026, pd.DataFrame(new_rows)], ignore_index=True)
forecast_2026 = forecast_2026.sort_values('month_date')

# Separate historical (up to Dec 2025) and future (2026) data
historical = forecast_2026[forecast_2026['month_date'] <= '2025-12-31'].copy()
future = forecast_2026[forecast_2026['month_date'] > '2025-12-31'].copy()

print(f"\nHistorical data points: {len(historical)}")
print(f"Future months to forecast: {len(future)}")
print(f"Future months to forecast: {len(future)}")

# Australian Seasonal factors (indexed by month)
# Summer: Dec-Feb (high retail), Autumn: Mar-May, Winter: Jun-Aug (mid), Spring: Sep-Nov (high)
AU_SEASONAL_FACTORS = {
    1: 1.05,   # Jan - Summer
    2: 1.02,   # Feb - Summer
    3: 0.98,   # Mar - Autumn
    4: 0.95,   # Apr - Autumn
    5: 0.96,   # May - Autumn
    6: 0.97,   # Jun - Winter
    7: 0.99,   # Jul - Winter
    8: 1.00,   # Aug - Winter
    9: 1.03,   # Sep - Spring
    10: 1.05,  # Oct - Spring
    11: 1.08,  # Nov - Spring (Black Friday)
    12: 1.12   # Dec - Summer (Christmas)
}

def forecast_with_seasonality(historical_data, periods, metric_name, seasonal_period=12):
    """Apply exponential smoothing with seasonality"""
    try:
        # Clean the data
        data = historical_data[metric_name].replace([np.inf, -np.inf], np.nan).dropna()
        
        if len(data) < 12:
            print(f"  Warning: Only {len(data)} data points for {metric_name}, using simple growth")
            # Use average growth rate
            growth = data.pct_change().mean()
            last_value = data.iloc[-1]
            forecasts = [last_value * (1 + growth) ** i for i in range(1, periods + 1)]
            return forecasts
        
        # Fit Exponential Smoothing model with seasonal component
        model = ExponentialSmoothing(
            data,
            seasonal_periods=seasonal_period,
            trend='add',
            seasonal='add',
            initialization_method='estimated'
        )
        fitted_model = model.fit(optimized=True)
        forecasts = fitted_model.forecast(steps=periods)
        
        return forecasts.values
    except Exception as e:
        print(f"  Error forecasting {metric_name}: {e}")
        # Fallback to simple trend
        data = historical_data[metric_name].replace([np.inf, -np.inf], np.nan).dropna()
        growth = data.pct_change().mean()
        last_value = data.iloc[-1]
        return [last_value * (1 + growth) ** i for i in range(1, periods + 1)]

# Forecast key metrics
if len(future) > 0:
    print(f"\nForecasting for {len(future)} months in 2026...")
    
    # Forecast Spend
    print("  - Forecasting Spend...")
    spend_forecast = forecast_with_seasonality(historical, len(future), 'Spend')
    
    # Apply Australian seasonality adjustments
    for i, (idx, row) in enumerate(future.iterrows()):
        month_num = row['month_date'].month
        seasonal_factor = AU_SEASONAL_FACTORS.get(month_num, 1.0)
        spend_forecast[i] *= seasonal_factor
    
    future['Spend'] = spend_forecast
    
    # Forecast Users
    print("  - Forecasting Users...")
    users_forecast = forecast_with_seasonality(historical, len(future), 'Users')
    future['Users'] = [int(u) for u in users_forecast]
    
    # Calculate ARPU from Spend and Users
    future['ARPU'] = (future['Spend'] / future['Users']).round(2)
    
    # Forecast Cashback % (average from recent history)
    recent_cb_pct = historical.tail(6)['Cashback %'].str.rstrip('%').astype(float).mean()
    future['Cashback %'] = f"{recent_cb_pct:.2f}%"
    future['Cashback'] = (future['Spend'] * recent_cb_pct / 100).round(2)
    
    # Forecast Fee % (average from recent history)
    recent_fee_pct = historical.tail(6)['Fee %'].str.rstrip('%').astype(float).mean()
    future['Fee %'] = f"{recent_fee_pct:.2f}%"
    future['Fee'] = (future['Spend'] * recent_fee_pct / 100).round(2)
    
    # Calculate growth rates
    combined = pd.concat([historical.tail(1), future]).reset_index(drop=True)
    combined['Spend Growth'] = combined['Spend'].pct_change()
    combined['User Growth'] = combined['Users'].pct_change()
    combined['ARPU Growth'] = combined['ARPU'].pct_change()
    combined['Cashback Growth'] = combined['Cashback'].pct_change()
    combined['Fee Growth'] = combined['Fee'].pct_change()
    
    # Update future with calculated growth rates
    future['Spend Growth'] = combined.iloc[1:]['Spend Growth'].values
    future['User Growth'] = combined.iloc[1:]['User Growth'].values
    future['ARPU Growth'] = combined.iloc[1:]['ARPU Growth'].values
    future['Cashback Growth'] = combined.iloc[1:]['Cashback Growth'].values
    future['Fee Growth'] = combined.iloc[1:]['Fee Growth'].values
    
    # Combine historical and future
    forecast_2026_final = pd.concat([historical, future]).sort_values('month_date')
else:
    forecast_2026_final = historical

# Recalculate ALL growth rates for the entire timeline (this fixes Jul 2025 growth issue)
print("\n  - Recalculating all growth rates...")
forecast_2026_final = forecast_2026_final.sort_values('month_date').reset_index(drop=True)
forecast_2026_final['Spend Growth'] = forecast_2026_final['Spend'].pct_change()
forecast_2026_final['User Growth'] = forecast_2026_final['Users'].pct_change()
forecast_2026_final['ARPU Growth'] = forecast_2026_final['ARPU'].pct_change()
forecast_2026_final['Cashback Growth'] = forecast_2026_final['Cashback'].pct_change()
forecast_2026_final['Fee Growth'] = forecast_2026_final['Fee'].pct_change()

# Drop the temporary date column and target columns
forecast_2026_final = forecast_2026_final.drop('month_date', axis=1)

# Remove target columns (from Spend_Target onwards)
target_cols = ['Spend_Target', 'Cashback_Target', 'CB Target %', 'Fee_Target', 'Fee Target %', 
               'Users_Target', 'ARPU_Target', 'Churn_45d_Target', 'Unnamed: 23', 'Unnamed: 24', 
               'Unnamed: 25', 'Unnamed: 26', 'Unnamed: 27']
cols_to_drop = [col for col in target_cols if col in forecast_2026_final.columns]
if cols_to_drop:
    print(f"  - Removing {len(cols_to_drop)} target-related columns...")
    forecast_2026_final = forecast_2026_final.drop(columns=cols_to_drop)

# Save to database
print("\n" + "="*80)
print("Saving forecast_2026 table to database...")
forecast_2026_final.to_sql('forecast_2026', conn, if_exists='replace', index=False)

# Display summary
print("="*80)
print("\nForecast Summary:")
print(forecast_2026_final[['Month', 'Spend', 'Users', 'ARPU', 'Cashback', 'Fee']].tail(15).to_string())

print("\n" + "="*80)
print("✓ forecast_2026 table created successfully!")
print(f"✓ Total rows: {len(forecast_2026_final)}")
print("✓ Jul-Dec 2025 updated with actual transaction data")
print("✓ 2026 forecasts generated with exponential smoothing + AU seasonality")
print("="*80)

conn.close()
