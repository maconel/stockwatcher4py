# -*- coding: gb2312 -*-

import wx

import mainFrame
import config

class App(wx.App):
    def OnInit(self):
        frame = mainFrame.MainFrame()
        self.SetTopWindow(frame)
        return True;

if __name__ == "__main__":
    #�������ļ���
    config.config().load("cfg.xml")

    app = App(0)
    app.MainLoop()

    #д�����ļ���
    config.config().save("cfg.xml")
