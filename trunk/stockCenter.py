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
        self._stockSymbols = []
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
        #���ز�������
        bigCode, newStocks = parse.parse(download.download(self._stockSymbols))
        newStocks.reverse()

        #�������ص����ݡ�
        if bigCode <> None and newStocks <> None and len(newStocks) <> 0:
            self._stocks = []
            self._stocks.append(bigCode)
            self._stocks.extend(newStocks)

        #���ȡ���ı�������٣����Կ�������䡣
        for i in range(len(self._stockSymbols) - len(newStocks)):
            self._stocks.append(stock.Stock())

    #�ƶ���Ʊ˳��
    def moveStock(self, oldIndex, newIndex):
        if oldIndex < 0 or oldIndex >= len(self._stockSymbols):
            return
        if newIndex < 0 or newIndex >= len(self._stockSymbols):
            return
        self._stockSymbols[oldIndex], self._stockSymbols[newIndex] = self._stockSymbols[newIndex], self._stockSymbols[oldIndex]

    #������ʾ��Щ��Ʊ��
    def setStockSymbols(self, stockSymbols):
        self._stockSymbils = stockSymbols

    #��ʱ���ˣ����¹�Ʊ���ݡ�
    def onTime(self):
        self.update()
        if self._onUpdate <> None:
            self._onUpdate()
