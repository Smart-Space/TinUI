from tkinter import *
from webbrowser import open as webopen
import time
from typing import Union
from types import FunctionType
import xml.etree.ElementTree  as ET
'''全部组件都是绘制的~~~，除了输入型组件无法使用tkinter画布完成对应效果'''
#==========
'''开发信息
开发者：Smart-Space（JunmingZhang）
版权：版权所有(C) 2019-present Smart-Space（JunmingZhang）
开发者邮箱：smart-space@qq.com
语言：Python
技术基础：tkinter（tcl/tk）
开源平台：pypi、GitHub、csdn
开源协议：GPLv3
贡献者：（暂无）
免费条款：注明TinUI的开发者，修改后必须开源，且同样使用GPL协议。商业软件需要为TinUI提供开源许可，并声明开发者版权所有
'''


class TinUINum:#数据载体，作者学习阶段的历史遗留产物
    pass


class TinUITheme:
    '''
    专门为特有样式的TinUI或BasicTinUI提供的类
    适用于重写样式配色的TinUI或BasicTinUI
    该类允许重写样式的TinUI或BasicTinUI使用TinUIXml
    '''

    def __init__(self,name='tinui-theme'):
        self.theme=name

    def change_theme_name(self,name:str):
        self.theme=name

    def get_theme(self):
        return self.theme


class BasicTinUI(Canvas):
    """基于tkinter的高级窗口绘制组件
    uid参数为每一个组件（除个别）的整体tag_name"""

    def __init__(self,master,**kw):
        Canvas.__init__(self,master,selectborderwidth=0,highlightthickness=0,bd=0, **kw)
        self.bind('<Button-1>',lambda event:self.focus_set())
        self.init()

    def init(self):
        self.title_size={0:20,1:18,2:16,3:14,4:12}

    def add_title(self,pos:tuple,text:str,fg='black',font='微软雅黑',size=1,anchor='nw',**kw):#绘制标题
        kw['anchor']=anchor
        return self.create_text(pos,text=text,fill=fg,font=(font,self.title_size[size]),**kw)

    def add_paragraph(self,pos:tuple,text:str,fg='black',font=('微软雅黑',12),side='left',width=500,anchor='nw',**kw):#绘制段落
        kw['anchor']=anchor
        return self.create_text(pos,text=text,fill=fg,font=font,justify=side,width=width,**kw)

    def add_button(self,pos:tuple,text:str,fg='#000000',bg='#CCCCCC',line='#CCCCCC',linew='3',activefg='black',activebg='#999999',activeline='#7a7a7a',font=('微软雅黑',12),command=None,anchor='nw'):#绘制按钮
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
        button=self.create_text(pos,text=text,fill=fg,font=font,anchor=anchor)
        uid='button'+str(button)
        self.itemconfig(button,tags=uid)
        bbox=self.bbox(button)
        x1,y1,x2,y2=bbox[0]-3,bbox[1]-3,bbox[2]+3,bbox[3]+3
        back=self.create_rectangle((x1,y1,x2,y2),fill=bg,outline=line,width=linew,tags=uid)
        self.tag_bind(button,'<Button-1>',on_click)
        self.tag_bind(button,'<Enter>',in_button)
        self.tag_bind(button,'<Leave>',out_button)
        self.tag_bind(back,'<Button-1>',on_click)
        self.tag_bind(back,'<Enter>',in_button)
        self.tag_bind(back,'<Leave>',out_button)
        self.tkraise(button)
        funcs=[change_command,disable,active]
        return button,back,funcs,uid

    def add_label(self,pos:tuple,text:str,fg='black',bg='#f0f0f0',outline='grey',font=('微软雅黑',12),anchor='nw'):#绘制标签
        label=self.create_text(pos,text=text,fill=fg,font=font,anchor=anchor)
        uid='label'+str(label)
        self.itemconfig(label,tags=uid)
        bbox=self.bbox(label)
        x1,y1,x2,y2=bbox[0]-3,bbox[1]-3,bbox[2]+3,bbox[3]+3
        back=self.create_rectangle((x1,y1,x2,y2),fill=bg,outline=outline,tags=uid)
        self.tkraise(label)
        return label,uid

    def add_checkbutton(self,pos:tuple,text:str,fontfg='black',fg='#868686',bg='#ededed',activefg='#868686',activebg='#e5e5e5',onfg='white',onbg='#334ac0',font=('微软雅黑',12),command=None,anchor='nw'):#绘制复选框
        def button_in(event):
            if self.itemcget(check,'fill')==onbg:
                pass
            else:
                self.itemconfig(check,outline=activebg,fill=activebg)
                self.itemconfig(outl,outline=activefg)
        def button_out(event):
            if self.itemcget(check,'fill')==onbg:
                pass
            else:
                self.itemconfig(check,outline=bg,fill=bg)
                self.itemconfig(outl,outline=fg)
        def go_func(event):
            if self.itemcget(check,'fill')!=onbg:
                self.itemconfig(check,fill=onbg,outline=onbg)
                self.itemconfig(outl,outline=onfg)
                self.itemconfig(state,state='normal')
                self.tkraise(state)
            else:
                self.itemconfig(check,fill=bg,outline=bg)
                self.itemconfig(outl,outline=fg)
                self.itemconfig(state,state='hidden')
            if command!=None:
                command(event)
        def flash():
            go_func(None)
        def on():
            self.itemconfig(check,fill=bg)
            go_func(None)
        def off():
            self.itemconfig(check,fill=onbg)
            go_func(None)
        def disable():
            self.itemconfig(checkbutton,state='disable',fill='#7a7a7a')
            self.itemconfig(check,state='disable')
            self.itemconfig(state,state='disable')
        def active():
            self.itemconfig(checkbutton,state='normal',fill=fontfg)
            self.itemconfig(check,state='normal')
            self.itemconfig(state,state='normal')
        checkbutton=self.create_text(pos,text=text,fill=fontfg,font=font,anchor=anchor)
        uid='checkbutton'+str(checkbutton)
        self.itemconfig(checkbutton,tags=uid)
        bbox=self.bbox(checkbutton)
        dic=bbox[3]-bbox[1]#位移长度
        self.move(checkbutton,dic+5,0)
        outl=self.create_polygon((pos[0]+1,pos[1]+1,pos[0]+dic-1,pos[1]+1,
        pos[0]+dic-1,pos[1]+dic-1,pos[0]+1,pos[1]+dic-1,pos[0]+1,pos[1]+1),
        width=5,outline=fg,fill=fg,tags=uid)
        check=self.create_polygon((pos[0]+2,pos[1]+2,pos[0]+dic-2,pos[1]+2,pos[0]+dic-2,pos[1]+dic-2,pos[0]+2,pos[1]+dic-2,pos[0]+2,pos[1]+2),
        width=5,outline=bg,fill=bg,tags=uid)
        state=self.create_line((pos[0]+2,pos[1]+2*dic/3-2,pos[0]+dic/3+2,pos[1]+dic-4,pos[0]+dic-2,pos[1]+dic/3-2),
        width=3,fill=onfg,state='hidden',tags=uid)
        self.tkraise(state)
        self.tag_bind(check,'<Enter>',button_in)
        self.tag_bind(check,'<Leave>',button_out)
        self.tag_bind(checkbutton,'<Enter>',button_in)
        self.tag_bind(checkbutton,'<Leave>',button_out)
        self.tag_bind(check,'<Button>',go_func)
        self.tag_bind(checkbutton,'<Button>',go_func)
        self.tag_bind(state,'<Button>',go_func)
        funcs=[flash,on,off,disable,active]
        return checkbutton,check,funcs,uid

    def add_entry(self,pos:tuple,width:int,text:str='',fg='#606060',bg='#f6f6f6',activefg='black',activebg='white',insert='#808080',font=('微软雅黑',12),linew=3,outline='#868686',onoutline='#3041d8',icon='>',anchor='nw',call='→',command=None):#绘制单行输入框
        #这是一个半绘制组件
        def if_empty(event):
            ch=entry.get()
            if ch=='':
                self.tag_unbind(funcw,'<Leave>')
                self.tag_unbind(funcw,'<Enter>')
                self.tag_unbind(funcw,'<Button-1>')
                self.itemconfig(funcw,text=icon,fill=fg)
            else:
                if self.itemcget(funcw,'text')==icon:
                    self.itemconfig(funcw,text='×')
                    self.tag_bind(funcw,'<Enter>',lambda event:self.itemconfig(funcw,fill=onoutline))
                    self.tag_bind(funcw,'<Leave>',lambda event:self.itemconfig(funcw,fill=fg))
                    self.tag_bind(funcw,'<Button-1>',lambda event:(entry.delete(0,'end'),if_empty(None)))
        def call_command(event):
            text=entry.get()
            command(text)
        entry=Entry(self,fg=fg,bg=bg,font=font,relief='flat',bd=0)
        entry.insert(0,text)
        entry.bind('<KeyRelease>',if_empty)
        entry.bind('<FocusIn>',lambda event:(self.itemconfig(back,outline=onoutline),entry.config(background=activebg,foreground=activefg)))
        entry.bind('<FocusOut>',lambda event:(self.itemconfig(back,outline=outline),entry.config(background=bg,foreground=fg)))
        funce=self.create_window(pos,window=entry,width=width,anchor=anchor)#输入框画布对象
        uid='entry'+str(funce)
        self.itemconfig(funce,tags=uid)
        bbox=self.bbox(funce)
        funcw=self.create_text((bbox[0]+width,bbox[1]),text=icon,fill=fg,font=font,anchor='nw',tags=uid)
        w=self.bbox(funcw)[2]
        h=self.bbox(funce)[3]
        bubbox=self.bbox(funcw)
        if command!=None:#调用函数的绑定仅当存在command时启动
            button=self.add_button((w+8,pos[1]+1),text=call,font=font,command=call_command,fg=fg,bg=bg,linew=0)
            self.addtag_withtag(uid,button[-1])
            entry.bind('<Return>',call_command)
            bubbox=self.bbox(button[-1])
        backpos=(bbox[0],bbox[1],bubbox[2],bbox[1],bubbox[2],bbox[3],bbox[0],bbox[3],bbox[0],bbox[1])
        outlinepos=(bbox[0]+linew,bbox[3]+4-linew,bubbox[2]-linew,bbox[3]+4-linew)
        back=self.create_polygon(outlinepos,fill=outline,outline=outline,width=6+linew,tags=uid)#outline
        back1=self.create_polygon(backpos,fill=bg,outline=bg,width=6,tags=uid)#back
        if command!=None:
            self.tkraise(button[-1])
        self.tkraise(funcw)
        if_empty(None)
        return entry,uid

    def add_separate(self,pos:tuple,width:int,direction='x',fg='grey'):#绘制分割线
        bbox=list(pos)
        if direction=='x':
            bbox.append(pos[0]+width)
            bbox.append(pos[1])
        elif direction=='y':
            bbox.append(pos[0])
            bbox.append(pos[1]+width)
        separate=self.create_line(bbox,fill=fg,width=3)
        return separate

    def add_radiobutton(self,pos:tuple,width,text='',choices=('choose me'),fg='black',bg='white',font=('微软雅黑',12),activefg='white',activebg='#4453db',command=None,anchor='nw'):#绘制单选框
        def button_in(tag,t):
            self.itemconfig(tag,fill=activebg,outline=activefg)
        def button_out(_tag,t):
            for tag in back_list:
                self.itemconfig(tag,fill=bg,outline=fg)
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
            self.itemconfig(tag,fill=activebg,outline=activefg)
            self.itemconfig(t,fill=activefg)
            if command!=None:
                command(_text)
        def select(num):
            back=choices_back[num]
            _text='select command'
            go_func(back,_text)
        def disable():
            for f,b in zip(choices_list,choices_back):
                self.itemconfig(f,state='disable',fill='#7a7a7a')
                self.itemconfig(b,state='disable')
        def active():
            for f,b in zip(choices_list,choices_back):
                self.itemconfig(f,state='normal',fill=fg)
                self.itemconfig(b,state='normal')
        word=self.create_text(pos,text=text,fill=fg,font=font,anchor=anchor,width=width)
        now_choice=None#当前选中项
        uid='radiobutton'+str(word)
        self.itemconfig(word,tags=uid)
        start_x=pos[0]#起始x位置
        height=self.bbox(word)[3]+3#变量y位置
        choices_list=[]
        choices_back=[]
        for i in choices:
            choice=self.create_text((start_x+2,height+2),text=i,fill=fg,font=font,anchor=anchor,width=width-4,tags=uid)
            bbox=self.bbox(choice)
            h=bbox[3]-bbox[1]+4
            back=self.create_rectangle((start_x,height,start_x+width,height+h),outline=fg,fill=bg,tags=uid)
            self.tkraise(choice)
            height+=h+2
            choices_list.append(choice)
            choices_back.append(back)
            self.tag_bind(choice,'<Enter>',lambda event,back=back,c=choice:button_in(back,c))
            self.tag_bind(choice,'<Leave>',lambda event,back=back,c=choice:button_out(back,c))
            self.tag_bind(back,'<Enter>',lambda event,back=back,c=choice:button_in(back,c))
            self.tag_bind(back,'<Leave>',lambda event,back=back,c=choice:button_out(back,c))
            self.tag_bind(choice,'<Button>',lambda event,_text=i,back=back,c=choice:go_func(back,_text,c))
            self.tag_bind(back,'<Button>',lambda event,_text=i,back=back,c=choice:go_func(back,_text,c))
        back_list=list(choices_back)
        funcs=[select,disable,active]
        return word,choices_list,choices_back,funcs,uid

    def add_link(self,pos:tuple,text,url:Union[str,FunctionType],fg='#4f62ca',activefg='red',activebg='#eaeaea',font:tuple=('微软雅黑',12),anchor='nw'):#绘制超链接
        def turn_red(event):
            self.itemconfig(link,fill=activefg)
            self.itemconfig(back,fill=activebg)
            self['cursor']='hand2'
        def turn_back(event):
            self.itemconfig(link,fill=fg)
            self.itemconfig(back,fill='')
            self['cursor']='arrow'
        def go_url(event):
            #如果是字符串，则打开网页；是方法，则执行函数
            if type(url)==str:
                webopen(url)
            else:
                url(event)
        def disable(fg='#b0b0b0'):
            self.itemconfig(link,state='disable',fill=fg)
            self.itemconfig(back,state='disable')
        def active():
            self.itemconfig(link,state='normal',fill=fg)
            self.itemconfig(back,state='normal')
        link=self.create_text(pos,text=text,fill=fg,font=font,anchor=anchor)
        uid='link'+str(link)
        self.itemconfig(link,tags=uid)
        font=self.itemcget(link,'font')+' underline'
        self.itemconfig(link,font=font)
        bbox=self.bbox(link)
        back=self.create_rectangle((bbox[0]-2,bbox[1]-2,bbox[2]+2,bbox[3]+2),width=0,tags=uid)
        self.tkraise(link)
        self.tag_bind(link,'<Enter>',turn_red)
        self.tag_bind(link,'<Leave>',turn_back)
        self.tag_bind(link,'<Button-1>',go_url)
        self.tag_bind(back,'<Enter>',turn_red)
        self.tag_bind(back,'<Leave>',turn_back)
        self.tag_bind(back,'<Button-1>',go_url)
        funcs=[disable,active]
        return link,funcs,uid

    def add_waitbar1(self,pos:tuple,fg='#0078D7',bg='',okfg='lightgreen',okbg='',bd=2,r=20):#绘制圆形等待组件
        def __start(i):
            if ifok.re==True:
                    return
            self.itemconfig(waitbar1,extent=i)
            self.update()
            if i==355:
                start()
        def start():
            if ifok.re==True:
                return
            for i in range(0,360,5):
                self.after(i*10,lambda i=i:__start(i))
        def ok():
            ifok.re=True
            self.itemconfig(waitbar1,outline=okfg,extent=359)
            self.itemconfig(back,fill=okbg)
        ifok=TinUINum
        ifok.re=False
        bbox=(pos[0],pos[1],pos[0]+2*r,pos[1]+2*r)
        back_bbox=(pos[0]+bd,pos[1]+bd,pos[0]+2*r-bd,pos[1]+2*r-bd)
        back=self.create_oval(back_bbox,width=0,fill=bg)
        uid='waitbar1'+str(back)
        self.itemconfig(back,tags=uid)
        waitbar1=self.create_arc(bbox,outline=fg,extent=5,start=90,width=bd,style='arc',tags=uid)
        start()
        return waitbar1,ok,uid

    def add_labelframe(self,widgets:tuple=(),title='',fg='#A8A8A8',bg='',pos=None):#绘制标题框
        sx,sy,ex,ey=self.bbox(widgets[0])#获取直接的起始位置
        for i in widgets:
            nsx,nsy,nex,ney=self.bbox(i)
            sx=nsx if nsx<sx else sx
            sy=nsy if nsy<sy else sy
            ex=nex if nex>ex else ex
            ey=ney if ney>ey else ey
        bg=self['background'] if bg=='' else bg
        frame=self.create_rectangle((sx-5,sy-20,ex+5,ey+5),fill=bg,outline=fg)
        label=self.create_text(((sx+ex)//2,sy-20),font='微软雅黑 10',text=title,fill=fg,anchor='center')
        self.create_rectangle(self.bbox(label),fill=bg,outline=bg)
        self.tag_raise(label)
        self.tag_lower(frame)
        return label,frame

    def add_waitbar2(self,pos:tuple,width:int=240,fg='#0078D7',bg='white',okcolor='lightgreen'):#绘制点状等待框
        #单点运动
        def ball_go(ball,w,x,num):
            self.move(ball,x,0)
            self.update()
            if num==4 and w>=width:
                for i in balls:
                    self.coords(i,ball_bbox)
                    self.update()
                start()
        #单点运动控制
        def _start(ball):
            if ifok.re==True:
                return
            self.itemconfig(ball,state='normal')
            num=balls.index(ball)
            fast=width//2
            for w in range(0,width+5-fast,5):
                self.after(w*15,lambda w=w:ball_go(ball,w,5,num))
            for w in range(width+5-fast,width+5-fast//2,5):
                self.after(w*15,lambda w=w:ball_go(ball,w+fast//2,10,num))
        #整体动画控制
        def start():
            if ifok.re==True:
                return
            for i in balls:
                self.after(balls.index(i)*500,lambda i=i:_start(i))
        def stop():
            ifok.re=True
            for i in balls:
                self.itemconfig(i,state='hidden')
            self.itemconfig(back,fill=okcolor)
        ifok=TinUINum()
        ifok.re=False
        bbox=(pos[0],pos[1],pos[0]+width+10,pos[1]+5)
        back=self.create_rectangle(bbox,fill=bg,outline=fg)
        uid='waitbar2'+str(back)
        self.itemconfig(back,tags=uid)
        balls=[]
        ball_bbox=(pos[0],pos[1],pos[0]+5,pos[1]+5)
        for b in range(1,6):
            ball=self.create_oval(ball_bbox,fill=fg,outline=fg,state='hidden',tags=uid)
            balls.append(ball)
        start()
        return back,balls,stop,uid

    def add_combobox(self,pos:tuple,width:int=200,text='',content:tuple=(),fg='black',bg='#F2F2F2',activefg='',activebg='#7B8ADA',font=('微软雅黑',12),command=None):#绘制组合/下拉框
        def button_in(_tag):
            self.itemconfig(_tag,fill=activebg,outline=activefg)
        def button_out(_tag):
            self.itemconfig(_tag,fill=bg,outline=fg)
        def open_box(event):
            if self.itemcget(button_text,'text')=='∨':
                self.itemconfig(button_text,text='∧',fill=activefg)
                self.itemconfig(box_tagname,state='normal')
            else:
                self.itemconfig(button_text,text='∨',fill=fg)
                self.itemconfig(box_tagname,state='hidden')
        def choose_this(back,word):
            self.itemconfig(main,text=word)
            open_box(None)
            if command!=None:
                command(word)
        def select(num):
            self.itemconfig(button_text,text='∧',fill=activefg)
            choose_this(*info[num])
        def disable():
            self.itemconfig(button_text,text='∧',fill=activefg)
            open_box(None)
            button_funcs[1](bg=bg)
        def active():
            button_funcs[2]()
        if activefg=='':
            activefg=self['background']
        main=self.create_text(pos,text=text,font=font,fill=fg,anchor='nw')
        uid='combobox'+str(main)
        self.itemconfig(main,tags=uid)
        bbox=self.bbox(main)
        x1,y1,x2,y2=bbox[0]-3,bbox[1]-3,bbox[0]+width+3,bbox[3]+3
        back=self.create_rectangle((x1,y1,x2,y2),fill=bg,outline=fg,tags=uid)
        self.tkraise(main)
        button_text,button_back,button_funcs,button_id=self.add_button((x2+3,y1+3),'∨',fg,bg,'#CCCCCC',1,activefg,activebg,'#7a7a7a',font=font,command=open_box)
        self.addtag_withtag(uid,button_id)
        start_x=bbox[0]#起始x位置
        height=bbox[3]+3#变量y位置
        box_tagname='combobox>'+str(main)+'>'+str(back)#绑定独立的tag名称
        info=[]
        for i in content:
            choice=self.create_text((start_x+2,height+2),text=i,fill=fg,font=(font[0],10),anchor='nw',width=width-4,tags=(uid,box_tagname))
            pos=self.bbox(choice)
            h=pos[3]-pos[1]+4
            cho_back=self.create_rectangle((start_x,height,start_x+width,height+h),outline=fg,fill=bg,tags=(uid,box_tagname))
            self.tkraise(choice)
            height+=h+2
            self.tag_bind(choice,'<Enter>',lambda event,back=cho_back:button_in(back))
            self.tag_bind(choice,'<Leave>',lambda event,back=cho_back:button_out(back))
            self.tag_bind(cho_back,'<Enter>',lambda event,back=cho_back:button_in(back))
            self.tag_bind(cho_back,'<Leave>',lambda event,back=cho_back:button_out(back))
            self.tag_bind(choice,'<Button>',lambda event,_text=i,back=cho_back:choose_this(back,_text))
            self.tag_bind(cho_back,'<Button>',lambda event,_text=i,back=cho_back:choose_this(back,_text))
            info.append((back,i))
        self.itemconfig(box_tagname,state='hidden')
        funcs=[select,disable,active]
        return main,back,box_tagname,funcs,uid

    def add_progressbar(self,pos:tuple,width=250,fg='#868686',bg='#334ac0',back='#f3f3f3',fontc='#79b8f8',percentage=True,text=''):#绘制进度条
        def goto(num:int):
            if not 0<=num<=100:
                return
            pw=width*num//100
            self.coords(progressbar,pos[0],pos[1],pos[0]+pw,pos[1]+15)
            if percentage==True:
                self.itemconfig(text,text=str(num)+'%')
            self.update()
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
        bbox=(pos[0],pos[1],pos[0]+width,pos[1]+15)
        back=self.create_rectangle((bbox),outline=fg,fill=back)
        uid='progressbar'+str(back)
        self.itemconfig(back,tags=uid)
        progressbar=self.create_rectangle((pos[0],pos[1],pos[0],pos[1]+15),outline=bg,fill=bg,tags=uid)
        pro_tagname='progressbar>'+str(back)
        self.addtag_withtag(progressbar,pro_tagname)
        #是否显示默认文本
        if percentage==True:
            text=self.create_text((pos[0]+width//2,pos[1]),anchor='n',text='0%',fill=fontc,font='微软雅黑 10',tags=uid)
        else:
            text=self.create_text((pos[0]+width//2,pos[1]),anchor='n',text=text,fill=fontc,font='微软雅黑 10',tags=uid)
        funcs=[now_running,now_paused,now_error]
        return back,pro_tagname,text,goto,funcs,uid

    def add_table(self,pos:tuple,outline='#E1E1E1',fg='black',bg='white',data=[['1','2','3'],['a','b','c']],minwidth=100,font=('微软雅黑',12),headbg='#d9ebf9'):#绘制表格
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
        title_num=len(data[0])#获取表头个数
        end_x,end_y=pos#起始位置
        height,relheight=0,0
        line_width={}#获取每列的固定宽度
        count=1
        ti_list=[]
        for i in data[0]:
            title=self.create_text((end_x,end_y),anchor='nw',text=i,fill=fg,font=font)
            if count==1:#只去第一个背景作为tag id
                uid='table'+str(title)
            self.itemconfig(title,tags=uid)
            bbox=self.bbox(title)
            if bbox[2]-bbox[0]<=minwidth:
                width=minwidth
            else:
                width=bbox[2]-bbox[0]
            line_width[count]=width
            height=bbox[3]-bbox[1]
            relheight=height if height>relheight else relheight
            ti_back=self.create_rectangle((end_x,end_y,end_x+width,end_y+height),outline=outline,fill=headbg,tags=uid)
            ti_list.append((ti_back,end_x,end_y,end_x+width))
            end_x=end_x+width+2
            count+=1
            self.tkraise(title)
        for i in ti_list:#保持表头高度一致
            self.coords(i[0],i[1],i[2],i[3],i[2]+relheight)
        end_y=pos[1]+relheight+2
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
                back=self.create_rectangle((end_x,end_y,end_x+width,end_y+height),outline=outline,fill=bg,tags=uid)
                self.tkraise(cont)
                a_dict[count]=(back,height,(end_x,end_y,end_x+width),cont)#(end_x,end_y,width)为重新绘制确定位置范围
                end_x=end_x+width+2
                count+=1
            height=get_max_height(a_dict)
            end_y=end_y+height+2
        return uid

    def add_onoff(self,pos:tuple,fg='#333333',bg='#FFFFFF',onfg='#FFFFFF',onbg='#4258CC',font=('微软雅黑',12),command=None):#绘制开关控件
        def __on():
            if command!=None:
                command(True)
        def __off():
            if command!=None:
                command(False)
        def __on_click(event):
            if self.itemcget(state,'fill')==fg:
                self.itemconfig(state,fill=onfg,text='on')
                self.move(state,width//10,0)
                self.itemconfig(back,fill=onbg,outline=onbg)
                __on()
            else:
                self.itemconfig(state,fill=fg,text='off')
                self.move(state,0-width//10,0)
                self.itemconfig(back,fill=bg,outline=fg)
                __off()
        state=self.create_text(pos,anchor='nw',text='off',fill=fg,font=font)
        uid='onoff'+str(state)
        self.itemconfig(state,tags=uid)
        bbox=self.bbox(state)
        d=int(bbox[3]-bbox[1])#获得绘制半径
        width=bbox[2]-bbox[0]#获取绘制宽度
        self.move(state,d,0)
        back=self.create_polygon((pos[0]+d,pos[1],pos[0],pos[1]+d/2,pos[0]+d,pos[1]+d,pos[0]+d+width,pos[1]+d,pos[0]+d*2+width,pos[1]+d/2,
        pos[0]+d+width,pos[1],pos[0]+d,pos[1]),fill=bg,outline=fg,width=2,joinstyle='miter',tags=uid)
        self.tkraise(state)
        self.tag_bind(state,'<Button-1>',__on_click)
        self.tag_bind(back,'<Button-1>',__on_click)
        return state,back,uid

    def add_spinbox(self,pos:tuple,width=150,data=('1','2','3'),now='',fg='black',bg='',activefg='black',activebg='#E5F1FB',font=('微软雅黑',12),command=None):#绘制选值框
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
                command(data[index])
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
                command(data[index])
        def check_in_data():
            val=wentry.get()
            if val in data:
                return True,val
            else:
                return False,val
        if bg=='':
            bg=self['background']
        wentry=Entry(self,font=font,fg=fg,bd=2,bg=bg,relief='groove')
        if now=='' or now not in data:
            now=data[0]
        wentry.insert(0,now)
        entry=self.create_window(pos,window=wentry,width=width,anchor='nw')
        uid='spinbox'+str(entry)
        self.itemconfig(entry,tags=uid)
        button1=self.add_button((pos[0]+width+2,pos[1]+2),text='∧',linew=1,fg=fg,bg=bg,activefg=activefg,activebg=activebg,font=font,command=updata)
        bbox=self.bbox(button1[-1])
        button2=self.add_button((bbox[2]+2,pos[1]+2),text='∨',linew=1,fg=fg,bg=bg,activefg=activefg,activebg=activebg,font=font,command=downdata)
        self.addtag_withtag(uid,button1[-1])
        self.addtag_withtag(uid,button2[-1])
        datanum=TinUINum()
        datanum.num=data.index(now)#记录数据位置
        maxnum=len(data)-1#最大位置
        return wentry,button1,button2,uid

    def add_scalebar(self,pos:tuple,width=200,fg='#3b50ba',activefg='#aeb5d7',bg='#868686',data=(1,2,3,4,5),start=1,command=None):#绘制调节框
        def mousedown(event):
            scale.startx=self.canvasx(event.x)
            bbox=self.bbox(button)
            self.coords(button,bbox[0],pos[1]-3,bbox[0]+10,pos[1]+29)
        def drag(event):
            move=self.canvasx(event.x)-scale.startx
            if self.canvasx(event.x)<pos[0] or self.canvasx(event.x)>pos[0]+width:
                return
            self.move(button,move,0)
            self.delete(name)
            active=self.create_line((pos[0],pos[1]+12,move+scale.startx,pos[1]+12),fill=fg,width=3,tags=(uid,name))
            scale.startx=self.canvasx(event.x)
        def check(event):
            bbox=self.bbox(button)
            self.coords(button,bbox[0],pos[1],bbox[0]+10,pos[1]+26)
            end=int(self.canvasx(event.x))
            if end<pos[0]:end=pos[0]
            if end>pos[0]+width:end=pos[0]+width
            rend=min(dash,key=lambda x:abs(x-end))
            num=dash.index(rend)
            if command!=None:
                command(data[num])
        def checkval(event):
            move=self.canvasx(event.x)
            self.coords(button,move,pos[1]-3,move+10,pos[1]+29)
            self.coords(name,pos[0],pos[1]+12,move,pos[1]+12)
            check(event)
        def select(num):
            self.coords(button,dash[num],pos[1]-3,dash[num]+10,pos[1]+29)
            self.coords(name,pos[0],pos[1]+12,dash[num],pos[1]+12)
        def disable():
            self.itemconfig(button,state='disable',fill='#7a7a7a')
            self.itemconfig(back,state='disable')
            self.itemconfig(name,state='disable',fill='#7a7a7a')
        def _active():
            self.itemconfig(button,state='normal',fill=fg)
            self.itemconfig(back,state='normal')
            self.itemconfig(name,state='normal',fill=fg)
        scale=TinUINum()#记录数据结构体
        back=self.create_line((pos[0],pos[1]+12,pos[0]+width,pos[1]+12),fill=bg,width=3)
        uid='scalebar'+str(back)
        self.itemconfig(back,tags=uid)
        self.tag_bind(back,'<ButtonRelease-1>',checkval)
        dash_t=width//(len(data)-1)
        s=pos[0]#调节线段起点
        dash=[s]#调节线段的终点位置
        for i in data[1:]:
            s+=dash_t
            dash.append(s)
        del s
        active=self.create_line((pos[0],pos[1]+12,dash[start],pos[1]+12),fill=fg,width=3,tags=uid)
        name='scaleactive'+str(active)
        self.tag_bind(name,'<ButtonRelease-1>',checkval)
        self.addtag_withtag(name,active)#为重绘绑定tag名称
        button=self.create_rectangle((dash[start],pos[1],dash[start]+10,pos[1]+26),width=0,fill=fg,tags=uid)
        self.tag_bind(button,'<Enter>',lambda event:self.itemconfig(button,fill=activefg))
        self.tag_bind(button,'<Leave>',lambda event:self.itemconfig(button,fill=fg))
        self.tag_bind(button,'<Button-1>',mousedown)
        self.tag_bind(button,'<B1-Motion>',drag)
        self.tag_bind(button,'<ButtonRelease-1>',check)#矫正位置
        funcs=[select,disable,_active]
        return name,back,button,funcs,uid

    def add_info(self,pos:tuple,font='微软雅黑 9',fg='#0078d4',bg='white',info_text='',info_font=('微软雅黑','12'),info_width=200,info_fg='black'):#绘制提示框
        def showinfo(event):
            self.itemconfig(infotagname,state='normal')
        def hideinfo(event):
            self.itemconfig(infotagname,state='hidden')
        text=self.create_text(pos,anchor='nw',text='i',font=font,fill=fg)
        uid='info'+str(text)
        self.itemconfig(text,tags=uid)
        bbox=self.bbox(text)
        back=self.create_rectangle((bbox[0]-2,bbox[1]-2,bbox[2]+2,bbox[3]+2),fill=bg,outline=fg,width=2,tags=uid)
        self.tkraise(text)
        self.tag_bind(back,'<Enter>',showinfo)
        self.tag_bind(back,'<Leave>',hideinfo)
        self.tag_bind(text,'<Enter>',showinfo)
        self.tag_bind(text,'<Leave>',hideinfo)
        info=self.create_text((bbox[2]+10,(bbox[3]+bbox[1])//2),anchor='nw',text=info_text,font=info_font,fill=info_fg,width=info_width,tags=uid)
        ibbox=self.bbox(info)
        info_back=self.create_rectangle((ibbox[0]-2,ibbox[1]-2,ibbox[2]+2,ibbox[3]+2),width=1,fill=bg,outline=fg,tags=uid)
        self.tkraise(info)
        infotagname='info'+str(info)+str(info_back)
        self.addtag_withtag(infotagname,info)
        self.addtag_withtag(infotagname,info_back)
        self.itemconfig(infotagname,state='hidden')
        return text,back,infotagname,uid

    def add_menubar(self,cid='all',bind='<Button-3>',font='微软雅黑 12',fg='#ecf3e8',bg='#2b2a33',activefg='#ecf3e8',activebg='#616161',cont=(('command',print),'-'),tran='#01FF11'):#绘制菜单
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
                pos=bar.bbox(back)
                bar.coords(back,(5,pos[1],10+maxwidth,pos[3]))
            for sep in seps:
                pos=bar.bbox(sep)
                bar.delete(sep)
                bar.add_separate((5,pos[1]),maxwidth+5,fg=activebg)
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
            sx,sy=event.x_root,event.y_root
            if sx+winw>maxx:
                x=sx-winw
            else:
                x=sx
            if sy+winh>maxy:
                y=sy-winh
            else:
                y=sy
            menu.geometry(f'{winw+20}x{winh+20}+{x}+{y}')
            bar.move('all',0,-height-7)
            menu.deiconify()
            menu.focus_set()
            for i in range(0,height+5,5):#滚动动画
                bar.move('all',0,5)
                time.sleep(0.01)
                bar.update()
            bar.move('all',0,5)
            bar.config(scrollregion=bar.bbox('all'))
            bar.yview_moveto(0)
            bar.update()
        self.tag_bind(cid,bind,show)
        menu=Toplevel(self)
        menu.overrideredirect(True)
        menu.withdraw()
        bar=BasicTinUI(menu,bg=tran)
        bar.pack(fill='both',expand=True)
        wind=TinUINum()#记录数据
        backs=[]#按钮
        funcs=[]#按钮函数接口
        seps=[]#分割线
        widths=[]#寻找最宽位置
        for i in cont:#添加菜单内容
            if i=='-':
                sep=bar.add_separate((15,endy()),100,fg=activebg)
                seps.append(sep)
            else:
                button=bar.add_button((15,endy()),i[0],fg,bg,bg,3,activefg,activebg,activebg,font,command=lambda event,i=i:(i[1](event),menu.withdraw()))
                backs.append(button[1])
                funcs.append(button[2])
                pos=bar.bbox(button[1])
                width=pos[2]-pos[0]
                widths.append(width)
        repaint()
        readyshow()
        #绘制圆角边框
        bbox=bar.bbox('all')
        height=bbox[3]-bbox[1]
        start=bbox[2]-bbox[0]
        gomap=((start,bbox[1]),(bbox[2],bbox[1]),(bbox[2],bbox[3]),(bbox[0],bbox[3]),(bbox[0],bbox[1]),(start,bbox[1]))
        mback=bar.create_polygon(gomap,fill=bg,outline=bg,width=15)
        bar.lower(mback)
        bar.move('all',15,0)
        menu.bind('<FocusOut>',lambda event:menu.withdraw())
        menu.attributes('-transparent',tran)
        return menu,bar,funcs

    def add_tooltip(self,uid,text='',fg='#3b3b3b',bg='#e7e7e7',font='微软雅黑 12',tran='#01FF11'):#绘制窗口提示框
        def show_toti(event):
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
            toti.withdraw()
        toti=Toplevel()
        toti.overrideredirect(True)
        toti.withdraw()
        bar=TinUI(toti,bg=tran)
        bar.pack(fill='both',expand=True)
        info=bar.create_text((10,10),text=text,fill=fg,font=font,anchor='nw')
        bbox=bar.bbox(info)
        width=bbox[2]-bbox[0]+10
        height=bbox[3]-bbox[1]+10
        #绘制圆角边框
        start=bbox[2]-bbox[0]
        gomap=((start,bbox[1]),(bbox[2],bbox[1]),(bbox[2],bbox[3]),(bbox[0],bbox[3]),(bbox[0],bbox[1]),(start,bbox[1]))
        tback=bar.create_polygon(gomap,fill=bg,outline=bg,width=15)
        bar.lower(tback)
        #屏幕尺寸
        maxx=self.winfo_screenwidth()
        maxy=self.winfo_screenheight()
        self.tag_bind(uid,'<Enter>',show_toti)
        self.tag_bind(uid,'<Leave>',hide_toti)
        toti.attributes('-transparent',tran)
        toti.attributes('-alpha',0.9)#透明度90%
        return toti,bar

    def add_back(self,pos:tuple,uids:tuple=(),fg='',bg='',linew=0):#绘制背景或间隔框
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
            cpos[0]-=2
            cpos[1]-=2
            cpos[2]+=2
            cpos[3]+=2
            back=self.create_rectangle(cpos,fill=bg,outline=fg,width=linew)
        self.lower(back)
        return back

    def add_waitbar3(self,pos:tuple,width:int=200,fg='#3041d8',bg='#f3f3f3',okcolor='lightgreen'):#绘制带状等待框
        def move(startx,endx,nowwidth):
            if nowwidth-maxwidth>width:#一轮动画完成
                start()
                return
            self.coords(bar,(pos[0]+startx,pos[1],pos[0]+endx,pos[1]+4))
            start(nowwidth+5)
        def start(nowwidth=0):#开始动画
            if ifok.ok==True:#已完成
                self.itemconfig(bar,fill=okcolor,outline=okcolor)
                self.coords(bar,(pos[0],pos[1],pos[0]+width,pos[1]+4))
            if nowwidth<=maxwidth:#增长阶段
                self.after(50,lambda : move(0,nowwidth,nowwidth))
            elif nowwidth>=width:#缩小阶段
                self.after(50,lambda : move(nowwidth-maxwidth,width,nowwidth))
            else:#平滑阶段。因为我们去整数，所以平滑阶段无法使用断点判断
                self.after(50,lambda : move(nowwidth-maxwidth,nowwidth,nowwidth))
        def stop():#停止
            ifok.ok=True
        ifok=TinUINum()#记录是否暂停
        ifok.ok=False
        bbox=(pos[0],pos[1],pos[0]+width,pos[1]+4)
        back=self.create_rectangle(bbox,fill=bg,outline=bg)
        uid='waitbar3'+str(back)
        self.itemconfig(back,tags=uid)
        maxwidth=width//3
        bar=self.create_rectangle((pos[0],pos[1],pos[0],pos[1]),fill=fg,outline=fg,tags=uid)
        start()
        return back,bar,stop,uid

    def add_textbox(self,pos:tuple,width:int=200,height:int=200,text:str='',anchor='nw',font='微软雅黑 12',fg='black',bg='white',linew=3,scrollbar=False,outline='#63676b',onoutline='#3041d8'):#绘制文本框
        textbox=Text(self,font=font,fg=fg,bg=bg,highlightthickness=linew,highlightbackground=outline,highlightcolor=onoutline,relief='flat')
        cavui=self.create_window(pos,window=textbox,width=width,height=height,anchor=anchor)
        uid='textbox'+str(cavui)
        self.addtag_withtag(uid,cavui)
        textbox.insert(1.0,text)
        if scrollbar==True:#不支持横向滚动自动绑定
            bbox=self.bbox(uid)
            cid=self.add_scrollbar((bbox[2]+5,bbox[1]),textbox,bbox[3]-bbox[1])[-1]
            self.addtag_withtag(uid,cid)
        return textbox,uid

    def add_scrollbar(self,pos:tuple,widget,height:int=200,direction='y',bg='#f0f0f0',color='#999999',oncolor='#89898b'):#绘制滚动条
        #滚动条宽度7px，未激活宽度3px；建议与widget相隔5xp
        def enter(event):#鼠标进入
            self.itemconfig(sc,outline=oncolor,width=7)
        def leave(event):#鼠标离开
            self.itemconfig(sc,outline=color,width=3)
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
                self.move(sc,0,move)
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
                widget.xview('moveto',startp*1.2)
        if direction.upper()=='X':
            mode='x'
        elif direction.upper()=='Y':
            mode='y'
        else:
            return None
        #上标、下标 ▲▼
        if mode=='y':
            #back=self.create_rectangle((pos[0],pos[1],pos[0]+10,pos[1]+height),fill=bg,width=0)
            back=self.create_polygon((pos[0]+5,pos[1]+5,pos[0]+5,pos[1]+height-5,pos[0]+5,pos[1]+5),
            width=12,outline=bg)
            uid='scrollbar'+str(back)
            self.itemconfig(back,tags=uid)
            top=self.create_text(pos,text='▲',font='微软雅黑 8',anchor='nw',fill=oncolor,tags=uid)
            bottom=self.create_text((pos[0],pos[1]+height),text='▼',font='微软雅黑 8',anchor='sw',fill=oncolor,tags=uid)
            #sc=self.create_rectangle((pos[0],pos[1]+15,pos[0]+10,pos[1]+height-15),fill=color,width=0,tags=uid)
            sc=self.create_polygon((pos[0]+5,pos[1]+20,pos[0]+5,pos[1]+height-20,pos[0]+5,pos[1]+20,),
            width=3,outline=color,tags=uid)
            #起始和终止位置
            start=pos[1]+15
            end=pos[1]+height-15
            canmove=end-start
            #绑定组件
            widget.config(yscrollcommand=widget_move)
        elif mode=='x':
            back=self.create_polygon((pos[0]+5,pos[1]+5,pos[0]+height-5,pos[1]+5,pos[0],pos[1]+5),
            width=12,outline=bg)
            uid='scrollbar'+str(back)
            self.itemconfig(back,tags=uid)
            top=self.create_text((pos[0]+2,pos[1]+11),text='▲',angle=90,font='微软雅黑 8',anchor='w',fill=oncolor,tags=uid)
            bottom=self.create_text((pos[0]+height,pos[1]),text='▼',angle=90,font='微软雅黑 8',anchor='se',fill=oncolor,tags=uid)
            sc=self.create_polygon((pos[0]+20,pos[1]+5,pos[0]+height-20,pos[1]+5,pos[0]+20,pos[1]+5),
            width=3,outline=color,tags=uid)
            start=pos[0]+8
            end=pos[0]+height-13
            canmove=(end-start)*0.95
            widget.config(xscrollcommand=widget_move)
        scroll=TinUINum()
        use_widget=True#是否允许控件控制滚动条
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
        return top,bottom,back,sc,uid

    def add_listbox(self,pos:tuple,width:int=200,height:int=200,font='微软雅黑 12',data=('a','b','c'),bg='#f2f2f2',fg='black',activebg='#e9e9e9',sel='#b4bbea',anchor='nw',command=None):#绘制列表框
        def repaint_back():
            for v in choices.values():
                bbox=box.coords(v[1])
                box.coords(v[1],3,bbox[1]-2,5+maxwidth+2,bbox[3]+2)
        def in_mouse(t):
            if choices[t][2]==True:#已被选中
                return
            box.itemconfig(choices[t][1],fill=activebg)
        def out_mouse(t):
            if choices[t][2]==True:#已被选中
                box.itemconfig(choices[t][1],fill=sel)
            else:
                box.itemconfig(choices[t][1],fill=bg)
        def sel_it(t):
            box.itemconfig(choices[t][1],fill=sel)
            choices[t][2]=True
            for i in choices.keys():
                if i==t:
                    continue
                choices[i][2]=False
                out_mouse(i)
            if command!=None:
                command(t)
        frame=BasicTinUI(self,bg=bg)#主显示框，显示滚动条
        box=BasicTinUI(frame,bg=bg,width=width,height=height)#显示选择内容
        box.place(x=12,y=12)
        cavui=self.create_window(pos,window=frame,width=width+24,height=height+24,anchor=anchor)
        uid='listbox'+str(cavui)
        self.addtag_withtag(uid,cavui)
        frame.add_scrollbar((width+12,12),widget=box,height=height,bg=bg,color=fg,oncolor=fg)#纵向
        frame.add_scrollbar((12,height+12),widget=box,height=height,direction='x',bg=bg,color=fg,oncolor=fg)#横向
        choices={}#'a':[a_text,a_back,is_sel:bool]
        maxwidth=0#最大宽度
        for i in data:
            end=box.bbox('all')
            end=5 if end==None else end[-1]
            text=box.create_text((5,end+7),text=i,fill=fg,font=font,anchor='nw')
            bbox=box.bbox(text)
            twidth=bbox[2]-bbox[0]
            maxwidth=twidth if twidth>maxwidth else maxwidth
            back=box.create_rectangle((3,bbox[1]-2,bbox[2]+2,bbox[3]+2),width=0,fill=bg)
            box.tkraise(text)
            choices[i]=[text,back,False]
            box.tag_bind(text,'<Enter>',lambda event,text=i : in_mouse(text))
            box.tag_bind(text,'<Leave>',lambda event,text=i : out_mouse(text))
            box.tag_bind(text,'<Button-1>',lambda event,text=i : sel_it(text))
            box.tag_bind(back,'<Enter>',lambda event,text=i : in_mouse(text))
            box.tag_bind(back,'<Leave>',lambda event,text=i : out_mouse(text))
            box.tag_bind(back,'<Button-1>',lambda event,text=i : sel_it(text))
        if maxwidth<width:
            maxwidth=width
        repaint_back()
        bbox=box.bbox('all')
        box.config(scrollregion=bbox)
        def set_y_view(event):
            box.yview_scroll(int(-1*(event.delta/120)), "units")
        box.bind('<MouseWheel>',set_y_view)
        return box,uid

    def add_listview(self,pos:tuple)->FunctionType:#绘制列表视图,function:add_list
        ...

    def add_canvas(self,pos:tuple,width:int=200,height:int=200,bg='white',outline='#808080',linew=1,scrollbar=False,anchor='nw'):#绘制画布
        def re_scrollregion():#更新滚动范围
            canvas.config(scrollregion=canvas.bbox('all'))
        canvas=Canvas(self,bg=bg,highlightthickness=linew,highlightbackground=outline,relief='flat')
        cavui=self.create_window(pos,window=canvas,width=width,height=height,anchor=anchor)
        uid='canvas'+str(cavui)
        self.addtag_withtag(uid,cavui)
        if scrollbar==True:
            bbox=self.bbox(uid)
            cid1=self.add_scrollbar((bbox[2]+5,bbox[1]),canvas,bbox[3]-bbox[1])[-1]
            cid2=self.add_scrollbar((bbox[0],bbox[3]+5),canvas,bbox[2]-bbox[0],'x')[-1]
            self.addtag_withtag(uid,cid1)
            self.addtag_withtag(uid,cid2)
        return canvas,re_scrollregion,uid

    def add_ui(self,pos:tuple,width:int=200,height:int=200,bg='white',scrollbar=False,region='man',anchor='nw'):#绘制BasicTinUI
        def __update():#更新宽高
            try:
                re_scrollregion()
            except:
                pass
            else:
                ui.after(1000,__update)
        def re_scrollregion():#更新滚动范围
            ui.config(scrollregion=ui.bbox('all'))
        ui=BasicTinUI(self,bg=bg)
        cavui=self.create_window(pos,window=ui,width=width,height=height,anchor=anchor)
        uid='ui'+str(cavui)
        self.addtag_withtag(uid,cavui)
        if scrollbar==True:
            bbox=self.bbox(uid)
            cid1=self.add_scrollbar((bbox[2]+5,bbox[1]),ui,bbox[3]-bbox[1])[-1]
            cid2=self.add_scrollbar((bbox[0],bbox[3]+5),ui,bbox[2]-bbox[0],'x')[-1]
            self.addtag_withtag(uid,cid1)
            self.addtag_withtag(uid,cid2)
        if region=='man':#手动调节
            pass
        elif region=='auto':#自动调节
            __update()
        ui_xml=TinUIXml(ui)
        return ui,re_scrollregion,ui_xml,uid

    def add_pipspager(self,pos:tuple,width:int=200,height:int=200,bg='#f3f3f3',fg='#898989',buttonbg='#f8f8f8',num:int=2):#绘制翻页视图
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
        def __move_to(number):
            nonlocal nowui
            self.itemconfig(uilist[nowui][0],state='hidden')
            nowui=number
            self.itemconfig(uilist[nowui][0],state='normal')
        def move_to(number):
            __dot_in(dotlist[nowui])
            __dot_select(dotlist[nowui])
            __move_to(nowui)
        def __dot_in(dote):
            bar.itemconfig(dote,width=3)
        def __dot_out(dote):
            if dotlist.index(dote)==nowui:
                pass
            else:
                bar.itemconfig(dote,width=0)
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
                        bar.itemconfig(i,width=0)
        startx=pos[0]+20#按钮与主窗口间隔
        uilist=list()#[(uiid-1,BasicTinUI-1,TinUIXml-1),(uiid-2,BasicTinUI-2,TinUIXml-2),...]
        doty=pos[1]+height+5#控制点的起始纵坐标
        dotlist=list()#[dot1,dot2,...]
        nowui=0#当前显示界面序号
        leftbutton=self.add_button((startx-2,pos[1]+width/2),'<',fg=fg,bg=buttonbg,linew=0,activefg=buttonbg,activebg=fg,command=move_left,anchor='e')[-1]
        rightbutton=self.add_button((startx+width+2,pos[1]+width/2),'>',fg=fg,bg=buttonbg,linew=0,activefg=buttonbg,activebg=fg,command=move_right,anchor='w')[-1]
        uid='pipspager'+str(leftbutton)+str(rightbutton)
        self.addtag_withtag(uid,leftbutton)
        self.addtag_withtag(uid,rightbutton)
        bar=Canvas(self,bg=bg,highlightthickness=0,relief='flat')#导航栏
        barid=self.create_window((startx,doty),window=bar,width=width,height=11,anchor='nw',tags=uid)
        dotx=3
        for i in range(0,num):
            ui=BasicTinUI(self,bg=bg)
            tinuixml=TinUIXml(ui)
            uiid=self.create_window((startx,pos[1]),window=ui,width=width,height=height,state='hidden',anchor='nw',tags=uid)
            uilist.append((uiid,ui,tinuixml))
            dot=bar.create_oval((dotx,3,dotx+5,8),fill=fg,outline=fg,width=0)
            dotlist.append(dot)
            dotx+=13
            bar.tag_bind(dot,'<Enter>',lambda event,dote=dot:__dot_in(dote))
            bar.tag_bind(dot,'<Leave>',lambda event,dote=dot:__dot_out(dote))
            bar.tag_bind(dot,'<Button-1>',lambda event,dote=dot:__dot_select(dote))
        __dot_in(dotlist[nowui])
        __dot_select(dotlist[nowui])
        __move_to(nowui)
        return uilist,dotlist,move_to,uid

    def add_notebook(self,pos:tuple,width:int=400,height:int=400,color='#f9f9fc',fg='#1a1a1a',bg='#f3f3f3',activefg='#595959',activebg='#ededed',onfg='#191919',onbg='#eaeaea'):#绘制标签栏视图
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
        def addpage(title:str,flag=None,scrollbar=False):#创建页面
            if tbu.bbox('all')==None:
                endx=3
            else:
                endx=tbu.bbox('all')[2]+3
            titleu=tbu.create_text((endx,2),text=title,fill=fg,font=font,anchor='nw')
            cbx=tbu.bbox(titleu)[2]+10
            cb=tbu.create_text((cbx,2),text='×',font=font,fill=fg,anchor='nw')
            tbbbox=tbu.bbox(titleu)
            bux=(endx+2,tbbbox[1],cbx+15,tbbbox[1],cbx+15,tbbbox[3],endx+2,tbbbox[3],endx+2,tbbbox[1])
            bu=tbu.create_polygon(bux,fill=bg,outline=bg,width=5)
            tbu.lower(bu)
            if flag==None:
                flag='flag'+str(titleu)
            if scrollbar:
                page=TinUI(self,True,bg=self['background'])
            elif scrollbar==False:
                page=BasicTinUI(self,bg=self['background'])
            uiid=self.create_window(viewpos,window=page,width=width,height=height,anchor='nw',state='hidden')
            uixml=TinUIXml(page)
            bbox=tbu.bbox('all')
            tbu.config(scrollregion=bbox)
            vdict[flag]=(page,uixml,uiid)
            tbdict[flag]=(titleu,cb,bu)
            flaglist.append(flag)
            tbu.tag_bind(titleu,'<Enter>',lambda event:__onenter(flag))
            tbu.tag_bind(cb,'<Enter>',lambda event:__onenter(flag))
            tbu.tag_bind(bu,'<Enter>',lambda event:__onenter(flag))
            tbu.tag_bind(titleu,'<Leave>',lambda event:__onleave(flag))
            tbu.tag_bind(cb,'<Leave>',lambda event:__onleave(flag))
            tbu.tag_bind(bu,'<Leave>',lambda event:__onleave(flag))
            tbu.tag_bind(titleu,'<Button-1>',lambda event:showpage(flag))
            tbu.tag_bind(bu,'<Button-1>',lambda event:showpage(flag))
            tbu.tag_bind(cb,'<Button-1>',lambda event:deletepage(flag))
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
            nonlocal nowpage
            wbbox=tbu.bbox(tbdict[flag][2])
            w=wbbox[2]-wbbox[0]
            w+=1
            for i in tbdict[flag]:
                tbu.delete(i)
            self.delete(vdict[flag][2])
            vdict[flag][0].destroy()
            index=flaglist.index(flag)
            if index+1==len(tbdict):
                pass
            else:
                for i in flaglist[index+1:]:
                    for iid in tbdict[i]:
                        tbu.move(iid,-w,0)
            if flag==nowpage:
                if len(tbdict)==1:
                    pass
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
            tbu.config(scrollregion=bbox)
        def getuis(flag):
            return vdict[flag]
        def gettitles(flag):
            return tbdict[flag]
        def getvdict():
            return vdict
        def gettbdict():
            return tbdict
        tbu=BasicTinUI(self,bg=color)
        tbuid=self.create_window((pos[0]+2,pos[1]+2),window=tbu,width=width,height=30,anchor='nw')
        uid='notebook'+str(tbuid)
        self.addtag_withtag(uid,tbuid)
        scro=self.add_scrollbar((pos[0]+5,pos[1]+32),tbu,height=width-5,direction='x',bg=bg,color=fg,oncolor=onfg)
        self.addtag_withtag(uid,scro[-1])
        barheight=self.bbox(scro[-1])[3]
        backpos=(pos[0]+5,pos[1]+3,pos[0]+width+2,pos[1]+3,pos[0]+width+2,barheight+height-3,pos[0]+5,barheight+height-3,pos[0]+5,pos[1]+5)
        back=self.create_polygon(backpos,outline=color,fill=color,width=10,tags=uid)
        self.tkraise(tbuid)
        self.tkraise(scro[-1])
        viewpos=(pos[0]+2,barheight+2)
        nowpage=''
        vdict=dict()#ui,uixml,uiid
        tbdict=dict()#title,cb,pyo
        flaglist=list()
        font='微软雅黑 12'
        notebook=TinUINum
        notebook.addpage=addpage
        notebook.showpage=showpage
        notebook.deletepage=deletepage
        notebook.getuis=getuis
        notebook.gettitles=gettitles
        notebook.getvdict=getvdict
        notebook.gettbdict=gettbdict
        return tbu,scro,back,notebook,uid



class TinUI(BasicTinUI):
    '''对BasicTinUI的封装，添加了滚动条自动刷新'''

    def __init__(self,master,update:bool=True,update_time:int=1000,**kw):
        self.frame = Frame(master)
        self.vbar = Scrollbar(self.frame)
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
        self.bind('<MouseWheel>',self.set_y_view)
        self.bind('<Configure>',lambda event:self.update__())
        self.update_time=update_time
        if update==False:
            self.unbind("<Configure>")

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
        else:
            self.after(self.update_time,self.update__)


class TinUIXml():#TinUI的xml渲染方式
    '''为TinUI提供更加方便的平面方式，使用xml
    TinUITheme基类无法直接使用，只能够重写TinUI或BasicTinUI的样式后才能够使用，参考 /theme 中的样式重写范例
    '''

    def __init__(self,ui:Union[BasicTinUI,TinUITheme]):
        self.ui=ui
        self.noload=('info','menubar','tooltip')#当前不解析的标签
        self.intargs=('width','linew','bd','r','minwidth','start','info_width','height','num')#需要转为数字的参数
        self.dataargs=('command','choices','widgets','content','percentage','data','cont','scrollbar','widget')#需要转为数据结构的参数
        self.funcs={}#内部调用方法集合
        self.datas={}#内部数据结构集合
        self.tags={}#内部组件tag集合

    def __attrib2kws(self,args:dict):#将部分特定参数转化为正确类型
        keys=args.keys()
        for ia in self.intargs:
            if ia in keys:
                args[ia]=int(args.get(ia))
        for da in self.dataargs:
            if da in keys:
                args[da]=eval(args.get(da))
        return args
    def __tags2uid(self,tag:str):#将self.tags中的内容转为画布uid
        name=self.tags[tag]
        if type(name)!=tuple or len(name)==1:
            uid=name
        else:
            uid=name[-1]
        return uid

    def __load_line(self,line,x=5,y=5):#根据xml的<line>逐行渲染TinUI组件
        lineatt=line.attrib
        last_y=y
        linex=None#纵块中的最大宽度
        if 'x' in lineatt.keys():
            xendx=int(line.get('x'))
        else:
            xendx=x
        if 'y' in lineatt.keys():
            xendy=int(line.get('y'))
        else:
            xendy=y
        for i in line.iterfind('*'):#只检索直接子元素
            if i.tag=='line':
                #linex=0
                liney,newlinex=self.__load_line(i,xendx,xendy)
                if liney>self.yendy-5:#在同一位置判断纵向大小
                    last_y=xendy=liney
                if linex==None:#判断是否是该纵块的第一个<line>
                    linex=0
                if newlinex>linex-5:
                    linex=newlinex+5
                continue
            if i.tag in self.noload:#不渲染的组件
                continue
            #特殊渲染的组件，有些仅对参数处理，有些需要特殊处理
            if i.tag=='back':#调整uids参数
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
            #调整内部参数=====
            xendy=y#从新获取本行其实纵坐标
            if linex!=None:#存在纵块
                xendx=linex
                linex=None
            i.attrib['pos']=(xendx,xendy)
            attrib=self.__attrib2kws(i.attrib)
            #==========
            tagall=eval(f'self.ui.add_{i.tag}(**attrib)')
            if type(tagall)!=tuple or len(tagall)==1:
                bboxtag=tagall
            else:
                bboxtag=tagall[-1]
            bbox=self.ui.bbox(bboxtag)
            xendx=bbox[2]+10
            if bbox[3]>last_y-5:#比较当前最低y坐标
                last_y=bbox[3]+5#获取下一行最高y坐标
            #为内部组件命名
            if i.text!=None:
                self.tags[i.text]=tagall
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

    def clean(self):#清空TinUI
        self.ui.delete('all')



def test(event):
    a.title('TinUI Test')
    b.add_paragraph((50,150),'这是TinUI按钮触达的事件函数回显，此外，窗口标题也被改变、首行标题缩进减小')
    b.coords(m,100,5)
def test1(word):
    print(word)
def test2(event):
    ok1()
def test3(event):
    ok2()
def test4(event):
    from time import sleep
    for i in range(1,101):
        sleep(0.02)
        progressgoto(i)
def test5(result):
    b.itemconfig(scale_text,text='当前选值：'+str(result))
def test6():
    for i in range(0,5):
        num=i
        xml=f'''
<tinui><line><label text='这是第{num}个BasicTinUI组件'></label></line>
<line><button text='功能按钮' command='lambda event:print("第{i}个功能按钮")'></button>
<combobox width='80' text='可选测试' content='("{i}","其它选项")'></combobox></line></tinui>'''
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

if __name__=='__main__':
    a=Tk()
    a.geometry('700x700+5+5')

    b=TinUI(a,bg='white')
    b.pack(fill='both',expand=True)
    m=b.add_title((600,0),'TinUI is a modern way to show tkinter widget in your application, as they are drawn by tkinter canvas')
    m1=b.add_title((0,680),'test TinUI scrolled',size=2,angle=24)
    b.add_paragraph((20,290),'''     TinUI是基于tkinter画布开发的界面UI布局方案，作为tkinter拓展和TinEngine的拓展而存在。目前，TinUI已可应用于项目。''',
    angle=-18)
    b.add_paragraph((20,100),'下面的段落是测试画布的非平行字体显示效果，也是TinUI的简单介绍')
    b.add_button((250,450),'测试按钮',activefg='white',activebg='red',command=test,anchor='center')
    b.add_checkbutton((60,430),'允许TinUI测试',command=test1)
    b.add_label((10,220),'这是由画布TinUI绘制的Label组件')
    b.add_entry((250,330),350,'这里用来输入',command=print)
    b.add_separate((20,200),600)
    b.add_radiobutton((50,480),300,'sky is blue, water is blue, too. So, what is your heart',('red','blue','black'),command=test1)
    b.add_link((400,500),'TinGroup知识库','http://tinhome.baklib-free.com/')
    b.add_link((400,530),'执行print函数',print)
    _,ok1,_=b.add_waitbar1((500,220),bg='#CCCCCC')
    b.add_button((500,270),'停止等待动画',activefg='cyan',activebg='black',command=test2)
    bu1=b.add_button((700,200),'停止点状滚动条',activefg='white',activebg='black',command=test3)[1]
    bu2=b.add_button((700,250),'nothing button 2')[1]
    bu3=b.add_button((700,300),'nothing button 3')[1]
    b.add_labelframe((bu1,bu2,bu3),'box buttons')
    _,_,ok2,_=b.add_waitbar2((600,400))
    b.add_combobox((600,550),text='你有多大可能去珠穆朗玛峰',content=('20%','40%','60%','80%','100%','1000%'))
    b.add_button((600,480),text='测试进度条（无事件版本）',command=test4)
    _,_,_,progressgoto,_,_=b.add_progressbar((600,510))
    b.add_table((180,630),data=(('a','space fans over the\nworld','c'),('you\ncan','2','3'),('I','II','have a dream, then try your best to get it!')))
    b.add_paragraph((300,850),text='上面是一个表格')
    b.add_onoff((600,100))
    b.add_spinbox((680,100))
    b.add_scalebar((680,50),command=test5)
    scale_text,_=b.add_label((890,50),text='当前选值：2')
    b.add_info((680,140),info_text='this is info widget in TinUI')
    mtb=b.add_paragraph((0,720),'测试菜单（右键单击）')
    b.add_menubar(mtb,cont=(('command',print),('menu',test1),'-',('TinUI文本移动',test)))
    ttb=b.add_paragraph((0,800),'TinUI能做些什么？')
    b.add_tooltip(ttb,'很多很多')
    b.add_back(pos=(0,0),uids=(ttb,),bg='cyan')
    _,_,ok3,_=b.add_waitbar3((600,800),width=240)
    b.add_button((600,750),text='停止带状等待框',command=lambda event:ok3())
    textbox=b.add_textbox((890,100),text='这是文本输入框，当然，无法在textbox的参数中绑定横向滚动'+'\n换行'*30)[0]
    textbox['wrap']='none'
    b.add_scrollbar((1095,100),textbox)
    b.add_scrollbar((890,305),textbox,direction='x')
    b.add_listbox((890,430),data=('item1','item2','item3','item4\n item4.1\n item4.2\n item4.3\n itme4.4\n item4.5','item5 and item5.1 and item5.2 and item5.3'),
    command=print)
    cav,cavf,_=b.add_canvas((890,670),scrollbar=True)
    for i in range(1,15):
        cav.create_text((5,i*40),text='画布对象：'+str(i)*i,font='微软雅黑 12',anchor='nw')
    cavf()
    uixml,add_ui_id=b.add_ui((150,890),scrollbar=True,region='auto')[-2:]
    uixml.loadxml('''<tinui><line>
    <button text='button in child tinui'></button>
    <label text='you can use BasicTinUI in a father TinUI&#x000A;by using&#x000A;tinui.add_uid(...)'></label>
    </line><line>
    <label text='you can use&#x000A;manual function re-region&#x000A;also can use&#x000A;auto function&#x000A;just one&#x000A;like&#x000A;this'>
    </label>
    </line></tinui>''')
    ppgl=b.add_pipspager((400,890),num=5)[0]
    test6()
    ntb=b.add_notebook((800,900))[-2]
    for i in range(1,11):
        ntb.addpage('test'+str(i),'t'+str(i))
    test7()
    a.mainloop()
