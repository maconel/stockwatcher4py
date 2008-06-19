
import os
import shutil

from distutils.core import setup
import py2exe

setup(windows = ["stockWatcher.pyw"])

shutil.copyfile("cfg.xml", ".\\dist\\cfg.xml")
shutil.copyfile("stockWatcher.ico", ".\\dist\\stockWatcher.ico")
