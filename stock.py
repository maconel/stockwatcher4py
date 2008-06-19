# -*- coding: gb2312 -*-

def indexDataType(dataType):
    for dataTypeKey in Stock.DATA_TYPE_DICT:
        if dataType == Stock.DATA_TYPE_DICT[dataTypeKey]:
            return dataTypeKey
    return None

class Stock:
    CODE,\
    NAME,\
    CLOSING_PRICE,\
    OPEN_PRICE,\
    MINIMUM_PRICE,\
    MAXIMUM_PRICE,\
    CURRENT_PRICE,\
    MARKUP_VALUE,\
    MARKUP_PERCENT,\
    BARGAINON_COUNT,\
    BARGAINON_TOTAL_VALUE,\
    SYMBOL\
    = range(12)

    DATA_TYPE_DICT = {\
        CODE: "股票代码",\
        NAME: "股票名称",\
        CLOSING_PRICE: "昨收盘",\
        OPEN_PRICE: "今开盘",\
        MINIMUM_PRICE: "今低",\
        MAXIMUM_PRICE: "今高",\
        CURRENT_PRICE: "当前价",\
        MARKUP_VALUE: "涨跌额",\
        MARKUP_PERCENT: "涨跌幅",\
        BARGAINON_COUNT: "成交量",\
        BARGAINON_TOTAL_VALUE: "成交额"
        }

    def __init__(self):
        self._datas = []
        for i in range(12):
            self._datas.append("-")
