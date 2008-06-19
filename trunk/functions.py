# -*- coding: gb2312 -*-

import wx

#将一个long型的rgb值转为wxColor.
def rgbToWxcolor(rgb):
    return wx.Color((rgb & 0xFF0000) >> 16, (rgb & 0x00FF00) >> 8, rgb & 0x0000FF)

#将一个wxColor转为long型的rgb值.
def wxcolorToRgb(color):
    return (color.Red() << 16) | (color.Green() << 8) | (color.Blue())
