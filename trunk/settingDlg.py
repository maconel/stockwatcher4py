# -*- coding: gb2312 -*-

import wx

import colorSettingCtrl
import stock
import functions

class SettingData:
    def __init__(self, showStockCount = 1, calmForeColor = 0xFFFFFF, gainForeColor = 0xFF0000, payForeColor = 0x00FF00, backColor = 0x000000, showDataTypes = [], stockSymbols = []):
        self._showStockCount = showStockCount   #ͬʱ������ʾ���ٸ���Ʊ��
        self._calmForeColor = calmForeColor     #��׬����ǰ��ɫ��
        self._gainForeColor = gainForeColor     #׬Ǯǰ��ɫ��
        self._payForeColor = payForeColor       #��Ǯǰ��ɫ��
        self._backColor = backColor             #����ɫ��
        self._showDataTypes = showDataTypes     #��ǰ����ʾ��Щ���ݣ������Ʊ������ǰ��ʲô�ġ�
        self._stockSymbols = stockSymbols       #��ǰ����ʾ��Щ��Ʊ��

class SettingDlg(wx.Dialog):
    def __init__(self, settingData, parent):
        PUBLICBUTTON_SIZE = (72, 24)
        CTRL_CX = 4
        CTRL_CY = 8

        self._settingData = settingData

        wx.Dialog.__init__(self, parent = parent, id = wx.ID_ANY, title = "����")

        #��ʼ����Ա��

        #�����ؼ���
        #��panel.
        self._backPanel = wx.Panel(self, size = self.GetClientSize())
        #��ҳ�ؼ���
        COLORSETTINGCTRL_SIZE = (128, 16)
        self._notebook = wx.Notebook(self._backPanel, id = wx.ID_ANY, pos = wx.Point(0, 0), size = wx.Size(self._backPanel.Size.GetWidth(), self._backPanel.Size.GetHeight() - CTRL_CX - PUBLICBUTTON_SIZE[1] - CTRL_CX))
        #����ҳ��
        self._pageGeneral = wx.Panel(self._notebook, pos = wx.Point(0, 0))
        self._notebook.AddPage(self._pageGeneral, "����")
        pos = [20, CTRL_CY]
        self._stockCountStaticText = wx.StaticText(self._pageGeneral, id = wx.ID_ANY, label = "ͬʱ��ʾ��Ʊ������", pos = pos, size = (120, COLORSETTINGCTRL_SIZE[1]))
        pos = [pos[0] + self._stockCountStaticText.GetSize().GetWidth(), self._stockCountStaticText.GetPosition().y]
        self._stockCountSpinCtrl = wx.SpinCtrl(self._pageGeneral, id = wx.ID_ANY, value = str(self._settingData._showStockCount), pos = pos, size = (64, 16), max = 0xFFFF)
        pos = [20, pos[1] + self._stockCountStaticText.GetSize().GetHeight() + CTRL_CY]
        self._calmColorSettingCtrl = colorSettingCtrl.ColorSettingCtrl(self._pageGeneral, "��ƽɫ��", color = functions.rgbToWxcolor(self._settingData._calmForeColor), pos = pos, size = COLORSETTINGCTRL_SIZE)
        pos[1] += CTRL_CY + COLORSETTINGCTRL_SIZE[1]
        self._gainColorSettingCtrl = colorSettingCtrl.ColorSettingCtrl(self._pageGeneral, "��ֵɫ��", color = functions.rgbToWxcolor(self._settingData._gainForeColor), pos = pos, size = COLORSETTINGCTRL_SIZE)
        pos[1] += CTRL_CY + COLORSETTINGCTRL_SIZE[1]
        self._payColorSettingCtrl = colorSettingCtrl.ColorSettingCtrl(self._pageGeneral, "��ֵɫ��", color = functions.rgbToWxcolor(self._settingData._payForeColor), pos = pos, size = COLORSETTINGCTRL_SIZE)
        pos[1] += CTRL_CY + COLORSETTINGCTRL_SIZE[1]
        self._backColorSettingCtrl = colorSettingCtrl.ColorSettingCtrl(self._pageGeneral, "����ɫ��", color = functions.rgbToWxcolor(self._settingData._backColor), pos = pos, size = COLORSETTINGCTRL_SIZE)
        #��Ʊҳ��
        STOCKLISTBOX_POS = (8, 8)
        STOCKBUTTON_SIZE = PUBLICBUTTON_SIZE
        self._pageStock = wx.Panel(self._notebook, pos = wx.Point(0, 0))
        self._notebook.AddPage(self._pageStock, "��Ʊѡ��")
        self._stockListBox = wx.ListBox(self._pageStock, wx.ID_ANY, pos = STOCKLISTBOX_POS, size = (self._pageStock.GetSize().GetWidth() - STOCKLISTBOX_POS[0] * 2, self._pageStock.GetSize().GetHeight() - STOCKLISTBOX_POS[0] * 2 - STOCKBUTTON_SIZE[1] - CTRL_CY))
        self._stockCodeTextCtrl = wx.TextCtrl(self._pageStock, wx.ID_ANY, pos = (STOCKLISTBOX_POS[0], self._stockListBox.GetPosition().y + self._stockListBox.GetSize().GetHeight() + CTRL_CY), size = (self._pageStock.GetSize().GetWidth() - STOCKLISTBOX_POS[0] * 2 - (STOCKBUTTON_SIZE[0] + CTRL_CX) * 4, STOCKBUTTON_SIZE[1]))
        pos = [self._stockCodeTextCtrl.GetPosition().x + self._stockCodeTextCtrl.GetSize().GetWidth() + CTRL_CX, self._stockCodeTextCtrl.GetPosition().y]
        self._addStockButton = wx.Button(self._pageStock, wx.ID_ANY, label = "���", pos = pos, size = (STOCKBUTTON_SIZE))
        pos[0] += CTRL_CX + STOCKBUTTON_SIZE[0]
        self._deleteStockButton = wx.Button(self._pageStock, wx.ID_ANY, label = "ɾ��", pos = pos, size = (STOCKBUTTON_SIZE))
        pos[0] += CTRL_CX + STOCKBUTTON_SIZE[0]
        self._stockUpMoveButton = wx.Button(self._pageStock, wx.ID_ANY, label = "����", pos = pos, size = (STOCKBUTTON_SIZE))
        pos[0] += CTRL_CX + STOCKBUTTON_SIZE[0]
        self._stockDownMoveButton = wx.Button(self._pageStock, wx.ID_ANY, label = "����", pos = pos, size = (STOCKBUTTON_SIZE))
        for symbol in self._settingData._stockSymbols:
            self._stockListBox.Append(symbol)
        #��Ʊ����ѡ��ҳ��
        COLUMNLISTBOX_POS = (8, 8)
        COLUMNBUTTON_SIZE = (24, 24)
        self._pageColumn = wx.Panel(self._notebook, pos = wx.Point(0, 0))
        self._notebook.AddPage(self._pageColumn, "��Ʊ����ѡ��")
        self._unSelectedListBox = wx.ListBox(self._pageColumn, wx.ID_ANY, pos = COLUMNLISTBOX_POS, size = ((self._pageColumn.GetSize().GetWidth() - COLUMNLISTBOX_POS[0] * 2 - COLUMNBUTTON_SIZE[0] - CTRL_CX * 2) / 2, self._pageColumn.GetSize().GetHeight() - COLUMNLISTBOX_POS[1] * 2))
        self._selectedListBox = wx.ListBox(self._pageColumn, wx.ID_ANY, pos = (self._pageColumn.GetSize().GetWidth() - self._unSelectedListBox.GetSize().GetWidth() - COLUMNLISTBOX_POS[0], COLUMNLISTBOX_POS[1]), size = self._unSelectedListBox.GetSize())
        pos = [COLUMNLISTBOX_POS[0] + self._unSelectedListBox.GetSize().GetWidth() + CTRL_CX, (self._pageColumn.GetSize().GetHeight() - (COLUMNBUTTON_SIZE[1] + CTRL_CY) * 4 - CTRL_CY) / 2]
        self._selectButton = wx.Button(self._pageColumn, wx.ID_ANY, label = ">>", pos = pos, size = COLUMNBUTTON_SIZE)
        pos[1] += COLUMNBUTTON_SIZE[1] + CTRL_CY
        self._unSelectButton = wx.Button(self._pageColumn, wx.ID_ANY, label = "<<", pos = pos, size = COLUMNBUTTON_SIZE)
        pos[1] += COLUMNBUTTON_SIZE[1] + CTRL_CY
        self._columnUpMoveButton = wx.Button(self._pageColumn, wx.ID_ANY, label = "��", pos = pos, size = COLUMNBUTTON_SIZE)
        pos[1] += COLUMNBUTTON_SIZE[1] + CTRL_CY
        self._columnDownMoveButton = wx.Button(self._pageColumn, wx.ID_ANY, label = "��", pos = pos, size = COLUMNBUTTON_SIZE)
        for dataTypeKey in stock.Stock.DATA_TYPE_DICT:
            found = False
            for dataType in self._settingData._showDataTypes:
                if dataTypeKey == dataType:
                    found = True
                    break
            if not found:
                self._unSelectedListBox.Append(stock.Stock.DATA_TYPE_DICT[dataTypeKey])
        for dataType in self._settingData._showDataTypes:
            self._selectedListBox.Append(stock.Stock.DATA_TYPE_DICT[dataType])
        #ȷ����ȡ����
        self._cancelButton = wx.Button(self._backPanel, id = wx.ID_ANY, label = "ȡ��", pos = wx.Point(self._backPanel.Size.GetWidth() - PUBLICBUTTON_SIZE[0] - CTRL_CX, self._backPanel.Size.GetHeight() - CTRL_CX - PUBLICBUTTON_SIZE[1]), size = PUBLICBUTTON_SIZE)
        self._okButton = wx.Button(self._backPanel, id = wx.ID_ANY, label = "ȷ��", pos = wx.Point(self._backPanel.Size.GetWidth() - PUBLICBUTTON_SIZE[0] - CTRL_CX - PUBLICBUTTON_SIZE[0] - CTRL_CX, self._backPanel.Size.GetHeight() - CTRL_CX - PUBLICBUTTON_SIZE[1]), size = PUBLICBUTTON_SIZE)

        #���¼���
        self._okButton.Bind(wx.EVT_BUTTON, self.onOkButtonClick)
        self._cancelButton.Bind(wx.EVT_BUTTON, self.onCancelButtonClick)
        self._addStockButton.Bind(wx.EVT_BUTTON, self.onAddStockButtonClick)
        self._deleteStockButton.Bind(wx.EVT_BUTTON, self.onDeleteStockButtonClick)
        self._stockUpMoveButton.Bind(wx.EVT_BUTTON, self.onStockUpMoveButtonClick)
        self._stockDownMoveButton.Bind(wx.EVT_BUTTON, self.onstockDownMoveButtonClick)
        self._selectButton.Bind(wx.EVT_BUTTON, self.onSelectButtonClick)
        self._unSelectButton.Bind(wx.EVT_BUTTON, self.onUnSelectButtonClick)
        self._columnUpMoveButton.Bind(wx.EVT_BUTTON, self.onColumnUpMoveButtonClick)
        self._columnDownMoveButton.Bind(wx.EVT_BUTTON, self.onColumnDownMoveButtonClick)

    #ok�¼���
    def onOkButtonClick(self, event):
        self._settingData._showStockCount = self._stockCountSpinCtrl.GetValue()
        self._settingData._calmForeColor = functions.wxcolorToRgb(self._calmColorSettingCtrl._color)
        self._settingData._gainForeColor = functions.wxcolorToRgb(self._gainColorSettingCtrl._color)
        self._settingData._payForeColor = functions.wxcolorToRgb(self._payColorSettingCtrl._color)
        self._settingData._backColor = functions.wxcolorToRgb(self._backColorSettingCtrl._color)
        self._settingData._showDataTypes = []
        for dataTypeString in self._selectedListBox.GetStrings():
            self._settingData._showDataTypes.append(stock.indexDataType(dataTypeString.encode("gb2312")))
        self._settingData._stockSymbols = self._stockListBox.GetStrings()
        if self.IsModal():
            self.EndModal(wx.ID_OK)
        else:
            self.Close()

    #cancel�¼���
    def onCancelButtonClick(self, event):
        if self.IsModal():
            self.EndModal(wx.ID_CANCEL)
        else:
            self.Close()

    #addStock�¼���
    def onAddStockButtonClick(self, event):
        self._stockListBox.Append(self._stockCodeTextCtrl.GetValue())

    #deleteStock�¼���
    def onDeleteStockButtonClick(self, event):
        self.deleteListBoxSelection(self._stockListBox)

    #stociUpMove�¼���
    def onStockUpMoveButtonClick(self, event):
        selectIndex = self._stockListBox.GetSelection()
        if selectIndex <> wx.NOT_FOUND:
            self.swapListBoxItem(self._stockListBox, selectIndex, selectIndex - 1)
            if selectIndex - 1 >= 0:
                self._stockListBox.SetSelection(selectIndex - 1)

    #stockDownMove�¼���
    def onstockDownMoveButtonClick(self, event):
        selectIndex = self._stockListBox.GetSelection()
        if selectIndex <> wx.NOT_FOUND:
            self.swapListBoxItem(self._stockListBox, selectIndex, selectIndex + 1)
            if selectIndex + 1 < self._stockListBox.GetCount():
                self._stockListBox.SetSelection(selectIndex + 1)

    #select�¼���
    def onSelectButtonClick(self, event):
        selectIndex = self._unSelectedListBox.GetSelection()
        if selectIndex <> wx.NOT_FOUND:
            self._selectedListBox.Append(self._unSelectedListBox.GetString(selectIndex))
            self.deleteListBoxSelection(self._unSelectedListBox)

    #unSelect�¼���
    def onUnSelectButtonClick(self, event):
        selectIndex = self._selectedListBox.GetSelection()
        if selectIndex <> wx.NOT_FOUND:
            self._unSelectedListBox.Append(self._selectedListBox.GetString(selectIndex))
            self.deleteListBoxSelection(self._selectedListBox)

    #columnUpMove�¼���
    def onColumnUpMoveButtonClick(self, event):
        selectIndex = self._selectedListBox.GetSelection()
        if selectIndex <> wx.NOT_FOUND:
            self.swapListBoxItem(self._selectedListBox, selectIndex, selectIndex - 1)
            if selectIndex - 1 >= 0:
                self._selectedListBox.SetSelection(selectIndex - 1)

    #columnDownMove�¼���
    def onColumnDownMoveButtonClick(self, event):
        selectIndex = self._selectedListBox.GetSelection()
        if selectIndex <> wx.NOT_FOUND:
            self.swapListBoxItem(self._selectedListBox, selectIndex, selectIndex + 1)
            if selectIndex + 1 < self._selectedListBox.GetCount():
                self._selectedListBox.SetSelection(selectIndex + 1)

    #����listbox�е�2�
    def swapListBoxItem(self, listbox, index1, index2):
        if 0 <= index1 < listbox.GetCount() and 0 <= index2 < listbox.GetCount():
            value1 = listbox.GetString(index1)
            value2 = listbox.GetString(index2)
            listbox.SetString(index1, value2)
            listbox.SetString(index2, value1)

    #��listbox��ɾȥһ�
    def deleteListBoxSelection(self, listbox):
        selectIndex = listbox.GetSelection()
        if selectIndex <> wx.NOT_FOUND:
            if 0 <= selectIndex < listbox.GetCount():
                listbox.Delete(selectIndex)
                if selectIndex < listbox.GetCount():
                    listbox.SetSelection(selectIndex)
                else:
                    listbox.SetSelection(listbox.GetCount() - 1)
            

if __name__ == "__main__":
    class App(wx.App):
        def OnInit(self):
            frame = SettingDlg(SettingData())
            frame.Show()
            return True

    app = App(0)
    app.MainLoop()
