# Forecast Methodology Documentation

## 📋 Table of Contents
1. [Overview](#overview)
2. [Core Business Forecasting](#core-business-forecasting)
3. [VOX-Network_Partner_2 Forecasting](#vox-ing-forecasting)
4. [Target Calculation Logic](#target-calculation-logic)
5. [ARPU Methodology](#arpu-methodology)
6. [Seasonal Adjustments](#seasonal-adjustments)
7. [Compound Growth Formulas](#compound-growth-formulas)
8. [Data Validation Rules](#data-validation-rules)

---

## Overview

### Philosophy
The Pokitpal forecast methodology uses **compound growth** calculations with **data-driven seasonal adjustments** to provide conservative, achievable targets. VOX-Network_Partner_2 revenue is treated as **incremental** to core business, not as a replacement.

### Key Principles
- ✅ **Mathematical Consistency**: All calculations use compound growth formulas
- ✅ **Conservative Targets**: 7% stretch goals (vs. industry 15-20%)
- ✅ **Data-Driven Seasonality**: Based on actual 2024 patterns, not outliers
- ✅ **Independent Streams**: Core business and VOX-Network_Partner_2 tracked separately
- ✅ **Reality-Based**: Anchored to actual Aug/Sep 2025 VOX-Network_Partner_2 performance

### Forecast Period
- **Historical Data**: Jun 2023 - Jun 2025 (25 months actuals)
- **Current Forecast**: Jul 2025 - Dec 2025 (6 months)
- **Next Update**: Jan 2026 - Jun 2026 (6 months)

---

## Core Business Forecasting

### Starting Point (June 2025 Baseline)
```
Spend:  $4.19M
Users:  25,823
ARPU:   $10.54
```

### Monthly Growth Rates
- **Spend Growth**: 6% monthly compound
- **User Growth**: 4% monthly compound
- **ARPU Growth**: 6% monthly compound
- **Churn Reduction**: -3.5% monthly compound (-19.25% total over 6 months)

### Calculation Formula

#### Spend Forecast
```
Spend(month) = $4.19M × (1.06)^n
where n = months since June 2025
```

**Example: December 2025**
```
n = 6 months
Spend(Dec) = $4.19M × (1.06)^6
Spend(Dec) = $4.19M × 1.4185
Spend(Dec) = $5.94M (target)
```

#### User Forecast
```
Users(month) = 25,823 × (1.04)^n
where n = months since June 2025
```

**Example: December 2025**
```
n = 6 months
Users(Dec) = 25,823 × (1.04)^6
Users(Dec) = 25,823 × 1.2653
Users(Dec) = 32,674 users (target)
```

#### ARPU Forecast
```
ARPU(month) = $10.54 × (1.06)^n
where n = months since June 2025
```

**Example: December 2025**
```
n = 6 months
ARPU(Dec) = $10.54 × (1.06)^6
ARPU(Dec) = $10.54 × 1.4185
ARPU(Dec) = $14.95
```

### Month-by-Month Core Business Progression

| Month | n | Spend Multiplier | Spend | User Multiplier | Users | ARPU |
|-------|---|------------------|-------|-----------------|-------|------|
| Jun 2025 | 0 | 1.0000 | $4.19M | 1.0000 | 25,823 | $10.54 |
| Jul 2025 | 1 | 1.0600 | $4.44M | 1.0400 | 26,856 | $11.17 |
| Aug 2025 | 2 | 1.1236 | $4.71M | 1.0816 | 27,930 | $11.84 |
| Sep 2025 | 3 | 1.1910 | $4.99M | 1.1249 | 29,047 | $12.55 |
| Oct 2025 | 4 | 1.2625 | $5.29M | 1.1699 | 30,209 | $13.31 |
| Nov 2025 | 5 | 1.3382 | $5.61M | 1.2167 | 31,417 | $14.10 |
| Dec 2025 | 6 | 1.4185 | $5.94M | 1.2653 | 32,674 | $14.95 |

---

## VOX-Network_Partner_2 Forecasting

### Actual Performance (Confirmed)
```
August 2025:    $1.46M spend | 11,770 users
September 2025: $5.49M spend | 39,180 users
```

### Projection Method
VOX-Network_Partner_2 forecasts for Oct-Dec 2025 are based on **continued growth from September baseline**, factoring in market penetration and seasonal patterns.

### October-December 2025 Projections
```
October 2025:   $7.87M spend | 47,500 users
November 2025:  $7.00M spend | 47,500 users  
December 2025:  $7.00M spend | 47,500 users
```

### VOX-Network_Partner_2 Growth Logic
- **Aug → Sep**: 276% growth (early ramp-up phase)
- **Sep → Oct**: Stabilization at ~$7-8M monthly run rate
- **Oct → Dec**: Maintained steady state with slight seasonal lift

### Market Share Calculation
```
VOX Share = VOX Spend ÷ Total Spend × 100%

Example (December 2025):
VOX Share = $7.00M ÷ $12.09M × 100%
VOX Share = 57.9%
```

---

## Target Calculation Logic

### Target Philosophy
Targets are set **independently** for core business and VOX-Network_Partner_2, then combined. This prevents unrealistic expectations from inflating core business targets based on uncertain VOX-Network_Partner_2 performance.

### Core Business Targets
```
Core Target = Core Forecast × Growth Factor
where Growth Factor = (1.06)^n for spend, (1.04)^n for users
```

**December 2025 Example:**
```
Forecast: $4.84M (seasonally adjusted) → Target: $5.94M
This represents the 6-month compound growth trajectory, plus seasonal adjustment
```

### Combined Targets
```
Combined Target = Core Business Target + VOX-Network_Partner_2 Forecast
```

**December 2025 Example:**
```
Core Target:    $5.94M
VOX-Network_Partner_2:        $7.00M
Combined:       $12.94M
```

### Target Stretch Percentage
```
Stretch % = (Target - Forecast) ÷ Forecast × 100%

December 2025:
Stretch % = ($12.94M - $12.09M) ÷ $12.09M × 100%
Stretch % = 7.0%
```

**Industry Context:**
- Conservative: 5-10% stretch
- Standard: 10-15% stretch
- Aggressive: 15-20%+ stretch

Our **7.0%** is intentionally conservative.

---

## ARPU Methodology

### Critical Rule: Compound Growth, Not Ratios

❌ **WRONG METHOD:**
```
ARPU = Total Spend ÷ Total Users
```
This produces inconsistent results due to VOX-Network_Partner_2's different user economics.

✅ **CORRECT METHOD:**
```
ARPU(month) = $10.54 × (1.06)^n
```
ARPU follows its own compound growth trajectory independent of spend/user ratios.

### Why This Matters

**Example December 2025:**
```
Wrong Method:
ARPU = $12.09M ÷ 79,333 users = $152.40 ❌ (Inflated by VOX-Network_Partner_2)

Correct Method:
ARPU = $10.54 × (1.06)^6 = $14.95 ✅ (Consistent core business metric)
```

### ARPU Display in Dashboard
- **Core Business ARPU**: Shows compound growth ($10.54 → $14.95)
- **Combined ARPU**: Not displayed (misleading due to VOX-Network_Partner_2 mix)
- **VOX-Network_Partner_2 ARPU**: Separate calculation based on VOX-specific economics

### ARPU Glide Path (Jun → Dec 2025)
```
Jun: $10.54
Jul: $11.17  (+6.0%)
Aug: $11.84  (+6.0%)
Sep: $12.55  (+6.0%)
Oct: $13.31  (+6.0%)
Nov: $14.10  (+6.0%)
Dec: $14.95  (+6.0%)

Total: +41.84% over 6 months
```

---

## Seasonal Adjustments

### Methodology: Data-Driven Pattern Analysis

We analyze **multi-year historical patterns** to identify consistent seasonal trends, excluding outliers.

### December Seasonality

**Historical Analysis:**
| Year | Nov Spend | Dec Spend | Growth % | Pattern |
|------|-----------|-----------|----------|---------|
| 2023 | $2.48M | $4.61M | +85.6% | 🚫 Outlier (anomaly) |
| 2024 | $4.12M | $4.33M | +5.1% | ✅ Normal pattern |

**Decision:** Use **+5.1%** based on 2024 (most recent, non-outlier data)

### Seasonal Adjustment Application

**November 2025:**
```
Base Forecast: $4.61M
Seasonal Factor: +30.5% (historical Nov pattern)
Adjusted: $4.61M × 1.305 = $6.01M
```

**December 2025:**
```
Base Forecast: $4.84M
Seasonal Factor: +5.1% (2024 Dec pattern)
Adjusted: $4.84M × 1.051 = $5.09M
```

### Why Not Use 2023's +85.6%?

1. **Statistical Outlier**: 85.6% is far outside normal variance
2. **One-Time Event**: Likely caused by specific 2023 factors
3. **Not Repeatable**: 2024 returned to normal (+5.1%)
4. **Defensibility**: 5.1% is justifiable; 85.6% is not

---

## Compound Growth Formulas

### General Formula
```
Future Value = Present Value × (1 + growth_rate)^periods
```

### Reverse Calculation (Find Required Growth Rate)
```
growth_rate = (Future Value ÷ Present Value)^(1/periods) - 1
```

**Example: What growth rate do we need to hit $12.94M from $10.34M in 3 months?**
```
growth_rate = ($12.94M ÷ $10.34M)^(1/3) - 1
growth_rate = (1.2514)^0.3333 - 1
growth_rate = 1.0776 - 1
growth_rate = 0.0776 = 7.76% monthly
```

### Total Compound Growth Over Period
```
Total Growth % = [(1 + monthly_rate)^months - 1] × 100%
```

**Example: 6% monthly over 6 months:**
```
Total Growth = [(1.06)^6 - 1] × 100%
Total Growth = [1.4185 - 1] × 100%
Total Growth = 41.85%
```

### Key Growth Rates Used

| Metric | Monthly | 6-Month Total | Formula |
|--------|---------|---------------|---------|
| **Spend** | 6.0% | 41.85% | `(1.06)^6 - 1` |
| **Users** | 4.0% | 26.53% | `(1.04)^6 - 1` |
| **ARPU** | 6.0% | 41.85% | `(1.06)^6 - 1` |
| **Churn** | -3.5% | -19.25% | `(0.965)^6 - 1` |

---

## Data Validation Rules

### Pre-Update Checklist

Before updating forecasts for Jan-Jun 2026, validate:

#### ✅ Data Accuracy
- [ ] All actuals match source data (finance system, analytics)
- [ ] VOX-Network_Partner_2 and core business properly separated
- [ ] No duplicate entries or missing months
- [ ] User counts match active user definitions

#### ✅ Calculation Consistency
- [ ] ARPU calculated via compound growth (not Spend/Users)
- [ ] Seasonal adjustments based on most recent non-outlier year
- [ ] Compound growth formulas applied correctly
- [ ] Targets independent of VOX-Network_Partner_2 performance

#### ✅ Business Logic
- [ ] Core business growth rates realistic (4-6% monthly)
- [ ] VOX-Network_Partner_2 projections anchored to actual performance
- [ ] Combined metrics = Core + VOX (not inflated)
- [ ] Stretch percentages reasonable (5-10%)

#### ✅ Dashboard Alignment
- [ ] All tiles show consistent December values
- [ ] Charts display correct data series
- [ ] Tables match JavaScript arrays
- [ ] Methodology text reflects current calculations

### Validation Formulas

**Test: Core Business December 2025**
```
Expected Spend:  $5.94M = $4.19M × (1.06)^6
Expected Users:  32,674 = 25,823 × (1.04)^6
Expected ARPU:   $14.95 = $10.54 × (1.06)^6

If actual values differ by >1%, investigate discrepancy.
```

**Test: Combined December 2025**
```
Expected Combined Spend = Core + VOX
$12.94M = $5.94M + $7.00M ✅

If doesn't match, check:
- Core business calculation
- VOX-Network_Partner_2 forecast
- Addition logic
```

### Common Errors to Avoid

❌ **Using Spend/Users for ARPU**  
✅ Use compound growth formula

❌ **Applying 2023's 85.6% seasonal factor**  
✅ Use 2024's 5.1% (recent, non-outlier)

❌ **Inflating core targets based on VOX-Network_Partner_2**  
✅ Keep streams independent

❌ **Forgetting to compound growth rates**  
✅ Use `(1 + rate)^periods`, not `rate × periods`

❌ **Inconsistent data across dashboard components**  
✅ Update all tiles, tables, and charts together

---

## Update Cadence

### Monthly Review (Required)
- Update actuals in CSV
- Compare forecast vs. actual
- Adjust next month's projection if needed

### Quarterly Deep Dive (Recommended)
- Validate growth rate assumptions
- Review seasonal factor accuracy
- Assess VOX-Network_Partner_2 market share trends
- Recalibrate 6-month forecasts

### Annual Strategy Review
- Set new annual targets
- Update compound growth rates
- Refresh historical seasonal patterns
- Document methodology changes

---

## Formula Quick Reference

```javascript
// Core Business Spend
spend_target = 4.19 * Math.pow(1.06, months);

// Core Business Users
users_target = 25823 * Math.pow(1.04, months);

// Core Business ARPU
arpu = 10.54 * Math.pow(1.06, months);

// Seasonal Adjustment (December)
adjusted_spend = base_spend * 1.051;

// Target Stretch Percentage
stretch_pct = ((target - forecast) / forecast) * 100;

// VOX Market Share
vox_share = (vox_spend / total_spend) * 100;

// Required Growth Rate (reverse calculation)
required_rate = Math.pow(target / current, 1 / months) - 1;
```

---

## Change Log

| Date | Version | Change | Reason |
|------|---------|--------|--------|
| Oct 2025 | 2.0 | Changed "Baseline" to "Core Business" | Clarify terminology (not baseline vs. enhanced) |
| Oct 2025 | 1.9 | ARPU growth rate 8.5% → 6% | Align with spend growth methodology |
| Oct 2025 | 1.8 | Seasonal adjustment 31% → 5.1% | Use 2024 pattern vs. 2023 outlier |
| Oct 2025 | 1.7 | Fixed ARPU calculation method | Compound growth vs. Spend/Users ratio |
| Sep 2025 | 1.6 | Integrated VOX-Network_Partner_2 actuals | Aug $1.46M, Sep $5.49M confirmed |

---

**Last Updated:** October 2025  
**Next Review:** January 2026 (Jan-Jun 2026 update)  
**Owner:** Pokitpal Analytics Team
