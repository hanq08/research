__author__ = 'Kang'
import os
import time
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from dataScript.analyzeLog import analyze
from dataScript.readData import  read
import pprint

def buy(dataRow, nStd, nv):
    if (dataRow['Adj Close'] < dataRow['Moving Mean'] - nStd * dataRow['Moving Std'] and dataRow['Daily Volume'] > nv * dataRow['OneYear Volume']):
        stocks = 1000/dataRow['Adj Close']
        return stocks
    return False

def sell(dataRow, nStd, nv):
    if (dataRow['Adj Close'] > dataRow['Moving Mean'] + nStd * dataRow['Moving Std'] and dataRow['ThreeDays Volume'] < nv * dataRow['OneYear Volume']):
        sold = dataRow['Adj Close']
        return (sold)
    return False

def buyshort(dataRow, nStd, nv):
    if (dataRow['Adj Close'] < dataRow['Moving Mean'] - nStd * dataRow['Moving Std'] and dataRow['Daily Volume'] > nv * dataRow['OneYear Volume']):
        stocks = dataRow['Adj Close']
        return stocks
    return False

def sellshort(dataRow, nStd, nv):
    if (dataRow['Adj Close'] > dataRow['Moving Mean'] + nStd * dataRow['Moving Std'] and dataRow['ThreeDays Volume'] < nv * dataRow['OneYear Volume']):
        sold = 1000/dataRow['Adj Close']
        return (sold)
    return False

def buyAndSellOneCompany(data,log,company, buyNStd, buyNVol, sellNStd, sellNVol, klapse, sp500, holding):
    plotBuyList = []
    plotSellList = []
    stocks = 0
    profit = 0.0
    invest = 0
    for i, dataRow in data.iterrows():
        bought = buy(dataRow,buyNStd,buyNVol)
        if bought:
            d = i - timedelta(days=klapse)
            k = getK(data['Adj Close'][d: i].values)
            #ksp = getK(sp500['Adj Close'][d:i].values)
            if (k > 0.01):
                log['Date'].append(i)
                log['Company'].append(company)
                log['Adj Close'].append(dataRow["Adj Close"])
                log['buyOrSell'].append(1)
                log['stocks'].append(bought)
                invest = invest + 1000
                stocks = stocks + bought
                plotBuyList.append(dataRow['Adj Close'])
            else:
                plotBuyList.append(5)
        else:
            plotBuyList.append(0)
        if stocks>0:
            sold = sell(dataRow,sellNStd,sellNVol)
            if sold:
                print stocks
                log['Date'].append(i)
                log['Company'].append(company)
                log['Adj Close'].append(dataRow["Adj Close"])
                log['buyOrSell'].append(0)
                log['stocks'].append(stocks)
                profit = profit + stocks*sold
                stocks = 0
                plotSellList.append(dataRow['Adj Close'])
            else:
                plotSellList.append(0)
        else:
            plotSellList.append(0)
        holding['Date'].append(i)
        holding['Value'].append(stocks*dataRow["Adj Close"])
    #print(profit/invest,profit,invest)
    #print (holding)
    leftOver = stocks * data['Adj Close'].iloc[-1]
    return profit, invest, leftOver, plotBuyList, plotSellList

def ShortOneCompany(data,log,company, buyNStd, buyNVol, sellNStd, sellNVol, klapse, sp500, holding):
    plotBuyList = []
    plotSellList = []
    soldstocks = 0
    shortbuy = 0.0
    shortsell = 0
    for i, dataRow in data.iterrows():
        sold = sellshort(dataRow,sellNStd,sellNVol)
        if sold and soldstocks == 0:
            d = i - timedelta(days=klapse)
            k = getK(data['Adj Close'][d: i].values)
            #ksp = getK(sp500['Adj Close'][d:i].values)
            if (k < -0.02):
                log['Date'].append(i)
                log['Company'].append(company)
                log['Adj Close'].append(dataRow["Adj Close"])
                log['buyOrSell'].append(0)
                log['stocks'].append(sold)
                shortsell = shortsell + 1000
                soldstocks = soldstocks + sold
                plotSellList.append(dataRow['Adj Close'])
            else:
                plotSellList.append(5)
        else:
            plotSellList.append(0)
        if soldstocks>0:
            bought = buyshort(dataRow,buyNStd,buyNVol)
            if bought:
                log['Date'].append(i)
                log['Company'].append(company)
                log['Adj Close'].append(dataRow["Adj Close"])
                log['buyOrSell'].append(1)
                log['stocks'].append(soldstocks)
                shortbuy = shortbuy + soldstocks*bought
                soldstocks = 0
                plotBuyList.append(dataRow['Adj Close'])
            else:
                plotBuyList.append(0)
        else:
            plotBuyList.append(0)
        holding['Date'].append(i)
        holding['Value'].append(soldstocks*dataRow["Adj Close"])
    #print(profit/invest,profit,invest)
    leftOver = -1*soldstocks * data['Adj Close'].iloc[-1]
    return shortsell, shortbuy, leftOver, plotBuyList, plotSellList

def plot(data, plotBuyList, plotSellList, shortBuyList, shortSellList, ticker):
    period = len(shortBuyList)
    x = data.tail(period).index.get_values()
    plt.suptitle(ticker)
    #x = [datetime.strptime(d,'%Y-%m-%d').date() for d in data['Datetime'].tail(365)]
    #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    #plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.plot(data['Adj Close'].tail(period))
    plt.plot(data['Moving Mean'].tail(period))
    plt.plot((data['Moving Mean']+data['Moving Std']).tail(period))
    plt.plot((data['Moving Mean']-data['Moving Std']).tail(period))
    plt.plot((data['Daily Volume']/data['OneYear Volume']).tail(period))
    plt.plot((data['Daily Volume']/data['Daily Volume']).tail(period))
    #plt.gcf().autofmt_xdate()
    #plt.plot(x,plotBuyList,'ro')
    #plt.plot(x, plotSellList, 'g^')
    plt.plot(x, shortSellList, 'bv')
    plt.plot(x, shortBuyList, 'b*')
    #plt.plot(x, plotSellList, 'g^')
    plt.show()

def getK(y):
    x = np.arange(len(y), dtype=float).reshape((len(y), 1))
    regr = LinearRegression()
    result = regr.fit(x, y)
    k = result.predict(1) - result.predict(0)
    return k


