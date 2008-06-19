# -*- coding: gb2312 -*-

import xml.dom.minidom

import stock

instance = None

def config():
    global instance
    if instance == None:
        instance = Config()
    return instance

class Config:
    def __init__(self):
        self._showStockCount = 1        #同时可以显示多少个股票。
        self._calmForeColor = 0xFFFFFF  #不赚不赔前景色。
        self._gainForeColor = 0xFF0000  #赚钱前景色。
        self._payForeColor = 0x00FF00   #赔钱前景色。
        self._backColor = 0x000000      #背景色。
        self._showDataTypes = []        #当前都显示哪些数据，比如股票名，当前价什么的。
        self._stockSymbols = []         #当前都显示哪些股票。
        self._mainWindowPos = [0, 0]    #主窗体的位置。

    def load(self, filename):
        dom = xml.dom.minidom.parse(filename)

        #root.
        root = dom.documentElement

        for node in root.childNodes:
            #showStockCount.
            if node.nodeName == "showStockCount":
                value = self.getPropertyValue(node)
                if value <> None:
                    self._showStockCount = int(value)
                else:
                    print "error: showStockCount"
            #calmForeColor.
            if node.nodeName == "calmForeColor":
                value = self.getPropertyValue(node)
                if value <> None:
                    self._calmForeColor = int(value, 16)
                else:
                    print "error: calmForeColor"
            #gainForeColor.
            if node.nodeName == "gainForeColor":
                value = self.getPropertyValue(node)
                if value <> None:
                    self._gainForeColor = int(value, 16)
                else:
                    print "error: gainForeColor"
            #payForeColor.
            if node.nodeName == "payForeColor":
                value = self.getPropertyValue(node)
                if value <> None:
                    self._payForeColor = int(value, 16)
                else:
                    print "error: payForeColor"
            #backColor.
            if node.nodeName == "backColor":
                value = self.getPropertyValue(node)
                if value <> None:
                    self._backColor = int(value, 16)
                else:
                    print "error: backColor"
            #showDataTypes.
            if node.nodeName == "showDataTypes":
                self._showDataTypes = []
                for node2 in node.childNodes:
                    if node2.nodeName == "showDataType":
                        value = self.getPropertyValue(node2)
                        if value <> None:
                            self._showDataTypes.append(int(value))
                        else:
                            print "error: showDataTypes"
            #stockSymbols.
            if node.nodeName == "stockSymbols":
                self._stockSymbols = []
                for node2 in node.childNodes:
                    if node2.nodeName == "stockSymbol":
                        value = self.getPropertyValue(node2)
                        if value <> None:
                            self._stockSymbols.append(value)
                        else:
                            print "error: stockSymbols"
            #mainWindowPos.
            if node.nodeName == "mainWindowPos":
                for node2 in node.childNodes:
                    if node2.nodeName == "x":
                        value = self.getPropertyValue(node2)
                        if value <> None:
                            self._mainWindowPos[0] = int(value)
                        else:
                            print "error: mainWindowPos_x"
                    if node2.nodeName == "y":
                        value = self.getPropertyValue(node2)
                        if value <> None:
                            self._mainWindowPos[1] = int(value)
                        else:
                            print "error: mainWindowPos_y"

    def save(self, filename):
        impl = xml.dom.minidom.getDOMImplementation()

        #root.
        dom = impl.createDocument(None, "root", None)
        root = dom.documentElement

        #showStockCount.
        node = dom.createElement("showStockCount")
        root.appendChild(node)
        textNode = dom.createTextNode(str(self._showStockCount))
        node.appendChild(textNode)

        #calmForeColor.
        node = dom.createElement("calmForeColor")
        root.appendChild(node)
        textNode = dom.createTextNode("%06X" % (self._calmForeColor))
        node.appendChild(textNode)

        #gainForeColor.
        node = dom.createElement("gainForeColor")
        root.appendChild(node)
        textNode = dom.createTextNode("%06X" % (self._gainForeColor))
        node.appendChild(textNode)

        #payForeColor.
        node = dom.createElement("payForeColor")
        root.appendChild(node)
        textNode = dom.createTextNode("%06X" % (self._payForeColor))
        node.appendChild(textNode)

        #backColor.
        node = dom.createElement("backColor")
        root.appendChild(node)
        textNode = dom.createTextNode("%06X" % (self._backColor))
        node.appendChild(textNode)

        #showDataTypes.
        node = dom.createElement("showDataTypes")
        root.appendChild(node)
        for showDataType in self._showDataTypes:
            node2 = dom.createElement("showDataType")
            node.appendChild(node2)
            textNode = dom.createTextNode(str(showDataType))
            node2.appendChild(textNode)

        #stockSymbols.
        node = dom.createElement("stockSymbols")
        root.appendChild(node)
        for stockSymbol in self._stockSymbols:
            node2 = dom.createElement("stockSymbol")
            node.appendChild(node2)
            textNode = dom.createTextNode(stockSymbol.decode("gb2312").encode("utf-8"))
            node2.appendChild(textNode)

        #mainWindowPos.
        node = dom.createElement("mainWindowPos")
        root.appendChild(node)
        #x.
        node2 = dom.createElement("x")
        node.appendChild(node2)
        textNode = dom.createTextNode(str(self._mainWindowPos[0]))
        node2.appendChild(textNode)
        #y.
        node2 = dom.createElement("y")
        node.appendChild(node2)
        textNode = dom.createTextNode(str(self._mainWindowPos[1]))
        node2.appendChild(textNode)

        #写入文件。
        f = open(filename, "w")
        dom.writexml(writer = f, encoding = "utf-8")
        f.close()

    def getPropertyValue(self, node):
        if len(node.childNodes) > 0:
            return node.childNodes[0].nodeValue.encode("gb2312")
        return None

if __name__ == "__main__":
    config().load("cfg.xml")
    print type(config()._showStockCount),
    print "\t:",
    print config()._showStockCount
    print type(config()._calmForeColor),
    print "\t:",
    print config()._calmForeColor
    print type(config()._gainForeColor),
    print "\t:",
    print config()._gainForeColor
    print type(config()._payForeColor),
    print "\t:",
    print config()._payForeColor
    print type(config()._backColor),
    print "\t:",
    print config()._backColor
    print type(config()._showDataTypes),
    print "\t:",
    print config()._showDataTypes
    print type(config()._stockSymbols),
    print "\t:",
    print config()._stockSymbols
    print type(config()._mainWindowPos),
    print "\t:",
    print config()._mainWindowPos
    config().save("cfg.xml")
