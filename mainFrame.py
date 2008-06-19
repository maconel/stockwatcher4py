# -*- coding: gb2312 -*-

import wx

import stockCenter
import period
import config
import stock
import settingDlg
import functions

class MainFrame(wx.Frame):
    #��ʼ����
    def __init__(self):
        #��ʼ����Ա��
        self._originalMousePos = None                               #�ϴ����λ�á�
        self._currentStockIndexs = []                               #��ǰָ����֧��Ʊ��
        self._stockCenter = stockCenter.StockCenter(self.onUpdate)  #��Ʊ���ġ�
        self._period = period.Period(self.onTime)                   #������ʱ�л���Ʊ�Ķ�ʱ����
        self._period.setInterval(5)                                 #����л�һ�ε�ǰ��Ʊ��
        self._settingData = None                                    #�������ݡ�

        #����config.
        self.loadConfig()

        #��ʼ���ؼ���
        wx.Frame.__init__(self, parent = None, id = wx.ID_ANY, title = "Stock watcher", pos = self._originalMousePos, size = (0, 0), style = wx.NO_BORDER | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR)
        self._backPanel = wx.Panel(self, size = self.GetClientSize())
        self._stockStaticTexts = []
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        #�������½�ͼ�ꡣ
        icon = wx.Icon("stockWatcher.ico", wx.BITMAP_TYPE_ICO)
        self._taskBarIcon = wx.TaskBarIcon()
        self._taskBarIcon.SetIcon(icon, "Stock Watcher")

        #�˵���
        self._menu = wx.Menu()
        menuItemSetting = self._menu.Append(wx.ID_ANY, "����")
        self._menu.AppendSeparator()
        menuItemExit = self._menu.Append(wx.ID_ANY, "�˳�")

        #���¼���
        self.Bind(wx.EVT_MOUSE_EVENTS, self.onMouseEvent)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self._backPanel.Bind(wx.EVT_MOUSE_EVENTS, self.onMouseEvent)
        self._taskBarIcon.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.onTaskBarLButtonDown)
        self._taskBarIcon.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, self.onTaskBarRButtonDown)
        self._menu.Bind(wx.EVT_MENU, self.onNemuItemSetting, menuItemSetting)
        self._menu.Bind(wx.EVT_MENU, self.onNemuItemExit, menuItemExit)

        #�������ԡ�
        self.setShowStockCount(self._settingData._showStockCount)
        self.setForeColor(-1, self._settingData._calmForeColor)
        self.setBackColor(self._settingData._backColor)

        #��ʾ���塣
        self.Show(True)

        #����һЩ������
        self.onTime()
        self._stockCenter.start()
        self._period.start()

    #����¼���
    def onMouseEvent(self, event):
        #�ҵ���˭�������¼���
        control = self.FindWindowById(event.GetId())
        if control == None:
            control = self
        #�������ʱ����¼���λ�ã�����������
        if event.LeftDown():
            self._originalMousePos = event.GetPosition()
            control.CaptureMouse()
        #���̧��ʱ���ͷ���ꡣ
        elif event.LeftUp():
            if control.HasCapture():
                control.ReleaseMouse()
        elif event.RightDown():
            self._taskBarIcon.PopupMenu(self._menu)
        #��קʱ���϶����ڡ�
        elif event.Dragging() and event.LeftIsDown():
            self.Move(self.GetPosition() + event.GetPosition() - self._originalMousePos)

    #�رմ��塣
    def onClose(self, event):
        self._stockCenter.stop()
        self._period.stop()
        self.Destroy()
        self.saveConfig()

    #����������������е�ͼ�ꡣ
    def onTaskBarLButtonDown(self, event):
        self.Iconize(not self.IsIconized())
        self.Show(not self.IsIconized())

    #���Ҽ������������е�ͼ�ꡣ
    def onTaskBarRButtonDown(self, event):
        self._taskBarIcon.PopupMenu(self._menu)

    #����setting�˵��
    def onNemuItemSetting(self, event):
        dlg = settingDlg.SettingDlg(self._settingData, self)
        if dlg.ShowModal() == wx.ID_OK:
            self._currentStockIndexs = []
            self._stockCenter.setStockSymbols(self._settingData._stockSymbols)
            self.onTime()
            self._stockCenter.update()
            self.onTime()
            self.setShowStockCount(self._settingData._showStockCount)
            self.setBackColor(self._settingData._backColor)

    #����exit�˵��
    def onNemuItemExit(self, event):
        self.Close()

    #�յ����µ�֪ͨ��
    def onUpdate(self):
        self.onTime()

    #��ʱ���ˣ��л�stock.
    def onTime(self):
        self.getCurrentStocks()
        i = 0
        #������ÿ����Ʊ���ݡ�
        for index in self._currentStockIndexs:
            #���index��������Χ�ģ���ȡ�������ݡ�
            if -1 < index < len(self._stockCenter._stocks):
                #��ʾ����Ҫ����ʾ�ġ�
                data = ""
                for dataType in self._settingData._showDataTypes:
                    data += self._stockCenter._stocks[index]._datas[dataType]
                    data += " | "
                self._stockStaticTexts[i].SetLabel(data)
                #�õ��ǵ��
                #���ֻ��һ��"-"����ʾû���̡�
                if self._stockCenter._stocks[index]._datas[stock.Stock.MARKUP_VALUE] == "-":
                    markupValue = 0
                else:
                    markupValue = float(self._stockCenter._stocks[index]._datas[stock.Stock.MARKUP_VALUE])
                #����ǵ���Ϊ��������ʾ��Ǯ��ɫ��
                if markupValue < 0:
                    self.setForeColor(i, self._settingData._payForeColor)
                #���Ϊ��������ʾ׬Ǯ��ɫ��
                elif markupValue > 0:
                    self.setForeColor(i, self._settingData._gainForeColor)
                #������ʾ��ƽ��ɫ��
                else:
                    self.setForeColor(i, self._settingData._calmForeColor)
            #����ʲôҲ����ʾ��
            else:
                self._stockStaticTexts[i].SetLabel("")
            i += 1
        #�ı䴰���С��
        self._backPanel.SetSize(self.GetSizer().GetMinSize())
        self.SetSize(self.GetSizer().GetMinSize())

    #���㵱ǰӦ����ʾ��Щ��Ʊ��
    def getCurrentStocks(self):
        #����й�Ʊ��
        if len(self._stockCenter._stocks) > 0:
            #�����ǰ����������ʹ���һ�ε����һ������һ����ʼ�����֡�
            if len(self._currentStockIndexs) > 0:
                stockIndex = self._currentStockIndexs[-1]
                stockIndex += 1
                if stockIndex >= len(self._stockCenter._stocks):
                    stockIndex = 0
            #���򶯵�һ����ʼ�֡�
            else:
                stockIndex = 0
            #ѭ���õ���Ʊ�±ꡣ
            stockCount = len(self._stockStaticTexts)
            self._currentStockIndexs = []
            for i in range(0, stockCount):
                self._currentStockIndexs.append(stockIndex)
                stockIndex += 1     #����ֻ�ܼ�1��������ΧҲû��ϵ����ʾ��ʱ��ᴦ��
        #���һ��Ҳû�С�
        else:
            self._currentStockIndexs = []

    #����ǰ��ɫ��indexָ�������ĸ�StaticText��ǰ��ɫ��Ϊ-1��ʾ�������еġ�
    def setForeColor(self, index, foreColor):
        if index == -1:
            for stockStaticText in self._stockStaticTexts:
                stockStaticText.SetForegroundColour(functions.rgbToWxcolor(foreColor))
        else:
            self._stockStaticTexts[index].SetForegroundColour(functions.rgbToWxcolor(foreColor))

    #���ñ���ɫ��
    def setBackColor(self, backColor):
        self.SetBackgroundColour(functions.rgbToWxcolor(backColor))

    #����ͬʱ��ʾ�Ĺ�Ʊ����
    def setShowStockCount(self, count):
        self.GetSizer().Clear()
        self._stockStaticTexts = []
        for i in range(0, count):
            stockStaticText = wx.StaticText(self._backPanel, wx.ID_ANY)
            stockStaticText.Bind(wx.EVT_MOUSE_EVENTS, self.onMouseEvent)
            self.GetSizer().Add(stockStaticText)
            self._stockStaticTexts.append(stockStaticText)

    #����config.
    def loadConfig(self):
        self._originalMousePos = config.config()._mainWindowPos
        self._settingData = settingDlg.SettingData(\
            config.config()._showStockCount,\
            config.config()._calmForeColor,\
            config.config()._gainForeColor,\
            config.config()._payForeColor,\
            config.config()._backColor,\
            config.config()._showDataTypes,\
            config.config()._stockSymbols)

    #����config.
    def saveConfig(self):
        config.config()._mainWindowPos = self.GetPosition()
        config.config()._showStockCount = self._settingData._showStockCount
        config.config()._calmForeColor = self._settingData._calmForeColor
        config.config()._gainForeColor = self._settingData._gainForeColor
        config.config()._payForeColor = self._settingData._payForeColor
        config.config()._backColor = self._settingData._backColor
        config.config()._showDataTypes = self._settingData._showDataTypes
        config.config()._stockSymbols = self._settingData._stockSymbols
