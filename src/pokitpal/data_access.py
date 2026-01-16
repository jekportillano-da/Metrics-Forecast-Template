"""
PokitPal Historical Data Access Module
====================================

This module provides easy access to the consolidated historical database.
All analysis scripts should use this module instead of reading CSV files directly.
"""

import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import os

# Database path relative to this module
MODULE_DIR = Path(__file__).parent
DEFAULT_DB_PATH = MODULE_DIR.parent.parent / 'data' / 'processed' / 'pokitpal_historical_data.db'

class PokitPalData:
    """Main class for accessing PokitPal historical data"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or DEFAULT_DB_PATH
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database not found: {self.db_path}")
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def get_transactions(self, start_date=None, end_date=None, user_network=None, merchant=None):
        """Get transaction data with optional filters"""
        query = "SELECT * FROM transactions WHERE 1=1"
        params = []
        
        if start_date:
            query += " AND [Transaction Date] >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND [Transaction Date] <= ?"
            params.append(end_date)
        
        if user_network:
            query += " AND [User Network] = ?"
            params.append(user_network)
        
        if merchant:
            query += " AND Merchant = ?"
            params.append(merchant)
        
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn, params=params)
    
    def get_monthly_summary(self):
        """Get monthly aggregated data"""
        with self.get_connection() as conn:
            return pd.read_sql_query("SELECT * FROM monthly_summary ORDER BY month", conn)
    
    def get_forecast_data(self):
        """Get forecast data"""
        with self.get_connection() as conn:
            return pd.read_sql_query("SELECT * FROM forecast_data", conn)
    
    def get_network_performance(self, month=None):
        """Get user network performance data"""
        if month:
            query = """
            SELECT [User Network] as User_Network, 
                   SUM(Amount) as total_spend,
                   COUNT(DISTINCT Email) as unique_users,
                   COUNT(*) as transaction_count,
                   AVG(Amount) as avg_transaction_value
            FROM transactions 
            WHERE strftime('%Y-%m', [Transaction Date]) = ?
            GROUP BY [User Network] 
            ORDER BY total_spend DESC
            """
            with self.get_connection() as conn:
                return pd.read_sql_query(query, conn, params=[month])
        else:
            query = """
            SELECT [User Network] as User_Network, 
                   SUM(Amount) as total_spend,
                   COUNT(DISTINCT Email) as unique_users,
                   COUNT(*) as transaction_count,
                   AVG(Amount) as avg_transaction_value
            FROM transactions 
            GROUP BY [User Network] 
            ORDER BY total_spend DESC
            """
            with self.get_connection() as conn:
                return pd.read_sql_query(query, conn)
    
    def get_merchant_performance(self, month=None):
        """Get merchant performance data"""
        if month:
            query = """
            SELECT Merchant, 
                   SUM(Amount) as total_spend,
                   COUNT(DISTINCT Email) as unique_users,
                   COUNT(*) as transaction_count
            FROM transactions 
            WHERE strftime('%Y-%m', [Transaction Date]) = ?
            GROUP BY Merchant 
            ORDER BY total_spend DESC
            """
            with self.get_connection() as conn:
                return pd.read_sql_query(query, conn, params=[month])
        else:
            query = """
            SELECT Merchant, 
                   SUM(Amount) as total_spend,
                   COUNT(DISTINCT Email) as unique_users,
                   COUNT(*) as transaction_count
            FROM transactions 
            GROUP BY Merchant 
            ORDER BY total_spend DESC
            """
            with self.get_connection() as conn:
                return pd.read_sql_query(query, conn)

# Convenience functions
def get_data():
    """Get a PokitPalData instance"""
    return PokitPalData()

def quick_monthly_stats():
    """Get quick monthly statistics"""
    data = get_data()
    return data.get_monthly_summary()

def latest_month_performance():
    """Get latest month performance data"""
    data = get_data()
    monthly = data.get_monthly_summary()
    if len(monthly) > 0:
        latest_month = monthly.iloc[-1]['month']
        return {
            'month': latest_month,
            'networks': data.get_network_performance(latest_month),
            'merchants': data.get_merchant_performance(latest_month)
        }
    return None
