'''
TinUI的控件整合展示
考虑到TinUI.py的测试界面比较杂乱，大版本（5.0）中启用该界面展示/测试文件
TinUI.py的测试部分仍然保持最新状态，本文件以及从属文件（./testpage）也会持续更新
'''
import sys
import os
sys.path.append('..')
from TinUI import *
from tkinter import Tk
path=os.path.dirname(os.path.abspath(__file__))

load_menubar=False

def opentutest(e):
    exec(open("tuxmltest.py",encoding='utf-8').read(),{'__file__':os.path.dirname(__file__)+r'\tuxmltest.py'})

def loadcontrol(controlname):
    global load_menubar
    #导入控件说明
    cfile=open("testpage/"+controlname+".xml",mode='r',encoding='utf-8')
    cxml=cfile.read()
    cfile.close()
    duixml.clean()

    duixml.funcs["opentutest"] = opentutest
    
    duixml.loadxml(cxml)
    if controlname=='canvas':
        canvas=duixml.tags['canvas'][0]
        canvas.create_text((5,5),text='画布对象：文字。\n需要获取add_canvas的第一个返回值',font='微软雅黑 12',anchor='nw')
    elif controlname=='expander':
        expander=duixml.tags['expander'][2]
        expander.loadxml('''<tinui><line>
        <button2 text='拓展UI框架的按钮'></button2></line>
        <line>
        <paragraph text='拓展UI框架可以节省布局位置，能够使用TinUIXml为可拓展UI框架编写界面布局。' width='190'></paragraph>
        </line>
        <line><paragraph text='感觉如何？' width='190'></paragraph></line><line><ratingbar></ratingbar>
        </line></tinui>
        ''')
    elif controlname=='menubar':
        #if not load_menubar:
        #    print('ok')
        #    label=duixml.tags['label'][-1]
        #    displayui.add_menubar(label)
        #load_menubar=True
        label=duixml.tags['label'][-1]
        displayui.add_menubar(label)
    elif controlname=='notebook':
        notebook=duixml.tags['notebook'][-2]
        for i in range(1,5):
            if i==5:#第五个不可删除:
                notebook.addpage('test'+str(i),'t'+str(i),cancancel=False)
            else:
                notebook.addpage('test'+str(i),'t'+str(i))
    elif controlname=='waitframe':
        waitframe=duixml.tags['waitframe'][-2]
        waitframe.start()
    elif controlname=='TinUIXml':#严格来说，这不是控件，而是TinUI框架的一部分
        pass



xmlf=open(os.path.dirname(__file__)+r'\testpage\main.xml','r')
xml=xmlf.read()
xmlf.close()

window = Tk()
window.resizable(False,False)
window.iconbitmap('../LOGO.ico')
window.title("TinUI main test")
window.geometry("850x600+5+5")
ui=BasicTinUI(window)
uix=TinUIXml(ui)

uix.funcs['loadcontrol']=loadcontrol
uix.datas['controls']=['back', 'barbutton', 'button', 'button2', 'canvas', 'checkbutton', 
 'combobox', 'entry', 'expander', 'image', 'info', 'label', 'labelframe',
 'link', 'listbox', 'listview', 'menubar', 'menubutton', 'notebook', 'notecard', 
 'onoff', 'paragraph', 'passwordbox', 'picker', 'pipspager', 'pivot', 'progressbar', 
 'radiobox', 'radiobutton', 'ratingbar', 'scalebar', 'scrollbar', 'separate', 
 'spinbox', 'swipecontrol', 'table', 'textbox', 'title', 'togglebutton', 'tooltip', 
 'treeview', 'ui', 'waitbar', 'waitframe','TinUIXml']
uix.loadxml(xml)
displayui,_,duixml,_=uix.tags['displayui']

ui.pack(fill='both',expand=True)

if __name__=='__main__':
    window.mainloop()
