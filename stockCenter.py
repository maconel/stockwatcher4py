# -*- coding: gb2312 -*-

import download
import parse
import period
import config
import stock

class StockCenter:
    #��ʼ����
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

    #����������
    def start(self):
        self._period.start()

    #ֹͣ��
    def stop(self):
        self._period.stop()

    #���¹�Ʊ���ݡ�
    def update(self):
        #�ռ�stockSymbols.
        stockSymbols = []
        self._stocks.remove(self._stocks[0])
        for stk in self._stocks:
            stockSymbols.append(stk._datas[stock.Stock.SYMBOL])

        #���ز�������
        bigCode, newStocks = parse.parse(download.download(stockSymbols))

        #��stockSymbols��������self._stocks.
        for i in range(len(stockSymbols)):
            newStocks[-1*(i+1)]._datas[stock.Stock.SYMBOL] = stockSymbols[i]
        self._stocks = newStocks
        self._stocks.insert(0, bigCode)

    #�ƶ���Ʊ˳��
    def moveStock(self, oldIndex, newIndex):
        if oldIndex < 0 or oldIndex >= len(self._stocks):
            return
        if newIndex < 0 or newIndex >= len(self._stocks):
            return
        self._stocks[oldIndex], self._stocks[newIndex] = self._stocks[newIndex], self._stocks[oldIndex]

    #����һ֧��Ʊ���ҵ����ظù�Ʊʵ����ʧ�ܷ���None.
    def findStockBySymbol(self, stockSymbol):
        for stk in self._stocks:
            if stk._datas[stock.Stock.SYMBOL] == stockSymbol:
                return stk
        return None

    #����һ֧��Ʊ���ҵ����ظù�Ʊʵ����ʧ�ܷ���None.
    def findStockByCode(self, code):
        for stk in self._stocks:
            if stk._datas[stock.Stock.CODE] == code:
                return stk
        return None

    #������ʾ��Щ��Ʊ��
    def setStockSymbols(self, stockSymbols):
        newStocks = []
        newStocks.append(self._stocks[0])   #�ȰѴ��̼ӽ�����
        for stockSymbol in stockSymbols:
            stk = self.findStockBySymbol(stockSymbol)
            if stk == None:
                stk = stock.Stock()
                stk._datas[stock.Stock.SYMBOL] = stockSymbol
            newStocks.append(stk)
        self._stocks = newStocks

    #��ʱ���ˣ����¹�Ʊ���ݡ�
    def onTime(self):
        self.update()
        if self._onUpdate <> None:
            self._onUpdate()
