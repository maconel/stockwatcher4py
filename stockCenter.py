# -*- coding: gb2312 -*-

import download
import parse
import period
import config
import stock

class StockCenter:
    #初始化。
    def __init__(self, onUpdate):
        self._stocks = []
        self._onUpdate = onUpdate
        self._period = period.Period(self.onTime)
        self._period.setInterval(60)
        self._stocks.append(stock.Stock())
        for symbol in config.config()._stockSymbols:
            stk = stock.Stock()
            stk._datas[stock.Stock.SYMBOL] = symbol
            self._stocks.append(stk)

    #运行起来。
    def start(self):
        self._period.start()

    #停止。
    def stop(self):
        self._period.stop()

    #更新股票数据。
    def update(self):
        #收集stockSymbols.
        stockSymbols = []
        self._stocks.remove(self._stocks[0])
        for stk in self._stocks:
            stockSymbols.append(stk._datas[stock.Stock.SYMBOL])

        #下载并解析。
        bigCode, newStocks = parse.parse(download.download(stockSymbols))

        #将stockSymbols重新填入self._stocks.
        for i in range(len(stockSymbols)):
            newStocks[-1*(i+1)]._datas[stock.Stock.SYMBOL] = stockSymbols[i]
        self._stocks = newStocks
        self._stocks.insert(0, bigCode)

    #移动股票顺序。
    def moveStock(self, oldIndex, newIndex):
        if oldIndex < 0 or oldIndex >= len(self._stocks):
            return
        if newIndex < 0 or newIndex >= len(self._stocks):
            return
        self._stocks[oldIndex], self._stocks[newIndex] = self._stocks[newIndex], self._stocks[oldIndex]

    #查找一支股票。找到返回该股票实例，失败返回None.
    def findStockBySymbol(self, stockSymbol):
        for stk in self._stocks:
            if stk._datas[stock.Stock.SYMBOL] == stockSymbol:
                return stk
        return None

    #查找一支股票。找到返回该股票实例，失败返回None.
    def findStockByCode(self, code):
        for stk in self._stocks:
            if stk._datas[stock.Stock.CODE] == code:
                return stk
        return None

    #设置显示哪些股票。
    def setStockSymbols(self, stockSymbols):
        newStocks = []
        newStocks.append(self._stocks[0])   #先把大盘加进来。
        for stockSymbol in stockSymbols:
            stk = self.findStockBySymbol(stockSymbol)
            if stk == None:
                stk = stock.Stock()
                stk._datas[stock.Stock.SYMBOL] = stockSymbol
            newStocks.append(stk)
        self._stocks = newStocks

    #到时间了，更新股票数据。
    def onTime(self):
        self.update()
        if self._onUpdate <> None:
            self._onUpdate()
