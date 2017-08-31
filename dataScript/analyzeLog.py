import pandas as pd
import matplotlib.pyplot as plt
from pprint import  pprint
import time

def analyze(filename, holding):
    df = pd.read_csv(filename, index_col='Date')
    df.index = pd.to_datetime(df.index)
    cash = [0]
    for i, val in holding.iteritems():
        if df.ix[i]['buyOrSell'] == 1:
            cash.append(cash[-1] - 1000)
        else:
            cash.append(cash[-1] + df.ix[i]['Adj Close']*df.ix[i]['stocks'])
    cashAndHold = cash[1:] + holding
    pprint (cash)
    plt.plot(cashAndHold)
    plt.show()

#analyze("/home/han/stock/core/Logs/log1486517816.91.csv")
#df = pd.read_csv("/home/han/stock/core/Logs/log1486681662.12.csv", index_col='Date')
#print type(df.ix["2016-01-13"])