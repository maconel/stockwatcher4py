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
        self._stockSymbols = config.config()._stockSymbols

    #����������
    def start(self):
        self._period.start()

    #ֹͣ��
    def stop(self):
        self._period.stop()

    #���¹�Ʊ���ݡ�
    def update(self):
        bigCode, self._stocks = parse.parse(download.download(self._stockSymbols))
        self._stocks.insert(0, bigCode)

    #�ƶ���Ʊ˳��
    def moveStock(self, oldIndex, newIndex):
        if oldIndex < 0 or oldIndex >= len(self._stockSymbols):
            return
        if newIndex < 0 or newIndex >= len(self._stockSymbols):
            return
        self._stockSymbols[oldIndex], self._stockSymbols[newIndex] = self._stockSymbols[newIndex], self._stockSymbols[oldIndex]

    #����һ֧��Ʊ���ҵ����ظù�Ʊʵ����ʧ�ܷ���None.
    def findStock(self, stockSymbol):
        for stk in self._stocks:
            if stk._datas[stock.Stock.CODE][0] == stockSymbol:
                return stk
        return None

    #������ʾ��Щ��Ʊ��
    def setStockSymbols(self, stockSymbols):
        self._stockSymbols = stockSymbols
        newStocks = []
        for stockSymbol in self._stockSymbols:
            stk = self.findStock(stockSymbol)
            if stk == None:
                stk = stock.Stock()
                stk._datas[stock.Stock.CODE][0] = stockSymbol
            newStocks.append(stk)

    #��ʱ���ˣ����¹�Ʊ���ݡ�
    def onTime(self):
        self.update()
        if self._onUpdate <> None:
            self._onUpdate()
