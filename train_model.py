import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import lightgbm as lgb
import joblib

def add_features(df):
    df['SMA_5'] = df['close'].rolling(window=5).mean()
    df['SMA_10'] = df['close'].rolling(window=10).mean()
    df['EMA_10'] = df['close'].ewm(span=10, adjust=False).mean()
    df['Momentum'] = df['close'] - df['close'].shift(1)
    df['Return'] = df['close'].pct_change()
    df = df.dropna()
    return df

def prepare_data(df):
    df = add_features(df)
    X = df[['open','high','low','close','volume','SMA_5','SMA_10','EMA_10','Momentum','Return']]
    y = (df['close'].shift(-1) > df['close']).astype(int)  # Next minute up/down
    y = y[:-1]  # Align target
    X = X[:-1]
    return X, y

def train():
    df = pd.read_csv('btc_usd_sample.csv', parse_dates=['timestamp'])
    X, y = prepare_data(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    train_data = lgb.Dataset(X_train, label=y_train)
    valid_data = lgb.Dataset(X_test, label=y_test)
    
    params = {
        'objective': 'binary',
        'metric': 'binary_logloss',
        'verbosity': -1,
        'boosting_type': 'gbdt',
        'seed': 42
    }
    
    model = lgb.train(params, train_data, valid_sets=[valid_data], num_boost_round=100, early_stopping_rounds=10)
    
    print("Model trained with best iteration:", model.best_iteration)
    joblib.dump(model, 'model.pkl')

if __name__ == "__main__":
    train()
