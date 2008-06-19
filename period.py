# -*- coding: gb2312 -*-

import threading

class Period:
    #��ʼ����
    def __init__(self, onTime):
        self._interval = 1      #ʱ����Ĭ��Ϊ1�롣
        self._ontime = onTime
        self._timer = None

    #������ʱ��������Ѿ������������������immediatelyOntimeΪTrue������������һ��onTime�¼���
    def start(self, immediatelyOntime = True):
        if self._timer == None:
            self._timer = threading.Timer(self._interval, self.onTime)
            self._timer.start()
            if immediatelyOntime:
                self.onTime(False)

    #ֹͣ��ʱ����
    def stop(self):
        if self._timer <> None:
            self._timer.cancel()
            self._timer = None

    #����ʱ�����������Զ�������ʱ������������������һ��onTime�¼���
    def setInterval(self, interval):
        self._interval = interval
        if self._timer <> None:
            self.stop()
            self.start(False)

    #��ʱ���ˡ�
    def onTime(self, again = True):
        if again:
            self.stop()
            self.start(False)
        if self._ontime <> None:
            self._ontime()
