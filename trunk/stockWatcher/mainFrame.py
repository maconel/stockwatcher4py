# -*- coding: gb2312 -*-

import wx

import stockCenter
import period
import config
import stock
import settingDlg

#��һ��long�͵�rgbֵתΪwxColor.
def rgbToWxcolor(rgb):
    return wx.Color((rgb & 0xFF0000) >> 16, (rgb & 0x00FF00) >> 8, rgb & 0x0000FF)

#��һ��wxColorתΪlong�͵�rgbֵ.
def wxcolorToRgb(color):
    return (color.Red() << 16) | (color.Green() << 8) | (color.Blue())

class MainFrame(wx.Frame):
    #��ʼ����
    def __init__(self):
        #��ʼ����Ա��
        self._originalMousePos = wx.Point(0, 0)                     #�ϴ����λ�á�
        self._currentStockIndexs = []                               #��ǰָ����֧��Ʊ��
        self._stockCenter = stockCenter.StockCenter(self.onUpdate)  #��Ʊ���ġ�
        self._period = period.Period(self.onTime)                   #������ʱ�л���Ʊ�Ķ�ʱ����
        self._period.setInterval(5)                                 #����л�һ�ε�ǰ��Ʊ��

        #��ʼ���ؼ���
        wx.Frame.__init__(self, parent = None, id = wx.ID_ANY, title = "Stock watcher", pos = config.config()._mainWindowPos, size = (0, 0), style = wx.NO_BORDER | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR)
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
        self.setShowStockCount(config.config()._showStockCount)
        self.setForeColor(-1, config.config()._calmForeColor)
        self.setBackColor(config.config()._backColor)

        #��ʾ���塣
        self.Show(True)

        #����һЩ������
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
        #��קʱ���϶����ڡ�
        elif event.Dragging() and event.LeftIsDown():
            self.Move(self.GetPosition() + event.GetPosition() - self._originalMousePos)
            config.config()._mainWindowPos = self.GetPosition()

    #�رմ��塣
    def onClose(self, event):
        self._stockCenter.stop()
        self._period.stop()
        self.Destroy()

    #����������������е�ͼ�ꡣ
    def onTaskBarLButtonDown(self, event):
        self.Iconize(not self.IsIconized())
        self.Show(not self.IsIconized())

    #���Ҽ������������е�ͼ�ꡣ
    def onTaskBarRButtonDown(self, event):
        self._taskBarIcon.PopupMenu(self._menu)

    #����setting�˵��
    def onNemuItemSetting(self, event):
        dlg = settingDlg.SettingDlg()
        if dlg.ShowModal() == wx.ID_OK:
            config.config()._showStockCount = dlg._stockCountSpinCtrl.GetValue()
            config.config()._calmForeColor = wxcolorToRgb(dlg._calmColorSettingCtrl._color)
            config.config()._gainForeColor = wxcolorToRgb(dlg._gainColorSettingCtrl._color)
            config.config()._payForeColor = wxcolorToRgb(dlg._payColorSettingCtrl._color)
            config.config()._backColor = wxcolorToRgb(dlg._backColorSettingCtrl._color)
#            config.config()._showDataTypes = []
            self._stockCenter.setStockSymbols(dlg._stockListBox.GetStrings())

    #����exit�˵��
    def onNemuItemExit(self, event):
        self.Close()

    #�յ����µ�֪ͨ��
    def onUpdate(self):
        pass

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
                for dataType in config.config()._showDataTypes:
                    data += self._stockCenter._stocks[index]._datas[dataType][0]
                    data += " "
                self._stockStaticTexts[i].SetLabel(data)
                #�õ��ǵ��
                #���ֻ��һ��"-"����ʾû���̡�
                if self._stockCenter._stocks[index]._datas[stock.Stock.MARKUP_VALUE][0] == "-":
                    markupValue = 0
                else:
                    markupValue = float(self._stockCenter._stocks[index]._datas[stock.Stock.MARKUP_VALUE][0])
                #����ǵ���Ϊ��������ʾ��Ǯ��ɫ��
                if markupValue < 0:
                    self.setForeColor(i, config.config()._payForeColor)
                #���Ϊ��������ʾ׬Ǯ��ɫ��
                elif markupValue > 0:
                    self.setForeColor(i, config.config()._gainForeColor)
                #������ʾ��ƽ��ɫ��
                else:
                    self.setForeColor(i, config.config()._calmForeColor)
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
                stockStaticText.SetForegroundColour(rgbToWxcolor(foreColor))
        else:
            self._stockStaticTexts[index].SetForegroundColour(rgbToWxcolor(foreColor))

    #���ñ���ɫ��
    def setBackColor(self, backColor):
        self.SetBackgroundColour(rgbToWxcolor(backColor))

    #����ͬʱ��ʾ�Ĺ�Ʊ����
    def setShowStockCount(self, count):
        self.GetSizer().Clear()
        self._stockStaticTexts = []
        for i in range(0, count):
            stockStaticText = wx.StaticText(self._backPanel, wx.ID_ANY)
            stockStaticText.Bind(wx.EVT_MOUSE_EVENTS, self.onMouseEvent)
            self.GetSizer().Add(stockStaticText)
            self._stockStaticTexts.append(stockStaticText)
