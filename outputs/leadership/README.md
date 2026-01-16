# Leadership Dashboard & Analytics

This folder contains all leadership-focused dashboards, analysis scripts, and documentation for executive reporting.

## 📁 Folder Structure

### `/dashboards` - Executive Dashboards
- **Leadership_Presentation_Nov2025.html** - Current executive dashboard (November 2025)
  - Performance trends with historical data, forecasts, and targets
  - GMV and User metrics with VOX-ING breakdown
  - SPLY (Same Period Last Year) analysis with holiday surge insights
  - Merchant performance tables (Top 10 GMV, Material Declines)
  - Fully interactive, standalone HTML file
  
- **Merchant_Variance_Dashboard.html** - Merchant and network variance analysis
  
- **Legacy dashboards** - Previous versions for reference

### `/analysis` - Analysis Scripts
- **sply_analysis.py** - Year-over-year comparison analysis
  - Calculates Nov-Dec holiday surge patterns
  - Projects transaction volumes and operational readiness metrics
  - Generates insights for leadership presentations

### `/documentation` - Documentation & Methodology
- **FORECAST_METHODOLOGY.md** - Forecasting approach and calculations
- **LEADERSHIP_DASHBOARD_SUMMARY.md** - Dashboard features and metrics explained
- **PORTFOLIO_SUMMARY.md** - Portfolio overview and key insights
- **UPDATE_GUIDE.md** - How to update dashboards with new data

## 🚀 Quick Start

### Viewing Dashboards
1. Navigate to `/dashboards`
2. Double-click `Leadership_Presentation_Nov2025.html`
3. Opens in your browser - fully interactive, no server needed

### Sharing Dashboards
- Email the HTML file directly to stakeholders
- Upload to OneDrive/SharePoint for team access
- No installation or dependencies required for viewers

### Updating Data
1. New month data arrives → Update SQLite database (`pokitpal_historical_data.db`)
2. Run queries to get updated metrics
3. Update HTML arrays with new values
4. See `UPDATE_GUIDE.md` for detailed steps

## 📊 Current Dashboard Metrics (November 2025)

**October 2025 Performance:**
- GMV: $4.44M organic + $3.98M VOX-ING = $8.42M total
- Users: 25.37K organic + 25.40K VOX-ING = 50.77K total

**Nov-Dec 2025 Forecast:**
- Nov: $10M GMV (57K users) - +19% GMV, +12% users from October
- Dec: $11M GMV (60K users) - +10% GMV, +5% users from November
- Holiday surge pattern applied based on 2024 SPLY analysis

**Key Features:**
- ✅ VOX-ING contribution tracked separately
- ✅ Organic vs partnership growth clearly distinguished
- ✅ Material merchant declines identified (50+ txns, 30%+ decline)
- ✅ Holiday surge projections with operational readiness metrics
- ✅ BWS merchants excluded from performance tables

## 🔗 Data Sources

All dashboards pull from: `../pokitpal_historical_data.db`
- Historical transactions: Jan-Oct 2025
- Network breakdowns (Organic, VOX-ING)
- Merchant performance data
- Monthly aggregated metrics

## 📝 Notes

- Dashboards are self-contained HTML files with embedded data
- No external dependencies or API calls
- All data is embedded at build time
- For live data updates, regenerate HTML with fresh database queries
