import dataScript.ystockquote as ys
import datetime
import csv

todaysDate = datetime.date.today().strftime("%Y%m%d")
print todaysDate

with open("tickers.txt") as f:
    tickers = f.readlines()

for ticker in tickers:
    ticker = ticker.strip("\n")
    todayRow = ys.get_historical_prices(ticker,todaysDate,todaysDate)
    try:
        if todayRow[0][0]=='Date':
            print "Updating", ticker
            with open("/home/han/stock/historicalData/"+ ticker,"ab") as file:
                wr = csv.writer(file, quoting=csv.QUOTE_NONE)
                wr.writerow(todayRow[1])
        else:
            print "Wrong", ticker
    except Exception as e:
        print "Wrong", ticker
