import pandas as pd
import os 


def get_filtered_districts(state):
    """Return districts filtered by state"""
    file_path = os.path.join('myapp', 'data', 'market_prices.csv')
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        df.columns = df.columns.str.strip().str.replace('\u200b', '').str.lower()
        
        # Filter districts based on state
        districts = sorted(df[df['state'] == state]['district name'].dropna().unique())
        return districts
    except Exception as e:
        print(f"Error getting districts: {e}")
        return []

def get_filtered_markets(state, district):
    """Return markets filtered by state and district"""
    file_path = os.path.join('myapp', 'data', 'market_prices.csv')
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        df.columns = df.columns.str.strip().str.replace('\u200b', '').str.lower()
        
        # Filter markets based on state and district
        filtered_df = df[(df['state'] == state) & (df['district name'] == district)]
        markets = sorted(filtered_df['market name'].dropna().unique())
        return markets
    except Exception as e:
        print(f"Error getting markets: {e}")
        return []

def get_filtered_commodities(state, district, market):
    """Return commodities filtered by state, district and market"""
    file_path = os.path.join('myapp', 'data', 'market_prices.csv')
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        df.columns = df.columns.str.strip().str.replace('\u200b', '').str.lower()
        
        # Filter commodities based on state, district and market
        filtered_df = df[(df['state'] == state) & 
                         (df['district name'] == district) & 
                         (df['market name'] == market)]
        commodities = sorted(filtered_df['commodity'].dropna().unique())
        return commodities
    except Exception as e:
        print(f"Error getting commodities: {e}")
        return []

def get_filtered_varieties(state, district, market, commodity):
    """Return varieties filtered by state, district, market and commodity"""
    file_path = os.path.join('myapp', 'data', 'market_prices.csv')
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        df.columns = df.columns.str.strip().str.replace('\u200b', '').str.lower()
        
        # Filter varieties based on state, district, market and commodity
        filtered_df = df[(df['state'] == state) & 
                         (df['district name'] == district) & 
                         (df['market name'] == market) &
                         (df['commodity'] == commodity)]
        varieties = sorted(filtered_df['variety'].dropna().unique())
        return varieties
    except Exception as e:
        print(f"Error getting varieties: {e}")
        return []