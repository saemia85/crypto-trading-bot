import os
import time
import joblib
import pandas as pd
import requests
from datetime import datetime
from alpaca_trade_api.rest import REST, TimeFrame

# Load env vars
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
ALPACA_BASE_URL = os.getenv('ALPACA_BASE_URL', 'https://paper-api.alpaca.markets')

MODEL_PATH = 'model.pkl'
SYMBOL = 'BTCUSD'

api = REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL, api_version='v2')
model = joblib.load(MODEL_PATH)

def fetch_latest_data():
    end = datetime.utcnow()
    start = end - pd.Timedelta(minutes=15)
    barset = api.get_crypto_bars(SYMBOL, TimeFrame.Minute, start.isoformat(), end.isoformat()).df
    if barset.empty:
        return None
    df = barset.reset_index()
    return df.tail(15)

def prepare_features(df):
    df['SMA_5'] = df['close'].rolling(window=5).mean()
    df['SMA_10'] = df['close'].rolling(window=10).mean()
    df['EMA_10'] = df['close'].ewm(span=10, adjust=False).mean()
    df['Momentum'] = df['close'] - df['close'].shift(1)
    df['Return'] = df['close'].pct_change()
    df = df.dropna()
    features = df[['open','high','low','close','volume','SMA_5','SMA_10','EMA_10','Momentum','Return']].iloc[-1]
    return features.values.reshape(1, -1)

def place_order(side, qty=0.001):
    try:
        order = api.submit_order(
            symbol=SYMBOL,
            qty=qty,
            side=side,
            type='market',
            time_in_force='gtc'
        )
        print(f"{side.capitalize()} order placed: {order.id}")
    except Exception as e:
        print(f"Order error: {e}")

def run_bot():
    print("Starting trading bot...")
    max_loss = 50.0  # $50 max loss
    qty = 0.001  # Starting with small qty
    
    while True:
        df = fetch_latest_data()
        if df is None or df.empty:
            print("No data fetched, retrying...")
            time.sleep(60)
            continue
        
        features = prepare_features(df)
        prediction = model.predict(features)[0]
        
        position = api.get_position(SYMBOL) if api.get_account().status == 'ACTIVE' else None
        
        if prediction > 0.5:
            print("Buy signal detected")
            place_order('buy', qty)
        else:
            print("Sell signal detected")
            place_order('sell', qty)
        
        time.sleep(60)  # Wait 1 minute before next check

if __name__ == "__main__":
    run_bot()
