#!/usr/bin/env python3
"""
Merchant Performance Analysis - August to September 2025
Loads large CSV into SQLite for efficient analysis
Analyzes merchant-wise performance excluding User Network ING and EML
Focus: Aug-Sep variance analysis for actionable insights
"""

import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime
from pathlib import Path
import os
import warnings
warnings.filterwarnings('ignore')

# Get database path relative to script location
SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR.parent / 'data' / 'processed' / 'pokitpal_historical_data.db'

def load_csv_to_sqlite(csv_file, db_file="transactions.db", table_name="transactions", chunk_size=10000):
    """Load large CSV file into SQLite database in chunks"""
    print(f"📊 Loading {csv_file} into SQLite database...")
    
    # Remove existing database if it exists
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"🗑️ Removed existing database: {db_file}")
    
    # Create connection
    conn = sqlite3.connect(db_file)
    
    try:
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        successful_encoding = None
        
        for encoding in encodings:
            try:
                # Test read first chunk to verify encoding works
                test_chunk = pd.read_csv(csv_file, nrows=1000, encoding=encoding, low_memory=False)
                successful_encoding = encoding
                print(f"✅ Successfully verified {encoding} encoding with {len(test_chunk)} test rows")
                break
            except (UnicodeDecodeError, Exception) as e:
                print(f"❌ Failed with {encoding} encoding: {str(e)[:100]}")
                continue
        
        if successful_encoding is None:
            raise Exception("Could not decode file with any encoding")
        
        # Read CSV in chunks and load to SQLite with error handling
        chunk_count = 0
        total_rows = 0
        error_count = 0
        
        try:
            chunk_iterator = pd.read_csv(csv_file, chunksize=chunk_size, encoding=successful_encoding, 
                                       low_memory=False, encoding_errors='replace')
            
            for chunk in chunk_iterator:
                try:
                    chunk_count += 1
                    chunk_rows = len(chunk)
                    total_rows += chunk_rows
                    
                    # Clean column names (remove spaces, special chars)
                    chunk.columns = [col.strip().replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '') 
                                   for col in chunk.columns]
                    
                    # Exclude unnecessary columns
                    exclude_columns = [
                        'Store', 'Applied_Rule', 'Age', 'Transaction_Reason', 
                        'Transaction_Auth_Code', 'StoreId', 'Transaction_LastFourDigits', 
                        'First_Transaction'
                    ]
                    
                    # Remove excluded columns if they exist
                    columns_to_keep = [col for col in chunk.columns if col not in exclude_columns]
                    chunk_filtered = chunk[columns_to_keep]
                    
                    print(f"  Chunk {chunk_count}: {len(chunk.columns)} -> {len(chunk_filtered.columns)} columns")
                    
                    # Load chunk to SQLite
                    chunk_filtered.to_sql(table_name, conn, if_exists='append', index=False)
                    
                    if chunk_count % 5 == 0:  # Progress update every 5 chunks
                        print(f"  Processed {chunk_count} chunks ({total_rows:,} rows)")
                        
                except Exception as chunk_error:
                    error_count += 1
                    print(f"  ⚠️ Error in chunk {chunk_count}: {str(chunk_error)[:100]}")
                    if error_count > 10:  # Too many errors
                        raise Exception("Too many chunk processing errors")
                    continue
                    
        except Exception as read_error:
            print(f"❌ Error during chunk reading: {read_error}")
            # Try alternative approach with different parameters
            print("🔄 Trying alternative reading approach...")
            try:
                # Read with latin-1 and error replacement
                chunk_iterator = pd.read_csv(csv_file, chunksize=chunk_size, encoding='latin-1', 
                                           low_memory=False, on_bad_lines='skip')
                
                for chunk in chunk_iterator:
                    chunk_count += 1
                    chunk_rows = len(chunk)
                    total_rows += chunk_rows
                    
                    # Clean column names
                    chunk.columns = [col.strip().replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '') 
                                   for col in chunk.columns]
                    
                    # Exclude unnecessary columns
                    exclude_columns = [
                        'Store', 'Applied_Rule', 'Age', 'Transaction_Reason', 
                        'Transaction_Auth_Code', 'StoreId', 'Transaction_LastFourDigits', 
                        'First_Transaction'
                    ]
                    
                    # Remove excluded columns if they exist
                    columns_to_keep = [col for col in chunk.columns if col not in exclude_columns]
                    chunk_filtered = chunk[columns_to_keep]
                    
                    if chunk_count == 1:
                        print(f"  Excluded columns: {[col for col in exclude_columns if col in chunk.columns]}")
                    
                    # Load chunk to SQLite
                    chunk_filtered.to_sql(table_name, conn, if_exists='append', index=False)
                    
                    if chunk_count % 5 == 0:
                        print(f"  Processed {chunk_count} chunks ({total_rows:,} rows)")
                        
            except Exception as final_error:
                raise Exception(f"All reading approaches failed: {final_error}")
        
        print(f"✅ Successfully loaded {total_rows:,} rows into {db_file}")
        
        # Get table info
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"📋 Columns in database: {len(columns)}")
        for i, col in enumerate(columns[:10]):  # Show first 10 columns
            print(f"  {i+1}. {col}")
        if len(columns) > 10:
            print(f"  ... and {len(columns) - 10} more columns")
        
        return conn, columns
        
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        conn.close()
        return None, []

def identify_columns(columns):
    """Identify relevant columns for analysis"""
    print("🔍 Identifying relevant columns...")
    
    # Common patterns for key columns
    patterns = {
        'merchant': ['merchant', 'publisher', 'partner', 'network', 'provider'],
        'amount': ['amount', 'value', 'revenue', 'gmv', 'total'],
        'user': ['user', 'customer', 'client'],
        'transaction': ['transaction', 'txn', 'id'],
        'date': ['date', 'time', 'created', 'timestamp']
    }
    
    found_columns = {}
    
    for key, keywords in patterns.items():
        for col in columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in keywords):
                found_columns[key] = col
                print(f"  {key.upper()}: {col}")
                break
        
        if key not in found_columns:
            print(f"  {key.upper()}: Not found")
    
    return found_columns

def analyze_merchants_sql(conn, table_name, column_mapping, exclude_merchants=['User Network ING', 'EML']):
    """Perform merchant analysis using SQL queries"""
    print("🧮 Analyzing merchant performance with SQL...")
    
    merchant_col = column_mapping.get('merchant')
    amount_col = column_mapping.get('amount')
    user_col = column_mapping.get('user')
    date_col = column_mapping.get('date')
    txn_col = column_mapping.get('transaction', merchant_col)  # Fallback to merchant col
    
    if not merchant_col or not amount_col or not date_col:
        print("❌ Critical columns not found. Cannot proceed with analysis.")
        print(f"   Merchant: {merchant_col}, Amount: {amount_col}, Date: {date_col}")
        return None
    
    # First, let's check what merchants we have
    check_query = f"SELECT DISTINCT {merchant_col}, COUNT(*) as count FROM {table_name} GROUP BY {merchant_col} ORDER BY count DESC LIMIT 20"
    check_df = pd.read_sql_query(check_query, conn)
    print(f"📋 Top 20 merchants in data:")
    for _, row in check_df.iterrows():
        print(f"  {row[merchant_col]}: {row['count']:,} transactions")
    
    # Build exclusion clause - use LIKE patterns for ING and EML networks + date filtering
    exclude_conditions = []
    
    # Exclude ING and EML networks from User_Network column (the actual data shows VOX - ING and EML Offline)
    if user_col:
        exclude_conditions.append(f"{user_col} LIKE '%ING%'")
        exclude_conditions.append(f"{user_col} LIKE '%EML%'")
    
    # Also exclude from Merchant column if needed
    if exclude_merchants:
        merchant_exclusions = ' OR '.join([f"{merchant_col} LIKE '%{merchant}%'" for merchant in exclude_merchants])
        if merchant_exclusions:
            exclude_conditions.append(f"({merchant_exclusions})")
    
    # Date filtering: Include only August and September 2025
    date_conditions = [
        f"({date_col} LIKE '%/08/%' OR {date_col} LIKE '%08-%' OR {date_col} LIKE '%-08-%')",  # August
        f"({date_col} LIKE '%/09/%' OR {date_col} LIKE '%09-%' OR {date_col} LIKE '%-09-%')"   # September
    ]
    
    exclude_clause = ""
    where_parts = []
    
    # Add network/merchant exclusions
    if exclude_conditions:
        where_parts.append(f"NOT ({' OR '.join(exclude_conditions)})")
    
    # Add date inclusion (August OR September)
    where_parts.append(f"({' OR '.join(date_conditions)})")
    
    if where_parts:
        exclude_clause = f"WHERE {' AND '.join(where_parts)}"
    
    print(f"🔍 Exclusion clause: {exclude_clause}")
    
    # Test the exclusion to see how many records remain
    test_query = f"SELECT COUNT(*) as remaining FROM {table_name} {exclude_clause}"
    test_result = pd.read_sql_query(test_query, conn)
    remaining_count = test_result['remaining'].iloc[0]
    print(f"📊 Records remaining after exclusions: {remaining_count:,} (excluded: {224876 - remaining_count:,})")
    
    # Main analysis query - clean Amount column by removing $ and converting to numeric
    query = f"""
    SELECT 
        {merchant_col} as merchant,
        COUNT(*) as transaction_count,
        SUM(CAST(REPLACE(REPLACE({amount_col}, '$', ''), ',', '') AS REAL)) as total_revenue,
        AVG(CAST(REPLACE(REPLACE({amount_col}, '$', ''), ',', '') AS REAL)) as avg_transaction_value,
        MIN(CAST(REPLACE(REPLACE({amount_col}, '$', ''), ',', '') AS REAL)) as min_transaction,
        MAX(CAST(REPLACE(REPLACE({amount_col}, '$', ''), ',', '') AS REAL)) as max_transaction,
        {f"COUNT(DISTINCT {user_col}) as unique_users," if user_col else ""}
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM {table_name} {exclude_clause}) as transaction_share
    FROM {table_name}
    {exclude_clause}
    GROUP BY {merchant_col}
    HAVING total_revenue > 0
    ORDER BY total_revenue DESC
    """
    
    print(f"📊 Executing analysis query...")
    print(f"🔍 Query: {query}")
    
    try:
        df = pd.read_sql_query(query, conn)
        
        # Calculate additional metrics
        total_revenue = df['total_revenue'].sum()
        df['revenue_share'] = (df['total_revenue'] / total_revenue) * 100
        
        if 'unique_users' in df.columns:
            df['revenue_per_user'] = df['total_revenue'] / df['unique_users']
        
        print(f"✅ Analysis complete for {len(df)} merchants")
        return df
        
    except Exception as e:
        print(f"❌ SQL query error: {e}")
        return None

def generate_insights_and_recommendations(df):
    """Generate actionable insights from merchant analysis"""
    print("\n💡 GENERATING INSIGHTS & RECOMMENDATIONS")
    print("=" * 50)
    
    insights = []
    recommendations = []
    
    # Basic stats
    total_merchants = len(df)
    total_revenue = df['total_revenue'].sum()
    total_transactions = df['transaction_count'].sum()
    
    print(f"📊 OVERVIEW:")
    print(f"  • Total Merchants: {total_merchants:,}")
    print(f"  • Total GMV (Merchant Sales): ${total_revenue:,.2f}")
    print(f"  • Total Transactions: {total_transactions:,}")
    if total_merchants > 0:
        print(f"  • Average GMV per Merchant: ${total_revenue/total_merchants:,.2f}")
    else:
        print("  • No merchants found after exclusions - check exclusion criteria")
        return df
    print(f"  • Note: PokitPal Revenue = Cashback + Fees (calculated separately)")
    
    # Top performers analysis
    top_10_revenue = df.head(10)
    print(f"\n🏆 TOP 10 GMV PERFORMERS (Merchant Sales Volume):")
    print("-" * 60)
    for i, row in top_10_revenue.iterrows():
        print(f"{i+1:2d}. {row['merchant']:<35} ${row['total_revenue']:>12,.2f} ({row['revenue_share']:.1f}%)")
    
    # Bottom performers
    bottom_10 = df.tail(10)
    print(f"\n📉 BOTTOM 10 REVENUE PERFORMERS:")
    print("-" * 60)
    for i, row in bottom_10.iterrows():
        pos = len(df) - len(bottom_10) + list(bottom_10.index).index(i) + 1
        print(f"{pos:2d}. {row['merchant']:<35} ${row['total_revenue']:>12,.2f} ({row['revenue_share']:.1f}%)")
    
    # Transaction volume leaders
    top_volume = df.nlargest(10, 'transaction_count')
    print(f"\n🎯 TOP 10 TRANSACTION VOLUME:")
    print("-" * 60)
    for i, row in top_volume.iterrows():
        print(f"{list(top_volume.index).index(i)+1:2d}. {row['merchant']:<35} {row['transaction_count']:>8,} txns ({row['transaction_share']:.1f}%)")
    
    # High-value transaction merchants
    top_avg_value = df.nlargest(10, 'avg_transaction_value')
    print(f"\n💎 TOP 10 AVERAGE TRANSACTION VALUE:")
    print("-" * 60)
    for i, row in top_avg_value.iterrows():
        print(f"{list(top_avg_value.index).index(i)+1:2d}. {row['merchant']:<35} ${row['avg_transaction_value']:>10.2f}")
    
    # Market concentration analysis
    top_5_share = top_10_revenue.head(5)['revenue_share'].sum()
    top_20_pct_merchants = int(total_merchants * 0.2)
    top_20_pct_share = df.head(top_20_pct_merchants)['revenue_share'].sum()
    
    print(f"\n📈 MARKET CONCENTRATION ANALYSIS:")
    print(f"  • Top 5 merchants: {top_5_share:.1f}% of revenue")
    print(f"  • Top 20% merchants: {top_20_pct_share:.1f}% of revenue")
    
    # Performance segments
    high_performers = df[df['revenue_share'] >= 5.0]  # 5%+ market share
    mid_performers = df[(df['revenue_share'] >= 1.0) & (df['revenue_share'] < 5.0)]  # 1-5%
    long_tail = df[df['revenue_share'] < 1.0]  # <1%
    
    print(f"\n🎯 MERCHANT SEGMENTS:")
    print(f"  • High Performers (≥5% share): {len(high_performers)} merchants ({len(high_performers)/total_merchants*100:.1f}%)")
    print(f"  • Mid Performers (1-5% share): {len(mid_performers)} merchants ({len(mid_performers)/total_merchants*100:.1f}%)")
    print(f"  • Long Tail (<1% share): {len(long_tail)} merchants ({len(long_tail)/total_merchants*100:.1f}%)")
    
    # Generate strategic recommendations
    print(f"\n🚀 STRATEGIC RECOMMENDATIONS:")
    print("=" * 50)
    
    # 1. Revenue concentration risk
    if top_5_share > 60:
        print("1. 🔴 HIGH CONCENTRATION RISK:")
        print(f"   • Top 5 merchants control {top_5_share:.1f}% of revenue")
        print("   • RECOMMENDATION: Diversify merchant portfolio to reduce dependency")
        print("   • ACTION: Launch merchant acquisition program targeting mid-tier publishers")
    
    # 2. Long tail optimization
    if len(long_tail) > total_merchants * 0.7:
        print("2. ⚡ LONG TAIL OPTIMIZATION OPPORTUNITY:")
        print(f"   • {len(long_tail)} merchants ({len(long_tail)/total_merchants*100:.1f}%) contribute <1% each")
        print("   • RECOMMENDATION: Implement tiered account management")
        print("   • ACTION: Automated growth programs for merchants with 0.1-1% share")
    
    # 3. High-value merchant retention
    premium_threshold = df['avg_transaction_value'].quantile(0.9)
    premium_merchants = df[df['avg_transaction_value'] >= premium_threshold]
    print("3. 💎 PREMIUM MERCHANT RETENTION:")
    print(f"   • {len(premium_merchants)} merchants have top 10% transaction values (>${premium_threshold:.2f})")
    print("   • RECOMMENDATION: VIP account management program")
    print("   • ACTION: Dedicated support + custom integration for high-value merchants")
    
    # 4. Volume efficiency analysis
    high_volume_low_value = df[
        (df['transaction_count'] >= df['transaction_count'].quantile(0.8)) &
        (df['avg_transaction_value'] <= df['avg_transaction_value'].quantile(0.5))
    ]
    if len(high_volume_low_value) > 0:
        print("4. 📊 VOLUME EFFICIENCY GAINS:")
        print(f"   • {len(high_volume_low_value)} merchants have high volume but below-median transaction value")
        print("   • RECOMMENDATION: Conversion optimization programs")
        print("   • ACTION: A/B test pricing strategies and upselling campaigns")
    
    # 5. Growth opportunity identification
    growth_candidates = df[
        (df['revenue_share'] >= 0.5) & (df['revenue_share'] < 2.0) &
        (df['avg_transaction_value'] >= df['avg_transaction_value'].median())
    ]
    print("5. 🌱 GROWTH ACCELERATION TARGETS:")
    print(f"   • {len(growth_candidates)} merchants show growth potential (0.5-2% share, good avg value)")
    print("   • RECOMMENDATION: Focused growth investment program")
    print("   • ACTION: Marketing co-investment and technical optimization support")
    
    return df

def create_database_views(conn, table_name, column_mapping):
    """Create useful database views for ongoing analysis"""
    print("📊 Creating database views for ongoing analysis...")
    
    merchant_col = column_mapping.get('merchant')
    amount_col = column_mapping.get('amount')
    
    # Monthly performance view
    monthly_view = f"""
    CREATE VIEW IF NOT EXISTS monthly_merchant_performance AS
    SELECT 
        {merchant_col} as merchant,
        strftime('%Y-%m', date_column) as month,
        COUNT(*) as transactions,
        SUM(CAST({amount_col} AS REAL)) as revenue,
        AVG(CAST({amount_col} AS REAL)) as avg_value
    FROM {table_name}
    WHERE {merchant_col} NOT IN ('User Network ING', 'EML')
    GROUP BY {merchant_col}, strftime('%Y-%m', date_column)
    """
    
    # Top performers view
    top_performers_view = f"""
    CREATE VIEW IF NOT EXISTS top_merchant_performers AS
    SELECT 
        {merchant_col} as merchant,
        COUNT(*) as transaction_count,
        SUM(CAST({amount_col} AS REAL)) as total_revenue,
        AVG(CAST({amount_col} AS REAL)) as avg_transaction_value,
        RANK() OVER (ORDER BY SUM(CAST({amount_col} AS REAL)) DESC) as revenue_rank
    FROM {table_name}
    WHERE {merchant_col} NOT IN ('User Network ING', 'EML')
    GROUP BY {merchant_col}
    HAVING total_revenue > 1000
    ORDER BY total_revenue DESC
    """
    
    try:
        conn.execute(monthly_view)
        conn.execute(top_performers_view)
        conn.commit()
        print("✅ Database views created successfully")
    except Exception as e:
        print(f"⚠️ Could not create views: {e}")

def main():
    """Main analysis function"""
    print("🚀 MERCHANT PERFORMANCE ANALYSIS - SQLite Edition")
    print("=" * 60)
    
    csv_file = "July to September 2025 Transactions.csv"
    db_file = "merchant_transactions.db"
    table_name = "transactions"
    
    print("📅 Focus: August to September 2025 performance analysis")
    print("🔍 Filtering out July data for targeted Aug-Sep variance insights")
    print()
    
    # Step 1: Load CSV to SQLite
    conn, columns = load_csv_to_sqlite(csv_file, db_file, table_name)
    if not conn:
        return
    
    # Step 2: Identify relevant columns
    column_mapping = identify_columns(columns)
    
    # Step 3: Perform merchant analysis
    merchant_df = analyze_merchants_sql(conn, table_name, column_mapping)
    if merchant_df is None:
        conn.close()
        return
    
    # Step 4: Generate insights and recommendations
    results = generate_insights_and_recommendations(merchant_df)
    
    # Step 5: Create database views for ongoing analysis
    create_database_views(conn, table_name, column_mapping)
    
    # Step 6: Export results
    output_file = "merchant_performance_analysis.csv"
    merchant_df.to_csv(output_file, index=False)
    print(f"\n💾 Results exported to: {output_file}")
    print(f"🗃️ SQLite database saved as: {db_file}")
    
    # Summary statistics
    print(f"\n📋 ANALYSIS SUMMARY:")
    print(f"  Database: {db_file} ({os.path.getsize(db_file)/(1024*1024):.1f} MB)")
    print(f"  Analysis: {len(merchant_df)} merchants analyzed")
    print(f"  Period: July - September 2025")
    print(f"  Exclusions: User Network ING, EML")
    
    conn.close()
    print(f"\n🎉 Analysis Complete!")
    
    return merchant_df

if __name__ == "__main__":
    # Configure pandas display
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 35)
    
    results = main()