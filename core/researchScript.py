from technical import plot, buyAndSellOneCompany, ShortOneCompany
import pandas as pd
from dataScript.readData import read
import time, os
from pprint import pprint
from Logs.analyze import analyze, analyzeCash
#from Logs.analyzeCash import  analyzeCash
import traceback
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

def readSP500():
    sp500 = read("/home/han/stock/sp500/^GSPC_20110101_20170201.csv")
    return sp500

def main(start_date, end_date, buyNStd, buyNVol, sellNStd, sellNVol, klapse, rootdir, ifplot, sp500):
    engine = create_engine('mysql+mysqldb://root:password@10.0.0.3/')
    engine.execute("use mydb;")
    totalLeftOver = 0
    holding = {'Date':[], "Value":[]}
    log = {'Date':[], 'Company':[], 'Adj Close':[],'buyOrSell':[], 'stocks':[]}
    #logShort = {'Date':[], 'Company':[], 'Adj Close':[],'buyOrSell':[], 'stocks':[]}
    totalProfit = 0
    totalInvest = 0
    #sp500 = pd.read_csv('^GSPC_20110101_20170201.csv')[['Adj Clos','Date']].iloc[-500:]
    #for subdir, dirs, files in os.walk(rootdir):
    with open('tickerNew.txt') as tickersFile:
        files = tickersFile.readlines()
    print files
    for ticker in files :
        try:
            ticker = ticker.strip("\r\n")
            ticker = "'" + ticker + "'"
            #print ticker
            query = "select * from rawquotenew where ticker=" + ticker + "and rawquotenew.Date between " + start_date + "and " + end_date + " ORDER BY rawquotenew.Date ASC"
            #print query
            data = pd.read_sql(query, engine)
            #print data.head()
            data = read(data)
            data.dropna(axis=0, how='any', inplace=True)
            print ticker
            profit, invest, leftOver, plotBuyList, plotSellList = buyAndSellOneCompany(data.tail(1), log, ticker,
                                                                                       buyNStd, buyNVol, sellNStd,
                                                                                       sellNVol, klapse, sp500, holding)
            #profitshort, investshort, leftOvershort, shortBuyList, shortSellList = ShortOneCompany(data, log, file, period,
             #                                                                                 0, 0, 0.8,
              #                                                                              sellNVol, klapse, sp500,
               #                                                                              holding)
            totalInvest = totalInvest  + invest
            totalProfit = totalProfit  + profit
            totalLeftOver = totalLeftOver  + leftOver
            if ifplot:
                plotBuyList = []
                plotSellList = []
                plot(data, plotBuyList, plotSellList, shortBuyList, shortSellList, file )
        except Exception as e:
            print str(e)
            #print (traceback.format_exc())

    totalNet = totalProfit - totalInvest
    holding = pd.DataFrame.from_dict(holding)
    holding = holding.set_index(['Date'])
    holding = holding.sort_index()
    sum = holding.groupby(level=0)['Value'].sum()
    #sum = sum[sum != 0]
    log = pd.DataFrame.from_dict(log)
    log = log.set_index(['Date'])
    log = log.sort_index()
    csvName = "Logs/" + "log" + str(time.time()) + ".csv"
    log.to_csv(csvName)
    #logShort = pd.DataFrame.from_dict(logShort)
    #logShort = logShort.set_index(['Date'])
    #logShort = logShort.sort_index()
    #csvNameShort = "Logs/" + "log" + "sell" + str(time.time()) + ".csv"
    #logShort.to_csv(csvNameShort)
    print(totalInvest, totalProfit, totalNet)
    print(totalLeftOver)
    analyzeCash(csvName,sum    )

# Set data directory
rootdir = "/home/han/stock/historicalData"

if __name__ == "__main__":
