#Author: John Ferlic
#Created: 1/12/2020

from flask import Flask
import json

app = Flask(__name__)

@app.route("/stocksBought")
def stocksBought():
    file = open("stocks.txt", "r")
    stocksBought = []
    contents = file.readlines()
    for line in contents:
        info = line.split("%")
        infoDict = {
            "name": info[0],
            "ticker": info[1],
            "price": info[2],
            "numStocks": info[3],
            "totStockPrice": info[4].rstrip()
        }
        stocksBought.append(infoDict)
    return json.dumps(stocksBought)

@app.route("/stocksSold")
def stocksSold():
    file = open("stocksSold.txt", "r")
    stocksSold = []
    contents = file.readlines()
    for line in contents:
        info = line.split("%")
        infoDict = {
            "timeSold": info[0],
            "name": info[1],
            "ticker": info[2],
            "priceBought": round(float(info[3]), 2),
            "priceNow": round(float(info[4]), 2),
            "numStocksBought": info[5].rstrip()
        }
        stocksSold.append(infoDict)
    return json.dumps(stocksSold)

@app.route("/closingPositions")
def closingPosition():
    file = open("closingPositions.txt", "r")
    stocks = []
    contents = file.readlines()
    for line in contents:
        info = line.split("%")
        infoDict = {
            "name": info[0],
            "priceBought": info[1],
            "stockClosingPrice": info[2],
            "numStocks": info[3].rstrip()
        }
        stocks.append(infoDict)
    return json.dumps(stocks)

@app.route("/finalResults")
def results():
    file = open("finalResults.txt", "r")
    contents = file.readline()
    info = contents.split("%")
    infoDict = {
        "beginningAmountOfMoney": info[0],
        "totMoneyToEnd": round(float(info[1]), 2),
        "percentageChange": round(float(info[2]), 2),
        "spyOpen": info[3],
        "spyClose": info[4],
        "spyPercentageChange": round(float(info[5]), 2)
    }
    return json.dumps(infoDict)
        
    

if __name__ == "__main__":
  app.run(host='0.0.0.0')