#Second Try on Day Trading Program
#Author: John Ferlic

from selenium import webdriver
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
from StockInfo import StockInfo
from StockInfo import TradeDetails
from datetime import datetime
import time
from TestTradingAlgo import isFibSmaOk
from TestTradingAlgo import isRsiOk

alphaVantageKey = 'Q4A5RYR91VTSMIGK'
beginningMoney = 1000
totalMoney = 1000
totalMoneyinStocks = 0
webDriverPath = '/Users/Jferlic/Desktop/ChromeDriver/chromedriver'
websiteForDataScraping = 'https://finance.yahoo.com/gainers'
timeToSell = 16

ts = TimeSeries(key=alphaVantageKey, output_format='pandas')
ti = TechIndicators(key=alphaVantageKey, output_format='pandas')

stocks = []
tempStocks = []
trades = []

driver = webdriver.Chrome(executable_path=webDriverPath)
driver.get(websiteForDataScraping)

def scrapeYahooData():
    name = row.find_element_by_xpath('td[@aria-label="Name"]')
    ticker = row.find_element_by_xpath('td/a[@class="Fw(600)"]')
    percentChange = row.find_element_by_xpath('td[@aria-label="% Change"]')
    price = row.find_element_by_xpath('td/span[@class="Trsdu(0.3s) "]')
    stock = StockInfo(name.text, ticker.text, percentChange.text, price.text)
    stocks.append(stock)

stockData = driver.find_element_by_xpath('//*[@class="W(100%)"]/tbody')
for row in stockData.find_elements_by_tag_name('tr'):
    scrapeYahooData()
driver.close()

for stock in stocks:
    print(stock.ticker)
    print("-------------------")
    try:
        if isFibSmaOk(stock.ticker):
            tempStocks.append(stock)
    except:
        print("Error getting SMA for {}, {}".format(stock.name, stock.ticker))
    time.sleep(60)


print("---------------------")
print("NOW CHECKING THE RSI:")
print("---------------------")
stocksToBuy = []
count = 0
for stock in tempStocks:
    try:
        if isRsiOk(stock.ticker, 60):
            stocksToBuy.append(stock)
    except:
        print("Error getting RSI for {}, {}".format(stock.name, stock.ticker))
    count = count + 1
    if count % 5 == 0:
        time.sleep(60)

#Remove stocks that aren't compatible with Alpha Vantage Time Series call
if len(stocksToBuy) != 0:
    time.sleep(60)
    count = 0
    for stock in stocksToBuy:
        count = count + 1
        try:
            ts.get_intraday(stock.ticker)
        except:
            print("{} had to be removed from list of bought stocks because Alpha Vantage doesn't have data for it".format(stock.name))
            stocksToBuy.remove(stock)
        if count % 5 == 0:
            time.sleep(60)

#Buy the stocks and show the price of the stocks
if len(stocksToBuy) != 0:
    splitMoney = totalMoney / len(stocksToBuy)
    print('***********************************')
    print('STOCKS BOUGHT: ({})'.format(len(stocksToBuy)))
    print('Amount of Money to Spend: {}'.format(totalMoney))
    print('***********************************')

    for stock in stocksToBuy:
        numStocks = int(splitMoney / float(stock.price))
        totPriceStock = numStocks * float(stock.price)
        totalMoney = totalMoney - totPriceStock
        totalMoneyinStocks = totalMoneyinStocks + totPriceStock
        trade = TradeDetails(stock, numStocks, totPriceStock)
        trades.append(trade)
        print("{} shares of {}, ticker : {}, at price : {}".format(numStocks, stock.name, stock.ticker, stock.price))
        print('Total amount of money spent on {}: {}'.format(stock.name, totPriceStock))
        print('***********************************')
    print('TOTAL MONEY SPENT: {}'.format(totalMoneyinStocks))
    time.sleep(60)

    # while int(datetime.now().hour) < timeToSell:
    for x in range(1):
        print("-------------------------------")
        print("Time: {}".format(datetime.now()))
        print("-------------------------------")
        tStocks = []
        tTrades = []
        for stock in stocksToBuy:
            try:
                dat, mData = ts.get_intraday(stock.ticker)
                stockPriceNow = dat['4. close'][-1]
                print("Bought {} at ${}; Now ${}".format(stock.name, stock.price, stockPriceNow))
                if isFibSmaOk(stock.ticker) == False:
                    totPriceStock = numStocks * float(stock.price)
                    totalMoney = totalMoney + totPriceStock
                    totalMoneyinStocks = totalMoneyinStocks - totPriceStock
                    print("Removed {} because 5-8-13 bar SMA is not acceptable".format(stock.name))
                else:
                    tStocks.append(stock)
                    for trade in trades:
                        if trade.stock.name == stock.name:
                            tTrades.append(trade)
                            break
                time.sleep(60)
            except:
                print("Error getting data for {}: Time Series call".format(stock.name))
        stocksToBuy = tStocks
        trades = tTrades
    #After 4 pm sell all the stocks and get the (hopeful profit)
    print('-----------------')
    print('CLOSING POSITIONS')
    print('-----------------')
    totalStockDiff = 0
    count = 0
    for trade in trades:
        count = count + 1
        try:
            dat, mData = ts.get_intraday(trade.stock.ticker)
            stockClosingPrice = dat['4. close'][0]
            print("STOCK: {}".format(trade.stock.name))
            print("Stock price bought: {}".format(trade.stock.price))
            print("Stock closing price: {}".format(stockClosingPrice))
            print("Number of stocks bought: {}".format(trade.numStocksBought))
            totalStockDiff = totalStockDiff + ((float(stockClosingPrice) - float(trade.stock.price)) * trade.numStocksBought) 
        except:
            print("Error getting data for {} : Time Series call".format(stock.name))
        if count % 5 == 0:
            time.sleep(60)
    spyPercentChange = 0
    time.sleep(60)
    try:
        spyData, metaDeta = ts.get_daily('SPY')
        spyOpen = spyData["1. open"][-1]
        spyClose = spyData["4. close"][-1]
        spyPercentChange = (spyClose - spyOpen) / spyOpen * 100
        print("-----------------------------------")
        print("S&P 500 Details: ")
        print("-----------------------------------")
        print("SPY opened at: ${}".format(spyOpen))
        print("SPY closed at: ${}".format(spyClose))
        print("-----------------------------------")
    except:
        print("Error getting data for SPY Time Series call.")

    print("Cash: {}".format(totalMoney))
    print("Diff in Stock: {}".format(totalStockDiff))
    print("Stocks: {}".format(totalMoneyinStocks))

    totalMoneyToEnd = totalMoney + totalStockDiff + totalMoneyinStocks
    totalPercentChange = (totalMoneyToEnd - beginningMoney) / beginningMoney * 100
    print('----------------')
    print('    RESULTS     ')
    print('----------------')
    print("Total Money after today: ${} , {}%".format(round(totalMoneyToEnd, 2), round(totalPercentChange, 2)))
    print("Market Percent change (SPY): {}%".format(round(spyPercentChange, 2)))
else:
    print('Time Series call didnt have any of the chosen stocks. Program finished.')