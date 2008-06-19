# -*- coding: gb2312 -*-

class Stock:
    CODE = 0                   #股票代码。
    NAME = 1                   #股票名称。
    CLOSING_PRICE = 2          #昨收盘。
    OPEN_PRICE = 3             #今开盘。
    MINIMUM_PRICE = 4          #今低。
    MAXIMUM_PRICE = 5          #今高。
    CURRENT_PRICE = 6          #当前价。
    MARKUP_VALUE = 7           #涨跌额。
    MARKUP_PERCENT = 8         #涨跌幅。
    BARGAINON_COUNT = 9        #成交量。
    BARGAINON_TOTAL_VALUE =10  #成交额。

    def __init__(self):
        self._datas = [\
            ["", "股票代码"],\
            ["", "股票名称"],\
            ["", "昨收盘"],\
            ["", "今开盘"],\
            ["", "今低"],\
            ["", "今高"],\
            ["", "当前价"],\
            ["", "涨跌额"],\
            ["", "涨跌幅"],\
            ["", "成交量"],\
            ["", "成交额"]\
            ]
