# -*- coding: gb2312 -*-

import stock

#传入包含股票信息的html页面，返回stock列表。
def parse(htmlContent):
    stocks = []

    if htmlContent == None:
        return stock.Stock(), []

    #得到大盘数据。
    htmlContent, bigCode = parseBigCode(htmlContent)

    #找到表格的开头。
    pos = htmlContent.find("股票代码")
    if pos == -1:
        return None
    htmlContent = htmlContent[pos:]

    #找到表格的结尾。
    pos = htmlContent.find("</table>")
    if pos == -1:
        return None
    htmlContent = htmlContent[:pos]
    
    #循环解析出每个股票数据。
    htmlContent, stk = parseFirstStock(htmlContent)
    while stk != None:
        stocks.append(stk)
        htmlContent, stk = parseFirstStock(htmlContent)

    return bigCode, stocks

#解析大盘指数。
def parseBigCode(text):
    bigCode = stock.Stock()
    bigCode._datas[stock.Stock.NAME] = "大盘"

    #找到大盘开始处。
    pos = text.find("../q/bc.php?code=1A0001")
    if pos == -1:
        return text, None
    text = text[pos:]

    #找到"上证".
    pos = text.find("上证")
    if pos == -1:
        return text, None
    text = text[pos:]

    #找到大盘指数前的"<font".
    pos = text.find("<font")
    if pos == -1:
        return text, None
    text = text[pos:]

    #找到大盘指数前的"<b>".
    pos = text.find("<b>")
    if pos == -1:
        return text, None
    text = text[pos + len("<b>"):]

    #找到大盘指数后的"</b>"，并得到大盘指数。
    pos = text.find("</b>")
    if pos == -1:
        return text, None
    bigCode._datas[stock.Stock.CURRENT_PRICE] = text[:pos]
    text = text[pos:]

    #找到下一个的"</font>".
    pos = text.find("</font>")
    if pos == -1:
        return text, bigCode
    text = text[pos + len("</font>"):]

    #再找一个"</font>"，并得到其他几个数据.
    pos = text.find("</font>")
    if pos == -1:
        return text, bigCode
    data = text[:pos]
    dataList = data.split("&nbsp;")
    if len(dataList) < 4:
        return text, bigCode

    #涨跌额。
    bigCode._datas[stock.Stock.MARKUP_VALUE] = dataList[1]

    #涨跌幅。
    bigCode._datas[stock.Stock.MARKUP_PERCENT] = dataList[2][1:-1]  #大盘的涨跌幅用()包起来了，所以去掉它

    #成交量。
    bigCode._datas[stock.Stock.BARGAINON_COUNT] = dataList[3]

    return text, bigCode

#解析出给定的text中的第一个股票。
def parseFirstStock(text):
    pos = text.find("<tr")
    if pos == -1:
        return text, None
    text = text[pos:]

    stk = stock.Stock()

    #第一个数据。股票代码。
    i = 0
    text, data = parseFirstData(text)
    if data != None:
        stk._datas[i] = data

    #第二个数据。股票名称。
    i += 1
    text, data = parseFirstData(text)
    if data != None:
        stk._datas[i] = data.strip("&nbsp;")

    #第三个数据。昨收盘。
    i += 1
    text, data = parseFirstData(text)
    if data != None:
        stk._datas[i] = data.strip("&nbsp;")

    #第四个数据。今开盘。
    i += 1
    text, data = parseFirstData(text)
    if data != None:
        stk._datas[i] = data.strip("&nbsp;")

    #第五个数据。今低 - 今高。
    i += 1
    text, data = parseFirstData(text)
    if data != None:
        pos = data.find("-")
        if pos != -1:
            stk._datas[i] = data[:pos].strip("&nbsp;")
            stk._datas[i + 1] = data[pos+1:].strip("&nbsp;")

    #第六个数据。当前价。
    i += 2
    text, data = parseFirstData(text)
    if data != None:
        stk._datas[i] = data.strip("&nbsp;")

    #第七个数据。涨跌额。
    i += 1
    text, data = parseFirstData(text)
    if data != None:
        stk._datas[i] = data.strip("&nbsp;")

    #第八个数据。涨跌幅。
    i += 1
    text, data = parseFirstData(text)
    if data != None:
        stk._datas[i] = data.strip("&nbsp;")

    #第九个数据。成交量。
    i += 1
    text, data = parseFirstData(text)
    if data != None:
        stk._datas[i] = data.strip("&nbsp;")

    #第十个数据。成交额。
    i += 1
    text, data = parseFirstData(text)
    if data != None:
        stk._datas[i] = data.strip("&nbsp;")

    return text, stk

#解析出给定的text中的第一个数据。
def parseFirstData(text):
    #找到开头。
    pos = text.find("<td")
    if pos == -1:
        return text, None
    text = text[pos:]
    
    #找到结尾。
    pos = text.find("</td>")
    if pos == -1:
        return text, None
    pos = pos + len("</td>")
    dataline = text[:pos]
    text = text[pos+1:]
    
    #遍历dataline，把第一个没被<>包起来的字符串找出来，那就是结果。
    bracketCount = 0
    data = ""
    for c in dataline:
        if c == "<":
            if (len(data) > 0):
                break
            bracketCount += 1
        elif c == ">":
            bracketCount -= 1
            if bracketCount < 0:
                break
        else:
            if bracketCount == 0:
                data += c

    return text, data
