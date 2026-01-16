# Quick Setup Guide

## Test Script Functionality

After restructuring, verify everything works:

### 1. Test Database Connection
```python
import sys
sys.path.insert(0, 'src')

from pokitpal.data_access import PokitPalData

# Initialize data access
data = PokitPalData()

# Test connection
conn = data.get_connection()
print("✅ Database connection successful!")

# Quick query
import pandas as pd
result = pd.read_sql_query("SELECT COUNT(*) as total FROM transactions", conn)
print(f"✅ Total transactions: {result['total'][0]:,}")

conn.close()
```

### 2. Run Forecast Script
```bash
cd scripts
python create_forecast_2026.py
```

### 3. View Dashboard
- Navigate to `outputs/leadership/dashboards/`
- Open `Leadership_Presentation_Nov2025.html` in browser

## Repository Initialization

```bash
# Initialize git (if not already initialized)
git init

# Check .gitignore is working
git status
# Should NOT see data/processed/ or *.db files

# Add files
git add .
git commit -m "Initial commit: Professional portfolio structure"

# Create GitHub repo and push
git remote add origin https://github.com/yourusername/pokitpal-metrics.git
git branch -M main
git push -u origin main
```

## Customization Checklist

Before pushing to GitHub:

- [ ] Update README.md contact information
- [ ] Add your name to LICENSE file
- [ ] Verify .gitignore excludes sensitive data
- [ ] Test all scripts still run correctly
- [ ] Add screenshots to README (optional)
- [ ] Review docs/ folder for any sensitive information
- [ ] Update repository name/URL in README

## Portfolio Presentation Tips

**Highlight:**
- Clean, professional folder structure
- Comprehensive documentation
- Production-ready code with error handling
- Data privacy considerations (git ignore strategy)
- Time series forecasting expertise
- Business intelligence dashboards

**GitHub Repository Settings:**
- Add topics: `python`, `data-analytics`, `forecasting`, `sqlite`, `business-intelligence`
- Add a description: "Professional financial analytics platform with time-series forecasting and executive dashboards"
- Pin to your profile for visibility
