import pandas as pd
import matplotlib.pyplot as plt
from pprint import  pprint
import time
from datetime import datetime, timedelta

def analyze(filename, holding):
    df = pd.read_csv(filename, index_col='Date')
    df.index = pd.to_datetime(df.index)
    cashSum = [0]
    for i, val in holding.iteritems():
        if i in df.index:
            cash = 0
            if isinstance(df.ix[i], pd.DataFrame):
                for i, row in df.ix[i].iterrows():
                    if row['buyOrSell'] == 1:
                        cash = cash - 1000
                    else:
                        cash = cash + row['Adj Close']*row['stocks']
            else:
                if df.ix[i]['buyOrSell'] == 1:
                    cash = cash - 1000
                else:
                    cash = cash + df.ix[i]['Adj Close'] * df.ix[i]['stocks']
            cashSum.append(cashSum[-1] + cash)
        else:
            cashSum.append(cashSum[-1])
    cashAndHold = cashSum[1:] + holding
    plt.plot(holding)
    plt.show()

def analyzeCash(filename, holding):
    df = pd.read_csv(filename, index_col='Date')
    df.index = pd.to_datetime(df.index)
    cash = {"Date":[df.first_valid_index() - timedelta(days=1)], "Value":[0]}
    for i, row in df.iterrows():
        cash["Date"].append(i)
        if row['buyOrSell'] == 1:
            cash["Value"].append(-1*row['Adj Close']*row['stocks'])
        else:
            cash["Value"].append(row['Adj Close']*row['stocks'])
    cash = pd.DataFrame.from_dict(cash)
    cash = cash.set_index(['Date'])
    cash = cash.sort_index()
    cashSum = cash.groupby(level=0)["Value"].sum()
    cashSum = cashSum.cumsum()
    cashAndHold = pd.concat([holding,cashSum], axis = 1, join='outer')
    cashAndHold.fillna(method='ffill', inplace=True)
    cashAndHold.columns = ['holding', 'cash']
    cashAndHold['net'] = cashAndHold['holding'] + cashAndHold['cash']
    plt.plot(cashAndHold['holding'],"b")
    plt.plot(cashAndHold['cash'], "r")
    plt.plot(cashAndHold['net'], "g")
    #plt.plot(holding["Value"])
    plt.show()