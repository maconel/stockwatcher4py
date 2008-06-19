# -*- coding: gb2312 -*-

import wx

class ColorSettingCtrl(wx.Panel):
    def __init__(self, parent, label, color = wx.RED, pos = wx.DefaultPosition, size = wx.DefaultSize):
        COLORCTRL_WIDTH = 64

        wx.Panel.__init__(self, parent = parent, id = wx.ID_ANY, pos = pos, size = size)

        #��ʼ����Ա��
        self._color = None

        #�����ؼ���
        self._label = wx.StaticText(self, wx.ID_ANY, label = label, pos = wx.Point(0, 0), size = wx.Size(self.GetSize().GetWidth() - COLORCTRL_WIDTH, self.GetSize().GetHeight()))
        self._colorCtrl = wx.Panel(self, wx.ID_ANY, pos = wx.Point(self._label.GetSize().GetWidth(), 0), size = wx.Size(COLORCTRL_WIDTH, self.GetSize().GetHeight()))

        #�������ԡ�
        self.setColor(color)

        #���¼���
        self._colorCtrl.Bind(wx.EVT_MOUSE_EVENTS, self.onColorCtrlMouseEvent)

    #���color�ؼ���
    def onColorCtrlMouseEvent(self, event):
        #������¡�
        if event.LeftDown():
            colourData = wx.ColourData()
            colourData.SetColour(self._color)
            dlg = wx.ColourDialog(self, colourData)
            if dlg.ShowModal() == wx.ID_OK:
                self._color = dlg.GetColourData().GetColour()
                self._colorCtrl.SetBackgroundColour(self._color)
                self._colorCtrl.Refresh()

    #���ñ��⡣
    def setLabel(self, label):
        self._label.SetLabel(label)

    #���ñ��⡣
    def setColor(self, color):
        self._color = color
        self._colorCtrl.SetBackgroundColour(self._color)
