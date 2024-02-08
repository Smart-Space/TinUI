'''
TinUI的控件整合展示
考虑到TinUI.py的测试界面比较杂乱，可能会在下一个大版本（5.0）中启用该界面展示/测试文件
TinUI.py的测试部分仍然保持最新状态，本文件以及从属文件（./testpage）也会持续更新
'''
import sys
sys.path.append('..')
from TinUI import *
from tkinter import Tk


def loadcontrol(controlname):
    #导入控件说明
    cfile=open("test/testpage/"+controlname+".xml",mode='r',encoding='utf-8')
    cxml=cfile.read()
    cfile.close()
    duixml.clean()
    duixml.loadxml(cxml)


xmlf=open(r'test\testpage\main.xml','r')
xml=xmlf.read()
xmlf.close()

window = Tk()
window.resizable(False,False)
window.iconbitmap('LOGO.ico')
window.title("TinUI main test")
window.geometry("850x600+5+5")
ui=BasicTinUI(window)
uix=TinUIXml(ui)

uix.funcs['loadcontrol']=loadcontrol
uix.datas['controls']=['back', 'button', 'button2', 'canvas', 'checkbutton', 
 'combobox', 'entry', 'expander', 'image', 'info', 'label', 'labelframe',
 'link', 'listbox', 'listview', 'menubar', 'menubutton', 'notebook', 'notecard', 
 'onoff', 'paragraph', 'passwordbox', 'picker', 'pipspager', 'pivot', 'progressbar', 
 'radiobox', 'radiobutton', 'ratingbar', 'scalebar', 'scrollbar', 'separate', 
 'spinbox', 'swipecontrol', 'table', 'textbox', 'title', 'togglebutton', 'tooltip', 
 'treeview', 'ui', 'waitbar1', 'waitbar2', 'waitbar3', 'waitframe']
uix.loadxml(xml)
displayui,_,duixml,_=uix.tags['displayui']

ui.pack(fill='both',expand=True)
window.mainloop()