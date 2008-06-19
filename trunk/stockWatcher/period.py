# -*- coding: gb2312 -*-

import threading

class Period:
    #初始化。
    def __init__(self, onTime):
        self._interval = 1      #时间间隔默认为1秒。
        self._ontime = onTime
        self._timer = None

    #启动定时器，如果已经启动则不再启动。如果immediatelyOntime为True，则立即产生一个onTime事件。
    def start(self, immediatelyOntime = True):
        if self._timer == None:
            self._timer = threading.Timer(self._interval, self.onTime)
            self._timer.start()
            if immediatelyOntime:
                self.onTime(False)

    #停止定时器。
    def stop(self):
        if self._timer <> None:
            self._timer.cancel()
            self._timer = None

    #设置时间间隔。将会自动重启定时器，但不会立即产生一个onTime事件。
    def setInterval(self, interval):
        self._interval = interval
        if self._timer <> None:
            self.stop()
            self.start(False)

    #到时间了。
    def onTime(self, again = True):
        if again:
            self.stop()
            self.start(False)
        if self._ontime <> None:
            self._ontime()
