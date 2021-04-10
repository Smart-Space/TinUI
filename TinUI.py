from tkinter import *
import io
import requests
from PIL import Image,ImageTk
from TinEngine import TinText

class TinUI(Canvas):
    """基于tkinter的高级窗口绘制组件"""

    def __init__(self,master,update:bool=True,update_time:int=1000,**kw):
        self.frame = Frame(master)
        self.vbar = Scrollbar(self.frame)
        self.vbar.pack(side=RIGHT, fill=Y)
        ###
        kw.update({'yscrollcommand': self.vbar.set})
        Canvas.__init__(self, self.frame, **kw)
        self.pack(fill=BOTH, expand=True)
        self.vbar['command'] = self.yview
        ###
        self.hbar=Scrollbar(self.frame,orient='horizontal',command=self.xview)
        self.hbar.pack(side=BOTTOM,fill=X)
        self.config(xscrollcommand=self.hbar.set)
        # Copy geometry methods
        canvas_meths = vars(Canvas).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(canvas_meths)
        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))
        self.bind('<MouseWheel>',self.set_y_view)
        self.init()
        self.update_time=update_time
        if update==True:#自动刷新滚动宽度
            self.update__()

    def init(self):
        self.title_size={0:20,1:18,2:16,3:14,4:12}
    def set_y_view(self,event):
        self.yview_scroll(int(-1*(event.delta/120)), "units")
    def update__(self):#更新宽高
        try:
            bbox=self.bbox('all')
            width,height=bbox[2:]
            if height<=self.winfo_height():
                self.vbar.pack_forget()
            else:
                self.vbar.pack(before=self,side=RIGHT,fill=Y)
            if width<=self.winfo_width():
                self.hbar.pack_forget()
            else:
                self.hbar.pack(side=BOTTOM,fill=X)
            self.config(scrollregion=bbox)
        except:
            pass
        finally:
            self.after(self.update_time,self.update__)

    def add_title(self,pos:tuple,text:str,fg='black',font='微软雅黑',size=1,**kw):#绘制标题
        return self.create_text(pos,text=text,fill=fg,font=(font,self.title_size[size]),anchor='nw',**kw)

    def add_paragraph(self,pos:tuple,text:str,fg='black',font=('微软雅黑',12),side='left',width=500,**kw):#绘制段落
        return self.create_text(pos,text=text,fill=fg,font=font,anchor='nw',justify=side,width=width,**kw)

    def add_button(self,pos:tuple,text:str,fg='black',bg='#E1E1E1',font=('微软雅黑',12),command=None):#绘制按钮
        def in_button(event):
            self.itemconfig(back,fill='#E5F1FB',outline='#82BDEB')
        def out_button(event):
            self.itemconfig(back,fill=bg,outline='grey')
        button=self.create_text(pos,text=text,fill=fg,font=font,anchor='nw')
        bbox=self.bbox(button)
        x1,y1,x2,y2=bbox[0]-3,bbox[1]-3,bbox[2]+3,bbox[3]+3
        back=self.create_rectangle((x1,y1,x2,y2),fill=bg,outline='grey')
        self.tag_bind(button,'<Button-1>',command)
        self.tag_bind(button,'<Enter>',in_button)
        self.tag_bind(button,'<Leave>',out_button)
        self.tkraise(button)
        return button

    def add_label(self,pos:tuple,text:str,fg='black',bg='#f0f0f0',outline='grey',font=('微软雅黑',12)):#绘制标签
        label=self.create_text(pos,text=text,fill=fg,font=font,anchor='nw')
        bbox=self.bbox(label)
        x1,y1,x2,y2=bbox[0]-3,bbox[1]-3,bbox[2]+3,bbox[3]+3
        back=self.create_rectangle((x1,y1,x2,y2),fill=bg,outline=outline)
        self.tkraise(label)
        return label

    def add_checkbutton(self,pos:tuple,text:str,fg='black',fill='lightgreen',font=('微软雅黑',12),command=None):#绘制复选框
        def button_in(event):
            self.itemconfig(check,outline='#82BDEB')
        def button_out(event):
            self.itemconfig(check,outline=fg)
        def go_func(event):
            if self.itemcget(check,'fill')!=fill:
                self.itemconfig(check,fill=fill)
            else:
                self.itemconfig(check,fill=self['background'])
            command(event)
        checkbutton=self.create_text(pos,text=text,fill=fg,font=font,anchor='nw')
        bbox=self.bbox(checkbutton)
        dic=bbox[3]-bbox[1]#位移长度
        self.move(checkbutton,dic-7,0)
        check=self.create_rectangle((pos[0],pos[1]+5,pos[0]+dic-10,pos[1]+dic-5),outline=fg,fill=self['background'])
        self.tag_bind(check,'<Enter>',button_in)
        self.tag_bind(check,'<Leave>',button_out)
        self.tag_bind(checkbutton,'<Enter>',button_in)
        self.tag_bind(checkbutton,'<Leave>',button_out)
        self.tag_bind(check,'<Button>',go_func)
        self.tag_bind(checkbutton,'<Button>',go_func)
        return checkbutton


def test(event):
    a.title('TinUI Test')
    b.add_paragraph((50,150),'这是TinUI按钮触达的事件函数回显，此外，窗口标题也被改变、首行标题缩进减小')
    b.coords(m,100,0)
def test1(event):
    pass
def test2(event):
    pass

a=Tk()
a.geometry('700x700+5+5')

b=TinUI(a,bg='white')
b.pack(fill='both',expand=True)
m=b.add_title((600,0),'TinUI is a test project for futher tin using')
m1=b.add_title((0,680),'test TinUI scrolled',size=2,angle=24)
b.add_paragraph((20,290),'''     TinUI是基于tkinter画布开发的界面UI布局方案，作为tkinter拓展和TinEngine的拓展而存在。目前，TinUI尚处于开发阶段。如果想要使用完整的TinUI，敬请期待。''',
angle=-18)
b.add_paragraph((20,100),'下面的段落是测试画布的非平行字体显示效果，也是TinUI的简单介绍')
b.add_button((250,450),'测试按钮',command=test)
b.add_checkbutton((80,430),'允许TinUI测试',command=test1)
b.add_label((10,220),'这是由画布TinUI绘制的Label组件')

a.mainloop()
