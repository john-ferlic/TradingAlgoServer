class StockInfo:
    def __init__(self, name, ticker, percentChange, price):
        self.name = name
        self.ticker = ticker
        self.percentChange = percentChange
        self.price = price

class TradeDetails:
    def __init__(self, stock, numStocksBought, totalPrice):
        self.stock = stock
        self.numStocksBought = numStocksBought
        self.totalPrice = totalPrice