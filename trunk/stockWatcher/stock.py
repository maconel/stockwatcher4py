# -*- coding: gb2312 -*-

class Stock:
    CODE = 0                   #��Ʊ���롣
    NAME = 1                   #��Ʊ���ơ�
    CLOSING_PRICE = 2          #�����̡�
    OPEN_PRICE = 3             #���̡�
    MINIMUM_PRICE = 4          #��͡�
    MAXIMUM_PRICE = 5          #��ߡ�
    CURRENT_PRICE = 6          #��ǰ�ۡ�
    MARKUP_VALUE = 7           #�ǵ��
    MARKUP_PERCENT = 8         #�ǵ�����
    BARGAINON_COUNT = 9        #�ɽ�����
    BARGAINON_TOTAL_VALUE =10  #�ɽ��

    def __init__(self):
        self._datas = [\
            ["", "��Ʊ����"],\
            ["", "��Ʊ����"],\
            ["", "������"],\
            ["", "����"],\
            ["", "���"],\
            ["", "���"],\
            ["", "��ǰ��"],\
            ["", "�ǵ���"],\
            ["", "�ǵ���"],\
            ["", "�ɽ���"],\
            ["", "�ɽ���"]\
            ]
