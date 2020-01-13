#Author: John Ferlic
#Day Trading Program

from selenium import webdriver
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
from StockInfo import StockInfo
from datetime import datetime
import time
from TestTradingAlgo import isFibSmaOk

alphaVantageKey = 'Q4A5RYR91VTSMIGK'
totalMoneyToStart = 1000
webDriverPath = '/Users/Jferlic/Desktop/ChromeDriver/chromedriver'
websiteForDataScraping = 'https://finance.yahoo.com/gainers'
timeToSell = 16

ts = TimeSeries(key=alphaVantageKey, output_format='pandas')
ti = TechIndicators(key=alphaVantageKey, output_format='pandas')


stocks = []
stocksToBuy = []

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
try:
    nextButton = driver.find_element_by_xpath('//*[@class="Va(m) H(20px) Bd(0) M(0) P(0) Fz(s) Pstart(10px) O(n):f Fw(500) C($c-fuji-blue-1-b)"]')
    nextButton.click()
    time.sleep(3)

    scrapeYahooData()
except:
    print("Didn't have enough data to grab another page")
driver.close()

print(len(stocks))

#Get RSI (Relative Strength Index) for the stocks above and see if they are good candidates for buying short term
count = 0
for stock in stocks:
    count = count + 1
    try:
        data, metaData = ti.get_rsi(stock.ticker)
        revData = data.iloc[::-1]
        recentRsi = revData["RSI"].iloc[0]
        print("Stock Name: ", stock.name)
        print("RSI: ", recentRsi)
        print("--------------------------")
        if recentRsi < 50:
            stocksToBuy.append(stock)
        if count % 5 == 0 :
            time.sleep(60)
    except:
        print('Error in call to get intraday data')

#Remove stocks that aren't compatible with Alpha Vantage Time Series call
if len(stocksToBuy) != 0:
    time.sleep(60)
    for stock in stocksToBuy:
        try:
            ts.get_intraday(stock.ticker)
        except:
            print("{} had to be removed from list of bought stocks because Alpha Vantage doesn't have data for it".format(stock.name))
            stocksToBuy.remove(stock)
    time.sleep(60)

#Buy the stocks and show the price of the stocks
if len(stocksToBuy) != 0:
    splitMoney = totalMoneyToStart / len(stocksToBuy)
    totalStockBought = []
    print('***********************************')
    print('STOCKS BOUGHT:')
    print('***********************************')
    for stock in stocksToBuy:
        numStocks = int(splitMoney/ float(stock.price))
        totalStockBought.append(numStocks)
        print("{} shares of {}, ticker : {}, at price : {}".format(numStocks, stock.name, stock.ticker, stock.price))
        print('***********************************')
    time.sleep(60)

    while int(datetime.now().hour) < timeToSell:
        print("-------------------------------")
        print("Time : {}".format(datetime.now()))
        print("-------------------------------")
        for stock in stocksToBuy:
            try:
                dat, mData = ts.get_intraday(stock.ticker)
                stockPriceNow = dat['4. close'][-1]
                print("Bought {} at ${}; Now ${}".format(stock.name, stock.price, stockPriceNow))
                # Will implement day trading capabilities in the future *** 
                # if stock price is greater than a certain amount compared to the initial price, sell the stock and remove it from the stocksToBuy list
                time.sleep(20)
            except:
                print("Error getting data for {}: Time Series call".format(stock.name))
        time.sleep(900)

    #After 4 pm sell all the stocks and get the (hopeful profit)
    print('-----------------')
    print('CLOSING POSITIONS')
    print('-----------------')
    totalStockDiff = 0
    for stock in stocksToBuy:
        try:
            dat, mData = ts.get_intraday(stock.ticker)
            stockClosingPrice = dat['4. close'][0]
            totalStockDiff = totalStockDiff + (float(stock.price) - float(stockClosingPrice))
        except:
            print("Error getting data for {} : Time Series call".format(stock.name))

    spyPercentChange = 0
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

    totalMoneyToEnd = totalMoneyToStart + totalStockDiff
    totalPercentChange = (totalMoneyToEnd - totalMoneyToStart) / totalMoneyToStart * 100
    print('----------------')
    print('    RESULTS     ')
    print('----------------')
    print("Total Money after today: ${} , {}%".format(round(totalMoneyToEnd, 2), round(totalPercentChange, 2)))
    print("Market Percent change (SPY): {}%".format(round(spyPercentChange, 2)))
else:
    print('Time Series call didnt have any of the chosen stocks. Program finished.')