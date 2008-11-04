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
        self._stockSymbols = []
        self._onUpdate = onUpdate
        self._period = period.Period(self.onTime)
        self._period.setInterval(60)
        self._stockSymbols = config.config()._stockSymbols

    #运行起来。
    def start(self):
        self._period.start()

    #停止。
    def stop(self):
        self._period.stop()

    #更新股票数据。
    def update(self):
        #下载并解析。
        bigCode, newStocks = parse.parse(download.download(self._stockSymbols))
        newStocks.reverse()

        #保存下载的数据。
        if bigCode <> None and newStocks <> None and len(newStocks) <> 0:
            self._stocks = []
            self._stocks.append(bigCode)
            self._stocks.extend(newStocks)

        #如果取到的比请求的少，则以空数据填充。
        for i in range(len(self._stockSymbols) - len(newStocks)):
            self._stocks.append(stock.Stock())

    #移动股票顺序。
    def moveStock(self, oldIndex, newIndex):
        if oldIndex < 0 or oldIndex >= len(self._stockSymbols):
            return
        if newIndex < 0 or newIndex >= len(self._stockSymbols):
            return
        self._stockSymbols[oldIndex], self._stockSymbols[newIndex] = self._stockSymbols[newIndex], self._stockSymbols[oldIndex]

    #设置显示哪些股票。
    def setStockSymbols(self, stockSymbols):
        self._stockSymbils = stockSymbols

    #到时间了，更新股票数据。
    def onTime(self):
        self.update()
        if self._onUpdate <> None:
            self._onUpdate()
