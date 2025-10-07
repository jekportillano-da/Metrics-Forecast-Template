# Update Guide: Jan-Jun 2026 Forecast

## 📅 Overview

This guide provides step-by-step instructions for updating the Pokitpal Metrics Dashboard with Jan-Jun 2026 actuals and forecasts. Follow these steps to maintain consistency with the established methodology.

**Timeline:** Perform this update in **January 2026** once December 2025 actuals are available.

---

## 🎯 Prerequisites

### Required Data
- ✅ December 2025 actual performance (spend, users, ARPU)
- ✅ Core business vs. VOX-ING breakdown
- ✅ Any new seasonal pattern observations
- ✅ Updated churn rates (if available)

### Tools Needed
- Text editor (VS Code, Notepad++, etc.)
- Spreadsheet software (Excel, Google Sheets)
- Calculator or Python (for compound growth calculations)
- Web browser (for dashboard testing)

---

## 📋 Step-by-Step Update Process

### **STEP 1: Gather Actual December 2025 Data**

#### Data Collection Checklist
```
Core Business (December 2025 Actuals):
[ ] Total Spend: $___________
[ ] Total Users: ___________
[ ] ARPU: $___________
[ ] Churn Rate: ___________%

VOX-ING (December 2025 Actuals):
[ ] Total Spend: $___________
[ ] Total Users: ___________

Combined (December 2025):
[ ] Total Spend: $___________
[ ] Total Users: ___________
```

#### Validation Steps
1. Verify core business and VOX-ING are properly separated
2. Confirm user counts match active user definition
3. Cross-check with finance/analytics systems
4. Document any anomalies or outliers

---

### **STEP 2: Calculate New Baseline (December 2025)**

The December 2025 **actuals** become the new baseline for Jan-Jun 2026 forecasts.

#### Update Baseline Values

**Old Baseline (June 2025):**
```
Spend:  $4.19M
Users:  25,823
ARPU:   $10.54
```

**New Baseline (December 2025 Actuals):**
```
Spend:  $________  (your Dec 2025 actual)
Users:  _________  (your Dec 2025 actual)
ARPU:   $________  (calculate: Spend ÷ Users)
```

#### Example Calculation
If December 2025 actuals are:
- Core Business Spend: $5.80M
- Core Business Users: 32,100

Then:
```
New Baseline Spend = $5.80M
New Baseline Users = 32,100
New Baseline ARPU = $5.80M ÷ 32,100 = $180.68
```

---

### **STEP 3: Update CSV Data File**

#### File: `pokitpal_forecast_updated_with_vox.csv`

**Add December 2025 Actuals:**
```csv
Month,Core_Spend,Core_Users,VOX_Spend,VOX_Users,Combined_Spend,Combined_Users
...
2025-12,5800000,32100,7000000,47500,12800000,79600
```

**Add Jan-Jun 2026 Forecasts:**

Use compound growth formulas from FORECAST_METHODOLOGY.md:

```csv
2026-01,[Core_Spend],[Core_Users],[VOX_Spend],[VOX_Users],[Combined],[Combined]
2026-02,[Core_Spend],[Core_Users],[VOX_Spend],[VOX_Users],[Combined],[Combined]
2026-03,[Core_Spend],[Core_Users],[VOX_Spend],[VOX_Users],[Combined],[Combined]
2026-04,[Core_Spend],[Core_Users],[VOX_Spend],[VOX_Users],[Combined],[Combined]
2026-05,[Core_Spend],[Core_Users],[VOX_Spend],[VOX_Users],[Combined],[Combined]
2026-06,[Core_Spend],[Core_Users],[VOX_Spend],[VOX_Users],[Combined],[Combined]
```

#### Forecast Calculation Formulas

**Core Business (using December 2025 baseline):**
```javascript
// For each month (n = 1 to 6):
Core_Spend(n) = Dec2025_Actual × (1.06)^n
Core_Users(n) = Dec2025_Actual × (1.04)^n
Core_ARPU(n) = Dec2025_ARPU × (1.06)^n
```

**Example for January 2026 (n=1):**
```
Core_Spend = $5.80M × 1.06 = $6.148M
Core_Users = 32,100 × 1.04 = 33,384
Core_ARPU = $180.68 × 1.06 = $191.52
```

**VOX-ING Projections:**
- Use December 2025 as baseline
- Apply same growth logic or update based on market trends
- Document any assumption changes

---

### **STEP 4: Update Dashboard HTML**

#### File: `VOX_Integration_Results/Executive_Dashboard.html`

#### 4A: Update Summary Tiles

**Find lines ~318-332** (December 2025 metrics):
```html
<div class="metric-value">$12.09M</div>
<div class="metric-label">Dec 2025 Forecast</div>
<div class="sub-metric">79.3K Users | Core Business + VOX-ING</div>
```

**Replace with June 2026 metrics:**
```html
<div class="metric-value">$[YOUR_JUNE_2026_FORECAST]M</div>
<div class="metric-label">Jun 2026 Forecast</div>
<div class="sub-metric">[YOUR_USERS]K Users | Core Business + VOX-ING</div>
```

#### 4B: Update Monthly Glide Path Table

**Find lines ~454-490** (Monthly data table):

**Current (Jul-Dec 2025):**
```html
<tr>
    <td>Dec 2025</td>
    <td>$12.09M</td>
    <td>$12.94M</td>
    <td>$0.85M</td>
    <td>$5.09M</td>
    <td>$7.00M</td>
    <td>57.9%</td>
</tr>
```

**Update to (Jan-Jun 2026):**
```html
<tr>
    <td>Jan 2026</td>
    <td>$[FORECAST]M</td>
    <td>$[TARGET]M</td>
    <td>$[GAP]M</td>
    <td>$[CORE]M</td>
    <td>$[VOX]M</td>
    <td>[VOX_SHARE]%</td>
</tr>
<!-- Repeat for Feb-Jun 2026 -->
```

#### 4C: Update JavaScript Arrays

**Find lines ~1394-1408** (Data arrays):

**Current arrays (Jul-Dec 2025 = indices 6-11):**
```javascript
const forecastSpend = [null, null, null, null, null, null, 4.54, 6.00, 10.34, 7.87, 8.04, 12.09];
const forecastUsers = [null, null, null, null, null, null, 21.189, 40.469, 67.873, 72.621, 73.549, 79.333];
```

**Extend for Jan-Jun 2026 (indices 12-17):**
```javascript
const forecastSpend = [null, null, null, null, null, null, 4.54, 6.00, 10.34, 7.87, 8.04, 12.09, [Jan], [Feb], [Mar], [Apr], [May], [Jun]];
const forecastUsers = [null, null, null, null, null, null, 21.189, 40.469, 67.873, 72.621, 73.549, 79.333, [Jan], [Feb], [Mar], [Apr], [May], [Jun]];
```

**Similarly update:**
- `targetSpend`
- `targetUsers`
- `baselineSpend`
- `baselineUsers`
- `baselineTargetUsers`
- `baselineTargetSpend`

#### 4D: Update Month Labels

**Find line ~1418** (Month labels):

**Current:**
```javascript
const months = ['Jun 2023', 'Jul 2023', ... 'Nov 2025', 'Dec 2025'];
```

**Extend:**
```javascript
const months = ['Jun 2023', 'Jul 2023', ... 'Nov 2025', 'Dec 2025', 'Jan 2026', 'Feb 2026', 'Mar 2026', 'Apr 2026', 'May 2026', 'Jun 2026'];
```

---

### **STEP 5: Update Methodology Text**

#### Update Forecast Period References

**Find and update:**
- "Jul-Dec 2025" → "Jan-Jun 2026"
- "December 2025" → "June 2026"
- "6 months" (should stay the same)
- Any specific date references

**Example locations:**
- Executive Summary section
- Methodology explanations
- Chart titles
- Table headers

#### Update Baseline References

**Find lines referencing "June 2025 baseline":**
```html
<p>6% monthly compound growth from June 2025 starting point</p>
```

**Update to:**
```html
<p>6% monthly compound growth from December 2025 starting point</p>
```

---

### **STEP 6: Recalculate Targets**

#### Target Calculation (using same 6% monthly growth)

**June 2026 Target:**
```
Core Target = Dec2025_Actual × (1.06)^6

Example:
Dec 2025 Actual = $5.80M
Jun 2026 Target = $5.80M × 1.4185 = $8.23M
```

**Combined Target:**
```
Combined Target = Core Target + VOX-ING Forecast

Example:
Core Target: $8.23M
VOX-ING: $8.50M (projected)
Combined: $16.73M
```

#### Verify Stretch Percentage
```
Stretch % = (Target - Forecast) / Forecast × 100%

Should be: 5-10% (conservative approach)
```

---

### **STEP 7: Update ARPU Calculations**

#### CRITICAL: Use Compound Growth Method

**DO NOT calculate ARPU as Spend ÷ Users!**

**Correct Method:**
```
ARPU(month) = Dec2025_ARPU × (1.06)^n

Example (June 2026, n=6):
Dec 2025 ARPU = $180.68
Jun 2026 ARPU = $180.68 × (1.06)^6 = $256.24
```

#### Update ARPU Display

**Find Core Business table (lines ~810-1200):**
Update ARPU column for Jan-Jun 2026 rows.

---

### **STEP 8: Apply Seasonal Adjustments**

#### Review Historical Patterns

**Check if new seasonal data is available:**
- January 2026 actual vs. forecast
- February 2026 actual vs. forecast
- Identify any new seasonal patterns

#### Update Seasonal Factors

**If new patterns emerge:**
1. Document in FORECAST_METHODOLOGY.md
2. Update adjustment calculations
3. Apply to relevant months (e.g., June might have end-of-Q2 seasonality)

**Example:**
```
If June historically shows +10% growth:
Adjusted June Forecast = Base Forecast × 1.10
```

---

### **STEP 9: Validate & Test**

#### Data Validation Checklist

```
Core Business Consistency:
[ ] Jun 2026 Spend = Dec 2025 × (1.06)^6
[ ] Jun 2026 Users = Dec 2025 × (1.04)^6
[ ] Jun 2026 ARPU = Dec 2025 ARPU × (1.06)^6
[ ] All months follow compound growth progression

Dashboard Consistency:
[ ] Summary tiles match final month (June 2026)
[ ] Monthly Glide Path table shows Jan-Jun 2026
[ ] Charts display all 12 data points (Dec 2023 - Jun 2026)
[ ] JavaScript arrays have 18 elements (indices 0-17)
[ ] ARPU calculated via compound growth (not Spend/Users)

Target Logic:
[ ] Targets independent of VOX-ING
[ ] Stretch percentage is 5-10%
[ ] Combined = Core + VOX (not inflated)
[ ] Methodology text matches calculations
```

#### Browser Testing

1. Open `Executive_Dashboard.html` in browser
2. Check all charts render correctly
3. Verify table data is complete
4. Test interactive elements (if any)
5. Check mobile/responsive layout

#### Cross-Reference Check

```
Tile Value = Last Table Row = Last JavaScript Array Element

Example:
Summary Tile: $16.73M
Table Row (Jun 2026): $16.73M
forecastSpend[17]: 16.73
```

---

### **STEP 10: Document Changes**

#### Update Change Log

**In FORECAST_METHODOLOGY.md:**
```markdown
| Date | Version | Change | Reason |
|------|---------|--------|--------|
| Jan 2026 | 2.1 | Extended forecast to Jan-Jun 2026 | New baseline from Dec 2025 actuals |
```

#### Update README.md

**Update badges:**
```markdown
![Forecast Period](https://img.shields.io/badge/Forecast-Jan%202026%20--%20Jun%202026-orange)
```

**Update key metrics section with June 2026 values.**

#### Create Update Summary

**Document in commit message:**
```
Update: Jan-Jun 2026 forecast based on Dec 2025 actuals

- New baseline: $5.80M core spend, 32,100 users
- June 2026 target: $16.73M combined
- Maintained 6% monthly compound growth methodology
- VOX-ING: $8.50M June projection (steady state)
- Validated all calculations and dashboard consistency
```

---

## 🔧 Troubleshooting

### Common Issues

#### Issue 1: Charts Not Displaying
**Symptom:** Blank chart area or console errors

**Fix:**
- Check array lengths match (`forecastSpend.length === months.length`)
- Verify no syntax errors in JavaScript arrays
- Ensure `null` values for historical months without data

#### Issue 2: Inconsistent Numbers
**Symptom:** Tiles show different values than tables

**Fix:**
- Update all three locations: tiles, tables, JavaScript arrays
- Use find/replace to update all instances of old values
- Validate with calculator

#### Issue 3: ARPU Looks Wrong
**Symptom:** ARPU too high or inconsistent

**Fix:**
- Verify using compound growth formula, not Spend/Users
- Check baseline ARPU is correct
- Recalculate: `ARPU = BaselineARPU × (1.06)^n`

#### Issue 4: Seasonal Adjustment Confusion
**Symptom:** December/January values seem off

**Fix:**
- Review historical patterns (2024 data preferred)
- Exclude outliers (e.g., 2023's +85.6%)
- Document reasoning in methodology

---

## 📊 Quick Reference Formulas

### Core Business Forecasts (from December 2025 baseline)

```javascript
// Month n (1-6 for Jan-Jun 2026)
spend = dec2025_spend * Math.pow(1.06, n);
users = dec2025_users * Math.pow(1.04, n);
arpu = dec2025_arpu * Math.pow(1.06, n);
```

### Targets

```javascript
// Same formula, applied to target baseline
target_spend = dec2025_target * Math.pow(1.06, n);
target_users = dec2025_target_users * Math.pow(1.04, n);
```

### Combined Metrics

```javascript
combined_spend = core_spend + vox_spend;
combined_users = core_users + vox_users;
vox_share = (vox_spend / combined_spend) * 100;
```

---

## ✅ Final Checklist Before Commit

```
Documentation:
[ ] README.md updated with Jun 2026 metrics
[ ] FORECAST_METHODOLOGY.md change log updated
[ ] UPDATE_GUIDE.md reviewed (this file)

Data Files:
[ ] pokitpal_forecast_updated_with_vox.csv extended to Jun 2026
[ ] All actuals vs. forecasts properly labeled
[ ] No missing or duplicate rows

Dashboard HTML:
[ ] Summary tiles show June 2026
[ ] Monthly Glide Path table has Jan-Jun 2026
[ ] JavaScript arrays extended to 18 elements
[ ] Month labels include Jan-Jun 2026
[ ] Charts render correctly
[ ] All ARPU values use compound growth

Validation:
[ ] Formulas verified with calculator
[ ] Dashboard consistency checked
[ ] Browser testing completed
[ ] No console errors
[ ] Mobile layout tested

Git:
[ ] All files staged
[ ] Meaningful commit message written
[ ] Ready to push to main
```

---

## 📞 Support

If you encounter issues not covered in this guide:

1. Review `FORECAST_METHODOLOGY.md` for detailed calculation logic
2. Check inline comments in `Executive_Dashboard.html`
3. Compare with Jul-Dec 2025 structure (known working version)
4. Validate formulas with external calculator

---

**Last Updated:** October 2025  
**Next Use:** January 2026  
**Estimated Time:** 2-3 hours for complete update
