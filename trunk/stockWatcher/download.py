# -*- coding: gb2312 -*-

import httplib

#�����Ʊ�Ĵ�����д�����֣����ذ�����Ʊ��Ϣ��htmlҳ�棬����htmlҳ������ݡ�
def download(stockSymbols):
    try:
        url = "/p/pl.php?sc=1&st=1&code="
        for symbol in stockSymbols:
            url = url + symbol + ","
        httpConn = httplib.HTTPConnection("stock.business.sohu.com")
        httpConn.request("GET", url)
        resp = httpConn.getresponse()
        return resp.read()
    except httplib.socket.error:
        return None
