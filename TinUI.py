'''
<TinUI, a modern frame to render various widgets elements for tkinter in one control.>
    Copyright (C) <2021-present>  <smart-space>
基于GPLv3和额外的LPGLv3许可发布
'''
from tkinter import Tk, Toplevel, Canvas, Entry, Text, Scrollbar, Frame, PhotoImage, StringVar,\
    BOTH, X, Y, RIGHT, BOTTOM, Place, Grid, Pack
from tkinter import ttk
from tkinter import font as tkfont
from webbrowser import open as webopen
from typing import Union
from xml.etree import ElementTree  as ET
import collections
import sys
import os
import shutil
import uuid
'''全部组件都是绘制的，除了输入型组件无法使用tkinter画布完成对应效果'''
#==========
'''开发信息
开发者：Smart-Space（Junming Zhang）
版权：版权所有(C) 2019（原型框架，TinGroup子项目）|2021（正式命名TinUI）- present Smart-Space（Junming Zhang）
开发者邮箱：smart-space@qq.com|tsan-zane@outlook.com
语言：Python
技术基础：tkinter（tcl/tk）
开源平台：pypi、GitHub、csdn
开源协议：GPLv3, LGPLv3
'''


class FuncList(list):#控件的函数列表类

    def __init__(self,num:int=10):
        list.__init__(self)
        for _ in range(0,num+1):
            self.append(None)


class TinUIString(str):#TinUI字符串类

    def __init__(self,string:str=''):
        str.__init__(self)
        self.text=string

class TinUINum(int):#TinUI数字类

    def __init__(self,integer:Union[int|float]=0):
        int.__init__(self)
        self.num=integer


class TinUITheme:
    '''
    专门为特有样式的TinUI或BasicTinUI提供的类
    适用于重写样式配色的TinUI或BasicTinUI
    该类允许重写样式的TinUI或BasicTinUI使用TinUIXml
    '''

    def __init__(self,ui,name='tinui-theme'):
        self.theme=name
        self.ui=ui
        self.bbox=ui.bbox

    def change_theme_name(self,name:str):
        self.theme=name

    def get_theme(self):
        return self.theme


class TinUIFont:
    #添加字体文件，见CustomTkinter

    linux_font_path = "~/.fonts/"
    darwin_font_path = "~/Library/Fonts/"

    @classmethod
    def init_font_manager(cls):
        # Linux
        if sys.platform.startswith("linux"):
            try:
                if not os.path.isdir(os.path.expanduser(cls.linux_font_path)):
                    os.mkdir(os.path.expanduser(cls.linux_font_path))
                return True
            except:
                return False

        # other platforms
        else:
            return True

    @classmethod
    def windows_load_font(cls, font_path: Union[str, bytes], private: bool = True, enumerable: bool = False) -> bool:
        """ Function taken from: https://stackoverflow.com/questions/11993290/truly-custom-font-in-tkinter/30631309#30631309 """

        from ctypes import windll, byref, create_unicode_buffer, create_string_buffer

        FR_PRIVATE = 0x10
        FR_NOT_ENUM = 0x20

        if isinstance(font_path, bytes):
            path_buffer = create_string_buffer(font_path)
            add_font_resource_ex = windll.gdi32.AddFontResourceExA
        elif isinstance(font_path, str):
            path_buffer = create_unicode_buffer(font_path)
            add_font_resource_ex = windll.gdi32.AddFontResourceExW
        else:
            raise TypeError('font_path must be of type bytes or str')

        flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
        num_fonts_added = add_font_resource_ex(byref(path_buffer), flags, 0)
        return bool(min(num_fonts_added, 1))

    @classmethod
    def load_font(cls, font_path: str) -> bool:
        # Windows
        if sys.platform.startswith("win"):
            return cls.windows_load_font(font_path, private=True, enumerable=False)

        # Linux
        elif sys.platform.startswith("linux"):
            try:
                shutil.copy(font_path, os.path.expanduser(cls.linux_font_path))
                return True
            except:
                return False
            
        # MacOS
        elif sys.platform.startswith("darwin"):
            try:
                shutil.copy(font_path, os.path.expanduser(cls.darwin_font_path))
                return True
            except:
                return False

        # others
        else:
            return False


class BasicTinUI(Canvas):
    """基于tkinter的高级窗口绘制组件
    uid参数为每一个组件（除个别）的整体tag_name"""

    def __init__(self,master,**kw):
        if 'highlightthickness' not in kw:
            kw['highlightthickness']=0
        Canvas.__init__(self, master, selectborderwidth=0, bd=0, **kw)
        self.init()

    def init(self):
        self.images=[]
        self.title_size={0:20,1:18,2:16,3:14,4:12}
        self.windows=[]#浮出控件的子窗口，需要开发者手动释放
    
    def __get_text_size(self,text):
        #获取文本元素字体大小
        font=self.itemcget(text,'font').split(' ')
        if len(font)==1:
            return ''
        else:
            return ' '+font[1]
    
    def __anchor_nw(bbox,pos):
        return pos[0]-bbox[0],pos[1]-bbox[1]
    def __anchor_n(bbox,pos):
        return pos[0]-(bbox[0]+bbox[2])/2,pos[1]-bbox[1]
    def __anchor_ne(bbox,pos):
        return pos[0]-bbox[2],pos[1]-bbox[1]
    def __anchor_e(bbox,pos):
        return pos[0]-bbox[2],pos[1]-(bbox[1]+bbox[3])/2
    def __anchor_se(bbox,pos):
        return pos[0]-bbox[2],pos[1]-bbox[3]
    def __anchor_s(bbox,pos):
        return pos[0]-(bbox[0]+bbox[2])/2,pos[1]-bbox[3]
    def __anchor_sw(bbox,pos):
        return pos[0]-bbox[0],pos[1]-bbox[3]
    def __anchor_w(bbox,pos):
        return pos[0]-bbox[0],pos[1]-(bbox[1]+bbox[3])/2
    def __anchor_center(bbox,pos):
        return pos[0]-(bbox[0]+bbox[2])/2,pos[1]-(bbox[1]+bbox[3])/2
    __anchor_dict={
        'nw':__anchor_nw,
        'n':__anchor_n,
        'ne':__anchor_ne,
        'e':__anchor_e,
        'se':__anchor_se,
        's':__anchor_s,
        'sw':__anchor_sw,
        'w':__anchor_w,
        'center':__anchor_center
    }
    def __auto_anchor(self,uid,pos,anchor='nw'):#统一对齐方式
        bbox=self.bbox(uid)
        dx,dy=self.__anchor_dict[anchor](bbox,pos)
        self.move(uid,dx,dy)
        return dx,dy
    def __layout_nw(bbox,bboxuid):
        return bbox[0]-bboxuid[0],bbox[1]-bboxuid[1]
    def __layout_n(bbox,bboxuid):
        return (bbox[0]+bbox[2])/2-(bboxuid[0]+bboxuid[2])/2,bbox[1]-bboxuid[1]
    def __layout_ne(bbox,bboxuid):
        return bbox[2]-bboxuid[2],bbox[1]-bboxuid[1]
    def __layout_e(bbox,bboxuid):
        return bbox[2]-bboxuid[2],(bbox[1]+bbox[3])/2-(bboxuid[1]+bboxuid[3])/2
    def __layout_se(bbox,bboxuid):
        return bbox[2]-bboxuid[2],bbox[3]-bboxuid[3]
    def __layout_s(bbox,bboxuid):
        return (bbox[0]+bbox[2])/2-(bboxuid[0]+bboxuid[2])/2,bbox[3]-bboxuid[3]
    def __layout_sw(bbox,bboxuid):
        return bbox[0]-bboxuid[0],bbox[3]-bboxuid[3]
    def __layout_w(bbox,bboxuid):
        return bbox[0]-bboxuid[0],(bbox[1]+bbox[3])/2-(bboxuid[1]+bboxuid[3])/2
    def __layout_center(bbox,bboxuid):
        return (bbox[0]+bbox[2])/2-(bboxuid[0]+bboxuid[2])/2,(bbox[1]+bbox[3])/2-(bboxuid[1]+bboxuid[3])/2
    __layout_dict={
        'nw':__layout_nw,
        'n':__layout_n,
        'ne':__layout_ne,
        'e':__layout_e,
        'se':__layout_se,
        's':__layout_s,
        'sw':__layout_sw,
        'w':__layout_w,
        'center':__layout_center
    }
    def __auto_layout(self,uid,bbox,anchor='center'):
        bbox2=self.bbox(uid)
        dx,dy=self.__layout_dict[anchor](bbox,bbox2)
        self.move(uid,dx,dy)
        return dx,dy
    
    def __ui_polygon(self,point2,fill='white',outline='black',width=1,tags=None):
        points = (*point2[0], point2[1][0], point2[0][1], *point2[1], point2[0][0], point2[1][1])
        return self.create_polygon(points,fill=fill,outline=outline,width=width,tags=tags)

    def __delete_uixml(self, uixml):
        # 删除伴随TinUIXml
        uixml.clean()
    
    def clean_windows(self):
        #清除浮出控件子窗口
        for i in self.windows:
            try:
                i.destroy()
            except:
                continue
        self.images.clear()
        self.windows.clear()

    def add_title(self,pos:tuple,text:str,fg='black',font='微软雅黑',size=1,anchor='nw',**kw):#绘制标题
        kw['anchor']=anchor
        title = self.create_text(pos,text=text,fill=fg,font=(font,self.title_size[size]),**kw)
        uid = TinUIString(f'title-{title}')
        self.itemconfig(title,tags=uid)
        uid.layout = lambda x1,y1,x2,y2,expand=False: self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
        return uid

    def add_paragraph(self,pos:tuple,text:str,fg='black',font=('微软雅黑',12),side='left',width=500,anchor='nw',**kw):#绘制段落
        kw['anchor']=anchor
        pgh = self.create_text(pos,text=text,fill=fg,font=font,justify=side,width=width,**kw)
        uid = TinUIString(f'paragraph-{pgh}')
        self.itemconfig(pgh,tags=uid)
        uid.layout = lambda x1,y1,x2,y2,expand=False: self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
        return uid

    def add_button(self,pos:tuple,text:str,fg='#000000',bg='#CCCCCC',line='#CCCCCC',linew=3,activefg='black',activebg='#999999',activeline='#7a7a7a',font=('微软雅黑',12),minwidth=0,maxwidth=0,command=None,anchor='nw'):#绘制按钮
        def in_button(event):
            self.itemconfig(back,fill=activebg,outline=activeline)
            self.itemconfig(button,fill=activefg)
        def out_button(event):
            self.itemconfig(back,fill=bg,outline=line)
            self.itemconfig(button,fill=fg)
        def on_click(event):
            self.itemconfig(back,fill=activebg,outline=activebg)
            self.itemconfig(button,fill=activefg)
            self.after(500,lambda : out_button(None))
            if command!=None:
                command(event)
        def __layout(x1,y1,x2,y2,expand=False):
            if not expand:
                self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
            else:
                self.__auto_layout(uid,(x1,y1,x2,y2),'center')
                self.coords(back,x1+linew,y1+linew,x2-linew,y2-linew)
        def change_command(new_func):
            nonlocal command
            command=new_func
        def disable(fg='#7a7a7a',bg='#cccccc'):
            self.itemconfig(button,state='disable',fill=fg)
            self.itemconfig(back,state='disable',disabledfill=bg)
        def active():
            self.itemconfig(button,state='normal')
            self.itemconfig(back,state='normal')
            out_button(None)
        button=self.create_text(pos,text=text,fill=fg,font=font,anchor='nw')
        uid=TinUIString(f'button-{button}')
        self.itemconfig(button,tags=uid)
        bbox=self.bbox(button)
        x1,y1,x2,y2=bbox[0]-3,bbox[1]-3,bbox[2]+3,bbox[3]+3
        #判断宽度的极限，分为最大化和最小化
        nowwidth=x2-x1
        if 0<maxwidth<=nowwidth:
            self.itemconfig(button,width=maxwidth)
            bbox=self.bbox(button)
            x1,y1,x2,y2=bbox[0]-3,bbox[1]-3,bbox[2]+3,bbox[3]+3
            nowwidth=x2-x1
        if nowwidth<minwidth:
            dx=minwidth-nowwidth
            x2+=dx/2
            x1-=dx/2
        back=self.create_rectangle((x1,y1,x2,y2),fill=bg,outline=line,width=linew,tags=uid)
        self.tag_bind(uid, '<Button-1>', on_click)
        self.tag_bind(uid, '<Enter>', in_button)
        self.tag_bind(uid, '<Leave>', out_button)
        self.tkraise(button)
        self.__auto_anchor(uid,pos,anchor)
        del bbox,x1,y1,x2,y2
        funcs=FuncList(3)
        funcs.change_command=funcs[0]=change_command
        funcs.disable=funcs[1]=disable
        funcs.active=funcs[2]=active
        uid.layout=__layout
        return button,back,funcs,uid

    def add_label(self,pos:tuple,text:str,fg='black',bg='#f0f0f0',outline='grey',font=('微软雅黑',12),anchor='nw'):#绘制标签
        def __layout(x1,y1,x2,y2,expand=False):
            if not expand:
                self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
            else:
                self.__auto_layout(uid,(x1,y1,x2,y2),'center')
                self.coords(back,x1+1,y1+1,x2-1,y2-1)
        label=self.create_text(pos,text=text,fill=fg,font=font,anchor='nw')
        uid=TinUIString(f'label-{label}')
        self.itemconfig(label,tags=uid)
        bbox=self.bbox(label)
        x1,y1,x2,y2=bbox[0]-3,bbox[1]-3,bbox[2]+3,bbox[3]+3
        back=self.create_rectangle((x1,y1,x2,y2),fill=bg,outline=outline,tags=uid)
        self.tkraise(label)
        self.__auto_anchor(uid,pos,anchor)
        del bbox
        uid.layout=__layout
        return label, back, uid

    def add_checkbutton(self,pos:tuple,text:str,fontfg='black',fg='#868686',bg='#ededed',activefg='#868686',activebg='#e5e5e5',onfg='white',onbg='#334ac0',font=('微软雅黑',12),command=None,anchor='nw'):#绘制复选框
        def button_in(event):
            if self.itemcget(check,'fill')==onbg:
                pass
            else:
                self.itemconfig(check,fill=activebg)
                self.itemconfig(outl,fill=activefg)
        def button_out(event):
            if self.itemcget(check,'fill')==onbg:
                pass
            else:
                self.itemconfig(check,fill=bg)
                self.itemconfig(outl,fill=fg)
        def go_func(event):
            nonlocal stateinfo
            if not stateinfo:
                self.itemconfig(check,fill=onbg)
                self.itemconfig(outl,fill=onfg)
                self.itemconfig(state,state='normal')
                stateinfo=True
            else:
                self.itemconfig(check,fill=bg)
                self.itemconfig(outl,fill=fg)
                self.itemconfig(state,state='hidden')
                stateinfo=False
            if command!=None:
                command(stateinfo)
        def flash():
            go_func(None)
        def on():
            nonlocal stateinfo
            stateinfo = False
            go_func(None)
        def off():
            nonlocal stateinfo
            stateinfo = True
            go_func(None)
        def disable():
            self.itemconfig(checkbutton,state='disable',fill='#7a7a7a')
            self.itemconfig(checkname,state='disable')
            if not stateinfo:#因为上面设置了checkname三个子元素，标识符会自动显示
                self.itemconfig(state,state='hidden')
        def active():
            self.itemconfig(checkbutton,state='normal',fill=fontfg)
            self.itemconfig(checkname,state='normal')
            if not stateinfo:
                self.itemconfig(state,state='hidden')
        stateinfo=False#是否勾选
        checkbutton=self.create_text(pos,text=text,fill=fontfg,font=font,anchor='nw')
        uid=TinUIString(f'checkbutton-{checkbutton}')
        self.itemconfig(checkbutton,tags=uid)
        bbox=self.bbox(checkbutton)
        dic=bbox[3]-bbox[1]#位移长度
        midy=pos[1]+dic/2#中间高度坐标
        midx=pos[0]+dic/2#中间宽度坐标
        font_size=str(int(self.__get_text_size(checkbutton))+2)#字体大小
        self.move(checkbutton,dic+5,0)
        checkname=f'{uid}checkname'
        outl=self.create_text((midx,midy),text='\uE739',anchor='center',font='{Segoe Fluent Icons} '+font_size,fill=fg,tags=(uid,checkname))#外围边框
        check=self.create_text((midx,midy),text='\uE73B',anchor='center',font='{Segoe Fluent Icons} '+font_size,fill=bg,tags=(uid,checkname))#标识符内部元素
        state=self.create_text((midx,midy),text='\uE73E',anchor='center',font='{Segoe Fluent Icons} '+font_size,fill=onfg,state='hidden',tags=(uid,checkname))#勾选标识符
        self.tkraise(state)
        self.tag_bind(uid, '<Enter>', button_in)
        self.tag_bind(uid, '<Leave>', button_out)
        self.tag_bind(uid, '<Button>', go_func)
        self.__auto_anchor(uid,pos,anchor)
        del bbox,dic,midy,midx,font_size
        funcs=FuncList(5)
        funcs.flash=funcs[0]=flash
        funcs.on=funcs[1]=on
        funcs.off=funcs[2]=off
        funcs.disable=funcs[3]=disable
        funcs.active=funcs[4]=active
        uid.layout=lambda x1,y1,x2,y2,expand=False: self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
        return checkbutton,check,funcs,uid

    def add_entry(self,pos:tuple,width:int,text:str='',fg='#1b1b1b',bg='#fbfbfb',activefg='#1a1a1a',activebg='#f6f6f6',onfg='#000000',onbg='#ffffff',line='#e5e5e5',activeline='#e5e5e5',insert='#000000',font=('微软雅黑',12),outline='#868686',onoutline='#3041d8',icon='>',anchor='nw',call='→',command=None):#绘制单行输入框
        #这是一个半绘制组件
        def if_empty(event):
            nonlocal empty_flag
            ch=entry.get()
            if ch=='':
                empty_flag = True
                self.tag_unbind(funcw,'<Leave>')
                self.tag_unbind(funcw,'<Enter>')
                self.tag_unbind(funcw,'<Button-1>')
                self.itemconfig(funcw,text=icon,fill=fg)
            elif empty_flag:
                empty_flag = False
                self.itemconfig(funcw,text='×')
                self.tag_bind(funcw,'<Enter>',lambda event:self.itemconfig(funcw,fill=onoutline))
                self.tag_bind(funcw,'<Leave>',lambda event:self.itemconfig(funcw,fill=fg))
                self.tag_bind(funcw,'<Button-1>',lambda event:(entry.delete(0,'end'),if_empty(None)))
        def call_command(event):
            text=entry.get()
            command(text)
        def focus_in(e):
            self.itemconfig(bottomline,fill=onoutline)
            backpos = self.coords(back)
            backpos[5] -= 1
            backpos[7] -= 1
            self.coords(back, *backpos)
            self.itemconfig(back,fill=onbg,outline=onbg)
            self.itemconfig(outl,fill=activeline,outline=activeline)
            entry.config(background=onbg,foreground=onfg)
        def focus_out(e):
            self.itemconfig(bottomline,fill=outline)
            backpos = self.coords(back)
            backpos[5] += 1
            backpos[7] += 1
            self.coords(back, *backpos)
            self.itemconfig(back,fill=bg,outline=bg)
            self.itemconfig(outl,fill=line,outline=line)
            entry.config(background=bg,foreground=fg)
        def mouse_enter(e):
            if entry.focus_get() == entry.nametowidget(entry):
                # 已获取焦点
                return
            self.itemconfig(back, fill=activebg, outline=activebg)
            entry.config(background=activebg, foreground=activefg)
        def mouse_leave(e):
            if entry.focus_get() == entry.nametowidget(entry):
                # 已获取焦点
                return
            self.itemconfig(back, fill=bg, outline=bg)
            entry.config(background=bg, foreground=fg)
        def __layout(x1,y1,x2,y2,expand=False):
            if not expand:
                self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
            else:
                self.itemconfig(funce,width=x2-x1-dwidth-6)
                bbox1=self.bbox(funce)
                coord=self.coords(back)
                coord[0]=coord[6]=bbox1[0]+2
                coord[2]=coord[4]=bbox1[2]+dwidth-2
                self.coords(back,coord)
                coord=self.coords(outl)
                coord[0]=coord[6]=bbox1[0]+1
                coord[2]=coord[4]=bbox1[2]+dwidth-1
                self.coords(outl,coord)
                coordl=self.coords(bottomline)
                coordl[0]=coord[0]
                coordl[2]=coord[2]
                self.coords(bottomline,coordl)
                self.__auto_anchor(entrybutton,(bbox1[2],(bbox1[1]+bbox1[3])/2),'w')
                self.__auto_layout(uid,(x1,y1,x2,y2),'center')
        #---
        def get_entry():#获取文本
            return entry.get()
        def __delete():#删除文本
            entry.delete(0,'end')
            entry.focus_set()
        def __insert(index=0,text=''):#插入文本
            entry.insert(index,text)
        def __error(errorline='#c42b1c'):#错误样式
            self.itemconfig(bottomline,fill=errorline)
        def __normal():#正常样式
            entry['state']='normal'
            entry.focus_set()
            self.itemconfig(back,fill=onbg,outline=onbg)
            self.itemconfig(bottomline,fill=onoutline)
        def __disable():#禁用
            entry['state']='disable'
            self.itemconfig(back,fill='#f0f0f0',outline='#f0f0f0')
            self.itemconfig(bottomline,fill=outline)
        empty_flag = True
        var = StringVar()#变量
        entry = Entry(self, fg=fg, bg=bg, font=font, relief='flat', bd=0, insertbackground=insert, textvariable=var)
        entry.var = var
        if text != '':
            empty_flag = False
            entry.insert(0, text)
        entry.bind('<FocusIn>',focus_in)
        entry.bind('<FocusOut>',focus_out)
        entry.bind('<Enter>', mouse_enter)
        entry.bind('<Leave>', mouse_leave)
        funce=self.create_window(pos,window=entry,width=width,anchor='nw')#输入框画布对象
        self.windows.append(entry)
        uid=TinUIString(f'entru-{funce}')
        entrybutton=f'enrtyb-{funce}'
        self.itemconfig(funce,tags=uid)
        bbox=self.bbox(funce)
        funcw=self.create_text((bbox[0]+width,bbox[1]),text=icon,fill=fg,font=font,anchor='nw',tags=(uid,entrybutton))
        bubbox=self.bbox(funcw)
        if command!=None:#调用函数的绑定仅当存在command时启动
            button=self.create_text((bubbox[2]+2,(bbox[1]+bbox[3])/2),text=call,fill=fg,font=font,anchor='w',tags=(uid,entrybutton))
            self.tag_bind(button,'<Enter>',lambda event:self.itemconfig(button,fill=onoutline))
            self.tag_bind(button,'<Leave>',lambda event:self.itemconfig(button,fill=fg))
            self.tag_bind(button,'<Button-1>',call_command)
            entry.bind('<Return>',call_command)
            bubbox=self.bbox(button)
        bottomline=self.create_line((bbox[0]+2,bbox[3]-1,bubbox[2]-2,bbox[3]-1),fill=outline,width=9,capstyle='round',tags=uid)#bottomline
        back=self.__ui_polygon(((bbox[0]+2,bbox[1]+2),(bubbox[2]-2,bbox[3]-2)),fill=bg,outline=bg,width=9,tags=uid)#back
        outl=self.__ui_polygon(((bbox[0]+1,bbox[1]+1),(bubbox[2]-1,bbox[3]-1)),fill=line,outline=line,width=9,tags=uid)#outline
        self.lower(outl,bottomline)
        bbox1=self.bbox(entrybutton)
        bbox2=self.bbox(funce)
        dwidth=bbox1[2]-bbox2[2]+6
        del bbox1,bbox2,bubbox,bbox
        self.tkraise(entrybutton)
        self.__auto_anchor(uid,pos,anchor)
        if_empty(None)
        var.trace_add('write', lambda name, index, mode, var=var: if_empty(None))#变量绑定
        funcs=FuncList(7)
        funcs.get=get_entry
        funcs.insert=__insert
        funcs.delete=__delete
        funcs.error=__error
        funcs.normal=__normal
        funcs.active=__normal
        funcs.disable=__disable
        uid.layout=__layout
        return entry,funcs,uid

    def add_separate(self,pos:tuple,width:int,direction='x',fg='grey',anchor=None):#绘制分割线
        def __layout(x1,y1,x2,y2,expand=False):
            if not expand:
                self.__auto_layout(uid,(x1,y1,x2,y2),'center')
            else:
                if direction=='x':
                    y=(y1+y2)/2
                    self.coords(separate,x1+1,y,x2-1,y)
                elif direction=='y':
                    x=(x1+x2)/2
                    self.coords(separate,x,y1+1,x,y2-1)
        bbox=list(pos)
        separate=self.create_line((*pos,*pos),fill=fg,width=3,capstyle='round')
        uid=TinUIString(f'separate-{separate}')
        self.itemconfig(separate,tags=uid)
        if direction=='x':
            bbox.append(pos[0]+width)
            bbox.append(pos[1])
        elif direction=='y':
            bbox.append(pos[0])
            bbox.append(pos[1]+width)
        self.coords(separate,bbox)
        del bbox
        uid.layout=__layout
        return uid

    def add_radiobutton(self,pos:tuple,width,text='',choices=('choose me',),fg='#1a1a1a',bg='#f2f2f2',font=('微软雅黑',12),activefg='#3c3c3c',activebg='#e9e9e9',command=None,anchor='nw'):#绘制单选框
        def button_in(tag,t):
            self.itemconfig(tag,fill=activebg,outline=activebg)
        def button_out(_tag,t):
            for tag in back_list:
                self.itemconfig(tag,fill=bg,outline=bg)
            for t in choices_list:
                if t==None or t!=now_choice:
                    self.itemconfig(t,fill=fg)
        def go_func(tag,_text,t):
            nonlocal now_choice
            now_choice=t
            for i in choices_back:#判断是否为当前选中
                if i not in back_list:
                    back_list.append(i)
                    button_out(tag,t)
            back_list.remove(tag)
            self.itemconfig(tag,fill=activebg,outline=activebg)
            self.itemconfig(t,fill=activefg)
            if command!=None:
                command(_text)
        def select(num):
            back=choices_back[num]
            _text='select command'
            go_func(back,_text,choices_list[num])
        def disable():
            for f,b in zip(choices_list,choices_back):
                self.itemconfig(f,state='disable',fill='#7a7a7a')
                self.itemconfig(b,state='disable')
        def active():
            for f,b in zip(choices_list,choices_back):
                self.itemconfig(f,state='normal',fill=fg)
                self.itemconfig(b,state='normal')
        word=self.create_text(pos,text=text,fill=fg,font=font,anchor='nw',width=width)
        now_choice=None#当前选中项
        uid=TinUIString(f'radiobutton-{word}')
        self.itemconfig(word,tags=uid)
        start_x=pos[0]#起始x位置
        height=self.bbox(word)[3]+3#变量y位置
        choices_list=[]
        choices_back=[]
        for i in choices:
            choice=self.create_text((start_x+2,height+2),text=i,fill=fg,font=font,anchor='nw',width=width-4,tags=uid)
            bbox=self.bbox(choice)
            h=bbox[3]-bbox[1]+4
            back=self.__ui_polygon(((start_x+4,height+4),(start_x+width-4,height+h-4)),outline=bg,fill=bg,tags=uid,width=9)
            self.tkraise(choice)
            height+=h+4
            choices_list.append(choice)
            choices_back.append(back)
            for item_id in (choice, back):
                self.tag_bind(item_id,'<Enter>',lambda event,back=back,c=choice:button_in(back,c))
                self.tag_bind(item_id,'<Leave>',lambda event,back=back,c=choice:button_out(back,c))
                self.tag_bind(item_id,'<Button>',lambda event,_text=i,back=back,c=choice:go_func(back,_text,c))
        back_list=list(choices_back)
        self.__auto_anchor(uid,pos,anchor)
        del start_x,height,bbox,h
        funcs=FuncList(3)
        funcs.select=funcs[0]=select
        funcs.disable=funcs[1]=disable
        funcs.active=funcs[2]=active
        uid.layout=lambda x1,y1,x2,y2,expand=False: self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
        return word,choices_list,choices_back,funcs,uid

    def add_link(self,pos:tuple,text,url,fg='#4f62ca',activefg='red',activebg='#eaeaea',font:tuple=('微软雅黑',12),anchor='nw',command=None):#绘制超链接
        def turn_red(event):
            self.itemconfig(link,fill=activefg)
            self.itemconfig(back,fill=activebg,outline=activebg)
            self['cursor']='hand2'
        def turn_back(event):
            self.itemconfig(link,fill=fg)
            self.itemconfig(back,fill='',outline='')
            self['cursor']='arrow'
        def go_url(event):
            #先判断是否含有目标函数，有则只执行目标函数
            if command!=None:
                command(url)
            else:
                #url如果是字符串，则打开网页；是方法，则执行函数
                if type(url)==str:
                    webopen(url)
                elif callable(url):
                    url(event)
        def disable(fg='#b0b0b0'):
            self.itemconfig(link,state='disable',fill=fg)
            self.itemconfig(back,state='disable')
        def active():
            self.itemconfig(link,state='normal',fill=fg)
            self.itemconfig(back,state='normal')
        link=self.create_text(pos,text=text,fill=fg,font=font,anchor='nw')
        uid=TinUIString(f'link-{link}')
        self.itemconfig(link,tags=uid)
        font=self.itemcget(link,'font')+' underline'
        self.itemconfig(link,font=font)
        bbox=self.bbox(link)
        back=self.__ui_polygon(((bbox[0]+1,bbox[1]+1),(bbox[2]-1,bbox[3]-1)),width=9,tags=uid,fill='',outline='')
        self.tkraise(link)
        self.tag_bind(uid,'<Enter>',turn_red)
        self.tag_bind(uid,'<Leave>',turn_back)
        self.tag_bind(uid,'<Button-1>',go_url)
        if type(url)==str:#为网址，显示提示框
            self.add_tooltip(uid,text=url,fg=fg,bg=self['background'],font=font,outline=activebg)
        self.__auto_anchor(uid,pos,anchor)
        del font,bbox
        funcs=FuncList(2)
        funcs.disable=funcs[0]=disable
        funcs.active=funcs[1]=active
        uid.layout=lambda x1,y1,x2,y2,expand=False: self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
        return link,back,funcs,uid

    # def add_waitbar1(self,pos:tuple,fg='#0078D7',bg='',okfg='lightgreen',okbg='',bd=5,r=20,anchor='nw'):#绘制圆形等待组件
    #     def __start(i):
    #         if is_ok:
    #             return
    #         self.itemconfig(waitbar1,extent=i,start=90+i)
    #         self.update_idletasks()
    #         if i==355:
    #             start()
    #     def start():
    #         if is_ok:
    #             return
    #         for i in range(0,360,5):
    #             self.after(i*8,lambda i=i:__start(i))
    #     def ok():
    #         nonlocal is_ok
    #         is_ok=True
    #         self.itemconfig(waitbar1,outline=okfg,extent=359)
    #         self.itemconfig(back,fill=okbg)
    #     is_ok = False
    #     bbox=(pos[0],pos[1],pos[0]+2*r,pos[1]+2*r)
    #     back_bbox=(pos[0]+bd,pos[1]+bd,pos[0]+2*r-bd,pos[1]+2*r-bd)
    #     back=self.create_oval(back_bbox,width=0,fill=bg)
    #     uid=f'waitbar1-{back}'
    #     self.itemconfig(back,tags=uid)
    #     waitbar1=self.create_arc(bbox,outline=fg,extent=5,start=90,width=bd,style='arc',tags=uid)
    #     self.__auto_anchor(uid,pos,anchor)
    #     start()
    #     return waitbar1,ok,uid

    def add_labelframe(self,widgets:tuple=(),title='',font='微软雅黑 10',fg='#A8A8A8',bg='',pos=None,anchor=None):#绘制标题框
        sx,sy,ex,ey=self.bbox(widgets[0])#获取直接的起始位置
        for i in widgets:
            nsx,nsy,nex,ney=self.bbox(i)
            sx=nsx if nsx<sx else sx
            sy=nsy if nsy<sy else sy
            ex=nex if nex>ex else ex
            ey=ney if ney>ey else ey
        bg=self['background'] if bg=='' else bg
        back=self.__ui_polygon(((sx+3,sy-9),(ex-3,ey-3)),fill=bg,outline=bg,width=17)
        uid=f'labelframe-{back}'
        self.itemconfig(back,tags=uid)
        self.lower(back)
        outline=self.__ui_polygon(((sx+2,sy-10),(ex-2,ey-2)),fill=fg,outline=fg,width=17,tags=uid)
        self.lower(outline)
        if title:
            label=self.create_text(((sx+ex)//2,sy-20),font=font,text=title,fill=fg,anchor='center',tags=uid)
            self.create_rectangle(self.bbox(label),fill=bg,outline=bg,tags=uid)
            self.tag_raise(label)
        else:
            label=None
        return label,back,outline,uid

    # def add_waitbar2(self,pos:tuple,width:int=240,fg='#3041d8',bg='#f3f3f3',okcolor='#0f7b0f',anchor='nw'):#绘制点状等待框
    #     #单点运动
    #     def ball_go(ball,w,x,num):
    #         self.move(ball,x,0)
    #         if num==4 and w>=width:
    #             for i in balls:
    #                 self.coords(i,pos)
    #                 self.update_idletasks()
    #             start()
    #     #单点运动控制
    #     def _start(ball):
    #         if ifok:
    #             return
    #         self.itemconfig(ball,state='normal')
    #         num=balls.index(ball)
    #         fast=width//2
    #         for w in range(0,width+5-fast,5):
    #             self.after(w*10,lambda w=w:ball_go(ball,w,5,num))
    #         for w in range(width+5-fast,width+5-fast//2,5):
    #             self.after(w*10,lambda w=w:ball_go(ball,w+fast//2,10,num))
    #     #整体动画控制
    #     def start():
    #         if ifok:
    #             return
    #         for i, ball in enumerate(balls):
    #             #每0.3秒释放一个小球标识
    #             self.after(i * 300, lambda ball=ball:_start(ball))
    #     def stop():
    #         nonlocal ifok
    #         ifok = True
    #         for i in balls:
    #             self.itemconfig(i,state='hidden')
    #         self.itemconfig(back,fill=okcolor,width=3)
    #     ifok = False
    #     back=self.create_line((pos[0],pos[1]+5,pos[0]+width+5,pos[1]+5),fill=fg,width=1,capstyle='round')
    #     uid=f'waitbar2-{back}'
    #     self.itemconfig(back,tags=uid)
    #     self.__auto_anchor(uid,pos,anchor)
    #     balls=[]
    #     for _ in range(5):
    #         ball=self.create_text(pos,text='\uF127',fill=fg,state='hidden',font='{Segoe Fluent Icons} 4',tags=uid)
    #         balls.append(ball)
    #     start()
    #     return back,balls,stop,uid

    def add_combobox(self,pos:tuple,width:int=200,height:int=200,text='',content:tuple=(),fg='#1a1a1a',bg='#f8f8f8',outline='#c8c8c8',activefg='#1a1a1a',activebg='#f6f6f6',activeline='#cccccc',onfg='#5d5d5d',onbg='#f5f5f5',online='#e5e5e5',listfg='#1a1a1a',listactivefg='#191919',listactivebg='#e9e9e9',listonfg='#191919',listonbg='#ececec',listsel='#b4bbea',scrollbg='#f0f0f0',scrollcolor='#999999',scrollon='#89898b',tran='#01FF11',font=('微软雅黑',12),anchor='nw',command=None):#绘制组合/下拉框
        def open_box(event):
            mouseout(None)
            self.move(button, 0, -1)
            if not drop:#未展开
                self.itemconfig(button,text='\uE70E')
                show(event)
            else:
                unshow(None)
                self.itemconfig(button,text='\uE70D')
        def move_box(event):
            self.itemconfig(back, fill=onbg, outline=onbg)
            self.itemconfig(main, fill=onfg)
            self.itemconfig(button, fill=onfg)
            self.itemconfig(oline, fill=online, outline=online)
            self.move(button, 0, 1)
        def mousein(e):
            #鼠标进入
            self.itemconfig(back,fill=activebg,outline=activebg)
            self.itemconfig(main,fill=activefg)
            self.itemconfig(button,fill=activefg)
            self.itemconfig(oline, fill=activeline, outline=activeline)
        def mouseout(e):
            #鼠标离开
            self.itemconfig(back,fill=bg,outline=bg)
            self.itemconfig(main,fill=fg)
            self.itemconfig(button,fill=fg)
            self.itemconfig(oline, fill=outline, outline=outline)
        def readyshow():#计算显示位置
            allpos=bar.bbox('all')
            #菜单尺寸
            winw=allpos[2]-allpos[0]+5
            winh=allpos[3]-allpos[1]+5
            #屏幕尺寸
            maxx=self.winfo_screenwidth()
            maxy=self.winfo_screenheight()
            wind.data=(maxx,maxy,winw,winh)
        def show(event):#显示的起始位置
            nonlocal drop
            drop=True
            #初始位置
            maxx,maxy,winw,winh=wind.data
            bbox=self.bbox(uid)
            scx,scy=event.x_root,event.y_root#屏幕坐标
            dx,dy=round(self.canvasx(event.x)-bbox[0]),round(self.canvasy(event.y)-bbox[3])#画布坐标差值
            sx,sy=scx-dx,scy-dy
            if sx+winw>maxx:
                x=sx-winw
            else:
                x=sx
            if sy+winh>maxy:
                y=sy-winh
            else:
                y=sy
            pickbox.geometry(f'{winw+15}x{winh+15}+{x-4}+{y}')
            pickbox.attributes('-alpha',0)
            pickbox.deiconify()
            it = 0
            for i in (0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1):
                pickbox.after(it*20, lambda alpha=i : __show(alpha))
                it += 1
        def __show(alpha):
            pickbox.attributes('-alpha',alpha)
            pickbox.update_idletasks()
            if alpha == 1:
                pickbox.focus_set()
        def unshow(event):
            nonlocal drop
            drop=False
            pickbox.withdraw()
            self.itemconfig(button,text='\uE70D',fill=fg)
        def choose_this(word):
            self.itemconfig(main,text=word)
            unshow(None)
            if command:
                command(word)
        def select(num):
            self.itemconfig(button,text='\uE70E',fill=activefg)
            choose_this(content[num])
        def disable(fg='#9d9d9d',bg='#f5f5f5'):
            self.itemconfig(button,text='\uE70D',fill=fg)
            self.itemconfig(main,fill=fg)
            self.itemconfig(back,fill=bg,outline=bg)
            self.itemconfig(uid,state='disabled')
            unshow(None)
        def active():
            self.itemconfig(button,fill=fg)
            self.itemconfig(main,fill=fg)
            self.itemconfig(back,fill=bg,outline=bg)
            self.itemconfig(uid,state='normal')
        if activefg=='':
            activefg=self['background']
        main=self.create_text(pos,text=text,font=font,fill=fg,anchor='nw')
        uid=TinUIString(f'combobox-{main}')
        self.itemconfig(main,tags=uid)
        bbox=self.bbox(main)#文本尺寸
        x1,y1,x2,y2=bbox[0]+3,bbox[1]+3,bbox[0]+width-3,bbox[3]-3
        drop=False#未展开
        iconfont=tkfont.Font(font=font)
        font_size=str(iconfont.cget('size'))
        button=self.create_text((x2-1,(y1+y2)/2),text='\uE70D',fill=fg,font='{Segoe Fluent Icons} '+font_size,tags=uid,anchor='w')#按钮
        x1,y1,x2,y2=self.bbox(uid)#文本与按钮区域
        back=self.__ui_polygon(((x1+1,y1+1),(x2-1,y2-1)),fill=bg,outline=bg,width=9,tags=uid)
        oline=self.__ui_polygon(((x1,y1),(x2,y2)),fill=outline,outline=outline,width=9,tags=uid)
        self.tkraise(back)
        self.tkraise(main)
        self.tkraise(button)
        self.tag_bind(uid,'<Button-1>',move_box)
        self.tag_bind(uid,'<ButtonRelease-1>',open_box)
        self.tag_bind(uid,'<Enter>',mousein)
        self.tag_bind(uid,'<Leave>',mouseout)
        pickbox=Toplevel(self)#浮出窗口
        pickbox.withdraw()
        pickbox.bind('<FocusOut>', unshow)
        self.windows.append(pickbox)
        pickbox.geometry(f'{width+16}x{height}')
        pickbox.overrideredirect(True)
        pickbox.attributes('-topmost',1)
        pickbox.attributes('-transparent',tran)
        wind=TinUINum()#记录数据
        bar=BasicTinUI(pickbox,bg=tran)
        bar.pack(fill='both',expand=True)
        bar.__ui_polygon(((13,13),(x2-x1-4,height-12)),fill=bg,outline=bg,width=17)
        bar.lower(bar.__ui_polygon(((12,12),(x2-x1-3,height-11)),fill=outline,outline=outline,width=17))
        boxback = bar.add_listbox((2,2),x2-x1-7,height-15,bg=bg,fg=listfg,data=content,activefg=listactivefg,activebg=listactivebg,onfg=listonfg,onbg=listonbg,sel=listsel,font=font,scrollbg=scrollbg,scrollcolor=scrollcolor,scrollon=scrollon,command=choose_this)[1]
        bar.delete(boxback)
        self.__auto_anchor(uid,pos,anchor)
        readyshow()
        del iconfont,font_size,bbox,x1,y1,x2,y2
        funcs=FuncList(3)
        funcs.select=funcs[0]=select
        funcs.disable=funcs[1]=disable
        funcs.active=funcs[2]=active
        uid.layout=lambda x1,y1,x2,y2,expand=False: self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
        return main,back,bar,funcs,uid

    def add_progressbar(self,pos:tuple,width=250,fg='#868686',bg='#334ac0',back='#f3f3f3',fontc='#79b8f8',percentage=True,text='',anchor='nw'):#绘制进度条
        def __layout(x1,y1,x2,y2,expand=False):
            nonlocal width
            if not expand:
                self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
            else:
                width=x2-x1
                width2=width*per/100
                y=(y1+y2)/2
                self.coords(outline,x1+4,y-3.5,x2-4,y-3.5,x2-4,y+3.5,x1+4,y+3.5)
                self.coords(back,x1+5,y-2.5,x2-5,y-2.5,x2-5,y+2.5,x1+5,y+2.5)
                self.coords(progressbar,x1+4,y-3.5,x1+4+width2,y-3.5,x1+4+width2,y+3.5,x1+4,y+3.5)
                self.coords(text,x1+width/2,y)
                pos[0]=x1
                pos[1]=y-7.5
        def goto(num:int):
            nonlocal per
            if not 0<=num<=100:
                return
            per=num
            pw=width*per/100
            pw=max(8,pw)
            self.coords(progressbar,pos[0]+4,pos[1]+4,pos[0]+pw-4,pos[1]+4,pos[0]+pw-4,pos[1]+11,pos[0]+4,pos[1]+11)
            if percentage:
                self.itemconfig(text,text=str(per)+'%')
            self.update_idletasks()
        def now_running():
            self.itemconfig(text,fill=fontc)
            self.itemconfig(back,outline=fg)
            self.itemconfig(progressbar,outline=bg,fill=bg)
        def now_paused(fg='#868686',bg='#9d5d00',fontc='#cdcdcd'):
            self.itemconfig(text,fill=fontc)
            self.itemconfig(back,outline=fg)
            self.itemconfig(progressbar,outline=bg,fill=bg)
        def now_error(fg='#868686',bg='#c42b1c',fontc='#cdcdcd'):
            self.itemconfig(text,fill=fontc)
            self.itemconfig(back,outline=fg)
            self.itemconfig(progressbar,outline=bg,fill=bg)
        pos=list(pos)
        per=0#当前进度
        outline=self.__ui_polygon(((pos[0]+4,pos[1]+4),(pos[0]+width-4,pos[1]+11)),outline=fg,fill=fg,width=9)
        uid=TinUIString(f'progressbar-{outline}')
        self.itemconfig(outline,tags=uid)
        back=self.__ui_polygon(((pos[0]+5,pos[1]+5),(pos[0]+width-5,pos[1]+10)),outline=back,fill=back,width=9,tags=uid)
        progressbar=self.__ui_polygon(((pos[0]+4,pos[1]+4),(pos[0]+4,pos[1]+11)),outline=bg,fill=bg,width=9,tags=uid)
        pro_tagname='progressbar>'+str(back)
        self.addtag_withtag(progressbar,pro_tagname)
        #是否显示默认文本
        if percentage:
            text=self.create_text((pos[0]+width//2,pos[1]+7.5),anchor='center',text='0%',fill=fontc,font='微软雅黑 10',tags=uid)
        else:
            text=self.create_text((pos[0]+width//2,pos[1]+7.5),anchor='center',text=text,fill=fontc,font='微软雅黑 10',tags=uid)
        dx,dy=self.__auto_anchor(uid,pos,anchor)
        pos[0]+=dx
        pos[1]+=dy
        del dx,dy
        funcs=FuncList(3)
        funcs.now_running=funcs[0]=now_running
        funcs.now_paused=funcs[1]=now_paused
        funcs.now_error=funcs[2]=now_error
        uid.layout=__layout
        return outline,back,pro_tagname,text,goto,funcs,uid

    def add_table(self,pos:tuple,outline='#E1E1E1',fg='black',bg='white',data=[['1','2','3'],['a','b','c']],minwidth=100,maxwidth=300,font=('微软雅黑',12),headbg='#d9ebf9',anchor='nw'):#绘制表格
        def get_max_height(widths:dict):
            height=0
            for i in widths.values():
                height=i[1] if i[1]>height else height
            #重新绘制
            for back in widths.keys():
                x1,y1,x2=widths[back][2]
                y2=y1+height
                self.coords(widths[back][0],x1,y1,x2,y2)
                self.tkraise(widths[back][3])
            return height
        end_x,end_y=pos#起始位置
        height,relheight=0,0
        line_width={}#获取每列的固定宽度
        count=1
        ti_list=[]
        uid=TinUIString(f'table-{uuid.uuid1()}')
        for i in data[0]:
            title=self.create_text((end_x,end_y),anchor='nw',text=i,fill=fg,font=font,width=maxwidth)
            self.itemconfig(title,tags=uid)
            bbox=self.bbox(title)
            if bbox[2]-bbox[0]<=minwidth:
                width=minwidth
            else:
                width=bbox[2]-bbox[0]
            line_width[count]=width
            height=bbox[3]-bbox[1]
            relheight=height if height>relheight else relheight
            ti_back=self.create_rectangle((end_x-1,end_y,end_x+width,end_y+height),outline='',fill='',tags=uid)
            ti_list.append((ti_back,end_x-1,end_y,end_x+width))
            end_x=end_x+width+2
            count+=1
            self.tkraise(title)
        for i in ti_list:#保持表头高度一致
            self.coords(i[0],i[1],i[2],i[3],i[2]+relheight)
        end_y=pos[1]+relheight+1
        v_endx,v_endy=pos[0],end_y+2
        for line in data[1:]:
            count=1
            a_dict={}
            end_x=pos[0]
            height=0
            for a in line:
                width=line_width[count]
                cont=self.create_text((end_x,end_y),anchor='nw',text=a,fill=fg,width=width,font=font,tags=uid)
                bbox=self.bbox(cont)
                height=bbox[3]-bbox[1]
                back=self.create_rectangle((end_x-1,end_y,end_x+width,end_y+height),outline=bg,fill=bg,tags=uid)
                self.tkraise(cont)
                a_dict[count]=(back,height,(end_x-1,end_y,end_x+width),cont)#(end_x,end_y,width)为重新绘制确定位置范围
                end_x=end_x+width+2
                count+=1
            height=get_max_height(a_dict)
            end_y=end_y+height+1
            last_line=self.create_line((pos[0],end_y-1,end_x,end_y-1),fill=outline,tags=uid)
        self.delete(last_line)#删除最后一行水平分割线
        for i in ti_list[1:]:#竖直分割线
            self.create_line((i[1]-1,pos[1],i[1]-1,end_y),fill=outline,tags=uid)
        all_back=self.__ui_polygon((pos,(end_x-1,end_y-1)),width=9,outline=headbg,fill=headbg,tags=uid)
        outline_back=self.__ui_polygon(((pos[0]-1,pos[1]-1),(end_x,end_y)),width=9,outline=outline,fill=outline,tags=uid)
        value_back=self.__ui_polygon(((v_endx,v_endy),(end_x-1,end_y-1)),width=9,outline=bg,fill=bg,tags=uid)
        self.lower(value_back)
        self.lower(all_back)
        self.lower(outline_back)
        self.__auto_anchor(uid,pos,anchor)
        del end_x,end_y,height,relheight,line_width,count,ti_list,v_endx,v_endy,a_dict
        uid.layout=lambda x1,y1,x2,y2,expand=False: self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
        return uid

    def add_onoff(self,pos:tuple,fg='#5a5a5a',bg='#ededed',activefg='#575757',activebg='#e5e5e5',onactivefg='#ffffff',onactivebg='#1975c5',onfg='#FFFFFF',onbg='#3041d8',anchor='nw',bd:int=40,command=None):#绘制开关控件
        def __on():
            nonlocal nowstate
            nowstate=True
            if command!=None:
                command(True)
        def __off():
            nonlocal nowstate
            nowstate=False
            if command!=None:
                command(False)
        def __left30():
            f=lambda:self.move(state,-1,0)
            for i in range(0,int(bd/4*3)):
                self.after(i*5,f)
        def __right30():
            f=lambda:self.move(state,1,0)
            for i in range(0,int(bd/4*3)):
                self.after(i*5,f)
        def __on_click(event):
            if not nowstate:
                self.itemconfig(state,fill=onfg)
                __right30()
                self.itemconfig(back,fill=onbg)
                self.itemconfig(outline,fill=onbg)
                __on()
            else:
                self.itemconfig(state,fill=fg)
                __left30()
                self.itemconfig(back,fill=bg)
                self.itemconfig(outline,fill=fg)
                __off()
        def mouse_in(event):
            if nowstate:
                self.itemconfig(state, fill=onactivefg)
                self.itemconfig(back, fill=onactivebg)
                self.itemconfig(outline, fill=onactivebg)
            else:
                self.itemconfig(state, fill=activefg)
                self.itemconfig(back, fill=activebg)
                self.itemconfig(outline, fill=activefg)
        def mouse_out(event):
            if nowstate:
                self.itemconfig(state, fill=onfg)
                self.itemconfig(back, fill=onbg)
                self.itemconfig(outline, fill=onbg)
            else:
                self.itemconfig(state, fill=fg)
                self.itemconfig(back, fill=bg)
                self.itemconfig(outline, fill=fg)
        def on():#开启
            if not nowstate:
                self.itemconfig(state,fill=onfg)
                __right30()
                self.itemconfig(back,fill=onbg)
                self.itemconfig(outline,fill=onbg)
            __on()
        def off():#关闭
            if nowstate:
                self.itemconfig(state,fill=fg)
                __left30()
                self.itemconfig(back,fill=bg)
                self.itemconfig(outline,fill=fg)
            __off()
        def disable(dfg='#f0f0f0',dbg='#bfbfbf'):#禁用
            self.itemconfig(uid,state='disable')
            self.itemconfig(state,fill=dfg)
            self.itemconfig(outline,fill=dbg)
            self.itemconfig(back,fill=dbg)
        def active():#启用
            self.itemconfig(uid,state='normal')
            if nowstate:
                self.itemconfig(state,fill=onfg)
                self.itemconfig(back,fill=onbg)
                self.itemconfig(outline,fill=onbg)
            else:
                self.itemconfig(state,fill=fg)
                self.itemconfig(back,fill=bg)
                self.itemconfig(outline,fill=fg)
        nowstate=False
        back=self.create_text(pos,text='\uEC11',font='{Segoe Fluent Icons} '+str(bd),fill=bg,anchor='nw')
        uid=TinUIString(f'onoff-{back}')
        self.itemconfig(back,tags=uid)
        outline=self.create_text(pos,text='\uEC12',font='{Segoe Fluent Icons} '+str(bd),fill=fg,tags=uid,anchor='nw')
        self.__auto_anchor(uid,pos,anchor)
        bbox=self.bbox(outline)
        state=self.create_text((bbox[0]+(bd/10*3)+1,(bbox[1]+bbox[3])/2-1),text='\uF127',font='{Segoe Fluent Icons} '+str(int(bd/4)),fill=fg,tags=uid,anchor='center')
        self.tag_bind(uid,'<Button-1>',__on_click)
        self.tag_bind(uid,'<Enter>',mouse_in)
        self.tag_bind(uid,'<Leave>',mouse_out)
        del bbox
        funcs=FuncList(4)
        funcs.on=on
        funcs.off=off
        funcs.disable=disable
        funcs.active=active
        uid.layout=lambda x1,y1,x2,y2,expand=False: self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
        return state,back,outline,funcs,uid

    def add_spinbox(self,pos:tuple,width=120,data=('3','2','1'),now='',fg='#1b1b1b',bg='#fefefe',line='#e5e5e5',activefg='#1a1a1a',activebg='#fafafa',onfg='#868686',onbg='#f3f3f3',boxfg='#5f5f5f',boxbg='#f9f9f9',boxactivefg='#5b5b5b',boxactivebg='#f0f0f0',font=('微软雅黑',12),anchor='nw',command=None):#绘制选值框
        def updata(event):
            val=check_in_data()
            if val[0]==True:
                datanum.num=data.index(val[1])
            index=datanum.num-1
            if index<0:
                return
            datanum.num-=1
            wentry.delete(0,'end')
            wentry.insert(0,data[index])
            if command!=None:
                result=TinUIString(data[index])
                result.num=index
                command(result)
        def downdata(event):
            val=check_in_data()
            if val[0]==True:
                datanum.num=data.index(val[1])
            index=datanum.num+1
            if index>maxnum:
                return
            datanum.num+=1
            wentry.delete(0,'end')
            wentry.insert(0,data[index])
            if command!=None:
                result=TinUIString(data[index])
                result.num=index
                command(result)
        def return_data(event):
            val=check_in_data()
            if val[0]==True:
                if command!=None:
                    result=TinUIString(val[1])
                    result.num=data.index(val[1])
                    command(result)
        def mouse_in(event):
            wentry.config(bg=activebg, fg=activefg)
            self.itemconfig(back, outline=activebg, fill=activebg)
        def mouse_out(event):
            wentry.config(bg=bg, fg=fg)
            self.itemconfig(back, outline=bg, fill=bg)
        def _change_data(event):
            self.itemconfig(cui, state='normal')
            self.lift(cui)
        def check_in_data():
            val=wentry.get()
            if val in data:
                return True,val
            else:
                return False,val
        if bg=='':
            bg=self['background']
        wentry=Entry(self,font=font,fg=fg,highlightthickness=0,insertwidth=1,bd=1,bg=bg,relief='flat',insertbackground=fg)
        if now=='' or now not in data:
            now=data[0]
        wentry.insert(0,now)
        entry=self.create_window(pos,window=wentry,width=width,anchor='nw')
        self.windows.append(wentry)
        uid=TinUIString(f'spinbox-{entry}')
        self.itemconfig(entry,tags=uid)
        _font=tkfont.Font(font=font)
        font_size=str(_font.cget('size'))
        _,y1,_,y2=self.bbox(entry)
        # 调节按钮触发调节按钮
        button = self.add_button2((pos[0]+width,(y1+y2)/2),anchor='w',text='\uEC8F',linew=1,line='',activeline='',online='',fg=fg,bg='',activefg=activefg,activebg='',onfg=onfg,onbg='',font='{Segoe Fluent Icons} '+font_size,command=_change_data)
        self.addtag_withtag(uid, button[-1])
        backbbox=self.bbox(uid)
        back=self.__ui_polygon(((backbbox[0]+2,backbbox[1]+4),(backbbox[2]-3,backbbox[3]-5)),fill=bg,outline=bg,width=9,tags=uid)
        outline=self.__ui_polygon(((backbbox[0]+1,backbbox[1]+3),(backbbox[2]-2,backbbox[3]-4)),fill=line,outline=line,width=9,tags=uid)
        # 隐藏的调节按钮
        cui = uid + '_cui'
        button1=self.add_button2((pos[0]+width+2,(y1+y2)/2),anchor='sw',text='\uE70E',linew=1,line=boxbg,activeline=boxactivebg,fg=boxfg,bg=boxbg,activefg=boxactivefg,activebg=boxactivebg,onfg=onfg,onbg=onbg,online=onbg,font='{Segoe Fluent Icons} '+font_size,command=updata)
        button2=self.add_button2((pos[0]+width+2,(y1+y2)/2),anchor='nw',text='\uE70D',linew=1,line=boxbg,activeline=boxactivebg,fg=boxfg,bg=boxbg,activefg=boxactivefg,activebg=boxactivebg,onfg=onfg,onbg=onbg,online=onbg,font='{Segoe Fluent Icons} '+font_size,command=downdata)
        cuiback = self.add_back((0, 0), (button1[-1], button2[-1]), fg=boxbg, bg=boxbg)
        self.addtag_withtag(uid, button1[-1])
        self.addtag_withtag(uid, button2[-1])
        self.addtag_withtag(uid, cuiback)
        self.addtag_withtag(cui, button1[-1])
        self.addtag_withtag(cui, button2[-1])
        self.addtag_withtag(cui, cuiback)
        self.tag_bind(cuiback, '<Leave>', lambda event: self.itemconfig(cui, state='hidden'))
        self.itemconfig(cui, state='hidden')
        self.tkraise(back)
        self.tkraise(entry)
        self.tkraise(button[-1])
        self.tkraise(cuiback)
        self.tkraise(button1[-1])
        self.tkraise(button2[-1])
        datanum=TinUINum()
        datanum.num=data.index(now)#记录数据位置
        maxnum=len(data)-1#最大位置
        self.__auto_anchor(uid,pos,anchor)
        wentry.bind('<Enter>', mouse_in)
        wentry.bind('<Leave>', mouse_out)
        wentry.bind('<Button-1>', mouse_out)
        wentry.bind('<Return>', return_data)
        del _font,font_size,y1,y2
        uid.layout=lambda x1,y1,x2,y2,expand=False: self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
        return wentry,button1,button2,back,outline,button,uid

    def add_scalebar(self,pos:tuple,width=200,fg='#4554dc',activefg='#4554dc',bg='#868686',buttonbg='#ffffff',buttonoutline='#cccccc',data=(1,2,3,4,5),start=1,anchor='nw',command=None):#绘制调节框
        def mousedown(event):
            scale.startx=self.canvasx(event.x)
            self.itemconfig(button_fore,text='\uECCC')
        def drag(event):
            move=self.canvasx(event.x)-scale.startx
            if self.canvasx(event.x)<pos[0] or self.canvasx(event.x)>pos[0]+width:
                return
            self.move(button,move,0)
            self.coords(name,pos[0],pos[1]+8,move+scale.startx,pos[1]+8)
            scale.startx=self.canvasx(event.x)
        def check(event):
            bbox=self.bbox(button_back)
            move=self.canvasx(event.x)-10
            if move>pos[0]+width:
                move=pos[0]+width-18.
            if move<pos[0]:
                move=pos[0]
            self.move(button,move-bbox[0],0)
            bbox=self.bbox(button_back)
            self.itemconfig(button_fore,text='\uE915')#小号圆点
            end=int(self.canvasx(event.x))
            if end<pos[0]:end=pos[0]
            if end>pos[0]+width:end=pos[0]+width
            rend=min(dash,key=lambda x:abs(x-end))
            num=dash.index(rend)
            if command!=None:
                command(data[num])
        def checkval(event):
            move=self.canvasx(event.x)
            self.coords(name,pos[0],pos[1]+8,move,pos[1]+8)
            check(event)
        def __layout(x1,y1,x2,y2,expand=False):
            if not expand:
                dx,dy=self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
            else:
                dx,dy=self.__auto_layout(uid,(x1,y1,x2,y2),'center')
            pos[0]+=dx
            pos[1]+=dy
        def select(num):
            move=dash[num]-self.bbox(button)[0]-10
            self.move(button,move,0)
            self.coords(name,pos[0],pos[1]+8,dash[num],pos[1]+8)
            if command!=None:
                command(data[num])
        def disable():
            self.itemconfig(button_fore,state='disable',fill='#7a7a7a')
            self.itemconfig(back,state='disable')
            self.itemconfig(name,state='disable',fill='#7a7a7a')
            self.itemconfig(uid,state='disable')
        def _active():
            self.itemconfig(uid,state='normal')
            self.itemconfig(button_fore,state='normal',fill=fg)
            self.itemconfig(back,state='normal')
            self.itemconfig(name,state='normal',fill=fg)
        scale=TinUINum()#记录数据结构体
        back=self.create_line((pos[0],pos[1]+8,pos[0]+width,pos[1]+8),fill=bg,width=3,capstyle='round')
        uid=TinUIString(f'scalebar-{back}')
        self.itemconfig(back,tags=uid)
        self.tag_bind(back,'<ButtonRelease-1>',checkval)
        dash_t=width//(len(data)-1)
        s=pos[0]#调节线段起点
        dash=[s]#调节线段的终点位置
        for _ in data[1:]:
            s+=dash_t
            dash.append(s)
        active=self.create_line((pos[0],pos[1]+8,dash[start],pos[1]+8),fill=fg,width=3,tags=uid,capstyle='round')
        name='scaleactive'+str(active)
        self.tag_bind(name,'<ButtonRelease-1>',checkval)
        self.addtag_withtag(name,active)#为重绘绑定tag名称
        button=f'scalebutton{back}'
        button_back=self.create_text((dash[start]+9,pos[1]+9),text='\uF127',font='{Segoe Fluent Icons} 12',fill=buttonbg,tags=(uid,button))
        self.create_text((dash[start]+9,pos[1]+9),text='\uECCA',font='{Segoe Fluent Icons} 12',fill=buttonoutline,tags=(uid,button))
        button_fore=self.create_text((dash[start]+9,pos[1]+9),text='\uE915',font='{Segoe Fluent Icons} 12',fill=fg,tags=(uid,button))
        self.tag_bind(button,'<Enter>',lambda event:self.itemconfig(button_fore,fill=activefg))
        self.tag_bind(button,'<Leave>',lambda event:self.itemconfig(button_fore,fill=fg))
        self.tag_bind(button,'<Button-1>',mousedown)
        self.tag_bind(button,'<B1-Motion>',drag)
        self.tag_bind(button,'<ButtonRelease-1>',check)#矫正位置
        dx,dy=self.__auto_anchor(uid,pos,anchor)
        pos=list(pos)
        pos[0]+=dx
        pos[1]+=dy
        del s,dash_t,dx,dy
        funcs=FuncList(3)
        funcs.select=funcs[0]=select
        funcs.disable=funcs[1]=disable
        funcs._active=funcs[2]=_active
        uid.layout=__layout
        return name,back,button,funcs,uid

    # def add_info(self,pos:tuple,info='info',font='微软雅黑 9',fg='#0078d4',bg='white',info_text='',info_font=('微软雅黑','12'),info_width=200,info_fg='black',width=400,anchor='nw'):#绘制提示框
    #     text=self.create_text(pos,anchor='nw',text=info,font=font,fill=fg)
    #     uid=f'info-{text}'
    #     self.itemconfig(text,tags=uid)
    #     bbox=self.bbox(text)
    #     font_size=self.__get_text_size(text)#字体大小
    #     info=self.create_text((bbox[2],(bbox[1]+bbox[3])/2),anchor='w',text='\uF167',fill=bg,font='{Segoe Fluent Icons}'+font_size,tags=uid)
    #     infoback=self.create_text((bbox[2],(bbox[1]+bbox[3])/2),anchor='w',text='\uE946',fill=fg,font='{Segoe Fluent Icons}'+font_size,tags=uid)
    #     bbox=self.bbox(uid)
    #     back=self.create_rectangle((bbox[0]-2,bbox[1]-2,bbox[2]+2,bbox[3]+2),fill=bg,outline=fg,width=2,tags=uid)
    #     self.tkraise(text)
    #     self.tkraise(info)
    #     self.tkraise(infoback)
    #     self.add_tooltip(uid,text=info_text,fg=info_fg,bg=bg,outline=fg,font=info_font,width=width)
    #     self.__auto_anchor(uid,pos,anchor)
    #     return text,back,uid

    def add_menubar(self,cid='all',bind='<Button-3>',font='微软雅黑 12',fg='#1b1b1b',bg='#fbfbfc',line='#cccccc',activefg='#191919',activebg='#f0f0f0',activeline='#f0f0f0',onfg='#5d5d5d',onbg='#f5f5f5',online='#e5e5e5',cont=(('command',print),'-'),tran='#01FF11'):#绘制菜单
        '''cont格式
        (('名称',绑定的函数（至少接受event参数）),#常规格式
        '-',#分割线
        ...
        )
        '''
        def endy():#获取最低位置
            pos=bar.bbox('all')
            return 0 if pos==None else pos[3]+10
        def repaint():#重新绘制以适配
            maxwidth=max(widths)
            for back in backs:
                if len(back)==2:
                    pos=bar.bbox(back[0])
                    bar_coords = (5,pos[1]+4.5,maxwidth+5-4.5,pos[1]+4.5,maxwidth+5-4.5,pos[3]-4.5,5,pos[3]-4.5)
                    bar_coords_2 = (6,pos[1]+5.5,maxwidth+4-4.5,pos[1]+5.5,maxwidth+4-4.5,pos[3]-5.5,6,pos[3]-5.5)
                    bar.coords(back[0], bar_coords_2)
                    bar.coords(back[1], bar_coords)
                elif len(back)==3:
                    pos=bar.bbox(back[1])
                    bar_coords = (5,pos[1]+4.5,maxwidth+5-4.5,pos[1]+4.5,maxwidth+5-4.5,pos[3]-4.5,5,pos[3]-4.5)
                    bar_coords_2 = (6,pos[1]+5.5,maxwidth+4-4.5,pos[1]+5.5,maxwidth+4-4.5,pos[3]-5.5,6,pos[3]-5.5)
                    bar.coords(back[1], bar_coords_2)
                    bar.coords(back[2], bar_coords)
                    # sign=bar.gettags(back[0])[-1]
            for sep in seps:
                pos=bar.bbox(sep)
                bar.coords(sep,(1,pos[1],5+maxwidth,pos[1]))
        def readyshow():#计算显示位置
            allpos=bar.bbox('all')
            #菜单尺寸
            winw=allpos[2]-allpos[0]+35
            winh=allpos[3]-allpos[1]+35
            #屏幕尺寸
            maxx=self.winfo_screenwidth()
            maxy=self.winfo_screenheight()
            wind.data=(maxx,maxy,winw,winh)
            bar.move('all',0,14)
        def show(event):#显示的起始位置
            #初始位置
            maxx,maxy,winw,winh=wind.data
            sx,sy=event.x_root,event.y_root
            if sx+winw>maxx:
                x=sx-winw
            else:
                x=sx
            if sy+winh>maxy:
                y=sy-winh
            else:
                y=sy
            menu.geometry(f'{winw+30}x{winh+20}+{x}+{y}')
            menu.attributes('-alpha',0)
            menu.deiconify()
            it = 0
            for i in (0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1):
                menu.after(it*20, lambda alpha=i : __show(alpha))
                it += 1
        def __show(alpha):
            menu.attributes('-alpha',alpha)
            menu.update_idletasks()
            if alpha == 1:
                menu.focus_set()
        self.tag_bind(cid,bind,show,True)
        menu=Toplevel(self)
        menu.withdraw()
        menu.bind('<FocusOut>',lambda event:menu.withdraw())
        self.windows.append(menu)
        menu.attributes('-topmost',1)
        menu.overrideredirect(True)
        bar=BasicTinUI(menu,bg=tran)
        bar.pack(fill='both',expand=True)
        wind=TinUINum()#记录数据
        backs=[]#按钮
        funcs=[]#按钮函数接口
        seps=[]#分割线
        widths=[]#寻找最宽位置
        for i in cont:#添加菜单内容
            if i=='-':
                sep=bar.create_line((5,endy(),20,endy()),fill=line,width=3)
                seps.append(sep)
            elif type(i[1]) in (list,tuple):
                #嵌套菜单，只接受列表或元组，不接受集合等
                button=bar.add_menubutton((5,endy()-5),i[0],'x',fg,bg,line,3,activefg,activebg,activeline,onfg,onbg,online,font=font,cont=i[1],tran=tran)
                backs.append((button[0],button[1],button[2]))
                funcs.append(button[3])
                pos=bar.bbox(button[1])
                width=pos[2]-pos[0]
                widths.append(width)
            elif callable(i[1]):
                button=bar.add_button2((0,endy()-13),i[0],None,'',fg,bg,bg,3,activefg,activebg,activeline,onfg,onbg,online,font=font,command=lambda event,i=i:(menu.withdraw(),i[1](event)))
                backs.append((button[1],button[2]))
                funcs.append(button[3])
                pos=bar.bbox(button[1])
                width=pos[2]-pos[0]
                widths.append(width)
        repaint()
        readyshow()
        #绘制圆角边框
        bbox=bar.bbox('all')
        x1=bbox[0]
        x2=bbox[0]+max(widths)+8
        mback=bar.__ui_polygon(((x1+9,bbox[1]+5),(x2-5,bbox[3]-5)),fill=bg,outline=bg,width=17)
        mline=bar.__ui_polygon(((x1+8,bbox[1]+4),(x2-4,bbox[3]-4)),fill=bg,outline=line,width=17)
        bar.lower(mback)
        bar.lower(mline)
        bar.move('all',12,5)
        menu.attributes('-transparent',tran)
        menu.wind=wind#给menubutton用
        return menu,bar,funcs

    def add_tooltip(self,uid,text='',fg='#3b3b3b',bg='#e7e7e7',outline='#3b3b3b',font='微软雅黑 12',tran='#01FF11',delay=0,width=400,pos=None,anchor=None):#绘制窗口提示框
        def show_toti(event,flag=True):
            nonlocal timethread,first
            if first:
                first=False
                first_create()
            if delay!=0 and flag:
                timethread = self.after(delay*1000, show_toti, event, None)
                return
            sx,sy=event.x_root,event.y_root
            if sx+width>maxx:
                x=sx-width
            else:
                x=sx
            if sy+height>maxy:
                y=sy-height
            else:
                y=sy
            toti.geometry(f'{width+20}x{height+20}+{x}+{y}')
            toti.deiconify()
        def hide_toti(event):
            if delay!=0:
                self.after_cancel(timethread)
            toti.withdraw()
        def first_create():#首次使用时创建
            nonlocal toti, bar, bbox, width, height
            toti=Toplevel()
            toti.withdraw()
            self.windows.append(toti)
            toti.overrideredirect(True)
            bar=BasicTinUI(toti,bg=tran)
            bar.pack(fill='both',expand=True)
            info=bar.create_text((10,10),text=text,fill=fg,width=width,font=font,anchor='nw')
            bbox=list(bar.bbox(info))
            width=bbox[2]-bbox[0]+10
            height=bbox[3]-bbox[1]+10
            bbox[0]+=5
            bbox[1]+=5
            bbox[2]-=5
            bbox[3]-=5
            bar.__ui_polygon(((bbox[0]-1,bbox[1]-1),(bbox[2]+1,bbox[3]+1)),fill=outline,outline=outline,width=17)# tline
            bar.__ui_polygon(((bbox[0],bbox[1]),(bbox[2],bbox[3])),fill=bg,outline=bg,width=17)# back
            bar.tkraise(info)
            toti.attributes('-transparent',tran)
            toti.attributes('-alpha',0.9)#透明度90%
        def get_return():
            return toti,bar
        toti=None
        bar=None
        bbox=None
        width=None
        height=None
        #屏幕尺寸
        maxx=self.winfo_screenwidth()
        maxy=self.winfo_screenheight()
        #绑定事件
        first=True
        self.tag_bind(uid,'<Enter>',show_toti,True)
        self.tag_bind(uid,'<Leave>',hide_toti,True)
        timethread=None#延时计时器
        return get_return

    def add_back(self,pos:tuple,uids:tuple=(),fg='',bg='',linew=0,anchor=None):#绘制背景或间隔框
        if len(uids)==0:#优先考虑uids参数，没有则使用pos参数
            back=self.create_rectangle((pos[0],pos[1],pos[0]+1,pos[1]+1),fill=bg,outline=fg,width=linew)
        else:#使用uids参数
            cpos=[None,None,None,None]
            for i in uids:
                bbox=self.bbox(i)
                count=0
                for p,old in zip(bbox,cpos):
                    if count<=1:
                        if old==None or p<old:#起始位置
                            cpos[count]=p
                    else:
                        if old==None or p>old:#最终位置
                            cpos[count]=p
                    count+=1
            back=self.__ui_polygon(((cpos[0]+2,cpos[1]+2),(cpos[2]-2,cpos[3]-2)),fill=bg,outline=fg,width=9+linew)
        self.lower(back)
        return back

    def add_waitbar3(self,pos:tuple,width:int=200,fg='#3041d8',bg='#f3f3f3',okcolor='#0f7b0f',anchor='nw'):#绘制带状等待框
        def move(startx,endx,nowwidth):
            if nowwidth-maxwidth>width:#一轮动画完成
                start()
                return
            self.coords(bar,(pos[0]+startx,pos[1],pos[0]+endx,pos[1]))
            start(nowwidth+5)
        def start(nowwidth=0):#开始动画
            nonlocal timesep,maxwidth
            if ifok:#已完成
                self.itemconfig(bar,fill=okcolor)
                self.coords(bar,(pos[0],pos[1],pos[0]+width,pos[1]))
            if nowwidth==0:#重新定义时间间隔与滑块长度
                if timesep==10:
                    timesep=40
                    maxwidth/=2
                else:
                    timesep=10
                    maxwidth*=2
            if nowwidth<=maxwidth:#增长阶段
                self.after(timesep,lambda : move(0,nowwidth,nowwidth))
            elif nowwidth>=width:#缩小阶段
                self.after(timesep,lambda : move(nowwidth-maxwidth,width,nowwidth))
            else:#平滑阶段。因为取整数，所以平滑阶段无法使用断点判断
                self.after(timesep,lambda : move(nowwidth-maxwidth,nowwidth,nowwidth))
        def __layout(x1,y1,x2,y2,expand=False):
            nonlocal width,maxwidth
            if not expand:
                dx,dy=self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
                pos[0]+=dx
                pos[1]+=dy
            else:
                width=x2-x1
                maxwidth=(width)//3*2
                dx,dy=self.__auto_layout(uid,(x1,y1,x2,y2),'w')
                pos[0]+=dx
                pos[1]+=dy
                self.coords(back,pos[0],pos[1],x2,pos[1])
        def stop():#停止
            nonlocal ifok
            ifok = True
        ifok = False
        timesep=10#时间间隔，快20，慢40
        bbox=(pos[0],pos[1],pos[0]+width,pos[1])
        back=self.create_line(bbox,fill=bg,width=3,capstyle='round')
        uid=TinUIString(f'waitbar3-{back}')
        self.itemconfig(back,tags=uid)
        maxwidth=width//3*2#原长为三分之一，快速模式为原长两倍
        bar=self.create_line((pos[0],pos[1],pos[0],pos[1]),fill=fg,width=3,capstyle='round',tags=uid)
        dx,dy=self.__auto_anchor(uid,pos,anchor)
        pos=list(pos)
        pos[0]+=dx
        pos[1]+=dy
        del bbox
        start()
        uid.layout=__layout
        return back,bar,stop,uid

    def add_textbox(self,pos:tuple,width:int=200,height:int=200,text:str='',anchor='nw',font='微软雅黑 12',fg='black',bg='white',scrollbar=False,outline='#63676b',onoutline='#3041d8',scrollbg='#f0f0f0',scrollcolor='#999999',scrollon='#89898b'):#绘制文本框
        def __layout(x1,y1,x2,y2,expand=False):
            nonlocal width, height
            if not expand:
                dx,dy=self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
                if scrollbar:
                    cid.move(dx,dy,height)
            else:
                dx,dy=self.__auto_layout(uid,(x1,y1,x2,y2),'nw')
                height=y2-y1
                if scrollbar:
                    width2=x2-x1-20
                    dw=width2-width
                    dx+=dw
                    width=width2
                    self.move(cid,dw,0)
                    cid.move(dx,dy,height)
                else:
                    width=x2-x1-4
                self.itemconfig(cavui,width=width,height=height-4)
                coords=self.coords(line)
                coords[2]=coords[4]=x1+width+1
                coords[5]=coords[7]=y2-3
                self.coords(line,coords)
                coords=self.coords(back)
                coords[2]=coords[4]=x1+width
                coords[5]=coords[7]=y2-4
                self.coords(back,coords)
        def focus_in(event):
            self.itemconfig(line,outline=onoutline)
        def focus_out(event):
            self.itemconfig(line,outline=outline)
        def get(start='1.0',end='end'):#获取输入
            return textbox.get(start,end)
        def delete(start='1.0',end='end'):#删除
            textbox.delete(start,end)
        def config(**kw):#设置样式
            textbox.config(**kw)
        textbox=Text(self,font=font,fg=fg,bg=bg,borderwidth=0,relief='flat')
        textbox.bind('<FocusIn>',focus_in,True)
        textbox.bind('<FocusOut>',focus_out,True)
        cavui=self.create_window(pos,window=textbox,width=width-2,height=height-2,anchor='nw')
        self.windows.append(textbox)
        uid=TinUIString(f'textbox-{cavui}')
        self.addtag_withtag(uid,cavui)
        textbox.insert(1.0,text)
        line=self.__ui_polygon(((pos[0]+2,pos[1]+2),(pos[0]+width-5,pos[1]+height-5)),fill=outline,outline=outline,width=9,tags=uid)
        back=self.__ui_polygon(((pos[0]+3,pos[1]+3),(pos[0]+width-6,pos[1]+height-6)),fill=bg,outline=bg,width=9,tags=uid)
        if scrollbar:#不支持横向滚动自动绑定
            bbox=self.bbox(uid)
            cid=self.add_scrollbar((bbox[2]+5,bbox[1]),textbox,bbox[3]-bbox[1],'y',bg=scrollbg,color=scrollcolor,oncolor=scrollon)[-1]
            self.addtag_withtag(uid,cid)
            del bbox
        dx,dy=self.__auto_anchor(uid,pos,anchor)
        if scrollbar:
            cid.move(dx,dy,height)
        del dx,dy
        funcs=FuncList(3)
        funcs.get=get
        funcs.delete=delete
        funcs.config=config
        uid.layout=__layout
        return textbox,funcs,uid

    def add_scrollbar(self,pos:tuple,widget,height:int=200,direction='y',bg='#f0f0f0',color='#999999',oncolor='#89898b',anchor=None):#绘制滚动条
        #滚动条宽度7px，未激活宽度3px；建议与widget相隔5xp
        def enter(event):#鼠标进入
            self.itemconfig(sc,outline=oncolor,width=7)
        def all_enter(event):
            self.itemconfig(top,fill=oncolor)
            self.itemconfig(bottom,fill=oncolor)
            self.itemconfig(back,outline=bg)
        def leave(event):#鼠标离开
            self.itemconfig(sc,outline=color,width=3)
        def all_leave(event):
            self.itemconfig(top,fill='')
            self.itemconfig(bottom,fill='')
            self.itemconfig(back,outline='')
        def widget_move(sp,ep):#控件控制滚动条滚动
            if mode=='y' and use_widget:
                startp=start+canmove*float(sp)
                endp=start+canmove*float(ep)
                self.coords(sc,(pos[0]+5,startp+5,pos[0]+5,endp-5))
            elif mode=='x' and use_widget:
                startp=start+canmove*float(sp)
                endp=start+canmove*float(ep)
                self.coords(sc,(startp+5,pos[1]+5,endp+5,pos[1]+5))
        def mousedown(event):
            nonlocal use_widget#当该值为真，才允许响应widget_move函数
            use_widget=False
            if mode=='y':
                scroll.start=self.canvasy(event.y)#定义起始纵坐标
            elif mode=='x':
                scroll.start=self.canvasx(event.x)#横坐标
        def mouseup(event):
            nonlocal use_widget
            use_widget=True
        def drag(event):
            bbox=self.bbox(sc)
            if mode=='y':#纵向
                move=self.canvasy(event.y)-scroll.start#将窗口坐标转化为画布坐标
                #防止被拖出范围
                if bbox[1]+move<start-1 or bbox[3]+move>end+1:
                    return
                self.move(sc,0,move)
            elif mode=='x':#横向
                move=self.canvasx(event.x)-scroll.start
                if bbox[0]+move<start-1 or bbox[2]+move>end+1:
                    return
                self.move(sc,move,0)
            #重新定义画布中的起始拖动位置
            scroll.start+=move
            sc_move()
        def topmove(event):#top
            bbox=self.bbox(sc)
            if mode=='y':
                move=-(bbox[3]-bbox[1])/2
                if bbox[1]+move<start:
                    move=-(bbox[1]-start)
                self.move(sc,0,move)
            elif mode=='x':
                move=-(bbox[2]-bbox[0])/2
                if bbox[0]+move<start:
                    move=-(bbox[0]-start)
                self.move(sc,move,0)
            sc_move()
        def bottommove(event):#bottom
            bbox=self.bbox(sc)
            if mode=='y':
                move=(bbox[3]-bbox[1])/2
                if bbox[3]+move>end:
                    move=(end-bbox[3])
                self.move(sc,0,move)
            elif mode=='x':
                move=(bbox[2]-bbox[0])/2
                if bbox[2]+move>end:
                    move=(end-bbox[2])
                self.move(sc,move,0)
            sc_move()
        def backmove(event):#back
            bbox=self.bbox(sc)
            if mode=='y':
                posy=self.canvasy(event.y)
                move=posy-bbox[1]
                if move>0 and move+bbox[3]>end:
                    move=end-bbox[3]
                if move<0 and move+bbox[1]<start:
                    move=start-bbox[1]
                self.move(sc,0,move)
            elif mode=='x':
                posx=self.canvasx(event.x)
                move=posx-bbox[0]
                if move>0 and move+bbox[2]>end:
                    move=end-bbox[2]
                if move<0 and move+bbox[0]<start:
                    move=start-bbox[0]
                self.move(sc,move,0)
            sc_move()
        def sc_move():#滚动条控制控件滚动
            bbox=self.bbox(sc)
            if mode=='y':
                startp=(bbox[1]-start)/canmove
                widget.yview('moveto',startp)
            elif mode=='x':
                startp=(bbox[0]-start)/canmove
                widget.xview('moveto',startp)
        def __move(dx,dy,size):
            nonlocal start,end,canmove,height
            pos[0]+=dx
            pos[1]+=dy
            if mode=='y':
                start+=dy
                end=start+size-30
                canmove=size-30
                self.move(bottom,0,size-height)
                coord=self.coords(back)
                coord[3] += size-height
                height=size
                self.coords(back,coord)
            elif mode=='x':
                start+=dx
                end=start+size-30
                canmove=size-40
                self.move(bottom,size-height,0)
                coord=self.coords(back)
                coord[2] += size-height
                height=size
                self.coords(back,coord)
        pos=list(pos)
        if direction.upper()=='X':
            mode='x'
        elif direction.upper()=='Y':
            mode='y'
        else:
            return None
        use_widget=True#是否允许控件控制滚动条
        if mode=='y':
            back=self.create_polygon((pos[0]+5,pos[1]+5,pos[0]+5,pos[1]+height-5,pos[0]+5,pos[1]+5),
            width=13,outline=bg)
            uid=TinUIString(f'scrollbar-{back}')
            self.itemconfig(back,tags=uid)
            top=self.create_text((pos[0]+5,pos[1]+10),text='\ueddb',font='{Segoe Fluent Icons} 7',anchor='s',fill=oncolor,tags=uid)
            bottom=self.create_text((pos[0]+5,pos[1]-10+height),text='\ueddc',font='{Segoe Fluent Icons} 7',anchor='n',fill=oncolor,tags=uid)
            sc=self.create_polygon((pos[0]+5,pos[1]+20,pos[0]+5,pos[1]+height-20,pos[0]+5,pos[1]+20),
            width=3,outline=color,tags=uid)
            #起始和终止位置
            start=pos[1]+15
            end=pos[1]+height-15
            canmove=end-start
            #绑定组件
            widget.config(yscrollcommand=widget_move)
        elif mode=='x':
            back=self.create_polygon((pos[0]+5,pos[1]+5,pos[0]+height-5,pos[1]+5,pos[0]+5,pos[1]+5),
            width=13,outline=bg)
            uid=TinUIString(f'scrollbar-{back}')
            self.itemconfig(back,tags=uid)
            top=self.create_text((pos[0]+10,pos[1]+5),text='\uEDD9',font='{Segoe Fluent Icons} 7',anchor='e',fill=oncolor,tags=uid)
            bottom=self.create_text((pos[0]-10+height,pos[1]+5),text='\uEDDA',font='{Segoe Fluent Icons} 7',anchor='w',fill=oncolor,tags=uid)
            sc=self.create_polygon((pos[0]+20,pos[1]+5,pos[0]+height-20,pos[1]+5,pos[0]+20,pos[1]+5),
            width=3,outline=color,tags=uid)
            start=pos[0]+15
            end=pos[0]+height-15
            canmove=end-start-10
            widget.config(xscrollcommand=widget_move)
        scroll=TinUINum()
        scroll.__move=False
        self.tag_bind(uid,'<Enter>',all_enter)
        self.tag_bind(uid,'<Leave>',all_leave)
        all_leave(None)
        self.tag_bind(sc,'<Button-1>',mousedown)
        self.tag_bind(sc,'<ButtonRelease-1>',mouseup)
        self.tag_bind(sc,'<B1-Motion>',drag)
        #绑定样式
        self.tag_bind(sc,'<Enter>',enter)
        self.tag_bind(sc,'<Leave>',leave)
        #绑定点击滚动
        self.tag_bind(top,'<Button-1>',topmove)
        self.tag_bind(bottom,'<Button-1>',bottommove)
        self.tag_bind(back,'<Button-1>',backmove)
        uid.move=__move
        return top,bottom,back,sc,uid

    def add_listbox(self,pos:tuple,width:int=200,height:int=200,font='微软雅黑 12',data=('a','b','c'),fg='#1a1a1a',bg='#f2f2f2',activefg='#191919',activebg='#e9e9e9',onfg='#191919',onbg='#ececec',sel='#b4bbea',scrollbg='#f0f0f0',scrollcolor='#999999',scrollon='#89898b',anchor='nw',command=None):#绘制列表框
        def repaint_back():
            for v in choices.values():
                bbox=box.coords(v[2])
                box.coords(v[2],3,bbox[1],maxwidth+1,bbox[3])
        def in_mouse(t):
            if choices[t][-1]==True:#已被选中
                return
            box.itemconfig(choices[t][1], fill=activefg)
            box.itemconfig(choices[t][2], fill=activebg)
        def out_mouse(t):
            if choices[t][-1]==True:#已被选中
                box.itemconfig(choices[t][1], fill=onfg)
                box.itemconfig(choices[t][2], fill=sel)
            else:
                box.itemconfig(choices[t][1], fill=fg)
                box.itemconfig(choices[t][2], fill=bg)
        def mouse_click(t):
            if choices[t][-1]==True:#已被选中
                return
            box.itemconfig(choices[t][1], fill=onfg)
            box.itemconfig(choices[t][2], fill=onbg)
        def sel_it(t):
            box.itemconfig(choices[t][1], fill=onfg)
            box.itemconfig(choices[t][2], fill=sel)
            choices[t][-1]=True
            for i in choices.keys():
                if i==t:
                    continue
                choices[i][-1]=False
                out_mouse(i)
            if command!=None:
                name=choices[t][0]
                index=all_keys.index(t)
                result=TinUIString(name)
                result.index=index
                command(result)
        def __re_scroll():
            bbox=box.bbox('all')
            if bbox == None:
                bbox = (0, 0, 0, 0)
            if bbox[2]-bbox[0] > width:
                self.itemconfig(cavui, height=height-8)
                self.itemconfig(vscroll, state='normal')
            else:
                self.itemconfig(cavui, height=height)
                self.itemconfig(vscroll, state='hidden')
            if bbox[3]-bbox[1] > height:
                self.itemconfig(cavui, width=width-8)
                self.itemconfig(hscroll, state='normal')
            else:
                self.itemconfig(cavui, width=width)
                self.itemconfig(hscroll, state='hidden')
            box.config(scrollregion=bbox)
        def _add(item:str='new item'):#添加元素
            load_data({item,})
        def _delete(index:int=0):#删除元素，默认第一个
            nonlocal maxwidth
            total=len(all_keys)
            if index+1>total:#序数超出总数
                return
            key=all_keys[index]
            bbox=box.bbox(choices[key][2])#获取背景尺寸
            item_height=bbox[3]-bbox[1]#高度 元素之间差7 "end+7"
            for cid in choices[key][1:3]:
                box.delete(cid)
            if index+1!=total:#往下所有元素上移
                for keyid in all_keys[index+1:]:
                    box.move(choices[keyid][1],0,-item_height-2)
                    box.move(choices[keyid][2],0,-item_height-2)
            del choices[key]
            del all_keys[index]
            tbbox=box.bbox('textcid')
            maxwidth=tbbox[2]-tbbox[0]
            if maxwidth<width:
                maxwidth=width
            repaint_back()
            __re_scroll()
        def _clear():#清空元素
            nonlocal maxwidth
            for key in choices.keys():
                for cid in choices[key][1:3]:
                    box.delete(cid)
            choices.clear()
            all_keys.clear()
            maxwidth=0
            self.itemconfig(cavui, height=height)
            self.itemconfig(vscroll, state='hidden')
            self.itemconfig(cavui, width=width)
            self.itemconfig(hscroll, state='hidden')
            box.config(scrollregion=(0,0,width,height))
        def load_data(datas):#导入元素
            nonlocal maxwidth
            for i in datas:
                end=box.bbox('item')
                end=5 if end==None else end[-1]
                text=box.create_text((5,end+7),text=i,fill=fg,font=font,anchor='nw',tags=('textcid','item'))
                bbox=box.bbox(text)#获取文本宽度
                back=box.create_rectangle((3,bbox[1]-4,bbox[2]+2,bbox[3]+4),width=0,fill=bg,tags=('item'))
                box.tkraise(text)
                choices[text]=[i,text,back,False]#用文本id代表键，避免选项文本重复带来的逻辑错误
                all_keys.append(text)
                for item_id in (text, back):
                    box.tag_bind(item_id, '<Enter>', lambda event,text=text : in_mouse(text))
                    box.tag_bind(item_id, '<Leave>', lambda event,text=text : out_mouse(text))
                    box.tag_bind(item_id, '<Button-1>', lambda event,text=text : mouse_click(text))
                    box.tag_bind(item_id, '<ButtonRelease-1>', lambda event,text=text : sel_it(text))
            tbbox=box.bbox('textcid')
            if tbbox==None:
                return
            twidth=tbbox[2]-tbbox[0]
            maxwidth=twidth
            if maxwidth<width:
                maxwidth=width
            repaint_back()
            __re_scroll()
        def set_y_view(event):
            box.yview_scroll(int(-1*(event.delta/120)), "units")
        def __layout(x1,y1,x2,y2,expand=False):
            nonlocal width,height
            if not expand:
                dx,dy=self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
                hscroll.move(dx,dy,height)
                vscroll.move(dx,dy,width)
            else:
                dx,dy=self.__auto_layout(uid,(x1,y1,x2,y2),'nw')
                width2=x2-x1-9
                dw=width2-width
                height2=y2-y1-9
                dh=height2-height
                width=width2
                height=height2
                self.move(hscroll,dw,0)
                hscroll.move(dx+dw,dy,height)
                self.move(vscroll,0,dh)
                vscroll.move(dx,dy+dh,width)
                coord=self.coords(allback)
                coord[2]=coord[4]=x2-4
                coord[5]=coord[7]=y2-4
                self.coords(allback,coord)
                self.itemconfig(cavui,width=width,height=height)
                load_data({})
        def clean(event):
            nonlocal all_keys, choices
            del all_keys
            del choices
        def select(index:int=0):#选中元素，默认第一个
            if index > len(all_keys)-1:
                return None
            key = choices[index]
            sel_it(key)
        box=BasicTinUI(self,bg=bg,width=width,height=height)#显示选择内容
        box.place(x=12,y=12)
        cavui=self.create_window(pos,window=box,width=width,height=height,anchor='nw')
        self.windows.append(box)
        uid=TinUIString(f'listbox-{cavui}')
        self.addtag_withtag(uid,cavui)
        hscroll = self.add_scrollbar((pos[0]+width-8,pos[1]),widget=box,height=height,bg=scrollbg,color=scrollcolor,oncolor=scrollon)[-1]#纵向
        vscroll = self.add_scrollbar((pos[0],pos[1]+height-8),widget=box,height=width,direction='x',bg=scrollbg,color=scrollcolor,oncolor=scrollon)[-1]#横向
        self.addtag_withtag(uid, hscroll)
        self.addtag_withtag(uid, vscroll)
        x1, y1, x2, y2 = self.bbox(uid)
        allback = self.__ui_polygon(((x1, y1), (x2, y2)), width=9, outline=bg, fill=bg, tags=uid)
        self.lower(allback,cavui)
        #choices不返回，避免编写者直接操作选项
        all_keys=[]#[a-id,b-id,...]
        choices={}#'a-id':[a,a_text,a_back,is_sel:bool]
        maxwidth=0#最大宽度
        load_data(data)#重复使用元素添加
        box.bind('<MouseWheel>',set_y_view)
        box.bind("<Destroy>", clean)
        del x1,y1,x2,y2
        dx,dy=self.__auto_anchor(uid,pos,anchor)
        hscroll.move(dx,dy,height)
        vscroll.move(dx,dy,width)
        del dx,dy
        funcs=FuncList(4)
        funcs.add=_add
        funcs.delete=_delete
        funcs.clear=_clear
        funcs.select=select
        uid.layout=__layout
        return box,allback,funcs,uid

    def add_listview(self,pos:tuple,width=300,height=300,linew=80,bg='#f3f3f3',activebg='#eaeaea',oncolor='#3041d8',scrobg='#f8f8f8',scroc='#999999',scrooc='#89898b',num=5,anchor='nw',command=None):#绘制列表视图,function:add_list
        def buttonin(itui):
            tinui=itui[0]
            bbox=tinui.bbox(tinui.background)
            if not bbox:
                # 防止被删除
                back=tinui.__ui_polygon(((4,4),(width-8,linew-5)),bg,bg,9)
                tinui.background=back
            tinui.lower(tinui.background)
            tinui.itemconfig(tinui.background,fill=activebg,outline=activebg)
        def buttonout(itui):
            if itui not in items:
                return
            if items.index(itui)!=nowon:
                tinui=itui[0]
                tinui.itemconfig(tinui.background,fill='',outline='')
        def click(itui, send=True):
            nonlocal nowon
            if itui not in items:
                # 这种情况发生于点击子元素内的按钮，触发元素删除
                # 而这仍然会触发此click事件，因此需要判断该元素是否被删除
                return
            index=items.index(itui)
            if nowon <= len(items)-1:
                tinui=items[nowon][0]
                tinui.itemconfig(tinui.background,fill='',outline='')
            nowon=index
            tinui=itui[0]
            tinui.itemconfig(tinui.background,fill=activebg,outline=activebg)
            ui.coords(line,1,index*(linew+2)+lineheight,1,index*(linew+2)+lineheight*2)
            if command!=None and send:
                command(nowon)
        def bindyview(event):
            ui.yview_scroll(int(-1*(event.delta/120)), "units")
        def clean(event):
            items.clear()
        def _load_item(num):
            nonlocal endy
            for _ in range(0,num):
                item=ui.add_ui((3,endy),width=width-3,height=linew,bg=bg)
                items.append(item)
                ui.addtag_withtag('item',item[-1])
                endy+=linew+2
                tinui=item[0]
                back=tinui.__ui_polygon(((4,4),(width-8,linew-5)),'','',9)
                tinui.background=back
                tinui.bind('<Enter>',lambda event,item=item:buttonin(item))
                tinui.bind('<Button-1>',lambda event,item=item:click(item))
                tinui.bind('<Leave>',lambda event,item=item:buttonout(item))
                tinui.bind('<MouseWheel>',bindyview)
            bbox = ui.bbox('item')
            if bbox != None:
                bbox = list(bbox)
                bbox[0] -= 3
                ui.config(scrollregion=bbox)
        def __layout(x1,y1,x2,y2,expand=False):
            nonlocal width,height
            if not expand:
                dx,dy=self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
                scro[-1].move(dx,dy,height)
            else:
                dx,dy=self.__auto_layout(uid,(x1,y1,x2,y2),'nw')
                width2=x2-x1-18
                dw=width2-width
                width=width2
                height=y2-y1-16
                self.move(scroitem,dw,0)
                scroitem.move(dx+dw,dy,height)
                coord=self.coords(allback)
                coord[2]=coord[4]=x2-4
                coord[5]=coord[7]=y2-4
                self.coords(allback,coord)
                self.itemconfig(view,width=width,height=height)
                for i in items:
                    tinui=i[0]
                    ui.itemconfig(i[-1],width=width-3)
                    tinui.coords(tinui.background,4,4,width-11,4,width-11,linew-6,4,linew-6)
        def getitems():#获取items
            return items
        def getui(index):#获取 add_ui uid
            return items[index]
        def delete(index):#删除 add_ui uid
            nonlocal endy, nowon
            if index >= len(items):
                return
            if index == nowon:
                nowon = -1
                ui.moveto(line, 1, -linew)
            elif index < nowon:
                nowon -= 1
                ui.move(line, 0, -linew-2)
            endy-=linew+2
            subui=items[index]
            ui.dtag(subui[-1],'item')
            ui.delete(subui[-1])
            subui[0].destroy()
            del items[index]#删除元素
            #其它UI上移
            if index != len(items):
                for item in items[index:]:
                    ui.move(item[-1],0,-linew-2)
            bbox = ui.bbox('item')
            if bbox == None:
                bbox = (0, 0, 0, 0)
            else:
                bbox = list(bbox)
                bbox[0]-=3
            ui.config(scrollregion=bbox)
        def clear():#清空所有元素
            nonlocal endy, nowon
            num = len(items)
            if num == 0:
                return
            ui.moveto(line, 1, -linew)
            endy = 0
            nowon = -1
            for subui in items:
                ui.dtag(subui[-1],'item')
                ui.delete(subui[-1])
                subui[0].destroy()
            items.clear()
            ui.config(scrollregion=(0,0,width,height))
        def add():#增加 add_ui uid 到底部，并获取返回值
            _load_item(1)
            return items[-1]
        def getsel():# 获取选中项
            return nowon
        def select(index:int):# 选中项，不会触发回调函数
            nonlocal nowon
            if index >= len(items) or index < 0 or index == nowon:
                return
            tinui=items[nowon][0]
            tinui.itemconfig(tinui.background,fill='',outline='')
            nowon = index
            tinui=items[nowon][0]
            tinui.itemconfig(tinui.background,fill=activebg,outline=activebg)
            ui.coords(line,1,index*(linew+2)+lineheight,1,index*(linew+2)+lineheight*2)
            rank = (index+0.5-ui.winfo_height()/2/linew)/items.__len__()
            ui.yview_moveto(rank)
        nowon=-1
        ui=BasicTinUI(self,bg=bg)
        view=self.create_window(pos,window=ui,height=height,width=width,anchor='nw')
        self.windows.append(ui)
        uid=TinUIString(f'listview-{view}')
        self.addtag_withtag(uid,view)
        bbox=self.bbox(view)
        pos=list(pos)
        pos[0],pos[1]=bbox[0],bbox[1]
        scro=self.add_scrollbar((pos[0]+width+2,pos[1]),ui,height=height,bg=scrobg,color=scroc,oncolor=scrooc)
        scroitem=scro[-1]
        self.addtag_withtag(uid,scro[-1])
        items=[]#使用列表作为存储类型，以后可能动态修改列表视图元素
        endy=0
        _load_item(num)#载入元素
        lineheight=linew/3
        line=ui.create_line((1,linew/3,1,linew*2/3),fill=oncolor,width=3,capstyle='round')
        ui.config(scrollregion=ui.bbox('all'))
        ui.move(line,0,-linew-height)
        allback=self.add_back((),(view,scro[-1]),fg=bg,bg=bg,linew=8)
        self.lower(allback,view)
        self.addtag_withtag(uid,allback)
        ui.bind('<MouseWheel>',bindyview)
        ui.bind('<Destroy>', clean)
        del bbox
        dx,dy=self.__auto_anchor(uid,pos,anchor)
        scroitem.move(dx,dy,height)
        del dx,dy
        funcs=FuncList(7)
        funcs.getitems=getitems
        funcs.getui=getui
        funcs.add=add
        funcs.delete=delete
        funcs.clear=clear
        funcs.getsel=getsel
        funcs.select=select
        uid.layout=__layout
        return ui,scro,items,funcs,uid

    # def add_canvas(self,pos:tuple,width:int=200,height:int=200,bg='white',outline='#808080',scrollbg='#f0f0f0',scrollcolor='#999999',scrollon='#89898b',linew=1,scrollbar=False,anchor='nw'):#绘制画布
    #     def re_scrollregion():#更新滚动范围
    #         canvas.config(scrollregion=canvas.bbox('all'))
    #     canvas=Canvas(self,bg=bg,highlightthickness=linew,highlightbackground=outline,highlightcolor=outline,relief='flat')
    #     cavui=self.create_window(pos,window=canvas,width=width,height=height,anchor=anchor)
    #     self.windows.append(canvas)
    #     uid=f'canvas-{cavui}'
    #     self.addtag_withtag(uid,cavui)
    #     if scrollbar==True:
    #         bbox=self.bbox(uid)
    #         cid2=self.add_scrollbar((bbox[0],bbox[3]+5),canvas,bbox[2]-bbox[0],'x',bg=scrollbg,color=scrollcolor,oncolor=scrollon)[-1]
    #         cid1=self.add_scrollbar((bbox[2]+5,bbox[1]),canvas,bbox[3]-bbox[1],bg=scrollbg,color=scrollcolor,oncolor=scrollon)[-1]
    #         self.addtag_withtag(uid,cid1)
    #         self.addtag_withtag(uid,cid2)
    #     return canvas,re_scrollregion,uid

    def add_ui(self,pos:tuple,width:int=200,height:int=200,bg='white',scrollbg='#f0f0f0',scrollcolor='#999999',scrollon='#89898b',scrollbar=False,region='man',anchor='nw'):#绘制BasicTinUI
        def __update():#更新宽高
            re_scrollregion()
            ui.after(1000,__update)
        def re_scrollregion():#更新滚动范围
            bbox=ui.bbox('all')
            if bbox!=None:
                ui.config(scrollregion=bbox)
        def __layout(x1,y1,x2,y2,expand=False):
            nonlocal width,height
            if not expand:
                dx,dy=self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
                if scrollbar:
                    cid1.move(dx,dy,height)
                    cid2.move(dx,dy,width)
            else:
                dx,dy=self.__auto_layout(uid,(x1,y1,x2,y2),'nw')
                if scrollbar:
                    width2=x2-x1-12
                    dw=width2-width
                    height2=y2-y1-12
                    dh=height2-height
                    width=width2
                    height=height2
                    self.move(cid1,dw,0)
                    cid1.move(dx+dw,dy,height)
                    self.move(cid2,0,dh)
                    cid2.move(dx,dy+dh,width)
                else:
                    width=x2-x1
                    height=y2-y1
                self.itemconfig(cavui,width=width,height=height)
        ui=BasicTinUI(self,bg=bg)
        cavui=self.create_window(pos,window=ui,width=width,height=height,anchor='nw')
        self.windows.append(ui)
        uid=TinUIString(f'ui-{cavui}')
        self.addtag_withtag(uid,cavui)
        if scrollbar:
            bbox=self.bbox(uid)
            cid1=self.add_scrollbar((bbox[2]+5,bbox[1]),ui,bbox[3]-bbox[1],bg=scrollbg,color=scrollcolor,oncolor=scrollon)[-1]
            cid2=self.add_scrollbar((bbox[0],bbox[3]+5),ui,bbox[2]-bbox[0],'x',bg=scrollbg,color=scrollcolor,oncolor=scrollon)[-1]
            self.addtag_withtag(uid,cid1)
            self.addtag_withtag(uid,cid2)
            del bbox
            if region=='auto':#自动调节
                __update()
        ui_xml=TinUIXml(ui)
        ui.bind('<Destroy>', lambda event: self.__delete_uixml(ui_xml))
        dx,dy=self.__auto_anchor(uid,pos,anchor)
        if scrollbar:
            cid1.move(dx,dy,height)
            cid2.move(dx,dy,width)
        uid.layout=__layout
        return ui,re_scrollregion,ui_xml,uid

    def add_pipspager(self,pos:tuple,width:int=200,height:int=200,bg='#f3f3f3',fg='#898989',buttonfg='#8a8a8a',buttonbg='#f9f9f9',activefg='#5f5f5f',activebg='#f9f9f9',buttononfg='#5f5f5f',buttononbg='#f9f9f9',num:int=2,anchor='nw'):#绘制翻页视图
        def move_left(event):
            nonlocal nowui
            if nowui==0:
                pass
            else:
                __dot_in(dotlist[nowui-1])
                __dot_select(dotlist[nowui-1])
        def move_right(event):
            nonlocal nowui
            if nowui==len(uilist)-1:
                pass
            else:
                __dot_in(dotlist[nowui+1])
                __dot_select(dotlist[nowui+1])
        def __move_to(number):#显示视图
            nonlocal nowui
            oldone=nowui
            def animate(startwidth,times):#展开动画
                if mode == 'right':
                    self.itemconfig(newui,width=startwidth+inchx)
                    self.move(newui,-inchx,0)
                else:
                    self.itemconfig(oldui,width=width-startwidth-inchx)
                    self.move(oldui,inchx,0)
                self.update_idletasks()
                if times<19:
                    self.after(10,lambda:animate(startwidth+inchx,times+1))
                else:
                    self.itemconfig(newui,width=width)
                    self.itemconfig(oldui,state='hidden')
            inchx=width/20#翻页动画参数
            newui=uilist[number][0]
            oldui=uilist[oldone][0]
            mode=None
            if number>=nowui:#向右翻页
                self.moveto(newui,startx+width,pos[1])
                mode='right'
            else:#向左翻页
                self.moveto(newui,startx,pos[1])
                self.moveto(oldui,startx,pos[1])
                mode='left'
            self.itemconfig(newui,state='normal')
            animate(0,0)
            nowui=number#新标志
        def move_to(number):
            __dot_in(dotlist[nowui])
            __dot_select(dotlist[nowui])
            __move_to(nowui)
        def __dot_in(dote):
            bar.itemconfig(dote,text='●')
        def __dot_out(dote):
            if dotlist.index(dote)==nowui:
                pass
            else:
                bar.itemconfig(dote,text='•')
        def __dot_select(dote):
            number=dotlist.index(dote)
            if number==nowui:
                pass
            else:
                __move_to(number)
                for i in dotlist:
                    if i==dote:
                        continue
                    else:
                        bar.itemconfig(i,text='•')
                #修正视图
                bbox=bar.bbox(dote)
                allbbox=bar.bbox('all')#全部元素
                rsrate=(bbox[2]+10)/allbbox[2]#需要展示的右边位置
                lsrate=(bbox[0]-10)/allbbox[2]#左边
                if rsrate>1:rsrate=1
                if lsrate<0:lsrate=0
                nowrate=bar.xview()
                if rsrate>nowrate[1]:
                    bar.xview_moveto(rsrate)
                elif lsrate<nowrate[0]:
                    bar.xview_moveto(lsrate)
                    bar.xview_scroll(-3,'unit')
        def __layout(x1,y1,x2,y2,expand=False):
            nonlocal width,height,startx
            if not expand:
                dx,dy=self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
                startx+=dx
                pos[1]+=dy
            else:
                width2=x2-x1-40
                height2=y2-y1-16
                dx,dy=self.__auto_layout(uid,(x1,y1,x2,y2),'nw')
                startx=x1+22
                pos[1]=y1
                self.itemconfig(barid,width=width2)
                for i in uilist:
                    self.itemconfig(i[0],width=width2,height=height2)
                dh=(height2-height)/2
                dw=width2-width
                self.move(leftbutton,0,dh)
                self.move(rightbutton,dw,dh)
                self.move(barid,0,dh*2)
                width=width2
                height=height2
        pos=list(pos)
        startx=pos[0]+20#按钮与主窗口间隔
        uilist=[]#[(uiid-1,BasicTinUI-1,TinUIXml-1),(uiid-2,BasicTinUI-2,TinUIXml-2),...]
        doty=pos[1]+height+5#控制点的起始纵坐标
        dotlist=[]#[dot1,dot2,...]
        nowui=0#当前显示界面序号
        leftbutton=self.add_button2((startx-1,pos[1]+width/2),'','\n\uedd9\n',font='{Segoe Fluent Icons} 7',fg=buttonfg,bg=buttonbg,line=buttonbg,linew=0,activefg=activefg,activebg=activebg,activeline=activebg,onbg=buttononbg,onfg=buttononfg,online=buttononbg,command=move_left,anchor='e')[-1]
        rightbutton=self.add_button2((startx+width,pos[1]+width/2),'','\n\uedda\n',font='{Segoe Fluent Icons} 7',fg=buttonfg,bg=buttonbg,line=buttonbg,linew=0,activefg=activefg,activebg=activebg,activeline=activebg,onbg=buttononbg,onfg=buttononfg,online=buttononbg,command=move_right,anchor='w')[-1]
        uid=TinUIString(f'pipspager-{leftbutton}')
        self.addtag_withtag(uid,leftbutton)
        self.addtag_withtag(uid,rightbutton)
        bar=Canvas(self,bg=bg,highlightthickness=0,relief='flat')#导航栏
        barid=self.create_window((startx,doty),window=bar,width=width,height=11,anchor='nw',tags=uid)
        self.windows.append(bar)
        dotx=3
        for _ in range(0,num):
            ui=BasicTinUI(self,bg=bg)
            tinuixml=TinUIXml(ui)
            ui.bind('<Destroy>', lambda event, uixml=tinuixml: self.__delete_uixml(uixml))
            uiid=self.create_window((startx,pos[1]),window=ui,width=width,height=height,state='hidden',anchor='nw',tags=uid)
            self.windows.append(ui)
            uilist.append((uiid,ui,tinuixml))
            dot=bar.create_text((dotx+2,5.5),text='•',fill=fg,font=('微软雅黑',8),anchor='center')
            dotlist.append(dot)
            dotx+=15
            bar.tag_bind(dot,'<Enter>',lambda event,dote=dot:__dot_in(dote))
            bar.tag_bind(dot,'<Leave>',lambda event,dote=dot:__dot_out(dote))
            bar.tag_bind(dot,'<Button-1>',lambda event,dote=dot:__dot_select(dote))
        self.itemconfig(uilist[nowui][0], state='normal')
        self.lift(uilist[nowui][0])
        bar.config(scrollregion=bar.bbox('all'))
        del doty,dotx
        dx,_=self.__auto_anchor(uid,pos,anchor)
        startx+=dx
        del dx
        uid.layout=__layout
        return uilist,dotlist,move_to,uid

    def add_notebook(self,pos:tuple,width:int=400,height:int=400,color='#f3f3f3',fg='#5d5d5d',bg='#f3f3f3',activefg='#595959',activebg='#e9e9e9',onfg='#1a1a1a',onbg='#f9f9f9',scrollbg='#f0f0f0',scrollcolor='#999999',scrollon='#89898b',anchor='nw'):#绘制标签栏视图
        def __onenter(flag):
            if flag==nowpage:
                return
            t,c,b=tbdict[flag]
            tbu.itemconfig(t,fill=activefg)
            tbu.itemconfig(c,fill=activefg)
            tbu.itemconfig(b,fill=activebg,outline=activebg)
        def __onleave(flag):
            if flag==nowpage:
                return
            t,c,b=tbdict[flag]
            tbu.itemconfig(t,fill=fg)
            tbu.itemconfig(c,fill=fg)
            tbu.itemconfig(b,fill=bg,outline=bg)
        def __onclick(flag):
            if flag==nowpage:
                return
            t,c,b=tbdict[flag]
            tbu.itemconfig(t,fill=onfg)
            tbu.itemconfig(c,fill=onfg)
            tbu.itemconfig(b,fill=onbg,outline=onbg)
        def __onnpin(e):
            tbu.itemconfig(newpageback,fill=activebg,outline=activebg)
        def __onnpleave(e):
            tbu.itemconfig(newpageback,fill=bg,outline=bg)
        def __onnpclick(e):
            if newfunction!=None:
                newfunction()
        def addpage(title:str,flag=None,scrollbar:bool=False,cancancel:bool=True):#创建页面
            nonlocal npx
            if tbu.bbox(labeluid)==None:
                endx=3
            else:
                endx=tbu.bbox(labeluid)[2]+3
            titleu=tbu.create_text((endx,6),text=title,fill=fg,font=font,anchor='nw',tags=labeluid)#标题
            tbubbox=tbu.bbox(titleu)
            cby=(tbubbox[1]+tbubbox[3])//2
            cbx=tbubbox[2]+10
            cb=tbu.create_text((cbx,cby),text='\uE8BB',font='{Segoe Fluent Icons} 7',fill=fg,anchor='w',tags=labeluid)#页面删除按钮文本
            tbbbox=tbu.bbox(titleu)
            if cancancel==False:
                tbu.itemconfig(cb,state='hidden')
            bu=tbu.__ui_polygon(((endx+2,tbbbox[1]),(cbx+13,tbbbox[3])),fill=bg,outline=bg,width=9,tags=labeluid)
            tbu.lower(bu)
            #移动newpageuid
            npmovex=cbx+15+5.5-npx
            tbu.move(newpageuid,npmovex,0)
            npx=cbx+15+5.5
            if flag==None:
                flag='flag'+str(titleu)
            if scrollbar:
                page=TinUI(self,True,bg=self['background'])
                uiid=self.create_window(viewpos,window=page.frame,width=width+4,height=height-3,anchor='nw',state='hidden',tags=uid)
                self.windows.append(page.frame)
            else:
                page=BasicTinUI(self,bg=self['background'])
                uiid=self.create_window(viewpos,window=page,width=width+4,height=height-3,anchor='nw',state='hidden',tags=uid)
                self.windows.append(page)
            uixml=TinUIXml(page)
            page.bind('<Destroy>', lambda event: self.__delete_uixml(uixml))
            bbox=tbu.bbox('all')
            if bbox and bbox[2]-bbox[0] > width:
                self.itemconfig(scro[-1], state='normal')
            else:
                self.itemconfig(scro[-1], state='hidden')
            tbu.config(scrollregion=bbox)
            vdict[flag]=(page,uixml,uiid)
            tbdict[flag]=(titleu,cb,bu)
            flaglist.append(flag)
            for item_id in (titleu, cb, bu):
                tbu.tag_bind(item_id,'<Enter>',lambda event,f=flag:__onenter(f))
                tbu.tag_bind(item_id,'<Leave>',lambda event,f=flag:__onleave(f))
            tbu.tag_bind(titleu,'<Button-1>',lambda event:showpage(flag))
            tbu.tag_bind(bu,'<Button-1>',lambda event:showpage(flag))
            tbu.tag_bind(cb,'<Button-1>',lambda event:deletepage(flag))
            return flag
        def showpage(flag):#显示页面
            nonlocal nowpage
            mp=nowpage#中间逻辑变量
            if nowpage!='':
                self.itemconfig(vdict[nowpage][2],state='hidden')
                nowpage=flag
                __onleave(mp)
                nowpage=mp
            self.itemconfig(vdict[flag][2],state='normal')
            __onclick(flag)
            nowpage=flag
        def deletepage(flag):#删除页面
            nonlocal nowpage,npx
            wbbox=tbu.bbox(tbdict[flag][2])
            w = wbbox[2] - wbbox[0] - 1
            for i in tbdict[flag]:
                tbu.delete(i)
            self.delete(vdict[flag][2])
            vdict[flag][0].destroy()
            index=flaglist.index(flag)
            if index+1 != len(tbdict):
                for i in flaglist[index+1:]:
                    for iid in tbdict[i]:
                        tbu.move(iid,-w,0)
            #移动newpageuid
            tbu.move(newpageuid,-w,0)
            npx-=w#调整当前位置
            #---
            if flag==nowpage:
                if len(tbdict)==1:
                    nowpage=''
                elif index+1<len(tbdict):
                    showpage(flaglist[index+1])
                    nowpage=flaglist[index+1]
                elif index+1==len(tbdict):
                    showpage(flaglist[index-1])
                    nowpage=flaglist[index-1]
            del tbdict[flag]
            del vdict[flag]
            del flaglist[index]
            bbox=tbu.bbox('all')
            if bbox and bbox[2]-bbox[0] > width:
                self.itemconfig(scro[-1], state='normal')
            else:
                self.itemconfig(scro[-1], state='hidden')
            tbu.config(scrollregion=bbox)
        def getuis(flag):#获取对应窗口
            return vdict[flag]
        def gettitles(flag):#获取对应标题
            return tbdict[flag]
        def getvdict():#获取元素字典
            return vdict
        def gettbdict():#获取标题元素字典
            return tbdict
        def cannew(can=False,newfunc=None):#是否响应新界面函数
            nonlocal newfunction
            newfunction=newfunc
            if can:
                tbu.itemconfig(newpageuid,state='normal')
            if not can:
                tbu.itemconfig(newpageuid,state='hidden')
            bbox=tbu.bbox('all')
            tbu.config(scrollregion=bbox)
        def newtitle(flag,title_text=''):#重设标题
            nonlocal npx
            newpustate=tbu.itemcget(newpageuid,'state')
            tbu.itemconfig(newpageuid,state='normal')#此刻连着新界面按钮一起移动
            title,cb,pyo=tbdict[flag]
            title_bbox=tbu.bbox(title)
            old_title_width=title_bbox[2]-title_bbox[1]#原文本宽度
            pyo_bbox=tbu.bbox(pyo)
            tbu.itemconfig(title,text=title_text)#修改标题
            title_bbox=tbu.bbox(title)
            tbu.itemconfig(title,text='')
            new_title_width=title_bbox[2]-title_bbox[1]#现文本宽度
            movex=new_title_width-old_title_width
            all_bbox=tbu.bbox('all')
            tbu.addtag(movename,'overlapping',pyo_bbox[2]+1,2,all_bbox[2],all_bbox[3])
            tbu.move(movename,movex,0)#移动其它标题
            tbu.dtag(movename)
            pyo_t=(pyo_bbox[0]+6,pyo_bbox[1]+6,pyo_bbox[2]+movex-6,pyo_bbox[1]+6,pyo_bbox[2]+movex-6,pyo_bbox[3]-6,pyo_bbox[0]+6,pyo_bbox[3]-6)
            tbu.coords(pyo,pyo_t)#调整背景
            tbu.move(cb,movex,0)
            tbu.itemconfig(title,text=title_text)#修改标题
            tbu.itemconfig(newpageuid,state=newpustate)#恢复样式
            npx+=movex
            bbox=tbu.bbox('all')
            if bbox and bbox[2]-bbox[0] > int(tbu.cget('width')):
                self.itemconfig(scro[-1], state='normal')
            else:
                self.itemconfig(scro[-1], state='hidden')
            tbu.config(scrollregion=bbox)
        def __layout(x1,y1,x2,y2,expand=False):
            nonlocal width,height
            if not expand:
                dx,dy=self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
                scroitem.move(dx,dy,width)
            else:
                dx,dy=self.__auto_layout(uid,(x1,y1,x2,y2),'nw')
                width=x2-x1-12
                height=y2-y1-50
                scroitem.move(dx,dy,width)
                self.itemconfig(tbuid,width=width)
                for i in vdict.values():
                    self.itemconfig(i[-1],width=width+4,height=height)
                coord=self.coords(back)
                coord[2]=coord[4]=x2-8
                coord[5]=coord[7]=y2-8
                self.coords(back,coord)
                bbox=tbu.bbox('all')
                if bbox and bbox[2]-bbox[0] > width:
                    self.itemconfig(scro[-1], state='normal')
                else:
                    self.itemconfig(scro[-1], state='hidden')
                tbu.config(scrollregion=bbox)
            viewpos[0]+=dx
            viewpos[1]+=dy
        tbu=BasicTinUI(self,bg=color)
        tbuid=self.create_window((pos[0]+2,pos[1]+2),window=tbu,width=width,height=30,anchor='nw')
        self.windows.append(tbu)
        uid=TinUIString(f'notebook-{tbuid}')
        labeluid='notebooklabel'#标签元素名称
        movename='movetags'#更改标题时整体移动的临时名称
        self.addtag_withtag(uid,tbuid)
        scro=self.add_scrollbar((pos[0]+5,pos[1]+32),tbu,height=width-10,direction='x',bg=scrollbg,color=scrollcolor,oncolor=scrollon)
        scroitem=scro[-1]
        self.addtag_withtag(uid,scroitem)
        barheight=self.bbox(scroitem)[3]
        #新的backpos横纵坐标集向内缩小3单位
        back=self.__ui_polygon(((pos[0]+8,pos[1]+6),(pos[0]+width,barheight+height-3)),outline=color,fill=color,width=17,tags=uid)
        self.tkraise(tbuid)
        self.tkraise(scroitem)
        viewpos=[pos[0]+2,barheight+2]
        nowpage=''
        vdict={}#ui,uixml,uiid
        tbdict={}#title,cb,pyo
        flaglist=[]
        font='微软雅黑 12'
        #新页面按钮（默认不显示）
        npx=3
        newpageuid=f'notebooknew{tbuid}'
        newpagetext=tbu.create_text((npx,9),text='\uf8aa',font='{Segoe Fluent Icons} 12',fill=fg,anchor='nw',tags=newpageuid)
        nptbbox=tbu.bbox(newpagetext)
        #newpageback
        newpageback=tbu.__ui_polygon(((nptbbox[0]+2,nptbbox[1]+2),(nptbbox[2]-2,nptbbox[3]-2)),fill=bg,outline=bg,width=9,tags=newpageuid)
        tbu.tkraise(newpagetext)
        tbu.itemconfig(newpageuid,state='hidden')
        newfunction=None#触发函数
        tbu.tag_bind(newpagetext,'<Enter>',__onnpin)
        tbu.tag_bind(newpagetext,'<Leave>',__onnpleave)
        tbu.tag_bind(newpagetext,'<Button-1>',__onnpclick)
        bbox=tbu.bbox('all')
        tbu.config(scrollregion=bbox)
        del nptbbox,bbox
        dx,dy=self.__auto_anchor(uid,pos,anchor)
        scroitem.move(dx,dy,width)
        viewpos[0]+=dx
        viewpos[1]+=dy
        del dx,dy
        #新页面按钮完成创建
        notebook=TinUINum
        notebook.addpage=addpage
        notebook.showpage=showpage
        notebook.deletepage=deletepage
        notebook.getuis=getuis
        notebook.gettitles=gettitles
        notebook.getvdict=getvdict
        notebook.gettbdict=gettbdict
        notebook.cannew=cannew
        notebook.newtitle=newtitle
        uid.layout=__layout
        return tbu,scro,back,notebook,uid

    def add_notecard(self,pos:tuple,title='note',text='note text\nmain content',tfg='black',tbg='#fbfbfb',fg='black',bg='#f4f4f4',sep='#e5e5e5',width=200,font='微软雅黑 12',anchor=None):#绘制便笺
        def mousedown(event):
            nonlocal startx,starty
            startx=self.canvasx(event.x)#定义起始横坐标
            starty=self.canvasy(event.y)
        def drag(event):
            nonlocal startx,starty
            nowx=self.canvasx(event.x)
            nowy=self.canvasy(event.y)
            self.move(uid, nowx - startx, nowy - starty)
            startx, starty = nowx, nowy
        startx,starty=None,None#拖动记录点
        toptext=self.create_text((pos[0]+10,pos[1]+10),text=title,font=font,fill=tfg,width=width,anchor='nw')#标题
        uid=f'notecard-{toptext}'
        self.addtag_withtag(uid,toptext)
        tx1,ty1,tx2,ty2=self.bbox(toptext)
        tx2 = max(tx1 + width, tx2)
        topback=self.__ui_polygon(((tx1,ty1),(tx2,ty2)),outline=tbg,fill=tbg,width=17,tags=uid)
        content=self.create_text((tx1,ty2+18),text=text,font=font,fill=fg,width=width,anchor='nw',tags=uid)#便笺内容
        cx1,cy1,cx2,cy2=self.bbox(content)
        cx2 = max(cx1 + width, cx2)
        contentback=self.__ui_polygon(((cx1,cy1),(cx2,cy2)),outline=bg,fill=bg,width=17,tags=uid)
        ax1,ay1,ax2,ay2=self.bbox(uid)#大背景
        self.__ui_polygon(((ax1+8,ay1+8),(ax2-8,ay2-8)),outline=sep,fill=sep,width=17,tags=uid)
        #调整元素层级关系
        self.tkraise(topback)
        self.tkraise(toptext)
        self.tkraise(contentback)
        self.tkraise(content)
        #绑定拖动事件
        for item_id in (topback, toptext):
            self.tag_bind(item_id, '<Button-1>', mousedown)
            self.tag_bind(item_id, '<B1-Motion>', drag)
        return toptext, content, uid

    def add_ratingbar(self,pos:tuple,fg='#585858',bg='#f3f3f3',onfg='#3041d8',onbg='#3041d8',size=12,num:int=5,linew:int=10,anchor='nw',command=None):#绘制评星级控件
        def __onnum(num):
            for i in bars[:num+1]:
                self.itemconfig(i.fill,fill=onbg)
                self.itemconfig(i.line,fill=onfg)
            if num!=len(bars):
                for i in bars[num+1:]:
                    self.itemconfig(i.fill,fill=bg)
                    self.itemconfig(i.line,fill=fg)
        def click(barid):
            nonlocal nowon,tempon
            oldone=nowon
            nowon=bars.index(barid)
            if oldone==nowon==0:#只选定一个时，点击取消选择
                tempon=nowon=-1
                leaveback(None)
            else:
                tempon=nowon
            if command!=None:
                command(nowon+1)
        def onin(barid):
            nonlocal tempon
            index=bars.index(barid)
            tempon=index
            __onnum(index)
        def onleave(barid):
            pass
        def leaveback(event):
            nonlocal tempon
            if nowon==-1:
                for i in bars:
                    self.itemconfig(i.fill,fill=bg)
                    self.itemconfig(i.line,fill=fg)
                return
            __onnum(nowon)
            tempon=nowon
        def __ontemp(event):#鼠标没有正好点在图标上时
            click(bars[tempon])
            __onnum(tempon)
        def setrate(p:int):
            if p > num:
                p = num
            if p < 1:
                p = 1
            nowon = p - 1
            __onnum(nowon)
            click(bars[nowon])
        nowon=-1#已选定
        tempon=-1#待选定
        bars=[]
        item_num=1#总数量
        line_num=1#行数量
        center_x=pos[0]+5
        center_y=pos[1]+5
        uid=TinUIString(f'ratinbar-{uuid.uuid1().hex}')
        starid=f'{uid}star'
        bbox=None
        for i in range(0,num):
            bar=TinUINum(i)
            bar.fill=self.create_text((center_x,center_y),text='\ue735',font='{Segoe Fluent Icons} '+str(size),anchor='nw',fill=bg,tags=(uid,starid))
            bar.line=self.create_text((center_x,center_y),text='\ue734',font='{Segoe Fluent Icons} '+str(size),anchor='nw',fill=fg,tags=(uid,starid))
            bars.append(bar)
            for item_id in (bar.fill, bar.line):
                self.tag_bind(item_id, '<Enter>', lambda event,b=bar:onin(b))
                self.tag_bind(item_id, '<Leave>', lambda event,b=bar:onleave(b))
                self.tag_bind(item_id, '<Button-1>', lambda event,b=bar:click(b))
            if bbox==None:
                bbox=self.bbox(bar.fill)
            if item_num==num:
                break
            if line_num==linew:
                center_x=pos[0]+5
                center_y+=5+(bbox[3]-bbox[1])
                line_num=1
                continue
            item_num+=1
            line_num+=1
            center_x+=5+(bbox[2]-bbox[0])
        start=list(self.bbox(uid))
        start[0]-=5
        start[1]-=5
        start[2]+=5
        start[3]+=5
        back=self.create_rectangle(start,fill=bg,outline=fg,width=1,tags=uid)
        self.lower(back,starid)
        self.tag_bind(back,'<Leave>',leaveback)
        self.tag_bind(back,'<Button>',__ontemp)
        del start,starid,item_num,line_num,bbox,center_x,center_y
        funcs = FuncList(1)
        funcs.setrate = setrate
        self.__auto_anchor(uid,pos,anchor)
        uid.layout=lambda x1,y1,x2,y2,expand=False:self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
        return bars, back, funcs, uid

    def add_radiobox(self,pos:tuple,fontfg='black',font='微软雅黑 12',fg='#8b8b8b',bg='#ededed',activefg='#898989',activebg='#e5e5e5',onfg='#3041d8',onbg='#ffffff',content:tuple=('1','','2'),padx=15,pady=10,anchor='nw',command=None):#绘制单选组控件
        def button_in(sel,sign,sback):
            if sel==select:
                return
            self.itemconfig(sign,fill=activefg)
            self.itemconfig(sback,fill=activebg)
        def button_out(sel,sign,sback):
            if sel==select:
                return
            self.itemconfig(sign,fill=fg)
            self.itemconfig(sback,fill=bg)
        def sel_it(sel,sign,sback):
            nonlocal select
            if sel==select:
                return
            old_select=select#原先选定项目序号
            select=sel
            if old_select>=0:#恢复原先的单选组
                old_sign_back,old_sign=boxes[old_select][0:2]
                self.itemconfig(old_sign,text='\uECCA')#字符还原为空心圆
                button_out(None,old_sign,old_sign_back)
                self.update_idletasks()
            self.itemconfig(sign,text='\uECCC',fill=onbg)#调整字符为实心小圆
            self.itemconfig(sback,fill=onfg)#fg,bg对调，因为此时的back作为边框元素
            if command!=None:
                textid=boxes[sel][2]
                text=self.itemcget(textid,'text')
                command(text)
        def active():
            #激活按钮
            count=0
            for item in boxes:
                if count==select:
                    self.itemconfig(item[0],fill=onfg)
                    self.itemconfig(item[1],fill=onbg)
                else:
                    self.itemconfig(item[0],fill=bg)
                    self.itemconfig(item[1],fill=fg)
                self.itemconfig(item[2],fill=fontfg)
                count+=1
            self.itemconfig(uid,state='normal')
        def disable(fg='#c1c1c1',bg='#f3f3f3'):
            #禁用按钮
            self.itemconfig(uid,state='disabled')
            count=0
            for item in boxes:
                if count==select:
                    self.itemconfig(item[0],fill=fg)
                    self.itemconfig(item[1],fill=bg)
                else:
                    self.itemconfig(item[0],fill=bg)
                    self.itemconfig(item[1],fill=fg)
                self.itemconfig(item[2],fill=fg)
                count+=1
        def _select(index):
            #选定指定项
            back, sign, _, _ = boxes[index]
            sel_it(index, sign, back)
        #标识符内部宽度width和边框宽度line
        back_width=18
        back_line=2#16+2*2=20
        boxes=[]#[(sign_back_id,sign_id,text_id,back_id),...]，换行为(None,'\n',None)
        nowx,nowy=pos#x坐标为左上角插入坐标，y坐标为底部坐标
        uid=TinUIString(f'radiobox-{uuid.uuid1().hex}')
        select=-1#当前选定
        count=-1
        t_bbox=None
        _font=tkfont.Font(font=font)
        size=str(_font.cget('size'))
        for i in content:
            count+=1#计数
            if i=='':
                if t_bbox==None:#没有底部坐标数据
                    nowy+=pady
                else:
                    nowy=t_bbox[3]+pady
                nowx=pos[0]
                boxes.append((None,'\n',None))
                continue
            x1=nowx+back_line
            x2=nowx+back_line+back_width
            sign_back=self.create_text((x1-1,nowy),text='\uF127',font='{Segoe Fluent Icons} '+size,anchor='w',fill=bg,tags=uid)
            sign=self.create_text((x1-1,nowy),text='\uECCA',font='{Segoe Fluent Icons} '+size,anchor='w',fill=fg,tags=uid)
            text=self.create_text((x2+1,nowy),text=i,font=font,fill=fontfg,anchor='w',tags=uid)
            s_bbox=self.bbox(sign)
            t_bbox=self.bbox(text)
            back=self.create_rectangle((s_bbox[0],s_bbox[1],t_bbox[2],t_bbox[3]),width=0,fill='',tags=uid)#一个虚拟元素，用于判定鼠标位置
            boxes.append((sign_back,sign,text,back))
            self.tag_bind(back,'<Enter>',lambda event,sel=count,sign=sign,sback=sign_back:button_in(sel,sign,sback))
            self.tag_bind(back,'<Leave>',lambda event,sel=count,sign=sign,sback=sign_back:button_out(sel,sign,sback))
            self.tag_bind(back,'<Button-1>',lambda event,sel=count,sign=sign,sback=sign_back:sel_it(sel,sign,sback))
            nowx=t_bbox[2]+padx
        self.__auto_anchor(uid,pos,anchor)
        funcs=FuncList(3)
        funcs.active=active
        funcs.disable=disable
        funcs.select=_select
        uid.layout=lambda x1,y1,x2,y2,expand=False:self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
        return boxes,funcs,uid

    def add_pivot(self,pos:tuple,fg='#959595',bg='',activefg='#525252',activecolor='#5969e0',content=(('a-title','tag1'),('b-title','tag2'),'',('c-title','tag3')),font='微软雅黑 16',padx=10,pady=10,anchor='nw',command=None):#绘制支点标题
        def button_in(num,text_uid):
            if num!=select:
                self.itemconfig(text_uid,fill=activefg)
        def button_out(num,text_uid):
            if num!=select:
                self.itemconfig(text_uid,fill=fg)
        def sel_it(num,text_uid,tag,send=True):
            nonlocal select
            if num==select:
                return
            self.itemconfig(texts[select][2],fill=fg)
            select=num
            self.itemconfig(text_uid,fill=activefg)
            bbox=self.bbox(text_uid)
            self.coords(line,(bbox[0],bbox[3]+2,bbox[2],bbox[3]+2))
            if command!=None and send:
                command(tag)
        def _select(index, send=False):
            #选定指定项
            text_uid=texts[index][2]
            tag=texts[index][1]
            sel_it(index, text_uid, tag, send)
        texts=[]#[(text,tag,text-uid),...]
        count=-1
        select=-1#当前选定
        t_bbox=None
        nowx,nowy=pos#x坐标为左上角插入坐标，y坐标为底部坐标
        uid=TinUIString(f'pivot-{uuid.uuid1().hex}')
        line=self.create_line((pos[0],pos[1],pos[0]+5,pos[1]),fill=activecolor,width=3,capstyle='round',tags=uid)
        for i in content:
            count+=1#计数
            if i=='':
                if t_bbox==None:#没有底部坐标数据
                    nowy+=pady
                else:
                    nowy=t_bbox[3]+pady
                nowx=pos[0]
                texts.append(('\n','\n',None))
                continue
            text=self.create_text((nowx,nowy),font=font,text=i[0],fill=fg,anchor='nw',tags=uid)
            t_bbox=self.bbox(text)
            width=t_bbox[2]-t_bbox[0]
            nowx=nowx+width+padx
            texts.append((i[0],i[1],text))
            self.tag_bind(text,'<Enter>',lambda event,num=count,tag=text:button_in(num,tag))
            self.tag_bind(text,'<Leave>',lambda event,num=count,tag=text:button_out(num,tag))
            self.tag_bind(text,'<Button-1>',lambda event,num=count,tag=text,tagname=i[1]:sel_it(num,tag,tagname))
        self.__auto_anchor(uid,pos,anchor)
        sel_it(0,texts[0][2],texts[0][1],False)
        funcs = FuncList(1)
        funcs.select = _select
        uid.layout=lambda x1,y1,x2,y2,expand=False:self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
        return texts, funcs, uid

    def add_button2(self,pos:tuple,text:str,icon=None,compound='left',fg='#1b1b1b',bg='#fbfbfb',line='#CCCCCC',linew=1,activefg='#1a1a1a',activebg='#f6f6f6',activeline='#cccccc',onfg='#5d5d5d',onbg='#f5f5f5',online='#e5e5e5',font=('微软雅黑',12),minwidth=0,maxwidth=0,command=None,anchor='nw'):#绘制圆角按钮
        def in_button(event):
            nonlocal mouse_in
            mouse_in=True
            self.itemconfig(outline,outline=activeline,fill=activeline)
            self.itemconfig(back,fill=activebg,outline=activebg)
            self.itemconfig(buttonuid,fill=activefg)
        def out_button(event):
            nonlocal mouse_in
            mouse_in=False
            self.itemconfig(back,fill=bg,outline=bg)
            self.itemconfig(outline,outline=line,fill=line)
            self.itemconfig(buttonuid,fill=fg)
        def on_click(event):
            self.itemconfig(back,fill=onbg,outline=onbg)
            self.itemconfig(buttonuid,fill=onfg)
            self.itemconfig(outline,outline=online,fill=online)
        def out_click(event):
            if mouse_in:
                in_button(event)
            else:
                out_button(event)
            if command != None:
                command(event)
        def change_command(new_func):
            nonlocal command
            command=new_func
        def disable(fg='#9d9d9d',bg='#f5f5f5'):
            self.itemconfig(buttonuid,state='disable',fill=fg)
            self.itemconfig(back,state='disable',disabledfill=bg)
            self.itemconfig(outline,state='disable')
        def active():
            self.itemconfig(buttonuid,state='normal')
            self.itemconfig(back,state='normal')
            self.itemconfig(outline,state='normal')
            out_button(None)
        def __layout(x1,y1,x2,y2,expand=False):
            if not expand:
                self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
            else:
                self.__auto_anchor(buttonuid,((x1+x2)/2,(y1+y2)/2),'center')
                self.coords(back,x1+5,y1+5,x2-5,y1+5,x2-5,y2-5,x1+5,y2-5)
                self.coords(outline,x1+4,y1+4,x2-4,y1+4,x2-4,y2-4,x1+4,y2-4)
        font=tkfont.Font(font=font)
        font_size=str(font.cget(option='size'))
        mouse_in = False# 鼠标是否在按钮上
        button=self.create_text(pos,text=text,fill=fg,font=font)
        uid=TinUIString(f'button2-{button}')
        buttonuid=uid+'button'
        self.itemconfig(button,tags=(uid,buttonuid))
        if icon:#Fluent Icons编码图标
            icontext=self.create_text(pos,text=icon,fill=fg,font='{Segoe Fluent Icons} '+font_size,tags=(uid,buttonuid,f'{uid}icon'))
            iconbbox=self.bbox(icontext)
            if compound=='left':
                textpos=(iconbbox[2]+1,(iconbbox[3]+iconbbox[1])/2)
                self.__auto_anchor(button,textpos,'w')
            elif compound=='right':
                textpos=(iconbbox[0]-1,(iconbbox[3]+iconbbox[1])/2)
                self.__auto_anchor(button,textpos,'e')
            elif compound=='top':
                textpos=((iconbbox[0]+iconbbox[2])/2,iconbbox[3]+1)
                self.__auto_anchor(button,textpos,'n')
            elif compound=='bottom':
                textpos=((iconbbox[0]+iconbbox[2])/2,iconbbox[1]-1)
                self.__auto_anchor(button,textpos,'s')
            if text=='':#有图标的时候，如果无文本，则隐藏文本元素
                self.delete(button)
                button = None
            del iconbbox
        x1,y1,x2,y2=self.bbox(buttonuid)
        linew-=1
        #判断宽度的极限，分为最大化和最小化
        nowwidth=x2-x1
        if 0<maxwidth<=nowwidth:
            self.itemconfig(button,width=maxwidth)
            bbox=self.bbox(button)
            x1,y1,x2,y2=bbox[0],bbox[1],bbox[2],bbox[3]
            nowwidth=x2-x1
            del bbox
        if nowwidth<minwidth:
            dx=minwidth-nowwidth
            x2+=dx/2
            x1-=dx/2
        outline=self.__ui_polygon(((x1-linew,y1-linew),(x2+linew,y2+linew)),width=9,tags=uid,fill=line,outline=line)
        back=self.__ui_polygon(((x1+1,y1+1),(x2-1,y2-1)),width=9,tags=uid,fill=bg,outline=bg)
        self.tag_bind(uid, '<Button-1>', on_click)
        self.tag_bind(uid, '<ButtonRelease-1>', out_click)
        self.tag_bind(uid, '<Enter>', in_button)
        self.tag_bind(uid, '<Leave>', out_button)
        self.tkraise(buttonuid)
        self.__auto_anchor(uid,pos,anchor)
        funcs=FuncList(3)
        funcs.change_command=change_command
        funcs.disable=disable
        funcs.active=active
        uid.layout=__layout
        return button,back,outline,funcs,uid

    def add_expander(self,pos:tuple,title='expand content',tfg='black',tbg='#fbfbfb',bg='#f4f4f4',sep='#e5e5e5',buttonfg='#1b1b1b',buttonbg='#fbfbfb',buttonline='#fbfbfb',activefg='#1a1a1a',activebg='#f2f2f2',activeline='#f2f2f2',onfg='#1a1a1a',onbg='#f5f5f5',online='#f5f5f5',width=200,height=200,scrollbar=False,font='微软雅黑 12',anchor=None):#绘制一个可拓展UI
        def do_expand(*e):
            nonlocal expand
            expand = not expand
            self.itemconfig(content, state='normal' if expand else 'hidden')
            self.itemconfig(button[-1]+'icon', text='\uE70E' if expand else '\uE70D')
            __size_back()
        def __size_back():#调整背景
            bx1,by1,bx2,by2=self.bbox(contentid)#大背景
            bx1+=8
            by1+=8
            bx2-=8
            by2-=3
            self.coords(allback,bx1,by1,bx2,by1,bx2,by2,bx1,by2)
        toptext=self.create_text((pos[0]+10,pos[1]+10),text=title,font=font,fill=tfg,width=width-30,anchor='nw')#标题
        uid=f'expander-{toptext}'
        contentid=f'expander-content-{toptext}'
        #movename='expander-move'+str(toptext)
        self.addtag_withtag(uid,toptext)
        self.addtag_withtag(contentid,toptext)
        tx1,ty1,tx2,ty2=self.bbox(toptext)
        if tx2-tx1<width:#判读当前文本宽度
            tx2=tx1+width
        topback=self.__ui_polygon(((tx1,ty1),(tx2,ty2)),outline=tbg,fill=tbg,width=17,tags=(uid,contentid))#标题背景
        font_size=self.__get_text_size(toptext)#字体大小
        button=self.add_button2((tx2+5,(ty1+ty2)/2),anchor='e',text='',icon='\uE70D',font='{Segoe Fluent Icons}'+font_size,fg=buttonfg,bg=buttonbg,line=buttonline,activeline=activeline,activefg=activefg,activebg=activebg,onfg=onfg,onbg=onbg,online=online,command=do_expand)
        self.addtag_withtag(uid,button[-1])
        self.addtag_withtag(contentid,button[-1])
        if not scrollbar:#不使用滚动条，BasicTinUI
            ui=BasicTinUI(self,bg=bg)
            self.windows.append(ui)
        elif scrollbar:#使用TinUI
            ui=TinUI(self,bg=bg)
            self.windows.append(ui.frame)
        ux=TinUIXml(ui)
        ui.bind('<Destroy>', lambda event: self.__delete_uixml(ux))
        content=self.create_window((tx1-3,ty2+10),window=ui,anchor='nw',width=width+6,height=height,tags=(uid,contentid),state='hidden')#便笺内容
        ax1,ay1,ax2,ay2=self.bbox(uid)#大背景
        allback=self.__ui_polygon(((ax1+8,ay1+8),(ax2-8,ay2-3)),outline=sep,fill=sep,width=17,tags=uid)
        expand=False#当前还没有扩展
        #调整元素层级关系
        self.tkraise(topback)
        self.tkraise(toptext)
        self.tkraise(button[-1])
        return toptext,ui,ux,uid

    def add_waitframe(self,pos:tuple,width=300,height=300,fg='#e0e0e0',bg='#ececee',anchor='nw'):#元素等待框
        def __start():
            nonlocal nowx,nowmove,animate
            if wait:
                if nowx>=width:#移动到位
                    nowx=0
                    frame.lower(nowmove)
                    frame.moveto(nowmove,0,0)
                    #切换移动元素，重新调整层级
                    if nowmove==itemfg:
                        nowmove=itembg
                    else:
                        nowmove=itemfg
                frame.move(nowmove,mx,my)
                nowx+=mx
                animate=frame.after(25,__start)
            else:
                self.itemconfig(uid,state='hidden')
        def start():
            nonlocal wait
            wait=True
            self.itemconfig(uid,state='normal')
            __start()
        def end():
            nonlocal wait
            wait=False
        def __layout(x1,y1,x2,y2,expand=False):
            nonlocal mx,my,width,height
            if not expand:
                self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
            else:
                flag = False
                if wait:
                    frame.after_cancel(animate)
                    end()
                    flag = True
                width=x2-x1
                height=y2-y1
                self.itemconfig(uid,anchor='nw',width=width,height=height)
                self.moveto(uid,x1,y1)
                coord=(0,0,width,0,width,height,0,height)
                frame.coords(itemfg,coord)
                frame.coords(itembg,coord)
                mx=width/40
                my=height/40
                if flag:
                    start()
        frame=BasicTinUI(self,width=width,height=height,bg=bg)
        frameid=self.create_window(pos,window=frame,width=width,height=height,anchor=anchor)
        self.windows.append(frame)
        uid=TinUIString(f'waitframe-{frameid}')
        self.addtag_withtag(uid,frameid)
        itemfg=frame.__ui_polygon(((0,0),(width,height)),outline=fg,fill=fg,width=17)
        itembg=frame.__ui_polygon(((0,0),(width,height)),outline=bg,fill=bg,width=17)
        frame.move(itemfg,-width,-height)
        mx=width/40
        my=height/40
        nowmove=itemfg#当前移动元素
        nowx=0#当前移动元素的横向移动量
        wait=False
        animate=None#动画ID
        funcs=FuncList(2)
        funcs.start=start
        funcs.end=end
        self.itemconfig(uid,state='hidden')
        uid.layout=__layout
        return frame,itemfg,itembg,funcs,uid

    def add_treeview(self,pos:tuple,fg='#1a1a1a',bg='#f3f3f3',onfg='#1a1a1a',onbg='#eaeaea',oncolor='#3041d8',signcolor='#8a8a8a',width=200,height=300,font='微软雅黑 12',content=(('one',('1','2','3')),'two',('three',('a',('b',('b1','b2','b3')),'c')),'four'),anchor='nw',command=None):#树状图
        '''
        content=(
        a,
        (b,(b1,b2,b3)),
        (c,(c1,(c2,(c2-1,c2-2)),c3)),
        d,
        )
        '''
        def buttonin(cid):
            if cid!=nowid:
                box.itemconfig(cid,fill=onbg,outline=onbg)
        def buttonout(cid):
            if cid!=nowid:
                box.itemconfig(cid,fill=bg,outline=bg)
        def click(cid,send=False):
            nonlocal nowid
            if nowid is not None:
                box.itemconfig(nowid,fill=bg,outline=bg)#原来的
                box.itemconfig(items[nowid][0], fill=fg)
            box.itemconfig(cid,fill=onbg,outline=onbg)#现在的
            box.itemconfig(items[cid][0], fill=onfg)
            nowid=cid#互换次序
            posi=box.bbox(nowid)
            if posi is None:
                box.itemconfig(line, state='hidden')
                return
            else:
                box.itemconfig(line, state='normal')
                posi = posi[1]
            box.moveto(line,1,posi+linew/5)
            if command!=None and send:
                fln.father_link=[cid]#父级关系
                find_father_link(fln,cid)
                command(fln.father_link[::-1])#[父级, 子1级, 子2级...]
        def find_father_link(fln,cid):#获取元素父级关系
            for i in items_dict:
                if cid in items_dict[i]:
                    fln.father_link.append(i)
                    find_father_link(fln,i)
        def endy():
            return box.bbox('all')[-1]
        def add_item(padx=5,texts:tuple=(),father_id=None):#添加元素
            child_id=[]
            for text in texts:
                y=endy()+3
                if type(text)==str:#单极
                    te=box.create_text((padx+15,y),text=text,font=font,fill=fg,tags='item',anchor='nw')
                    back=box.add_back((),tuple([te]),fg=bg,bg=bg,linew=0)
                    items[back]=(te,back)
                else:#存在子级
                    sign=box.create_text((padx-1,y+3),text='\uE96E',font='{Segoe Fluent Icons} 12',fill=signcolor,anchor='nw')
                    te=box.create_text((padx+15,y),text=text[0],font=font,fill=fg,tags='item',anchor='nw')
                    back=box.add_back((),tuple((sign,te)),fg=bg,bg=bg,linew=0)
                    items[back]=(te,back,sign)
                    add_item(padx+15,text[1],back)
                    box.tag_bind(sign,'<Button-1>',lambda event,s=sign,cid=back:close_view(s,cid))
                old_coords = box.coords(back)
                old_coords[0] = old_coords[6] = 6
                bbox = box.bbox(back)
                if bbox[2]-bbox[0] < width:
                    old_coords[2] = old_coords[4] = width-9
                box.coords(back, old_coords)
                for item_id in (back, te):
                    box.tag_bind(item_id, '<Enter>', lambda event,_id=back:buttonin(_id))
                    box.tag_bind(item_id, '<Leave>', lambda event,_id=back:buttonout(_id))
                    box.tag_bind(item_id, '<Button-1>', lambda event,_id=back:click(_id,True))
                child_id.append(back)
            if father_id!=None:#存在父级
                items_dict[father_id]=tuple(child_id)
        def get_cids(cid):
            cids=[]
            if cid in items_dict:
                for i in items_dict[cid]:
                    cids.append(i)
                    ccids=get_cids(i)
                    cids+=ccids
            return cids
        def _get_last_cuid(cid):
            while cid in items_dict:
                cid = items_dict[cid][-1]
            return cid
        def open_view(sign,cid):#展开
            if box.itemcget(sign,'text')=='\uE96E':
                return
            box.tag_bind(sign,'<Button-1>',lambda event:close_view(sign,cid))
            box.itemconfig(sign,text='\uE96E')
            cids=items_dict[cid]
            move='move'+str(cid)#单层管理命名元素
            for i in cids:#只展开一层
                for uid in items[i]:
                    box.addtag_withtag(move,uid)
            box.itemconfig(move,state='normal')
            bbox=box.bbox(move)
            if bbox==None: return
            index=tuple(items.keys()).index(_get_last_cuid(cid))+1
            if index!=len(items.keys()):
                moveheight=bbox[3]-bbox[1]#获取移动模块高度
                for i in tuple(items.keys())[index:]:
                    for uid in items[i]:
                        box.move(uid,0,moveheight)
            box.dtag(move)
            if nowid is not None:
                bbox = box.bbox(nowid)
            else:
                bbox = None
            if nowid in cids:#重新显示标识元素
                click(nowid)
            elif bbox!=None:
                click(nowid)#单级输出
                posi=box.bbox(nowid)[1]
                box.moveto(line,1,posi+linew/5)
            checkscroll()
        def close_view(sign,cid):#闭合
            if box.itemcget(sign,'text')=='\uE970':
                return
            box.tag_bind(sign,'<Button-1>',lambda event:open_view(sign,cid))
            box.itemconfig(sign,text='\uE970')
            cids=get_cids(cid)
            move='move'+str(cid)#单层管理命名元素
            for i in cids:
                for uid in items[i]:
                    box.addtag_withtag(move,uid)
                if i in items_dict:
                    close_view(items[i][-1],i)
            bbox=box.bbox(move)
            box.itemconfig(move,state='hidden')
            index=tuple(items.keys()).index(cids[-1])+1
            if index!=len(items.keys()):
                moveheight=bbox[3]-bbox[1]#获取移动模块高度
                for i in tuple(items.keys())[index:]:
                    for uid in items[i]:
                        box.move(uid,0,-moveheight)
            box.dtag(move)
            if nowid in cids:#标识元素控制
                box.itemconfig(line,state='hidden')
            elif nowid is not None:
                click(nowid)#重新绘制位置
            checkscroll()
        def bindview(event):
            if event.state==0:
                box.yview_scroll(int(-1*(event.delta/120)), "units")
            elif event.state==1:
                box.xview_scroll(int(-1*(event.delta/120)), "units")
        def clean(event):
            # 销毁对象
            nonlocal fln, items, items_dict
            del fln
            del items
            del items_dict
        def checkscroll():
            bbox = box.bbox('all')
            if bbox[2]-bbox[0] <= width:
                self.itemconfig(cavui, height=height)
                self.itemconfig(vscroll, state='hidden')
            else:
                self.itemconfig(cavui, height=height-8)
                self.itemconfig(vscroll, state='normal')
            if bbox[3]-bbox[1] <= height:
                self.itemconfig(cavui, width=width)
                self.itemconfig(hscroll, state='hidden')
            else:
                self.itemconfig(cavui, width=width-8)
                self.itemconfig(hscroll, state='normal')
            box.config(scrollregion=bbox)
        def repaintback():
            bbox=box.bbox('item')
            widgetwidth=bbox[2]
            widgetwidth=max(width,widgetwidth)-9
            for back in items:
                old_coords = box.coords(back)
                old_coords[2] = old_coords[4] = widgetwidth
                box.coords(back, old_coords)
        def __layout(x1,y1,x2,y2,expand=False):
            nonlocal width,height
            if not expand:
                dx,dy=self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
                hscroll.move(dx,dy,height)
                vscroll.move(dx,dy,width)
            else:
                dx,dy=self.__auto_layout(uid,(x1,y1,x2,y2),'nw')
                width2=x2-x1-9
                dw=width2-width
                width=width2
                height2=y2-y1-9
                dh=height2-height
                height=height2
                self.move(hscroll,dw,0)
                hscroll.move(dx+dw,dy,height)
                self.move(vscroll,0,dh)
                vscroll.move(dx,dy+dh,width)
                coord=self.coords(allback)
                coord[2]=coord[4]=x2-4
                coord[5]=coord[7]=y2-4
                self.coords(allback,coord)
                self.itemconfig(cavui,width=width,height=height)
                repaintback()
                checkscroll()
        nowid=None
        fln=TinUINum()#用于寻找父级关系，目前效率比较低，之后考虑优化
        box=BasicTinUI(self,bg=bg,width=width,height=height)#显示选择内容
        box.place(x=12,y=12)
        cavui=self.create_window(pos,window=box,width=width,height=height,anchor='nw')
        self.windows.append(box)
        uid=TinUIString(f'treeview-{cavui}')
        self.addtag_withtag(uid,cavui)
        hscroll = self.add_scrollbar((pos[0]+width-8,pos[1]),widget=box,height=height,bg=bg,color=signcolor,oncolor=signcolor)[-1]#纵向
        vscroll = self.add_scrollbar((pos[0],pos[1]+height-8),widget=box,height=width,direction='x',bg=bg,color=signcolor,oncolor=signcolor)[-1]#横向
        self.addtag_withtag(uid, hscroll)
        self.addtag_withtag(uid, vscroll)
        #id为back的uid
        items={}#元素对象{id:(text,back,[sign]),...}
        items_dict={}#链接关系（下一级）{id:(id1,id2,id3,...),id2:(id2-1,id2-2,...),id-new:(...)...}
        box.add_back((0,0,0,0),linew=0)
        add_item(5,content)
        #重绘宽度
        bbox=box.bbox(tuple(items.keys())[0])#第一个元素
        linew=bbox[3]-bbox[1]
        line=box.create_line((1,linew/3,1,linew*2/3),fill=oncolor,width=3,capstyle='round')
        x1, y1, x2, y2 = self.bbox(uid)
        allback=self.__ui_polygon(((x1, y1), (x2, y2)), outline=bg, fill=bg, width=9, tags=uid)# allback
        self.lift(cavui)
        self.lift(hscroll)
        self.lift(vscroll)
        checkscroll()
        box.moveto(line,0,-linew-height)
        box.itemconfig(line,state='hidden')
        box.bind('<MouseWheel>',bindview)
        box.bind('<Destroy>', clean)
        dx,dy=self.__auto_anchor(uid,pos,anchor)
        hscroll.move(dx,dy,height)
        vscroll.move(dx,dy,width)
        del bbox,x1,y1,x2,y2,dx,dy
        uid.layout=__layout
        return items,items_dict,box,uid

    def add_passwordbox(self,pos:tuple,width:int,fg='#1b1b1b',bg='#fbfbfb',activefg='#1a1a1a',activebg='#f6f6f6',onfg='#000000',onbg='#ffffff',line='#e5e5e5',activeline='#e5e5e5',insert='#000000',font=('微软雅黑',12),outline='#868686',onoutline='#3041d8',anchor='nw',command=None):#绘制密码输入框
        #参考entry控件
        def if_empty(event):
            if nowstate=='hidden':
                self.tag_bind(funcw,'<Enter>',lambda event:self.itemconfig(funcw,fill=onoutline))
                self.tag_bind(funcw,'<Leave>',lambda event:self.itemconfig(funcw,fill=fg))
                self.tag_bind(funcw,'<Button-1>',showkey)
            elif nowstate=='shown':
                self.tag_bind(funcw,'<Leave>',lambda event:self.itemconfig(funcw,fill=onoutline))
                self.tag_bind(funcw,'<Enter>',lambda event:self.itemconfig(funcw,fill=onoutline))
                self.tag_bind(funcw,'<Button-1>',hidekey)
        def showkey(e):
            nonlocal nowstate
            nowstate='shown'
            self.itemconfig(funcw,fill=onoutline)
            entry.config(show='')
            if_empty(None)
        def hidekey(e):
            nonlocal nowstate
            nowstate='hidden'
            self.itemconfig(funcw,fill=fg)
            entry.config(show='●')
            if_empty(None)
        def focus_in(e):
            self.itemconfig(bottomline,fill=onoutline)
            backpos = self.coords(back)
            backpos[5] -= 1
            backpos[7] -= 1
            self.coords(back, *backpos)
            self.itemconfig(back,fill=onbg,outline=onbg)
            self.itemconfig(outl,fill=activeline,outline=activeline)
            entry.config(background=onbg,foreground=onfg)
        def focus_out(e):
            self.itemconfig(bottomline,fill=outline)
            backpos = self.coords(back)
            backpos[5] += 1
            backpos[7] += 1
            self.coords(back,backpos)
            self.itemconfig(back,fill=bg,outline=bg)
            self.itemconfig(outl,fill=line,outline=line)
            entry.config(background=bg,foreground=fg)
        def mouse_enter(e):
            if entry.focus_get() == entry.nametowidget(entry):
                # 已获取焦点
                return
            self.itemconfig(back, fill=activebg, outline=activebg)
            entry.config(background=activebg, foreground=activefg)
        def mouse_leave(e):
            if entry.focus_get() == entry.nametowidget(entry):
                # 已获取焦点
                return
            self.itemconfig(back, fill=bg, outline=bg)
            entry.config(background=bg, foreground=fg)
        def __layout(x1,y1,x2,y2,expand=False):
            if not expand:
                self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
            else:
                self.itemconfig(funce,width=x2-x1-dwidth-6)
                bbox1=self.bbox(funce)
                coord=self.coords(back)
                coord[0]=coord[6]=bbox1[0]+2
                coord[2]=coord[4]=bbox1[2]+dwidth-2
                self.coords(back,coord)
                coord=self.coords(outl)
                coord[0]=coord[6]=bbox1[0]+1
                coord[2]=coord[4]=bbox1[2]+dwidth-1
                self.coords(outl,coord)
                coordl=self.coords(bottomline)
                coordl[0]=coord[0]
                coordl[2]=coord[2]
                self.coords(bottomline,coordl)
                self.__auto_anchor(entrybutton,(bbox1[2],(bbox1[1]+bbox1[3])/2),'w')
                self.__auto_layout(uid,(x1,y1,x2,y2),'center')
        #---
        def get_entry():#获取文本
            return entry.get()
        def __error(errorline='#c42b1c'):#错误样式
            self.itemconfig(bottomline,fill=errorline)
        def __normal():#正常样式
            entry['state']='normal'
            entry.focus_set()
            self.itemconfig(back,outline=onbg,fill=onbg)
            self.itemconfig(bottomline,fill=onoutline)
        def __disable():#禁用
            entry['state']='disable'
            self.itemconfig(back,fill='#f0f0f0',outline='#f0f0f0')
            self.itemconfig(bottomline,fill=outline)
        nowstate='hidden'#'shown'
        entry=Entry(self,fg=fg,bg=bg,font=font,relief='flat',bd=0,show='●',insertbackground=insert)
        entry.bind('<FocusIn>',focus_in)
        entry.bind('<FocusOut>',focus_out)
        entry.bind('<Enter>', mouse_enter)
        entry.bind('<Leave>', mouse_leave)
        funce=self.create_window(pos,window=entry,width=width,anchor=anchor)#输入框画布对象
        self.windows.append(entry)
        uid=TinUIString(f'entry-{funce}')
        entrybutton=f'enrtyb-{funce}'
        self.itemconfig(funce,tags=uid)
        bbox=self.bbox(funce)
        _font=tkfont.Font(font=font)
        font_size=str(_font.cget('size'))
        funcw=self.create_text((bbox[0]+width,(bbox[1]+bbox[3])/2),text='\uF78D',fill=fg,font='{Segoe Fluent Icons} '+font_size,anchor='w',tags=(uid,entrybutton))
        bubbox=self.bbox(funcw)
        bottomlinepos=(bbox[0]+2,bbox[3]-1,bubbox[2]-2,bbox[3]-1)
        bottomline=self.create_line(bottomlinepos,fill=outline,width=9,capstyle='round',tags=uid)#bottomline
        back=self.__ui_polygon(((bbox[0]+2,bbox[1]+2),(bubbox[2]-2,bbox[3]-2)),fill=bg,outline=bg,width=9,tags=uid)#back
        outl=self.__ui_polygon(((bbox[0]+1,bbox[1]+1),(bubbox[2]-1,bbox[3]-1)),fill=line,outline=line,width=9,tags=uid)#out
        self.lower(outl,bottomline)
        bbox1=self.bbox(entrybutton)
        bbox2=self.bbox(funce)
        dwidth=bbox1[2]-bbox2[2]+6
        del bbox1,bbox2,bubbox,bbox,_font,font_size
        self.tkraise(funcw)
        if_empty(None)
        self.__auto_anchor(uid,pos,anchor)
        funcs=FuncList(4)
        funcs.get=get_entry
        funcs.error=__error
        funcs.normal=__normal
        funcs.disable=__disable
        uid.layout=__layout
        return entry,funcs,uid
    
    def add_image(self,pos:tuple,width=None,height=None,state='fill',imgfile=None,anchor='nw'):#绘制静态图片
        #这个控件是静态gif或者是png图片
        #state::none裁剪操作，fill填充，uniform等比缩放
        state=state.lower()
        if state=='none' and (width!=None or height!=None):#直接左上角裁剪
            image=PhotoImage(file=imgfile,width=width,height=height)
            width,height=None,None
        else:
            image=PhotoImage(file=imgfile)
        self.images.append(image)#存储图片，防止被python垃圾回收
        img=self.create_image(pos,anchor='nw',image=self.images[-1])
        uid=TinUIString(f'image-{img}')
        self.addtag_withtag(uid,img)
        bbox=self.bbox(img)
        rwidth,rheight=bbox[2]-bbox[0],bbox[3]-bbox[1]
        if width!=None or height!=None:#缩放
            #缩放系数
            xrate=width/rwidth if width!=None else 1
            yrate=height/rheight if height!=None else 1
            if state=='uniform':#等比缩放
                #取最小值
                if yrate<xrate:
                    xrate=yrate
                else:#yrate>=xrate
                    yrate=xrate
            key=round(10)#计算精度
            image=PhotoImage.zoom(image,key,key)
            image=image.subsample(round(key/xrate),round(key/yrate))
            self.images[-1]=image
            self.itemconfig(img,image=self.images[-1])
        self.__auto_anchor(img,pos,anchor)
        del rwidth,rheight,bbox,width,height,state
        uid.layout=lambda x1,y1,x2,y2,expand=False:self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
        return uid

    def add_togglebutton(self,pos:tuple,text:str,fg='#1b1b1b',bg='#fbfbfb',line='#CCCCCC',linew=1,activefg='#f3f4fd',activebg='#3041d8',activeline='#5360de',font=('微软雅黑',12),command=None,anchor='nw'):#绘制状态开关按钮
        #状态开关按钮当前不再对鼠标进入和离开进行响应
        def out_button(event):
            pass
        def on_click(event):
            if state==False:
                __on()
            else:
                __off()
        def __on():
            nonlocal state
            if state==True:
                command(state)
                return
            state=True
            self.itemconfig(outline,fill=activeline,outline=activeline)
            change_color(0,2)
            if command!=None:
                command(state)
        def __off():
            nonlocal state
            if state==False:
                command(state)
                return
            state=False
            self.itemconfig(outline,fill=line,outline=line)
            change_color(0,1)
            if command!=None:
                command(state)
        def change_color(t,change:int):#变化颜色
            #change:: 1=>colors, 2=>re_colors
            nonlocal nowcolors
            if t<=25:
                self.itemconfig(back,fill=nowcolors[1][t],outline=nowcolors[1][t])
                self.itemconfig(button,fill=nowcolors[0][t])
                self.after(5,lambda : change_color(t+1,change))
            else:
                if change==1:
                    nowcolors=colors
                elif change==2:
                    nowcolors=re_colors
        def change_command(new_func):
            nonlocal command
            command=new_func
        def disable(fg='#9d9d9d',bg='#f5f5f5'):
            if state==False:#区分当前状态进行禁用配色
                self.itemconfig(button,state='disable',fill=fg)
                self.itemconfig(back,state='disable',disabledfill=bg)
            else:
                self.itemconfig(button,state='disable',fill=bg)
                self.itemconfig(back,state='disable',disabledfill=fg)
        def active():
            self.itemconfig(button,state='normal')
            self.itemconfig(back,state='normal')
            out_button(None)
        def __rgb2num(rgb):
            return int(rgb[1:3],16), int(rgb[3:5],16), int(rgb[5:],16)
        def __num2rgb(num):
            co='#'
            for i in num:
                co += f'{i:02x}'
            return co
        def get_color_change(st, ed):
            colors_list = []
            # 起始和终止颜色，十进制rgb
            a1, a2, a3 = __rgb2num(st)
            b1, b2, b3 = __rgb2num(ed)
            # 两颜色差值
            r, g, b = (b1 - a1), (b2 - a2), (b3 - a3)
            for i in range(26):
                t = i / 25
                new_rgb = (int(a1 + r * t), int(a2 + g * t), int(a3 + b * t))
                # 确保RGB值在0到255之间
                new_rgb = tuple(max(0, min(255, x)) for x in new_rgb)
                colors_list.append(__num2rgb(new_rgb))
            return colors_list
        state=False#off:False on:True
        colors=[]#渐变色颜色列表，25个，off->on，[[文本颜色,...],[背景色,...]]
        button=self.create_text(pos,text=text,fill=fg,font=font,anchor='nw')
        uid=TinUIString(f'togglebutton-{button}')
        self.itemconfig(button,tags=uid)
        x1,y1,x2,y2=self.bbox(button)
        linew-=1
        outline=self.__ui_polygon(((x1-linew,y1-linew),(x2+linew,y2+linew)),width=9,tags=uid,fill=line,outline=line)
        back=self.__ui_polygon(((x1+1,y1+1),(x2-1,y2-1)),width=9,tags=uid,fill=bg,outline=bg)
        self.tag_bind(button,'<Button-1>',on_click)
        self.tag_bind(back,'<Button-1>',on_click)
        self.tkraise(button)
        funcs=FuncList(5)
        funcs.change_command=change_command
        funcs.disable=disable
        funcs.active=active
        funcs.on=__on
        funcs.off=__off
        #处理渐变色
        colors.append(get_color_change(fg,activefg))#文本颜色
        colors.append(get_color_change(bg,activebg))#背景颜色
        #re_colors 反向颜色列表
        re_colors=[colors[0][::-1],colors[1][::-1]]
        nowcolors=colors
        self.__auto_anchor(uid,pos,anchor)
        del x1,y1,x2,y2
        uid.layout=lambda x1,y1,x2,y2,expand=False:self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
        return button,back,outline,funcs,uid
    
    # def add_swipecontrol(self,pos:tuple,text:str='',height=50,width=400,fg='#1a1a1a',bg='#f3f3f3',line='#fbfbfb',data:dict={'left':({'text':'OK','fg':'#202020','bg':'#bcbcbc','command':print},),'right':({'text':'CLOSE'},)},font=('微软雅黑',12),anchor='nw'):#绘制滑动控件
    #     def _animation(side):#移动动画
    #         it = 0
    #         if side=='left':
    #             for _ in range(0,rightw+5,5):
    #                 back.after(it*5, lambda: __animate(-5))
    #                 it += 1
    #         elif side=='right':
    #             for _ in range(0,leftw+5,5):
    #                 back.after(it*5, lambda: __animate(5))
    #                 it += 1
    #         elif side=='center':
    #             if nowmode==right:
    #                 for _ in range(0,rightw+5,5):
    #                     back.after(it*5, lambda: __animate(5))
    #                     it += 1
    #             elif nowmode==left:
    #                 for _ in range(0,leftw+5,5):
    #                     back.after(it*5, lambda: __animate(-5))
    #                     it += 1
    #     def __animate(movex):
    #         back.move('cont',movex,0)
    #         back.update_idletasks()
    #     def move(event):#滚动响应
    #         nonlocal nowmode
    #         back.unbind('<MouseWheel>')
    #         if event.state!=1:
    #             back.bind('<MouseWheel>',move)
    #             return
    #         if event.delta<0 and 'right' in data:#左滑，显示right
    #             if nowmode==right:
    #                 back.bind('<MouseWheel>',move)
    #                 return
    #             back.itemconfig(left,state='hidden')
    #             back.itemconfig(right,state='normal')
    #             _animation('center')
    #             _animation('left')
    #             nowmode=right
    #         elif event.delta>0 and 'left' in data:#右滑，显示left
    #             if nowmode==left:
    #                 back.bind('<MouseWheel>',move)
    #                 return
    #             back.itemconfig(right,state='hidden')
    #             back.itemconfig(left,state='normal')
    #             _animation('center')
    #             _animation('right')
    #             nowmode=left
    #         back.bind('<MouseWheel>',move)
    #     def _docommand(func):
    #         nonlocal nowmode
    #         _animation('center')
    #         nowmode=center
    #         if func!=None:
    #             func()
    #     def _recenter(e):
    #         nonlocal nowmode
    #         _animation('center')
    #         nowmode=center
    #     itemw=width//6#背景元素宽度。软限制为6个，多出内容没有意义
    #     back=BasicTinUI(self,bg=line)#背景容器
    #     backitem=self.create_window(pos,width=width+2,height=height+2,anchor='nw',window=back)
    #     self.windows.append(back)
    #     uid=f'swipecontrol-{backitem}'
    #     self.addtag_withtag(uid,backitem)
    #     right,left='rights','lefts'#背景元素位置
    #     center='centers'
    #     nowmode=center#当前状态
    #     if 'left' in data:#往右滑
    #         endx=1
    #         for item in data['left']:
    #             _bg=item['bg'] if 'bg' in item else '#bcbcbc'
    #             _fg=item['fg'] if 'fg' in item else '#202020'
    #             bitem=back.create_rectangle((endx,1,endx+itemw,1+height),fill=_bg,width=0,tags=left)
    #             fitem=back.create_text((endx+itemw/2,1+height/2),text=item['text'],fill=_fg,font=font,tags=left)
    #             command=item['command'] if 'command' in item else None
    #             back.tag_bind(bitem,'<Button-1>',lambda e,func=command:_docommand(func))
    #             back.tag_bind(fitem,'<Button-1>',lambda e,func=command:_docommand(func))
    #             endx+=itemw
    #         leftbbox=back.bbox(left)
    #         leftw=leftbbox[2]-leftbbox[0]
    #     if 'right' in data:#往左滑
    #         endx=width+1
    #         for item in data['right']:
    #             _bg=item['bg'] if 'bg' in item else '#bcbcbc'
    #             _fg=item['fg'] if 'fg' in item else '#202020'
    #             bitem=back.create_rectangle((endx-itemw,1,endx,1+height),fill=_bg,width=0,tags=right)
    #             fitem=back.create_text((endx-itemw/2,1+height/2),text=item['text'],fill=_fg,font=font,tags=right)
    #             command=item['command'] if 'command' in item else None
    #             back.tag_bind(bitem,'<Button-1>',lambda e,func=command:_docommand(func))
    #             back.tag_bind(fitem,'<Button-1>',lambda e,func=command:_docommand(func))
    #             endx-=itemw
    #         rightbbox=back.bbox(right)
    #         rightw=rightbbox[2]-rightbbox[0]
    #     contback=back.create_rectangle((1,1,width+1,height+1),fill=bg,width=0,tags='cont')
    #     cont=back.create_text((3,1+height/2),anchor='w',text=text,fill=fg,font=font,tags='cont')
    #     back.itemconfig(left,state='hidden')
    #     back.itemconfig(right,state='hidden')
    #     back.bind('<MouseWheel>',move)
    #     back.tag_bind(contback,'<Button-1>',_recenter)
    #     back.tag_bind(cont,'<Button-1>',_recenter)
    #     self.__auto_anchor(uid,pos,anchor)
    #     return back,backitem

    def add_picker(self,pos:tuple,height=250,fg='#1b1b1b',bg='#fbfbfb',outline='#ececec',activefg='#1b1b1b',activebg='#f6f6f6',onfg='#eaecfb',onbg='#3748d9',buttonfg='#1a1a1a',buttonbg='#f9f9f9',buttonactivefg='#1a1a1a',buttonactivebg='#f3f3f3',buttononfg='#5d5d5d',buttononbg='#f5f5f5',font=('微软雅黑',10),text=(('year',60),('season',100),),data=(('2022','2023','2024'),('spring','summer','autumn','winter')),tran='#01FF11',anchor='nw',command=None):#绘制滚动选值框
        def _mouseenter(event):
            self.itemconfig(back,fill=activebg,outline=activebg)
            for i in texts:
                self.itemconfig(i,fill=activefg)
        def _mouseleave(event):
            self.itemconfig(back,fill=bg,outline=bg)
            for i in texts:
                self.itemconfig(i,fill=fg)
        def set_it(e):#确定选择
            results=[]#结果列表
            for ipicker in pickerbars:
                num=pickerbars.index(ipicker)
                if ipicker.newres=='':#没有选择
                    picker.withdraw()
                    return
                ipicker.res=ipicker.newres
                tx=texts[num]
                self.itemconfig(tx,text=ipicker.res)
                results.append(ipicker.res)
            picker.withdraw()
            if command!=None:
                command(results)
        def cancel(e):#取消选择
            for ipicker in pickerbars:
                if ipicker.res=='':
                    pass
            picker.withdraw()
            #以后或许回考虑元素选择复原，也不一定，或许不更改交互选项更方便
        def pick_in_mouse(e,t):
            box=e.widget
            if box.choices[t][-1]==True:#已被选中
                return
            box.itemconfig(box.choices[t][2],fill=buttonactivebg)
            box.itemconfig(box.choices[t][1],fill=activefg)
        def pick_out_mouse(e,t):
            box=e.widget
            if box.choices[t][-1]==True:#已被选中
                box.itemconfig(box.choices[t][2],fill=onbg)
                box.itemconfig(box.choices[t][1],fill=onfg)
            else:
                box.itemconfig(box.choices[t][2],fill=bg)
                box.itemconfig(box.choices[t][1],fill=fg)
        def pick_sel_it(e,t):
            box=e.widget
            box.itemconfig(box.choices[t][2],fill=onbg)
            box.itemconfig(box.choices[t][1],fill=onfg)
            box.choices[t][-1]=True
            for i in box.choices.keys():
                if i==t:
                    continue
                box.choices[i][-1]=False
                pick_out_mouse(e,i)
            box.newres=box.choices[t][0]
        def readyshow():#计算显示位置
            allpos=bar.bbox('all')
            #菜单尺寸
            winw=allpos[2]-allpos[0]+5
            winh=allpos[3]-allpos[1]+5
            #屏幕尺寸
            maxx=self.winfo_screenwidth()
            maxy=self.winfo_screenheight()
            wind.data=(maxx,maxy,winw,winh)
        def show(event):#显示的起始位置
            #初始位置
            maxx,maxy,winw,winh=wind.data
            bbox=self.bbox(uid)
            scx,scy=event.x_root,event.y_root#屏幕坐标
            dx,dy=round(self.canvasx(event.x,)-bbox[0]),round(self.canvasy(event.y)-bbox[3])#画布坐标差值
            sx,sy=scx-dx,scy-dy
            if sx+winw>maxx:
                x=sx-winw
            else:
                x=sx
            if sy+winh>maxy:
                y=sy-winh
            else:
                y=sy
            picker.geometry(f'{winw+15}x{winh+15}+{x-3}+{y}')
            picker.attributes('-alpha',0)
            picker.deiconify()
            it = 0
            for i in (0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1):
                picker.after(it*20, lambda alpha=i : __show(alpha))
                it += 1
        def __show(alpha):
            picker.attributes('-alpha',alpha)
            picker.update_idletasks()
            if alpha == 1:
                picker.focus_set()
        def _loaddata(box,items,mw):
            def __set_y_view(event):
                box.yview_scroll(int(-1*(event.delta/120)), "units")
            #mw: 元素宽度
            for i in items:
                end=box.bbox('all')
                end=5 if end==None else end[-1]
                text=box.create_text((5,end+7),text=i,fill=fg,font=font,anchor='nw',tags='textcid')
                bbox=box.bbox(text)#获取文本宽度
                back=box.create_rectangle((3,bbox[1]-4,3+mw,bbox[3]+4),width=0,fill=bg)
                box.tkraise(text)
                box.choices[text]=[i,text,back,False]#用文本id代表键，避免选项文本重复带来的逻辑错误
                for item_id in (text, back):
                    box.tag_bind(item_id,'<Enter>',lambda event,text=text : pick_in_mouse(event,text))
                    box.tag_bind(item_id,'<Leave>',lambda event,text=text : pick_out_mouse(event,text))
                    box.tag_bind(item_id,'<Button-1>',lambda event,text=text : pick_sel_it(event,text))
            bbox=box.bbox('all')
            box.config(scrollregion=bbox)
            box.bind('<MouseWheel>',__set_y_view)
        out_line=self.create_polygon((*pos,*pos),fill=outline,outline=outline,width=9)
        uid=TinUIString(f'picker-{out_line}')
        self.addtag_withtag(uid,out_line)
        back=self.create_polygon((*pos,*pos),fill=bg,outline=bg,width=9,tags=uid)
        end_x=pos[0]+9
        y=pos[1]+9
        texts=[]#文本元素
        #测试文本高度
        txtest=self.create_text(pos,text=text[0][0],fill=fg,font=font)
        bbox=self.bbox(txtest)
        self.delete(txtest)
        uidheight=bbox[3]-bbox[1]
        uidcontent = f'{uid}content'
        for i in text:
            t,w=i#文本，宽度
            tx=self.create_text((end_x,y),anchor='w',text=t,fill=fg,font=font,tags=(uid,uidcontent))
            texts.append(tx)
            end_x+=w
            if text.index(i)+1==len(text):#最后一个省略分隔符
                _outline=outline
                outline=''
            self.create_line((end_x-3,pos[1],end_x-3,pos[1]+uidheight),fill=outline,tags=(uid,uidcontent))
        outline=_outline
        del _outline
        width=end_x-pos[0]+9#窗口宽度
        cds=self.bbox(uidcontent)
        coords=(cds[0],cds[1],cds[2],cds[1],cds[2],cds[3],cds[0],cds[3])
        self.coords(out_line,coords)
        coords=(cds[0]+1,cds[1]+1,cds[2]-1,cds[1]+1,cds[2]-1,cds[3]-1,cds[0]+1,cds[3]-1)
        self.coords(back,coords)
        self.tag_bind(uid,'<Enter>',_mouseenter)
        self.tag_bind(uid,'<Leave>',_mouseleave)
        self.tag_bind(uid,'<Button-1>',show)
        #创建窗口
        picker=Toplevel(self)
        picker.withdraw()
        picker.bind('<FocusOut>',lambda event:picker.withdraw())
        self.windows.append(picker)
        picker.geometry(f'{width}x{height}')
        picker.overrideredirect(True)
        picker.attributes('-topmost',1)
        picker.attributes('-transparent',tran)
        wind=TinUINum()#记录数据
        bar=BasicTinUI(picker,bg=tran)
        bar.pack(fill='both',expand=True)
        bar.__ui_polygon(((13,13),(width-13,height-11)),fill=bg,outline=bg,width=17)
        bar.lower(bar.__ui_polygon(((12,12),(width-12,height-10)),fill=outline,outline=outline,width=17))
        __count=0
        end_x=8
        y=9
        pickerbars=[]#选择UI列表
        for i in data:
            barw=text[__count][1]#本选择列表元素宽度
            pickbar=BasicTinUI(picker,bg=bg)
            pickbar.place(x=end_x,y=y,width=barw,height=height-50)
            pickbar.newres=''#待选
            pickbar.res=''#选择结果
            #pickbar.all_keys=[]#[a-id,b-id,...]
            pickbar.choices={}#'a-id':[a,a_text,a_back,is_sel:bool]
            _loaddata(pickbar,i,barw)
            pickerbars.append(pickbar)
            __count+=1
            end_x+=barw+3
        #ok button
        okpos=((5+(width-9)/2)/2,height-22)
        ok=bar.add_button2(okpos,text='\uE73E',font='{Segoe Fluent Icons} 12',fg=buttonfg,bg=buttonbg,line='',activefg=buttonactivefg,activebg=buttonactivebg,activeline=outline,onfg=buttononfg,onbg=buttononbg,online=buttononbg,anchor='center',command=set_it)
        bar.coords(ok[1],(9,height-35,(width-9)/2-5,height-35,(width-9)/2-5,height-9,9,height-9))
        bar.coords(ok[2],(8,height-34,(width-9)/2-4,height-34,(width-9)/2-4,height-8,8,height-8))
        #cancel button
        nopos=(((width-9)/2+width-4)/2,height-22)
        no=bar.add_button2(nopos,text='\uE711',font='{Segoe Fluent Icons} 12',fg=buttonfg,bg=buttonbg,line='',activefg=buttonactivefg,activebg=buttonactivebg,activeline=outline,onfg=buttononfg,onbg=buttononbg,online=buttononbg,anchor='center',command=cancel)
        bar.coords(no[1],((width-9)/2+5,height-35,width-9,height-35,width-9,height-9,(width-9)/2+5,height-9))
        bar.coords(no[2],((width-9)/2+4,height-34,width-8,height-34,width-8,height-8,((width-9)/2+4,height-8)))
        readyshow()
        del end_x,y,coords,__count,okpos,nopos
        self.__auto_anchor(uid,pos,anchor)
        uid.layout=lambda x1,y1,x2,y2,expand=False:self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
        return picker,bar,texts,pickerbars,uid
    
    def add_menubutton(self,pos:tuple,text:str,side='y',fg='#1b1b1b',bg='#fbfbfb',line='#CCCCCC',linew=1,activefg='#1a1a1a',activebg='#f6f6f6',activeline='#cccccc',onfg='#5d5d5d',onbg='#f5f5f5',online='#e5e5e5',menuonfg='#191919',menuonbg='#f0f0f0',menuonline='#f0f0f0',font=('微软雅黑',12),cont=(('command',print),'-'),widget=True,tran='#01FF11',anchor='nw'):#绘制按钮展开菜单
        #Segoe Fluent Icons x右侧展开\uE76B \uE76C，y下方展开\uE70D \uE70E，默认y
        def in_button(event):
            self.itemconfig(outline,outline=activeline,fill=activeline)
            self.itemconfig(back,fill=activebg,outline=activebg)
            self.itemconfig(uid+'button',fill=activefg)
        def out_button(event):
            self.itemconfig(back,fill=bg,outline=bg)
            self.itemconfig(outline,outline=line,fill=line)
            self.itemconfig(uid+'button',fill=fg)
        def unshow(event):#重写菜单
            menu.withdraw()
            menu.unbind('<FocusOut>')
        def show(event):#显示的起始位置
            # 按钮样式更改
            self.itemconfig(outline, outline=online, fill=online)
            self.itemconfig(back, fill=onbg, outline=onbg)
            self.itemconfig(uid+'button', fill=onfg)
            self.after(500, lambda: out_button(None))
            #初始位置
            maxx,maxy,winw,winh=menu.wind.data
            sx,sy=event.x_root,event.y_root
            #
            maxx,maxy,winw,winh=menu.wind.data
            bbox=self.bbox(uid)
            scx,scy=event.x_root,event.y_root#屏幕坐标
            if side=='y':
                dx,dy=round(self.canvasx(event.x,)-bbox[0]),round(self.canvasy(event.y)-bbox[3])#画布坐标差值
            elif side=='x':
                dx,dy=round(self.canvasx(event.x,)-bbox[2]),round(self.canvasy(event.y)-bbox[1])#画布坐标差值
            sx,sy=scx-dx,scy-dy
            #
            if sx+winw>maxx:
                x=sx-winw-5
            else:
                x=sx-5
            if sy+winh>maxy:
                y=sy-winh
            else:
                y=sy
            menu.geometry(f'{winw+10}x{winh+10}+{x}+{y}')
            menu.attributes('-alpha',0)
            menu.deiconify()
            it = 0
            for i in (0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1):
                menu.after(it*20, lambda alpha=i : __show(alpha))
                it += 1
        def __show(alpha):
            menu.attributes('-alpha',alpha)
            menu.update_idletasks()
            if alpha == 1:
                menu.focus_set()
                menu.bind('<FocusOut>',unshow)
        def disable(fg='#9d9d9d',bg='#f5f5f5'):
            self.itemconfig(uid+'button',state='disable',fill=fg)
            self.itemconfig(back,state='disable',disabledfill=bg)
            self.itemconfig(outline,state='disable')
        def active():
            self.itemconfig(uid+'button',state='normal')
            self.itemconfig(back,state='normal')
            self.itemconfig(outline,state='normal')
            out_button(None)
        button=self.create_text(pos,text=text,fill=fg,font=font,anchor='nw')
        uid=TinUIString(f'menubutton-{button}')
        self.itemconfig(button,tags=(uid,uid+'button'))
        x1,y1,x2,y2=self.bbox(uid)
        if side=='y':
            self.create_text((x2+5,(y1+y2)/2),text='\uE70D',fill=fg,font='{Segoe Fluent Icons} 12',anchor='w',tags=(uid,uid+'button',uid+'widget'))
        elif side=='x':
            self.create_text((x2+5,(y1+y2)/2),text='\uE76C',fill=fg,font='{Segoe Fluent Icons} 12',anchor='w',tags=(uid,uid+'button',uid+'widget'))
        if not widget:#如果被指定不显示标识符
            self.delete(uid+'widget')
            self.dtag(uid+'widget')
        x1,y1,x2,y2=self.bbox(uid+'button')
        linew-=1
        outline=self.__ui_polygon(((x1-linew,y1-linew),(x2+linew,y2+linew)),width=9,tags=uid,fill=line,outline=line)
        back=self.__ui_polygon(((x1+1,y1+1),(x2-1,y2-1)),width=9,tags=uid,fill=bg,outline=bg)
        #创建菜单
        menu=self.add_menubar(uid,'<Button-1>',font=font,fg=fg,bg=bg,line=line,activefg=menuonfg,activebg=menuonbg,activeline=menuonline,onfg=onfg,onbg=onbg,online=online,cont=cont,tran=tran)[0]
        self.tag_unbind(uid,'<Button-1>')
        #重新绑定事件
        for item_id in (uid+'button', back, outline):
            self.tag_bind(item_id,'<Button-1>',show)
            self.tag_bind(item_id,'<Enter>',in_button)
            self.tag_bind(item_id,'<Leave>',out_button)
        self.tkraise(uid+'button')
        self.__auto_anchor(uid,pos,anchor)
        del x1,y1,x2,y2,linew
        funcs=FuncList(2)
        funcs.disable=disable
        funcs.active=active
        uid.layout=lambda x1,y1,x2,y2,expand=False:self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
        return uid+'button',back,outline,funcs,uid
    
    def add_barbutton(self,pos:tuple,font='微软雅黑 12',fg='#636363',bg='#f3f3f3',line='#f3f3f3',linew=0,activefg='#191919',activebg='#eaeaea',activeline='#eaeaea',onfg='#5a5a5a',onbg='#ededed',online='#ededed',sepcolor='#e4e4e4',content=(('保存','\uE74E',None),('','\uE792',None),'',('','\uE74D',None)),anchor='nw'):#绘制一个工具栏按钮组件
        def new_pos():
            #获取最新位置
            bbox=self.bbox(buttons_id)
            if bbox:
                return bbox[2]+5,(bbox[1]+bbox[3])/2
            else:
                return pos
        #获取字体大小，转化为像素大小
        font=tkfont.Font(font=font)
        pixel=font.metrics('linespace')
        outline=self.create_polygon(*pos,*pos,width=9,fill=line,outline=line)
        uid=TinUIString(f'barbutton-{outline}')
        self.itemconfig(outline,tags=uid)
        buttons_id=f'{uid}button'
        back=self.create_polygon(*pos,*pos,width=9,fill=bg,outline=bg,tags=uid)
        #左侧纵轴线对齐，anchor=w
        buttons=[]
        for i in content:
            if i=='':
                position=new_pos()
                sp_pos=(position[0],position[1]-pixel/2,position[0],position[1]+pixel/2)
                self.create_line(sp_pos,width=1,fill=sepcolor,tags=(uid,buttons_id))
                continue
            position=new_pos()
            button=self.add_button2(position,text=i[0],icon=i[1],font=font,fg=fg,bg=bg,line=line,linew=linew,activefg=activefg,activebg=activebg,activeline=activeline,onfg=onfg,onbg=onbg,online=online,anchor='w',command=i[2])
            self.addtag_withtag(buttons_id,button[-1])
            self.addtag_withtag(uid,button[-1])
            buttons.append(button)
        bbox=self.bbox(buttons_id)
        bbox=(bbox[0]+1,bbox[1]+1,bbox[2]-1,bbox[1]+1,bbox[2]-1,bbox[3]-1,bbox[0]+1,bbox[3]-1)
        self.coords(back,bbox)
        bbox=(bbox[0],bbox[1],bbox[2],bbox[1],bbox[2],bbox[3],bbox[0],bbox[3])
        self.coords(outline,bbox)
        del bbox
        self.__auto_anchor(uid,pos,anchor)
        uid.layout=lambda x1,y1,x2,y2,expand=False:self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
        return outline,back,buttons,uid

    def add_flyout(self, fid, width:int=250, height:int=150, bind='<Button-1>', line='#dcdcdc', bg='#f9f9f9', anchor='n', offset:tuple[int,int]=(0,0), pos=None):# 绘制一个浮出ui控件
        # 注意，默认布局在fid正上方
        def show(e):
            self.tag_unbind(fid, bind)# 避免接下来绑定self <button-1>事件时同步触发
            self.itemconfig(uid, state='normal')
            motion(None, 1)
            self.after(100, go_to_bind)# 避免直接触发控件点击事件
        def go_to_bind():
            self.bind('<Button-1>', hide)
        def hide(e):
            self.unbind('<Button-1>')
            self.tag_bind(fid, bind, show)
            motion(None, -1)
        def motion(e, dis):
            # 展开/收缩动画
            # dxy为动画方向，0为不变，1为变化
            if dis == 1:
                # 展开
                _width = width * (1-dxy[0])
                _height = height * (1-dxy[1])
                dwidth = width / 20 * dxy[0]
                dheight = height / 20 * dxy[1]
            else:
                # 收缩
                _width = width
                _height = height
                dwidth = -width / 20 * dxy[0]
                dheight = -height / 20 * dxy[1]
            for i in range(20):
                _width += dwidth
                _height += dheight
                ui.after(5*i, lambda _width=_width, _height=_height, i=i: __motion(_width, _height, (i==19)+dis))
        def __motion(_width, _height, dis_state):
            self.itemconfig(uid, width=_width, height=_height)
            ui.update()
            if dis_state == 0:
                # 仅当i=19并且是收缩时有效
                self.itemconfig(uid, state='hidden')
        ui = BasicTinUI(self, bg=bg, highlightbackground=line, highlightthickness=1, relief='flat')
        self.windows.append(ui)
        uixml = TinUIXml(ui)
        ui.bind('<Destroy>', lambda event: self.__delete_uixml(uixml))
        # 围绕fid进行布局
        bbox = self.bbox(fid)
        if anchor == 'nw':
            x = bbox[0] - 4
            y = bbox[1] - 4
            _anchor = 'se'
            dxy = (1, 1)
        elif anchor == 'n':
            x = (bbox[0] + bbox[2]) / 2
            y = bbox[1] - 4
            _anchor ='s'
            dxy = (0, 1)
        elif anchor == 'ne':
            x = bbox[2] + 4
            y = bbox[1] - 4
            _anchor = 'sw'
            dxy = (1, 1)
        elif anchor == 'e':
            x = bbox[2] + 4
            y = (bbox[1] + bbox[3]) / 2
            _anchor = 'w'
            dxy = (1, 0)
        elif anchor =='se':
            x = bbox[2] + 4
            y = bbox[3] + 4
            _anchor = 'nw'
            dxy = (1, 1)
        elif anchor =='s':
            x = (bbox[0] + bbox[2]) / 2
            y = bbox[3] + 4
            _anchor = 'n'
            dxy = (0, 1)
        elif anchor =='sw':
            x = bbox[0] - 4
            y = bbox[3] + 4
            _anchor = 'ne'
            dxy = (1, 1)
        elif anchor == 'w':
            x = bbox[0] - 4
            y = (bbox[1] + bbox[3]) / 2
            _anchor = 'e'
            dxy = (1, 0)
        else:# 默认为center
            x = (bbox[0] + bbox[2]) / 2
            y = (bbox[1] + bbox[3]) / 2
            _anchor = 'center'
            dxy = (1, 1)
        x += offset[0]
        y += offset[1]
        uid = self.create_window(x, y, width=width, height=height, window=ui, anchor=_anchor)
        self.itemconfig(uid, state='hidden')
        self.tag_bind(fid, bind, show, True)
        return ui, uixml, hide, uid

    def add_breadcrumb(self,pos:tuple,font='微软雅黑 12',fg='#000000',bg='#ffffff',activefg='#5c5c5c',root='HOME',command=None,anchor='nw'):
        # 绘制面包屑导航组件
        def click(cid):
            if command == None:
                return
            res = []
            for i in stack:
                res.append(i)
                if i == cid:
                    break
            command(res)
        def in_button(cid):
            self.itemconfig(cid, fill=activefg)
        def out_button(cid):
            self.itemconfig(cid, fill=fg)
        def get():
            # 获取当前路径元素
            return list(stack)
        def add(text):
            # 添加一个路径元素
            nonlocal endx
            sym = self.create_text((endx+2,center_line), text='\uE76C', font=segeo_font, fill=fg, anchor='w', tags=(uid,uid_button))
            symstack.append(sym)
            endx = self.bbox(sym)[2]
            t = self.create_text((endx+2,center_line), text=text, font=font, fill=fg, anchor='w', tags=(uid,uid_button))
            lt = stack[-1]
            stack.append(t)
            bbox = self.bbox(uid_button)
            self.coords(back, (bbox[0]+2,bbox[1]+2,bbox[2]-2,bbox[1]+2,bbox[2]-2,bbox[3]-2,bbox[0]+2,bbox[3]-2))
            self.__auto_anchor(uid,pos,anchor)
            endx = self.bbox(t)[2]
            self.tag_bind(lt, '<Button-1>', lambda e: click(lt))
            self.tag_bind(lt, '<Enter>', lambda e: in_button(lt))
            self.tag_bind(lt, '<Leave>', lambda e: out_button(lt))
            return t
        def delete():
            # 删除最后一个路径元素
            nonlocal endx
            if stack.__len__() > 1:
                self.delete(stack.pop())
                self.delete(symstack.pop())
                bbox = self.bbox(uid_button)
                self.coords(back, (bbox[0]+2,bbox[1]+2,bbox[2]-2,bbox[1]+2,bbox[2]-2,bbox[3]-2,bbox[0]+2,bbox[3]-2))
                self.__auto_anchor(uid,pos,anchor)
                lt = stack[-1]
                endx = self.bbox(lt)[2]
                self.tag_unbind(lt, '<Button-1>')
                self.tag_unbind(lt, '<Enter>')
                self.tag_unbind(lt, '<Leave>')
        def delete_to(cid):
            nonlocal endx
            while stack.__len__() > 1 and stack[-1] != cid:
                self.delete(stack.pop())
                self.delete(symstack.pop())
            bbox = self.bbox(uid_button)
            self.coords(back, (bbox[0]+2,bbox[1]+2,bbox[2]-2,bbox[1]+2,bbox[2]-2,bbox[3]-2,bbox[0]+2,bbox[3]-2))
            self.__auto_anchor(uid,pos,anchor)
            lt = stack[-1]
            endx = self.bbox(lt)[2]
            self.tag_unbind(lt, '<Button-1>')
            self.tag_unbind(lt, '<Enter>')
            self.tag_unbind(lt, '<Leave>')
        def __layout(x1,y1,x2,y2,expand=False):
            nonlocal endx,center_line
            dx,dy=self.__auto_layout(uid,(x1,y1,x2,y2),anchor)
            pos[0]+=dx
            pos[1]+=dy
            endx+=dx
            center_line+=dy
        pos = list(pos)
        root = self.create_text(pos, text=root, font=font, fill=fg, anchor='w')
        font_size = self.__get_text_size(root)
        segeo_font = '{Segoe Fluent Icons}' + font_size
        uid = TinUIString(f'breadcrumb-{root}')
        uid_button = uid + 'button'
        self.itemconfig(root, tags=(uid,uid_button))
        bbox = self.bbox(root)
        back = self.__ui_polygon(((bbox[0]+2,bbox[1]+2),(bbox[2]-2,bbox[3]-2)),fill=bg,outline=bg,width=9,tags=uid)
        self.tkraise(root)
        stack = collections.deque()
        stack.append(root)
        symstack = collections.deque()
        _, dy = self.__auto_anchor(uid, pos, anchor)
        endx = self.bbox(root)[2]
        center_line = pos[1] + dy
        del dy,bbox
        funcs = FuncList(4)
        funcs.get = get
        funcs.add = add
        funcs.delete = delete
        funcs.delete_to = delete_to
        uid.layout = __layout
        return root, back, funcs, uid

    def add_accentbutton(self,pos:tuple,text:str,**kwargs):# 绘制一个突出提示色按钮
        # 用于theme
        return self.add_button2(pos,text,**kwargs)

    def add_toolbutton(self,pos:tuple,text:str,**kwargs):# 绘制一个扁平工具按钮
        # 用于theme
        return self.add_button2(pos,text,**kwargs)


class BasePanel:
    """面板的基类"""
    def __init__(self, canvas):
        self.canvas = canvas
        # self.bg_rect = None
        # self.id = f"{self.__class__.__name__}_{id(self)}"
    
    # def create_bg(self, fill_color, outline_color):
    #     if not self.bg_rect:
    #         self.bg_rect = self.canvas.create_rectangle(
    #             0, 0, 0, 0, 
    #             fill=fill_color, outline=outline_color, 
    #             tags=self.id
    #         )


class ExpandablePanel(BasePanel):
    """可扩展面板的基类（VerticalPanel和HorizonPanel的父类）"""
    def __init__(self, canvas, padding=(0, 0, 0, 0), min_width=0, min_height=0):
        super().__init__(canvas)
        self.children = []
        self.padding = padding
        self.min_width = min_width
        self.min_height = min_height
        self.spacing = 0
    
    def set_padding(self, padding):
        self.padding = padding
        
    def set_min_size(self, min_width, min_height):
        self.min_width = min_width
        self.min_height = min_height
        
    def set_spacing(self, spacing):
        self.spacing = spacing
        
    def add_child(self, child, size=100, min_size=0, weight=0):
        """
        size: 元素尺寸（宽度或高度）
        min_size: 元素最小尺寸
        weight: 权重（用于分配剩余空间）
        """
        ...


class ExpandPanel(BasePanel):
    def __init__(self, canvas, child=None, padding=(0, 0, 0, 0), min_width=0, min_height=0):
        super().__init__(canvas)
        self.child = child
        self.padding = padding
        self.min_width = min_width
        self.min_height = min_height
        # self.create_bg("#e0f7fa", "#00838f")
    
    def set_padding(self, padding):
        self.padding = padding
        
    def set_min_size(self, min_width, min_height):
        self.min_width = min_width
        self.min_height = min_height
        
    def set_child(self, child):
        self.child = child
        
    def update_layout(self, x1, y1, x2, y2):
        # 应用内边距
        top, right, bottom, left = self.padding
        content_x1 = x1 + left
        content_y1 = y1 + top
        content_x2 = x2 - right
        content_y2 = y2 - bottom
        # 确保内容区域不小于最小尺寸
        content_width = max(content_x2 - content_x1, self.min_width)
        content_height = max(content_y2 - content_y1, self.min_height)
        content_x2 = content_x1 + content_width
        content_y2 = content_y1 + content_height
        # 更新背景位置
        # self.canvas.coords(self.bg_rect, x1, y1, x2, y2)
        # 更新子元素位置
        if self.child:
            if issubclass(self.child.__class__, BasePanel):
                self.child.update_layout(content_x1, content_y1, content_x2, content_y2)
            elif isinstance(self.child, TinUIString):
                self.child.layout(content_x1, content_y1, content_x2, content_y2, True)
                # self.canvas.coords(self.child, content_x1, content_y1, content_x2, content_y2)


class VerticalPanel(ExpandablePanel):
    def __init__(self, canvas, padding=(0, 0, 0, 0), spacing=0, min_width=0, min_height=0):
        super().__init__(canvas, padding, min_width, min_height)
        self.spacing = spacing
        # self.create_bg("#f1f8e9", "#558b2f")
    
    def add_child(self, child, size=None, min_size=0, weight=0):
        if not size:
            if isinstance(child, TinUIString):
                bbox = self.canvas.bbox(child)
                size = bbox[3] - bbox[1]
            else:
                size = 100
        self.children.append((child, size, min_size, weight))
    
    def update_layout(self, x1, y1, x2, y2):
        top, right, bottom, left = self.padding
        content_x1 = x1 + left
        content_y1 = y1 + top
        content_x2 = x2 - right
        content_y2 = y2 - bottom
        content_width = max(content_x2 - content_x1, self.min_width)
        content_height = max(content_y2 - content_y1, self.min_height)
        content_x2 = content_x1 + content_width
        content_y2 = content_y1 + content_height
        # 更新背景位置
        # self.canvas.coords(self.bg_rect, x1, y1, x2, y2)
        # 计算总权重和固定尺寸
        total_weight = 0
        fixed_size = 0
        for i, (child, height, min_height, weight) in enumerate(self.children):
            # 计算间距（最后一个元素不加间距）
            spacing = self.spacing if i < len(self.children) - 1 else 0
            
            if weight > 0:
                total_weight += weight
            else:
                actual_height = max(height, min_height)
                fixed_size += actual_height + spacing
        # 计算剩余空间
        remaining_height = max(0, content_height - fixed_size)
        current_y = content_y1
        total_children = len(self.children)
        for i, (child, height, min_height, weight) in enumerate(self.children):
            # 计算间距（最后一个元素不加间距）
            spacing = self.spacing if i < total_children - 1 else 0
            # 计算元素高度
            if weight > 0:
                # 按权重分配剩余空间
                proportional_height = remaining_height * weight / total_weight
                actual_height = max(proportional_height, min_height)
            else:
                actual_height = max(height, min_height)
            child_y2 = current_y + actual_height
            # 确保不会超出面板范围
            if child_y2 > content_y2:
                child_y2 = content_y2
            # 更新子元素位置
            if issubclass(child.__class__, BasePanel):
                child.update_layout(content_x1, current_y, content_x2, child_y2)
            elif isinstance(child, TinUIString):
                child.layout(content_x1, current_y, content_x2, child_y2)
                # self.canvas.coords(child, content_x1, current_y, content_x2, child_y2)
            current_y += actual_height + spacing
            # 如果已经超出面板底部，停止布局
            if current_y >= content_y2:
                break


class HorizonPanel(ExpandablePanel):
    def __init__(self, canvas, padding=(0, 0, 0, 0), spacing=0, min_width=0, min_height=0):
        super().__init__(canvas, padding, min_width, min_height)
        self.spacing = spacing
        # self.create_bg("#fff3e0", "#f57c00")
    
    def add_child(self, child, size=None, min_size=0, weight=0):
        if not size:
            if isinstance(child, TinUIString):
                bbox = self.canvas.bbox(child)
                size = bbox[2] - bbox[0]
            else:
                size = 100
        self.children.append((child, size, min_size, weight))
    
    def update_layout(self, x1, y1, x2, y2):
        top, right, bottom, left = self.padding
        content_x1 = x1 + left
        content_y1 = y1 + top
        content_x2 = x2 - right
        content_y2 = y2 - bottom
        content_width = max(content_x2 - content_x1, self.min_width)
        content_height = max(content_y2 - content_y1, self.min_height)
        content_x2 = content_x1 + content_width
        content_y2 = content_y1 + content_height
        
        # 更新背景位置
        # self.canvas.coords(self.bg_rect, x1, y1, x2, y2)
        
        total_weight = 0
        fixed_size = 0
        for i, (child, width, min_width, weight) in enumerate(self.children):
            spacing = self.spacing if i < len(self.children) - 1 else 0
            if weight > 0:
                total_weight += weight
            else:
                actual_width = max(width, min_width)
                fixed_size += actual_width + spacing
        remaining_width = max(0, content_width - fixed_size)
        current_x = content_x1
        total_children = len(self.children)
        for i, (child, width, min_width, weight) in enumerate(self.children):
            spacing = self.spacing if i < total_children - 1 else 0
            if weight > 0:
                proportional_width = remaining_width * weight / total_weight
                actual_width = max(proportional_width, min_width)
            else:
                actual_width = max(width, min_width)
            child_x2 = current_x + actual_width
            if child_x2 > content_x2:
                child_x2 = content_x2
            if issubclass(child.__class__, BasePanel):
                child.update_layout(current_x, content_y1, child_x2, content_y2)
            elif isinstance(child, TinUIString):
                child.layout(current_x, content_y1, child_x2, content_y2)
                # self.canvas.coords(child, current_x, content_y1, child_x2, content_y2)
            current_x += actual_width + spacing
            if current_x >= content_x2:
                break


class TinUI(BasicTinUI):
    '''对BasicTinUI的封装，添加了滚动条自动刷新'''

    def __init__(self,master,update:bool=True,update_time:int=1000,**kw):
        self.frame = Frame(master)
        self.vbar = ttk.Scrollbar(self.frame)
        self.vbar.pack(side=RIGHT, fill=Y)
        ###
        kw.update({'yscrollcommand': self.vbar.set})
        BasicTinUI.__init__(self,self.frame,**kw)
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
        self.bind('<MouseWheel>',self.set_y_view,True)
        config_bind=self.bind('<Configure>',lambda event:self.update__(),True)
        self.update_time=update_time
        if update==False:
            self.unbind("<Configure>",config_bind)

    def set_y_view(self,event):
        if event.state==0:#纵向滚动
            self.yview_scroll(int(-1*(event.delta/120)), "units")
        elif event.state==1:#横向滚动
            self.xview_scroll(int(-1*(event.delta/120)), "units")
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
        else:
            self.after(self.update_time,self.update__)


class TinUIXmlFunc:

    def __init__(self, function):
        self.function = function
    
    def __call__(self, *args, **kwargs):
        if self.function is None:
            return None
        return self.function(*args, **kwargs)


class TinUIXmlFuncDict:

    def __init__(self):
        self.data = {}
    
    def __setitem__(self, key, fun):
        if key in self.data:
            self.data[key].function = fun
        else:
            self.data[key] = TinUIXmlFunc(fun)
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __delitem__(self, key):
        self.data.pop(key)
    
    def __or__(self, other):
        if not isinstance(other, dict):
            return NotImplemented
        # 创建一个新的TinUIXmlFuncDict实例，合并self和other的内容
        new_dict = TinUIXmlFuncDict()
        new_dict.update(other)
        return new_dict
    
    def update(self, other):
        for key, value in other.items():
            self[key] = value
    
    def clear(self):
        self.data.clear()
    
    def __repr__(self):
        return f'{type(self).__name__}({self.data})'


class TinUIXml():#TinUI的xml渲染方式
    '''为TinUI提供更加方便的平面方式，使用xml
    TinUITheme基类无法直接使用，只能够重写TinUI或BasicTinUI的样式后才能够使用，参考 /theme 中的样式重写范例
    '''

    def __init__(self,ui:Union[BasicTinUI,TinUI,TinUITheme]):
        self.ui = ui
        if isinstance(ui, TinUITheme):
            self.realui = ui.ui
        else:
            self.realui = ui
        self.noload=('','menubar')#当前不解析的标签
        self.intargs=('width','linew','bd','r','minwidth','maxwidth','start','padx','pady','info_width','height','num','delay',)#需要转为数字的参数
        self.dataargs=('command','choices','widgets','content','percentage','data','cont','scrollbar','widget','offset',)#需要转为数据结构的参数
        self.funcs=TinUIXmlFuncDict()# 内部调用方法集合
        self.datas={}#内部数据结构集合
        self.tags={}#内部组件tag集合
        self.xendx,self.xendy=5,5#横向最宽原点
        self.yendx,self.yendy=5,5#纵向最低原点

    def __attrib2kws(self, args:dict, ignorecmd):#将部分特定参数转化为正确类型
        for key in args:
            if key in self.intargs:
                args[key] = int(args[key])
            elif key in self.dataargs:
                if key == 'command' and ignorecmd:
                    # 忽略command参数，允许开发者稍后定义
                    exec(f'{args[key]} = None')
                args[key] = eval(args[key])
        return args
    def __tags2uid(self,tag:str):#将self.tags中的内容转为画布uid
        name=self.tags[tag]
        if type(name)!=tuple or len(name)==1:
            uid=name
        else:
            uid=name[-1]
        return uid

    def __load_line(self,line,x=5,y=5,padx=5,pady=5,anchor='nw',ftags:list=[],ignorecmd=False):#根据xml的<line>逐行渲染TinUI组件
        last_y=y
        linex=None#纵块中的最大宽度
        padx = int(line.get('padx', padx))
        pady = int(line.get('pady', pady))
        xendx = x = int(line.get('x', x))
        xendy = y = int(line.get('y', y))
        allanchor = line.get('anchor', anchor)
        lineanchor = line.get('lineanchor', '')# 整个模块的对齐方向
        ftag = 'ftag-' + str(uuid.uuid1().hex)
        ftags.append(ftag)
        for i in line.iterfind('*'):#只检索直接子元素
            if i.tag=='line':
                liney,newlinex=self.__load_line(i,xendx,xendy,padx,pady,allanchor,ftags,ignorecmd)
                if liney>self.yendy-pady:#在同一位置判断纵向大小
                    last_y=xendy=liney
                if linex==None:#判断是否是该纵块的第一个<line>
                    linex=0
                linex = max(linex, newlinex+padx)
                continue
            if i.tag in self.noload:#不渲染的组件
                continue
            #特殊渲染的组件，有些仅对参数处理，有些需要特殊处理
            elif i.tag=='back':#调整uids参数
                if 'uids' in i.attrib:
                    olds=eval(i.attrib['uids'])
                    news=[]
                    for tag in olds:
                        uid=self.__tags2uid(tag)
                        news.append(uid)
                    i.attrib['uids']=tuple(news)
            elif i.tag=='labelframe':#同back
                if 'widgets' in i.attrib:
                    olds=eval(i.attrib['widgets'])
                    news=[]
                    for tag in olds:
                        uid=self.__tags2uid(tag)
                        news.append(uid)
                    i.attrib['widgets']=str(tuple(news))
            elif i.tag == 'flyout':
                if 'fid' in i.attrib:
                    i.attrib['fid'] = self.__tags2uid(i.attrib['fid'])
            elif i.tag == 'tooltip':
                if 'uid' in i.attrib:
                    i.attrib['uid'] = self.__tags2uid(i.attrib['uid'])
            #调整内部参数=====
            xendy=y#重新获取本行起始纵坐标
            if linex!=None:#存在纵块
                xendx=linex
                linex=None
            i.attrib['pos']=(xendx,xendy)
            attrib = self.__attrib2kws(i.attrib, ignorecmd)
            if 'anchor' not in i.attrib:
                attrib['anchor']=allanchor
            #==========
            tagall=eval(f'self.ui.add_{i.tag}(**attrib)')
            bboxtag = tagall[-1] if isinstance(tagall, tuple) else tagall
            for each_ftag in ftags:
                self.realui.addtag_withtag(each_ftag,bboxtag)
            bbox=self.realui.bbox(bboxtag)
            if not bbox:
                continue
            xendx=bbox[2]+padx#获取当前最大x坐标
            last_y = max(last_y, bbox[3] + pady)  # 更新当前最低y坐标
            #==========
            #进行特定控件内部xml布局
            if i.tag in ('ui', 'expander'):
                # 判断i是否存在子元素
                if len(i) != 0:
                    # 存在子元素，递归渲染
                    tagall[-2].__load_line(i, ignorecmd=True)
            elif i.tag == 'flyout':
                if len(i) != 0:
                    # 存在子元素，递归渲染
                    tagall[1].__load_line(i, ignorecmd=True)
            #为内部组件命名
            if i.text!=None:
                self.tags[i.text.strip()]=tagall
        # 根据lineanchor调整最后一行的位置
        bbox = self.realui.bbox(ftag)
        if bbox == None:
            self.realui.dtag(ftag)
            return last_y, xendx
        xcenter = (bbox[0]+bbox[2])/2
        ycenter = (bbox[1]+bbox[3])/2
        if lineanchor == '':
            dx = 0
            dy = 0
        elif lineanchor == 'nw':
            dx = x - bbox[0]
            dy = y - bbox[1]
        elif lineanchor == 'n':
            dx = x - xcenter
            dy = y - bbox[1]
        elif lineanchor == 'ne':
            dx = x - bbox[2]
            dy = y - bbox[1]
        elif lineanchor == 'e':
            dx = x - bbox[2]
            dy = y - ycenter
        elif lineanchor == 'se':
            dx = x - bbox[2]
            dy = y - bbox[3]
        elif lineanchor == 's':
            dx = x - xcenter
            dy = y - bbox[3]
        elif lineanchor == 'sw':
            dx = x - bbox[0]
            dy = y - bbox[3]
        elif lineanchor == 'w':
            dx = x - bbox[0]
            dy = y - ycenter
        elif lineanchor == 'center':
            dx = x - xcenter
            dy = y - ycenter
        else:
            raise ValueError(f'Invalid lineanchor value: {lineanchor}')
        self.realui.move(ftag, dx, dy)
        bbox = self.realui.bbox(ftag)
        xendx = bbox[2] + padx
        last_y = bbox[3] + pady
        self.realui.dtag(ftag)
        return last_y,xendx

    def loadxml(self,xml:str):#从xml字符串载入窗口组件
        self.xendx,self.xendy=5,5#横向最宽原点
        self.yendx,self.yendy=5,5#纵向最低原点
        root=ET.fromstring(xml)
        if root.tag!='tinui':#严格控制规范
            return
        for line in root.findall('line'):
            y,_=self.__load_line(line,y=self.yendy)
            if y>self.yendy-5:
                self.yendy=y+5

    def environment(self,dict_item:dict):#在funcs和datas中加入默认标识内容，一般为globals()或locals()
        self.funcs=self.funcs|dict_item
        self.datas=self.datas|dict_item

    def clean(self):#清空TinUI
        self.realui.clean_windows()
        self.funcs.clear()
        self.datas.clear()
        self.tags.clear()
        self.xendx,self.xendy=5,5#横向最宽原点
        self.yendx,self.yendy=5,5#纵向最低原点


tinui_dir=os.path.dirname(os.path.abspath(__file__))
TinUIFont.init_font_manager()
TinUIFont.load_font(tinui_dir+"\\Segoe Fluent Icons.ttf")


if __name__=='__main__':
    testmode=2

    if testmode==1:
        # panel test
        a=Tk()
        a.geometry('500x500+5+5')
        a.title('TinUIPanel')
        a.iconbitmap('LOGO.ico')
        b=BasicTinUI(a,bg='white')
        b.pack(fill='both',expand=True)
        rp=ExpandPanel(b)
        hp=HorizonPanel(b)
        rp.set_child(hp)

        v1=ExpandPanel(b)
        # v1=VerticalPanel(b)

        hp.add_child(v1,size=150,weight=1)
        # hp.add_child(v1,size=150)

        ct=b.add_textbox((0,0))[-1]

        v1.set_child(ct)
        # hp.add_child(ct,size=80,weight=1)

        v2=VerticalPanel(b)
        hp.add_child(v2,size=150)

        def update(e):
            rp.update_layout(5,5,e.width-5,e.height-5)
        b.bind('<Configure>',update)
        a.mainloop()

    else:
        def test(event):
            a.title('TinUI Test')
            b.add_paragraph((50,150),'这是TinUI按钮触达的事件函数回显，此外，窗口标题也被改变、首行标题缩进减小')#,font='{A019-Sounso Quality} 12')
            b.coords(m,100,5)
        def __test4(prog):
            progressgoto(prog)
        def test4(event):
            for i in range(1,101):
                a.after(i*20, lambda i=i: __test4(i))
        def test5(result):
            b.itemconfig(scale_text,text='当前选值：'+str(result))
        def test6():
            for i in range(0,5):
                num=i
                xml=f'''
        <tinui><line x='{num*10+5}'><label text='这是第{num}个BasicTinUI组件'></label></line>
        <line><button text='功能按钮' command='lambda event:print("第{i}个功能按钮")'></button>
        <combobox width='80' text='可选测试' content='("{i}","其它")'></combobox></line></tinui>'''
                ppgl[i][2].loadxml(xml)
        def test7():
            ntvdict=ntb.getvdict()
            num=1
            for i in ntvdict:
                uxml=ntvdict[i][1]#tinuixml
                xml=f'''
        <tinui><line><button text='这是第{num}个BasicTinUI组件' command='print'></button></line>
        <line><label text='TinUI的标签栏视图'></label><label text='每个都是单独页面'></label></line>
        </tinui>'''
                uxml.loadxml(xml)
                num+=1
        def test8(rbtext):
            print(f'单选组控件选值=>{rbtext}')
        def test9():
            def new_title(*e):
                ntb.newtitle(newnotepage,'一个崭新的标题')
            newnotepage=ntb.addpage('newpage')
            uxml=ntb.getvdict()[newnotepage][1]#tinuixml
            uxml.funcs['newtitle']=new_title
            uxml.loadxml('''<tinui><line><button text='这是一个新的标题栏窗口' command='self.funcs["newtitle"]'></button></line>
        <line><label text='TinUI的标签栏视图'></label><label text='每个都是单独页面'></label></line>
        </tinui>''')
        def test10(tag):
            b.itemconfig(pivott,text='pivot text: '+tag)
        def test11_1(e):
            wffunc.start()
        def test11_2(e):
            wffunc.end()
        def test12(cid):
            for i in cid:
                print(trvbox.itemcget(trvl[i][0],'text')+'/',end='')
            print('')
        def test13(state):
            if state:
                b.itemconfig(tgbutton,text='状态开关按钮：开启')
            else:
                b.itemconfig(tgbutton,text='状态开关按钮：关闭')

        a=Tk()
        a.geometry('700x700+5+5')
        a.iconbitmap('LOGO.ico')
        a.title('TinUI控件展示')

        b=TinUI(a,bg='white')
        b.pack(fill='both',expand=True)

        m=b.add_title((600,0),'TinUI is a modern way to show tkinter widget in your application, as they are drawn by tkinter canvas')
        m1=b.add_title((0,680),'test TinUI scrolled',size=2,angle=24)
        b.add_paragraph((2000,5),'location')
        b.add_paragraph((20,100),'下面的段落是测试画布的非平行字体显示效果，也是TinUI的简单介绍')
        b.add_button((250,450),'测试按钮',activefg='white',activebg='red',command=test,anchor='center',maxwidth=100)
        b.add_checkbutton((60,430),'允许TinUI测试',command=print,anchor='w')
        b.add_label((10,220),'这是由画布TinUI绘制的Label组件')
        uientry = b.add_entry((250, 330), 350, '', command=print, anchor='w')[0]
        uientry.insert(0, '请输入内容')
        b.add_button((20,170),'创建分割线',command=lambda event:b.add_separate((20,200),600),minwidth=200)
        b.add_radiobutton((50,480),300,'sky is blue, water is blue, too. So, what is your heart',('red','blue','black'),command=print)
        b.add_link((400,500),'TinGroup知识库','https://tinhome.bk-free02.com',anchor='nw')
        b.add_link((400,530),'执行print函数',print)
        b.add_link((400,560),'执行print目标函数','https://smart-space.com.cn/',command=lambda url:print('open> '+url))
        # _,ok1,_=b.add_waitbar1((500,220),bg='#CCCCCC')
        # _,_,ok2,_=b.add_waitbar2((600,400))
        # b.add_button((500,270),'停止等待动画',activefg='cyan',activebg='black',command=lambda e: ok1())
        # bu1=b.add_button((700,200),'停止点状滚动条',activefg='white',activebg='black',command=lambda e: ok2())[1]
        bu2=b.add_button((700,250),'nothing button 2')[1]
        bu3=b.add_button((700,300),'nothing button 3')[1]
        b.add_labelframe((bu2,bu3),'')
        b.add_combobox((600,550),text='你有多大可能去珠穆朗玛峰',width=230,content=('20%','40%','60%','80%','100%','1000%'))
        b.add_button((600,480),text='测试进度条（无事件版本）',command=test4)
        _,_,_,_,progressgoto,_,_=b.add_progressbar((600,510))
        b.add_table((180,630),data=(('a','space fans over the\nworld','c'),('you\ncan','2','3'),('I','II','have a dream, then try your best to get it!')))
        b.add_paragraph((300,850),text='上面是一个表格')
        b.add_onoff((600,100),anchor='se')
        b.add_spinbox((680,100),command=lambda string:print(f'{string.num}: {string}'))
        b.add_scalebar((680,50),command=test5)
        scale_text,_,_=b.add_label((890,50),text='当前选值：2')
        # b.add_info((710,140),info_text='this is info widget in TinUI, using TinUI\'s tooltip widget with its own style.',anchor='n')
        mtb=b.add_paragraph((0,720),'测试菜单（右键单击）')
        b.add_menubar(mtb,cont=(('command',print),('menu',print),'-',('TinUI文本移动',test)))
        ttb=b.add_paragraph((10,800),'TinUI能做些什么？')
        b.add_tooltip(ttb,'很多很多',delay=1)
        b.add_back(pos=(0,0),uids=(ttb,),bg='cyan',fg='cyan')
        _,_,ok3,_=b.add_waitbar3((600,800),width=240)
        b.add_button((600,750),text='停止带状等待框',command=lambda event:ok3())
        textbox=b.add_textbox((890,100),text='这是文本输入框，当然，无法在textbox的参数中绑定横向滚动'+'\n换行'*30)[0]
        textbox['wrap']='none'
        b.add_scrollbar((1095,100),textbox)
        b.add_scrollbar((890,305),textbox,direction='x')
        b.add_listbox((890,430),data=('item1','item2','item3','item4\n item4.1\n item4.2\n item4.3\n itme4.4\n item4.5','item5 and item5.1 and item5.2 and item5.3'),
        command=print)
        uixml,add_ui_id=b.add_ui((150,890),scrollbar=True,region='auto')[-2:]
        uixml.loadxml('''<tinui><line>
        <button text='button in child tinui'></button>
        <label text='you can use BasicTinUI in a father TinUI&#x000A;by using&#x000A;tinui.add_ui(...)'></label>
        </line><line>
        <label text='you can use&#x000A;manual function re-region&#x000A;also can use&#x000A;auto function&#x000A;just one&#x000A;like&#x000A;this'>
        </label>
        </line></tinui>''')
        ppgl=b.add_pipspager((400,890),num=25)[0]
        test6()
        ntb=b.add_notebook((800,900))[-2]
        for i in range(1,11):
            if i==5:#第五个不可删除:
                ntb.addpage('test'+str(i),'t'+str(i),cancancel=False)
            else:
                ntb.addpage('test'+str(i),'t'+str(i))
        ntb.showpage('t1')
        ntb.cannew(True,test9)
        test7()
        b.add_ratingbar((0,1150),num=28,command=print)
        radiofuncs = b.add_radiobox((320,1150),content=('1','2','3','','新一行内容','','单选','组','控件'),command=test8)[-2]
        radiofuncs.select(0)
        b.add_notecard((1200,50))
        pivott=b.create_text((1200,400),text='pivot text',anchor='nw',font='微软雅黑 12')
        b.add_pivot((1200,300),command=test10)
        b.add_button2((1200,180),text='圆角按钮',icon='\uF093',compound='top',minwidth=200)
        exux=b.add_expander((1200,500))[2]
        exux.loadxml('''<tinui><line>
        <button2 text='拓展UI框架的按钮'></button2></line>
        <line>
        <paragraph text='拓展UI框架可以节省布局位置，能够使用TinUIXml为可拓展UI框架编写界面布局。' width='190'></paragraph>
        </line>
        <line><paragraph text='感觉如何？' width='190'></paragraph></line><line><ratingbar></ratingbar>
        </line></tinui>
        ''')
        b.add_button((1220,650),text='获取TinUI相关信息',command=test11_1)
        wf,_,_,wffunc,_=b.add_waitframe((1220,700),height=250)
        wf.add_paragraph((150,100),text='Loading . . .',anchor='n')
        wf.add_button2((150,150),text='取消等待❌',anchor='n',command=test11_2)
        lvitems=b.add_listview((1220,980))[2]
        lvcontent=(
        ('BasicTinUI','TinUI框架渲染核心','https://tinui.smart-space.com.cn'),
        ('TinUI','基于tkinter的现代元素控件框架','https://smart-space.com.cn/project/TinUI/index.html'),
        ('CSDN','中文IT技术交流平台','https://www.csdn.net/'),
        ('TinText','新版TinML实现平台','https://tintext.smart-space.com.cn/'),
        ('Smart-Space','个人开发者名称','https://smart-space.com.cn')
        )
        for i in range(0,5):
            lvitems[i][2].loadxml(f'''<tinui>
            <line>
            <line>
            <title text='{lvcontent[i][0]}'></title>
            <link text='相关链接' url='{lvcontent[i][2]}'></link>
            </line>
            <line>
            <label text='{lvcontent[i][1]}'></label>
            </line>
            </line>
            </tinui>''')
        trvl,_,trvbox,_=b.add_treeview((1220,1300),command=test12)
        try:
            b.add_image((10,1300),200,250,imgfile=__file__[:-8]+'image/LOGO.png')#仅测试
        except Exception as err:
            print(err)
        tgbutton=b.add_togglebutton((1200,230),text='状态开关按钮：关闭',command=test13)[0]
        # b.add_swipecontrol((320,1300),'swipe control')
        b.add_passwordbox((250,1400),350)
        b.add_picker((1400,230),command=print)
        # b.add_menubutton((1500,50),'menubutton',widget=False,cont=(('command',print),('menu',(('cmd1',print),('cmd2',test1))),'-',('TinUI文本移动',test)))
        b.add_menubutton((1500,50),'menubutton',cont=(('command',print),('menu',print),'-',('TinUI文本移动',test)))
        b.add_barbutton((1500,150))
        flylabel = b.add_label((1500,500),text='点击展开浮出UI')[-1]
        _, flyxml, flyhide, _ = b.add_flyout(flylabel, offset=(-20, 0))
        flyxml.funcs['flyhide']=flyhide
        flyxml.loadxml('''<tinui><line><paragraph text='浮出UI'></paragraph></line>
        <line><paragraph text='add_flyout(fid, anchor="...")'></paragraph></line>
        <line><paragraph text='使用hide关闭'></paragraph></line>
        <line><button2 text='关闭浮出UI控件' command="self.funcs['flyhide']"></button2>
        </line></tinui>''')
        bc = b.add_breadcrumb((1500,350),anchor='n',command=print)[-2]
        for i in range(1,4):
            bc.add(f'item{i}')

        b.bind('<Destroy>',lambda e:b.clean_windows())

        a.mainloop()
