from core.technical import sell
from dataScript.readData import read

holdList = ["TPX", "CTXS"]
sellList = {}
for company in holdList:
    file = "../historicalData/" + company
    data = read(file)
    sold = sell(data.iloc[-1], 1, 1)
    sellList[company] = sold
print sellList