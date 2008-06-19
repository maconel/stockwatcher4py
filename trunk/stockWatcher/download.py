# -*- coding: gb2312 -*-

import httplib

#传入股票的代码或简写或名字，下载包含股票信息的html页面，返回html页面的内容。
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
