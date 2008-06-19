# -*- coding: gb2312 -*-

import wx

import stockCenter
import period
import config
import stock
import settingDlg
import functions

class MainFrame(wx.Frame):
    #初始化。
    def __init__(self):
        #初始化成员。
        self._originalMousePos = None                               #上次鼠标位置。
        self._currentStockIndexs = []                               #当前指向哪支股票。
        self._stockCenter = stockCenter.StockCenter(self.onUpdate)  #股票中心。
        self._period = period.Period(self.onTime)                   #用来定时切换股票的定时器。
        self._period.setInterval(5)                                 #多久切换一次当前股票。
        self._settingData = None                                    #设置数据。

        #载入config.
        self.loadConfig()

        #初始化控件。
        wx.Frame.__init__(self, parent = None, id = wx.ID_ANY, title = "Stock watcher", pos = self._originalMousePos, size = (0, 0), style = wx.NO_BORDER | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR)
        self._backPanel = wx.Panel(self, size = self.GetClientSize())
        self._stockStaticTexts = []
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        #创建右下角图标。
        icon = wx.Icon("stockWatcher.ico", wx.BITMAP_TYPE_ICO)
        self._taskBarIcon = wx.TaskBarIcon()
        self._taskBarIcon.SetIcon(icon, "Stock Watcher")

        #菜单。
        self._menu = wx.Menu()
        menuItemSetting = self._menu.Append(wx.ID_ANY, "设置")
        self._menu.AppendSeparator()
        menuItemExit = self._menu.Append(wx.ID_ANY, "退出")

        #绑定事件。
        self.Bind(wx.EVT_MOUSE_EVENTS, self.onMouseEvent)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self._backPanel.Bind(wx.EVT_MOUSE_EVENTS, self.onMouseEvent)
        self._taskBarIcon.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.onTaskBarLButtonDown)
        self._taskBarIcon.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, self.onTaskBarRButtonDown)
        self._menu.Bind(wx.EVT_MENU, self.onNemuItemSetting, menuItemSetting)
        self._menu.Bind(wx.EVT_MENU, self.onNemuItemExit, menuItemExit)

        #设置属性。
        self.setShowStockCount(self._settingData._showStockCount)
        self.setForeColor(-1, self._settingData._calmForeColor)
        self.setBackColor(self._settingData._backColor)

        #显示窗体。
        self.Show(True)

        #启动一些东西。
        self.onTime()
        self._stockCenter.start()
        self._period.start()

    #鼠标事件。
    def onMouseEvent(self, event):
        #找到是谁引发的事件。
        control = self.FindWindowById(event.GetId())
        if control == None:
            control = self
        #左键按下时，记录鼠标位置，并捕获它。
        if event.LeftDown():
            self._originalMousePos = event.GetPosition()
            control.CaptureMouse()
        #左键抬起时，释放鼠标。
        elif event.LeftUp():
            if control.HasCapture():
                control.ReleaseMouse()
        elif event.RightDown():
            self._taskBarIcon.PopupMenu(self._menu)
        #拖拽时，拖动窗口。
        elif event.Dragging() and event.LeftIsDown():
            self.Move(self.GetPosition() + event.GetPosition() - self._originalMousePos)

    #关闭窗体。
    def onClose(self, event):
        self._stockCenter.stop()
        self._period.stop()
        self.Destroy()
        self.saveConfig()

    #当左键按下任务栏中的图标。
    def onTaskBarLButtonDown(self, event):
        self.Iconize(not self.IsIconized())
        self.Show(not self.IsIconized())

    #当右键按下任务栏中的图标。
    def onTaskBarRButtonDown(self, event):
        self._taskBarIcon.PopupMenu(self._menu)

    #点了setting菜单项。
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

    #点了exit菜单项。
    def onNemuItemExit(self, event):
        self.Close()

    #收到更新的通知。
    def onUpdate(self):
        self.onTime()

    #到时间了，切换stock.
    def onTime(self):
        self.getCurrentStocks()
        i = 0
        #依次下每个股票数据。
        for index in self._currentStockIndexs:
            #如果index是正常范围的，才取它的数据。
            if -1 < index < len(self._stockCenter._stocks):
                #显示所有要求显示的。
                data = ""
                for dataType in self._settingData._showDataTypes:
                    data += self._stockCenter._stocks[index]._datas[dataType]
                    data += " | "
                self._stockStaticTexts[i].SetLabel(data)
                #得到涨跌额。
                #如果只有一个"-"，表示没开盘。
                if self._stockCenter._stocks[index]._datas[stock.Stock.MARKUP_VALUE] == "-":
                    markupValue = 0
                else:
                    markupValue = float(self._stockCenter._stocks[index]._datas[stock.Stock.MARKUP_VALUE])
                #如果涨跌额为负，就显示赔钱颜色。
                if markupValue < 0:
                    self.setForeColor(i, self._settingData._payForeColor)
                #如果为正，就显示赚钱颜色。
                elif markupValue > 0:
                    self.setForeColor(i, self._settingData._gainForeColor)
                #否则显示持平颜色。
                else:
                    self.setForeColor(i, self._settingData._calmForeColor)
            #否则什么也不显示。
            else:
                self._stockStaticTexts[i].SetLabel("")
            i += 1
        #改变窗体大小。
        self._backPanel.SetSize(self.GetSizer().GetMinSize())
        self.SetSize(self.GetSizer().GetMinSize())

    #计算当前应该显示哪些股票。
    def getCurrentStocks(self):
        #如果有股票。
        if len(self._stockCenter._stocks) > 0:
            #如果以前曾经算过，就从上一次的最后一个的下一个开始往下轮。
            if len(self._currentStockIndexs) > 0:
                stockIndex = self._currentStockIndexs[-1]
                stockIndex += 1
                if stockIndex >= len(self._stockCenter._stocks):
                    stockIndex = 0
            #否则动第一个开始轮。
            else:
                stockIndex = 0
            #循环得到股票下标。
            stockCount = len(self._stockStaticTexts)
            self._currentStockIndexs = []
            for i in range(0, stockCount):
                self._currentStockIndexs.append(stockIndex)
                stockIndex += 1     #这里只管加1，超出范围也没关系，显示的时候会处理。
        #如果一个也没有。
        else:
            self._currentStockIndexs = []

    #设置前景色。index指定设置哪个StaticText的前景色，为-1表示设置所有的。
    def setForeColor(self, index, foreColor):
        if index == -1:
            for stockStaticText in self._stockStaticTexts:
                stockStaticText.SetForegroundColour(functions.rgbToWxcolor(foreColor))
        else:
            self._stockStaticTexts[index].SetForegroundColour(functions.rgbToWxcolor(foreColor))

    #设置背景色。
    def setBackColor(self, backColor):
        self.SetBackgroundColour(functions.rgbToWxcolor(backColor))

    #设置同时显示的股票数。
    def setShowStockCount(self, count):
        self.GetSizer().Clear()
        self._stockStaticTexts = []
        for i in range(0, count):
            stockStaticText = wx.StaticText(self._backPanel, wx.ID_ANY)
            stockStaticText.Bind(wx.EVT_MOUSE_EVENTS, self.onMouseEvent)
            self.GetSizer().Add(stockStaticText)
            self._stockStaticTexts.append(stockStaticText)

    #载入config.
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

    #保存config.
    def saveConfig(self):
        config.config()._mainWindowPos = self.GetPosition()
        config.config()._showStockCount = self._settingData._showStockCount
        config.config()._calmForeColor = self._settingData._calmForeColor
        config.config()._gainForeColor = self._settingData._gainForeColor
        config.config()._payForeColor = self._settingData._payForeColor
        config.config()._backColor = self._settingData._backColor
        config.config()._showDataTypes = self._settingData._showDataTypes
        config.config()._stockSymbols = self._settingData._stockSymbols
