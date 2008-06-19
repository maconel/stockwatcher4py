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
        CODE: "��Ʊ����",\
        NAME: "��Ʊ����",\
        CLOSING_PRICE: "������",\
        OPEN_PRICE: "����",\
        MINIMUM_PRICE: "���",\
        MAXIMUM_PRICE: "���",\
        CURRENT_PRICE: "��ǰ��",\
        MARKUP_VALUE: "�ǵ���",\
        MARKUP_PERCENT: "�ǵ���",\
        BARGAINON_COUNT: "�ɽ���",\
        BARGAINON_TOTAL_VALUE: "�ɽ���"
        }

    def __init__(self):
        self._datas = []
        for i in range(12):
            self._datas.append("-")
