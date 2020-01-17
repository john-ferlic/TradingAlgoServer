from alpha_vantage.techindicators import TechIndicators
import time

alphaVantageKey = 'Q4A5RYR91VTSMIGK'
ti = TechIndicators(key=alphaVantageKey, output_format='pandas')

def isFibSmaOk(ticker):
    bars = [5,8,13]
    smaValues = []
    hasSMA = True
    print("***************       {}       ****************".format(ticker))
    for i in range(0,3):
        data, metadata = ti.get_sma(symbol=ticker, interval='30min', time_period=bars[i])
        reversedData = data.iloc[::-1]
        sma = reversedData["SMA"][0]
        print("The SMA for the last {} data points is: {} ".format(bars[i], sma))
        smaValues.append(sma)
    #Check to see if sma for 8-bar is greater than 13-bar and if 5-bar is greater than 8-bar
    if hasSMA:
        if smaValues[1] > smaValues[2]:
            if smaValues[0] > smaValues[1]:
                print("BUY")
                return True
            else:
                print("DON'T BUY")
                return False
        else:
            print("DON'T BUY")
            return False

def isRsiOk(ticker, thresholdRsi):
    data, metaData = ti.get_rsi(ticker)
    revData = data.iloc[::-1]
    recentRsi = revData["RSI"].iloc[0]
    print("Stock Name: ", ticker)
    print("RSI: ", recentRsi)
    print("--------------------------")
    if recentRsi < thresholdRsi:
        return True
    else:
        return False
