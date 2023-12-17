'''
TinUI的控件整合展示
考虑到TinUI.py的测试界面比较杂乱，可能会在下一个大版本（5.0）中启用该界面展示/测试文件
TinUI.py的测试部分仍然保持最新状态，本文件以及从属文件（./testpage）也会持续更新
'''
import sys
sys.path.append('..')
from TinUI import *
from tkinter import Tk




xmlf=open(r'test\testpage\main.xml','r')
xml=xmlf.read()
xmlf.close()

window = Tk()
window.iconbitmap('LOGO.ico')
window.title("TinUI main test")
window.geometry("850x600+5+5")
ui=BasicTinUI(window)
uix=TinUIXml(ui)
uix.loadxml(xml)
ui.pack(fill='both',expand=True)
window.mainloop()