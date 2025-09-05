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
    displayui.delete('all')
    duixml.clean()

    duixml.funcs["opentutest"] = opentutest
    
    duixml.loadxml(cxml)
    if controlname=='menubar':
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
    elif controlname=='breadcrumb':
        bc=duixml.tags['bc'][-2]
        for i in range(1,5):
            bc.add('test'+str(i))
    elif controlname=='TinUIXml':#严格来说，这不是控件，而是TinUI框架的一部分
        pass


window = Tk()

window.iconbitmap('../LOGO.ico')
window.title("TinUI main test")
window.geometry("850x600+5+5")
ui=BasicTinUI(window, bg='#f3f3f3')

ui.pack(fill='both',expand=True)

root=ExpandPanel(ui)
hp=HorizonPanel(ui,spacing=5)
root.set_child(hp)

vp=VerticalPanel(ui,spacing=5)
hp.add_child(vp,200)

t=ui.add_title((0,0),text='TinUI Gallery',anchor='n')
img=ui.add_image((0,0),imgfile='LOGO.png',width=200,height=200,anchor='n')
listbox=ui.add_listbox((0,0),height=340,bg='#f0f0f0',data=('back', 'barbutton', 'breadcrumb', 'button', 'button2', 'checkbutton', 
 'combobox', 'entry', 'expander', 'flyout', 'image', 'label', 'labelframe',
 'link', 'listbox', 'listview', 'menubar', 'menubutton', 'notebook', 'notecard', 
 'onoff', 'paragraph', 'passwordbox', 'picker', 'pipspager', 'pivot', 'progressbar', 
 'radiobox', 'radiobutton', 'ratingbar', 'scalebar', 'scrollbar', 'separate', 
 'spinbox', 'segmentbutton', 'table', 'textbox', 'title', 'togglebutton', 'tooltip', 
 'treeview', 'ui', 'waitbar', 'waitframe','TinUIXml'),command=loadcontrol)[-1]
vp.add_child(t,50)
vp.add_child(img,200)
ep1=ExpandPanel(ui)
ep1.set_child(listbox)
vp.add_child(ep1,200,weight=1)
 
displayui,_,duixml,uid=ui.add_ui((0,0),bg='#f3f3f3',width=610,height=575,scrollbar="True",region='auto')
ep=ExpandPanel(ui)
ep.set_child(uid)
hp.add_child(ep,500,weight=1)

def update(e):
    root.update_layout(5,5,e.width-5,e.height-5)
ui.bind('<Configure>',update)

def maintest():
    window.mainloop()

if __name__=='__main__':
    maintest()
