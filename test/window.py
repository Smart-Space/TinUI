import sys
sys.path.append('..')
from TinUI import *
from tkinter import Tk


class TinUIWindow(Tk):

    def __init__(self,title='tinui-window',width=500,height=500,tran='#01ff11'):
        super().__init__()
        self.title=title
        self.tran=tran
        self.config(width=width,height=height,background=tran)
        self.attributes('-transparent',self.tran)
        self.__load_tinui()

    def __load_tinui(self):
        self.titlebar=BasicTinUI(self,height=40,bg=self.tran,relief='flat')
        self.titlebar.place(x=0,y=0,relwidth=1)
        width=self.cget('width')
        height=self.cget('height')
        self.titlebar.create_polygon((12,12,width-12,12,width-12,50,12,50,12,12),
                                     width=15,fill='#f1f3f9',outline='#f1f3f9')
        bbox=self.titlebar.bbox('all')
        self.titlebar.add_button((width-25,15),text='×',anchor='nw',
                                 bg='#f1f3f9',line='#f1f3f9',fg='black',
                                 activebg='#c42b1c',activeline='#c42b1c',)
        width=bbox[2]-bbox[0]
        self.main=BasicTinUI(self,bg='#f1f3f9')
        self.main.place(x=bbox[0]+2,y=40,width=width-3,height=height-46)
        self.xml=TinUIXml(self.main)


class win:
    def __init__(self):
        self.r=Tk()
        self.r.geometry('500x500+10+10')
        self.u=TinUI(self.r)#,bg='#01FF11')
        self.u.pack(fill='both',expand=True)
    def go(self):
        self.r.mainloop()


if __name__=='__main__':
    #root=win()
    #root.go()
    r=TinUIWindow('test')
    r.mainloop()
