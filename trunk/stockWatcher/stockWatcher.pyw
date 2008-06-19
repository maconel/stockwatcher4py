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
    #读配置文件。
    config.config().load("cfg.xml")

    app = App(0)
    app.MainLoop()

    #写配置文件。
    config.config().save("cfg.xml")
