import os
import sys

try:  #作为tinui包的子模块被导入（pip安装）
    from .. import *
except ImportError:  #源码目录
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    from TinUI import *

from tkinter import Tk
from tkinter.ttk import Button


class win:
    def __init__(self):
        self.r=Tk()
        self.r.geometry('500x500+10+10')
        self.u=TinUI(self.r)#,bg='#01FF11')
        self.u.pack(fill='both',expand=True)
        #gomap=((10,0),(460,0),(460,450),(10,450),(10,0))
        #self.u.create_polygon(gomap,fill='#f0f0f0',outline='#f0f0f0',width=15)
        #self.r.attributes('-transparent','#01FF11')
        Button(self.r,text='上一页(ctrl+U)',command=self.upit).pack()
        Button(self.r,text='下一页(ctrl+D)',command=self.downit).pack()
        self.r.bind('<Control-u>',self.upit)
        self.r.bind('<Control-d>',self.downit)
    def go(self):
        self.r.mainloop()
    def upit(self,*e):
        self.u.yview("scroll", -1, "pages")
    def downit(self,*e):
        self.u.yview("scroll", 1, "pages")


if __name__=='__main__':
    root=win()
    root.go()
