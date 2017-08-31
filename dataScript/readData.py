__author__ = 'Kang'
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def read(df):
    #print file
    #df = pd.read_csv(file, index_col='Date')
    df = df.set_index(['Date'])
    df.index = pd.to_datetime(df.index)
    df.sort_index()
    df['Moving Mean'] = pd.rolling_mean(df['Adj_Clos'], 50, 50)
    df['Adj Close'] = df['Adj_Clos']
    df['OneYear Volume'] = pd.rolling_mean(df['Volume'], 300, 300)
    screenVolumeandPrice(df)
    df['Moving Std'] = pd.rolling_std(df['Moving Mean'], 300, 300)
    df['Daily Volume'] = df['Volume']
    df['ThreeDays Volume'] = pd.rolling_mean(df['Volume'],3,3)
    data = df[['Adj Close','Moving Mean', 'Daily Volume', 'OneYear Volume', 'ThreeDays Volume','Moving Std']]
    return data

def screenVolumeandPrice(df):
    if (df['Moving Mean'].iloc[-1] < 15 or df['OneYear Volume'].iloc[-1] < 1000000):
        raise ValueError("Bad Value")