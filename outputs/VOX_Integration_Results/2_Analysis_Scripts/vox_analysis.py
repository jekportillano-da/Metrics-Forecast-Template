import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# VOX-Network_Partner_2 Data Analysis
print("=== VOX-Network_Partner_2 Data Analysis ===")
print()

# Given data
vox_august_gmv = 1412043.09  # $1,412,043.09
vox_september_gmv = 3605870.03  # $3,605,870.03
vox_august_users = 11730  # 11.73k
vox_september_users = 28200  # 28.2k

print(f"August GMV: ${vox_august_gmv:,.2f}")
print(f"September GMV: ${vox_september_gmv:,.2f}")
print(f"August Users: {vox_august_users:,}")
print(f"September Users: {vox_september_users:,}")
print()

# Calculate growth rates
gmv_growth = (vox_september_gmv - vox_august_gmv) / vox_august_gmv * 100
users_growth = (vox_september_users - vox_august_users) / vox_august_users * 100

print(f"Month-over-month GMV Growth: {gmv_growth:.1f}%")
print(f"Month-over-month Users Growth: {users_growth:.1f}%")
print()

# Adjust August for partial month (started Aug 21 = 11 days out of 31)
august_days = 11
august_total_days = 31
august_coverage = august_days / august_total_days

print(f"August coverage: {august_days} days out of {august_total_days} = {august_coverage:.1%}")

# Annualized August estimates
annualized_august_gmv = vox_august_gmv / august_coverage
annualized_august_users = vox_august_users / august_coverage

print(f"Annualized August GMV estimate: ${annualized_august_gmv:,.2f}")
print(f"Annualized August Users estimate: {annualized_august_users:,.0f}")
print()

# Recalculate growth based on annualized August
adjusted_gmv_growth = (vox_september_gmv - annualized_august_gmv) / annualized_august_gmv * 100
adjusted_users_growth = (vox_september_users - annualized_august_users) / annualized_august_users * 100

print(f"Adjusted month-over-month GMV Growth: {adjusted_gmv_growth:.1f}%")
print(f"Adjusted month-over-month Users Growth: {adjusted_users_growth:.1f}%")
print()

# Calculate daily rates for projection
# August daily rates (for 11 days)
august_daily_gmv = vox_august_gmv / august_days
august_daily_users = vox_august_users / august_days

print(f"August daily GMV rate: ${august_daily_gmv:,.2f}")
print(f"August daily Users rate: {august_daily_users:,.0f}")
print()

# September daily rates (assuming 29 days completed by Sept 29)
september_days = 29
september_daily_gmv = vox_september_gmv / september_days
september_daily_users = vox_september_users / september_days

print(f"September daily GMV rate: ${september_daily_gmv:,.2f}")
print(f"September daily Users rate: {september_daily_users:,.0f}")
print()

# Growth in daily rates
daily_gmv_growth = (september_daily_gmv - august_daily_gmv) / august_daily_gmv * 100
daily_users_growth = (september_daily_users - august_daily_users) / august_daily_users * 100

print(f"Daily rate GMV Growth: {daily_gmv_growth:.1f}%")
print(f"Daily rate Users Growth: {daily_users_growth:.1f}%")
print()

# Project October based on current trajectory
# Simple linear trend projection
october_daily_gmv = september_daily_gmv * (1 + daily_gmv_growth/100/30)  # Daily compounding
october_daily_users = september_daily_users * (1 + daily_users_growth/100/30)

print("=== October Projection ===")
print(f"Projected October daily GMV rate: ${october_daily_gmv:,.2f}")
print(f"Projected October daily Users rate: {october_daily_users:,.0f}")
print(f"Projected October total GMV (31 days): ${october_daily_gmv * 31:,.2f}")
print(f"Projected October total Users (31 days): {october_daily_users * 31:,.0f}")