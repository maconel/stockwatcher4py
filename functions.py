# -*- coding: gb2312 -*-

import wx

#��һ��long�͵�rgbֵתΪwxColor.
def rgbToWxcolor(rgb):
    return wx.Color((rgb & 0xFF0000) >> 16, (rgb & 0x00FF00) >> 8, rgb & 0x0000FF)

#��һ��wxColorתΪlong�͵�rgbֵ.
def wxcolorToRgb(color):
    return (color.Red() << 16) | (color.Green() << 8) | (color.Blue())
