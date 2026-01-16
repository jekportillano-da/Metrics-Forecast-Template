# 📊 PokitPal Metrics & Forecasting Platform

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Status](https://img.shields.io/badge/Status-Production-success)
![License](https://img.shields.io/badge/License-MIT-green)
![Data Coverage](https://img.shields.io/badge/Data%20Coverage-Jun%202023--Dec%202025-orange)

> **Professional financial analytics and forecasting system** for transaction data analysis, featuring automated ETL pipelines, time-series forecasting with exponential smoothing, and interactive executive dashboards.

---

## 🎯 Project Overview

A comprehensive data analytics platform built for analyzing **450K+ financial transactions** spanning 30 months, providing executive insights through automated forecasting models and interactive visualizations. The system handles merchant performance analysis, network attribution, and predictive modeling with Australian market seasonality.

### Key Features
- ✅ **Automated ETL Pipeline** - Transaction ingestion with validation and deduplication
- ✅ **Time Series Forecasting** - Holt-Winters exponential smoothing with seasonal adjustment
- ✅ **Executive Dashboards** - Interactive HTML dashboards for leadership reporting
- ✅ **Merchant Analytics** - Deep-dive analysis on merchant performance (BWS, Petbarn)
- ✅ **Network Attribution** - VOX-ING integration tracking and analysis
- ✅ **Data Privacy** - Database git-ignored for security compliance

---

## 📁 Repository Structure

```
pokitpal-metrics/
│
├── src/pokitpal/              # Core Python package
│   ├── data_access.py         # Database interface and query layer
│   └── __init__.py
│
├── scripts/                   # Analysis and ETL scripts
│   ├── create_forecast_2026.py       # Main forecasting pipeline
│   ├── merchant_analysis.py          # Merchant performance analysis
│   └── analysis/
│       └── bws_petbarn/              # BWS/Petbarn specific scripts
│
├── data/
│   ├── raw/                   # Source CSV files (git tracked)
│   └── processed/             # SQLite database (git ignored)
│       └── pokitpal_historical_data.db
│
├── docs/                      # Documentation and reports
│   ├── BWS_PETBARN_ANALYSIS_REPORT.md
│   └── BWS_PETBARN_QUICK_REFERENCE.md
│
├── outputs/                   # Analysis outputs
│   ├── leadership/            # Executive dashboards
│   │   ├── dashboards/        # HTML interactive dashboards
│   │   ├── analysis/          # SPLY and forecast scripts
│   │   └── documentation/     # Methodology guides
│   └── VOX_Integration_Results/  # VOX-ING analysis
│
├── requirements.txt           # Python dependencies
├── .gitignore                # Comprehensive ignore rules
└── README.md                 # This file
```

---

## 🗄️ Database Architecture

**Technology Stack:** SQLite 3  
**Total Records:** 454,515 transactions  
**Date Range:** July 2025 - December 2025 (with historical aggregates from June 2023)

### Schema Design

#### `transactions` Table
Raw transaction-level data with full attribution
- **Columns:** Transaction Date, Amount, User ID, Merchant, Category, Network, State
- **Size:** 454K+ rows
- **Indexes:** Date, User ID, Merchant for query optimization

#### `forecast_2026` Table  
Consolidated forecasting table with actuals and projections
- **Date Range:** June 2023 - December 2026 (43 months)
- **Columns:** Month, Spend, Spend Growth, Cashback, Users, ARPU, Churn
- **Actuals:** Jul-Dec 2025 derived from transactions
- **Forecasts:** Jan-Dec 2026 using exponential smoothing

#### Additional Tables
- `forecast_data` - Legacy forecast storage
- `monthly_summary` - Pre-aggregated monthly metrics
- `baseline_spend` - Historical baseline calculations

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.13+
pip install -r requirements.txt
```

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/pokitpal-metrics.git
cd pokitpal-metrics

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Unix

# Install dependencies
pip install -r requirements.txt
```

### Running Analysis

#### 1. Generate 2026 Forecast
```bash
python scripts/create_forecast_2026.py
```
**Output:** Updates `forecast_2026` table with latest actuals and projections

#### 2. Merchant Performance Analysis
```bash
python scripts/merchant_analysis.py
```
**Output:** Merchant-level insights and trend analysis

#### 3. View Executive Dashboard
```bash
# Navigate to outputs/leadership/dashboards/
# Open Leadership_Presentation_Nov2025.html in browser
```
**Features:** Interactive charts, YoY comparisons, network breakdowns

---

## 📊 Forecasting Methodology

### Model: Holt-Winters Exponential Smoothing
- **Seasonality:** 12-month period (additive)
- **Trend Component:** Additive linear trend
- **Australian Market Factors:** Monthly adjustment dictionary
  - Peak: December (1.12x), November (1.08x) - Summer/Christmas season
  - Low: April (0.95x), May (0.96x) - Autumn slowdown

### Workflow
1. **Data Extraction** - Query transactions table for latest actuals
2. **Historical Analysis** - Load Jun 2023-Jun 2025 baseline data
3. **Model Training** - Fit exponential smoothing on historical patterns
4. **Seasonal Adjustment** - Apply Australian market multipliers
5. **Projection Generation** - Forecast Jan-Dec 2026 metrics
6. **Database Update** - Write results to forecast_2026 table

### Metrics Forecasted
- 💰 **Spend** - Total transaction volume
- 🎁 **Cashback** - Rewards paid to users
- 💵 **Fees** - Merchant processing fees
- 👥 **Active Users** - Monthly unique users
- 📉 **Churn** - 45-day inactive users
- 💎 **ARPU** - Average revenue per user

---

## 🔍 Key Analyses

### 1. BWS/Petbarn Merchant Deep-Dive
**Location:** [scripts/analysis/bws_petbarn/](scripts/analysis/bws_petbarn/)  
**Reports:** [docs/BWS_PETBARN_ANALYSIS_REPORT.md](docs/BWS_PETBARN_ANALYSIS_REPORT.md)

- Variant performance comparison (cashback tiers)
- Offer pause impact analysis
- VOX-ING network exclusion studies

### 2. VOX Integration Impact
**Location:** [outputs/VOX_Integration_Results/](outputs/VOX_Integration_Results/)  
**Key Finding:** Network attribution and spend correlation

### 3. Leadership Reporting
**Location:** [outputs/leadership/](outputs/leadership/)  
**Dashboard:** Monthly performance vs. targets with SPLY comparison

---

## 📈 Sample Results (2025 Actuals)

| Metric | Jul 2025 | Dec 2025 | Growth |
|--------|----------|----------|--------|
| **Spend** | $9.8M | $8.5M* | -13% |
| **Users** | 62,518 | 56,489* | -10% |
| **Cashback** | $488K | $382K* | -22% |
| **ARPU** | $156 | $151* | -3% |

*December 2025 data incomplete (55% of expected volume)

### 2026 Forecast Summary
- **Total Spend:** $117.6M (+68% vs 2025)
- **Peak Month:** December 2026 ($11.2M)
- **Average Users:** 65K/month
- **Total Cashback:** $5.3M

---

## 🛡️ Data Privacy & Security

### Git Ignore Strategy
```gitignore
# Sensitive transaction data excluded
data/processed/              # Entire database folder
*.db
*.sqlite

# Aggregate data and scripts are tracked
# Raw CSVs excluded by default (uncomment if sensitive)
```

### Rationale
- ✅ **Code & Analysis Scripts** - Tracked for portfolio demonstration
- ✅ **Documentation & Reports** - Tracked (no PII)
- ✅ **Dashboard Templates** - Tracked (visualization code only)
- ❌ **Raw Transactions** - Git ignored (contains user-level data)
- ❌ **Database Files** - Git ignored (sensitive information)

---

## 🧪 Testing & Validation

### Data Quality Checks
- Transaction state validation (Cleared, Pending, Cancelled)
- Date format consistency (DD/MM/YYYY for new data)
- Amount parsing (handles $ symbols, negatives)
- Deduplication on import

### Forecast Validation
- Historical backtest accuracy
- Seasonal factor verification against market trends
- Growth rate sanity checks

---

## 🤝 Contributing

This is a portfolio project demonstrating professional data analytics capabilities. While not actively seeking contributions, feedback and suggestions are welcome via Issues.

---

## 📧 Contact

**Developer:** [Your Name]  
**Portfolio:** [Your Website]  
**LinkedIn:** [Your LinkedIn]  
**Email:** [Your Email]

---

## 📜 License

MIT License - See LICENSE file for details

---

## 🏆 Skills Demonstrated

This project showcases expertise in:

- **Data Engineering:** ETL pipeline design, SQLite optimization, data validation
- **Statistical Modeling:** Time series forecasting, exponential smoothing, seasonal decomposition
- **Business Intelligence:** Executive dashboard design, KPI tracking, variance analysis
- **Python Development:** Clean architecture, modular design, package structure
- **Data Visualization:** Interactive HTML dashboards, trend analysis, comparative reporting
- **Documentation:** Technical writing, methodology documentation, knowledge transfer
- **Version Control:** Git workflow, professional repository structure, sensitive data handling

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Built with ❤️ and Python | © 2025

</div>
