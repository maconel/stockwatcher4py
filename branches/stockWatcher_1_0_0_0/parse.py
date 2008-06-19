# -*- coding: gb2312 -*-

import stock

#���������Ʊ��Ϣ��htmlҳ�棬����stock�б�
def parse(htmlContent):
    stocks = []

    if htmlContent == None:
        return stock.Stock(), []

    #�õ��������ݡ�
    htmlContent, bigCode = parseBigCode(htmlContent)

    #�ҵ����Ŀ�ͷ��
    pos = htmlContent.find("��Ʊ����")
    if pos == -1:
        return None
    htmlContent = htmlContent[pos:]

    #�ҵ����Ľ�β��
    pos = htmlContent.find("</table>")
    if pos == -1:
        return None
    htmlContent = htmlContent[:pos]
    
    #ѭ��������ÿ����Ʊ���ݡ�
    htmlContent, stk = parseFirstStock(htmlContent)
    while stk != None:
        stocks.append(stk)
        htmlContent, stk = parseFirstStock(htmlContent)

    return bigCode, stocks

#��������ָ����
def parseBigCode(text):
    bigCode = stock.Stock()
    bigCode._datas[stock.Stock.NAME] = "����"

    #�ҵ����̿�ʼ����
    pos = text.find("../q/bc.php?code=1A0001")
    if pos == -1:
        return text, None
    text = text[pos:]

    #�ҵ�"��֤".
    pos = text.find("��֤")
    if pos == -1:
        return text, None
    text = text[pos:]

    #�ҵ�����ָ��ǰ��"<font".
    pos = text.find("<font")
    if pos == -1:
        return text, None
    text = text[pos:]

    #�ҵ�����ָ��ǰ��"<b>".
    pos = text.find("<b>")
    if pos == -1:
        return text, None
    text = text[pos + len("<b>"):]

    #�ҵ�����ָ�����"</b>"�����õ�����ָ����
    pos = text.find("</b>")
    if pos == -1:
        return text, None
    bigCode._datas[stock.Stock.CURRENT_PRICE] = text[:pos]
    text = text[pos:]

    #�ҵ���һ����"</font>".
    pos = text.find("</font>")
    if pos == -1:
        return text, bigCode
    text = text[pos + len("</font>"):]

    #����һ��"</font>"�����õ�������������.
    pos = text.find("</font>")
    if pos == -1:
        return text, bigCode
    data = text[:pos]
    dataList = data.split("&nbsp;")
    if len(dataList) < 4:
        return text, bigCode

    #�ǵ��
    bigCode._datas[stock.Stock.MARKUP_VALUE] = dataList[1]

    #�ǵ�����
    bigCode._datas[stock.Stock.MARKUP_PERCENT] = dataList[2][1:-1]  #���̵��ǵ�����()�������ˣ�����ȥ����

    #�ɽ�����
    bigCode._datas[stock.Stock.BARGAINON_COUNT] = dataList[3]

    return text, bigCode

#������������text�еĵ�һ����Ʊ��
def parseFirstStock(text):
    pos = text.find("<tr")
    if pos == -1:
        return text, None
    text = text[pos:]

    stk = stock.Stock()

    #��һ�����ݡ���Ʊ���롣
    i = 0
    text, data = parseFirstData(text)
    if data != None:
        stk._datas[i] = data

    #�ڶ������ݡ���Ʊ���ơ�
    i += 1
    text, data = parseFirstData(text)
    if data != None:
        stk._datas[i] = data.strip("&nbsp;")

    #���������ݡ������̡�
    i += 1
    text, data = parseFirstData(text)
    if data != None:
        stk._datas[i] = data.strip("&nbsp;")

    #���ĸ����ݡ����̡�
    i += 1
    text, data = parseFirstData(text)
    if data != None:
        stk._datas[i] = data.strip("&nbsp;")

    #��������ݡ���� - ��ߡ�
    i += 1
    text, data = parseFirstData(text)
    if data != None:
        pos = data.find("-")
        if pos != -1:
            stk._datas[i] = data[:pos].strip("&nbsp;")
            stk._datas[i + 1] = data[pos+1:].strip("&nbsp;")

    #���������ݡ���ǰ�ۡ�
    i += 2
    text, data = parseFirstData(text)
    if data != None:
        stk._datas[i] = data.strip("&nbsp;")

    #���߸����ݡ��ǵ��
    i += 1
    text, data = parseFirstData(text)
    if data != None:
        stk._datas[i] = data.strip("&nbsp;")

    #�ڰ˸����ݡ��ǵ�����
    i += 1
    text, data = parseFirstData(text)
    if data != None:
        stk._datas[i] = data.strip("&nbsp;")

    #�ھŸ����ݡ��ɽ�����
    i += 1
    text, data = parseFirstData(text)
    if data != None:
        stk._datas[i] = data.strip("&nbsp;")

    #��ʮ�����ݡ��ɽ��
    i += 1
    text, data = parseFirstData(text)
    if data != None:
        stk._datas[i] = data.strip("&nbsp;")

    return text, stk

#������������text�еĵ�һ�����ݡ�
def parseFirstData(text):
    #�ҵ���ͷ��
    pos = text.find("<td")
    if pos == -1:
        return text, None
    text = text[pos:]
    
    #�ҵ���β��
    pos = text.find("</td>")
    if pos == -1:
        return text, None
    pos = pos + len("</td>")
    dataline = text[:pos]
    text = text[pos+1:]
    
    #����dataline���ѵ�һ��û��<>���������ַ����ҳ������Ǿ��ǽ����
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
