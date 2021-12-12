from tkinter import *
from webbrowser import open as webopen
import ctypes




class TinUINum:#数据载体，请忽略
    pass


class TinUI(Canvas):
    """基于tkinter的高级窗口绘制组件"""

    def __init__(self,master,update:bool=True,update_time:int=1000,**kw):
        self.frame = Frame(master)
        self.vbar = Scrollbar(self.frame)
        self.vbar.pack(side=RIGHT, fill=Y)
        ###
        kw.update({'yscrollcommand': self.vbar.set})
        Canvas.__init__(self, self.frame,selectborderwidth=0,highlightthickness=0,bd=0, **kw)
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
        self.init()
        self.update_time=update_time
        if update==False:
            self.unbind("<Configure>")

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

    def add_title(self,pos:tuple,text:str,fg='black',font='微软雅黑',size=1,anchor='nw',**kw):#绘制标题
        kw['anchor']=anchor
        return self.create_text(pos,text=text,fill=fg,font=(font,self.title_size[size]),**kw)

    def add_paragraph(self,pos:tuple,text:str,fg='black',font=('微软雅黑',12),side='left',width=500,anchor='nw',**kw):#绘制段落
        kw['anchor']=anchor
        return self.create_text(pos,text=text,fill=fg,font=font,justify=side,width=width,**kw)

    def add_button(self,pos:tuple,text:str,fg='#000000',bg='#CCCCCC',line='#CCCCCC',linew='3',activefg='black',activebg='#999999',activeline='#7a7a7a',font=('微软雅黑',12),command=None,anchor='nw'):#绘制按钮
        def in_button(event):
            self.itemconfig(back,fill=bg,outline=activeline)
            self.itemconfig(button,fill=activefg)
        def out_button(event):
            self.itemconfig(back,fill=bg,outline=line)
            self.itemconfig(button,fill=fg)
        def on_click(event):
            self.itemconfig(back,fill=activebg,outline=activeline)
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
        bbox=self.bbox(button)
        x1,y1,x2,y2=bbox[0]-3,bbox[1]-3,bbox[2]+3,bbox[3]+3
        back=self.create_rectangle((x1,y1,x2,y2),fill=bg,outline=line,width=linew)
        self.tag_bind(button,'<Button-1>',on_click)
        self.tag_bind(button,'<Enter>',in_button)
        self.tag_bind(button,'<Leave>',out_button)
        self.tag_bind(back,'<Button-1>',on_click)
        self.tag_bind(back,'<Enter>',in_button)
        self.tag_bind(back,'<Leave>',out_button)
        self.tkraise(button)
        funcs=[change_command,disable,active]
        return button,back,funcs

    def add_label(self,pos:tuple,text:str,fg='black',bg='#f0f0f0',outline='grey',font=('微软雅黑',12),anchor='nw'):#绘制标签
        label=self.create_text(pos,text=text,fill=fg,font=font,anchor=anchor)
        bbox=self.bbox(label)
        x1,y1,x2,y2=bbox[0]-3,bbox[1]-3,bbox[2]+3,bbox[3]+3
        back=self.create_rectangle((x1,y1,x2,y2),fill=bg,outline=outline)
        self.tkraise(label)
        return label

    def add_checkbutton(self,pos:tuple,text:str,fontfg='black',fg='#a6a6a6',bg='',onfg='white',onbg='#0067c0',font=('微软雅黑',12),command=None,anchor='nw'):#绘制复选框
        def button_in(event):
            self.itemconfig(check,outline='#82BDEB')
        def button_out(event):
            self.itemconfig(check,outline=fg)
        def go_func(event):
            if self.itemcget(check,'fill')==bg:
                self.itemconfig(check,fill=onbg,outline=onbg)
                self.itemconfig(state,state='normal')
            else:
                self.itemconfig(check,fill=bg,outline=fg)
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
        def active():
            self.itemconfig(checkbutton,state='normal',fill=fontfg)
            self.itemconfig(check,state='normal')
        checkbutton=self.create_text(pos,text=text,fill=fontfg,font=font,anchor=anchor)
        bbox=self.bbox(checkbutton)
        dic=bbox[3]-bbox[1]#位移长度
        self.move(checkbutton,dic-7,0)
        check=self.create_rectangle((pos[0]-2,pos[1]+4,pos[0]+dic-12,pos[1]+dic-4),outline=fg,fill=bg)
        state=self.create_text((pos[0]-2,pos[1]),text='√',fill=onfg,font=font,anchor='nw',state='hidden')
        self.tag_bind(check,'<Enter>',button_in)
        self.tag_bind(check,'<Leave>',button_out)
        self.tag_bind(checkbutton,'<Enter>',button_in)
        self.tag_bind(checkbutton,'<Leave>',button_out)
        self.tag_bind(check,'<Button>',go_func)
        self.tag_bind(checkbutton,'<Button>',go_func)
        funcs=[flash,on,off,disable,active]
        return checkbutton,check,funcs

    def add_entry(self,pos:tuple,width:int,text:str='',fg='black',bg='white',font=('微软雅黑',12),outline='#999999',onoutline='#4258cc',icon='>',anchor='nw'):#绘制单行输入框
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
        entry=Entry(self,fg=fg,bg=bg,font=font,relief='flat',highlightcolor=fg,bd=2)
        entry.insert(0,text)
        entry.bind('<KeyRelease>',if_empty)
        entry.bind('<FocusIn>',lambda event:self.itemconfig(back,outline=onoutline))
        entry.bind('<FocusOut>',lambda event:self.itemconfig(back,outline=outline))
        funce=self.create_window(pos,window=entry,width=width,anchor=anchor)#输入框画布对象
        funcw=self.create_text((pos[0]+width,pos[1]),text=icon,fill=fg,font=font,anchor='nw')
        w=self.bbox(funcw)[2]
        h=self.bbox(funce)[3]
        back=self.create_rectangle((pos[0]-2,pos[1]-2,w+2,h+2),outline=outline,fill=bg)
        self.tkraise(funcw)
        if_empty(None)
        return entry

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

    def add_radiobutton(self,pos:tuple,width,text='',choices=('choose me'),fg='black',bg='white',font=('微软雅黑',12),command=None,anchor='nw'):#绘制单选框
        def button_in(tag):
            self.itemconfig(tag,fill='#E5F1FB',outline='#82BDEB')
        def button_out(_tag):
            for tag in back_list:
                self.itemconfig(tag,fill=bg,outline=fg)
        def go_func(tag,_text):
            for i in choices_back:#判断是否为当前选中
                if i not in back_list:
                    back_list.append(i)
                    button_out(tag)
            back_list.remove(tag)
            self.itemconfig(tag,fill='#E5F1FB',outline='#82BDEB')
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
        start_x=pos[0]#起始x位置
        height=self.bbox(word)[3]+3#变量y位置
        choices_list=[]
        choices_back=[]
        for i in choices:
            choice=self.create_text((start_x+2,height+2),text=i,fill=fg,font=font,anchor=anchor,width=width-4)
            bbox=self.bbox(choice)
            h=bbox[3]-bbox[1]+4
            back=self.create_rectangle((start_x,height,start_x+width,height+h),outline=fg,fill=bg)
            self.tkraise(choice)
            height+=h+2
            choices_list.append(choice)
            choices_back.append(back)
            self.tag_bind(choice,'<Enter>',lambda event,back=back:button_in(back))
            self.tag_bind(choice,'<Leave>',lambda event,back=back:button_out(back))
            self.tag_bind(back,'<Enter>',lambda event,back=back:button_in(back))
            self.tag_bind(back,'<Leave>',lambda event,back=back:button_out(back))
            self.tag_bind(choice,'<Button>',lambda event,_text=i,back=back:go_func(back,_text))
            self.tag_bind(back,'<Button>',lambda event,_text=i,back=back:go_func(back,_text))
        back_list=list(choices_back)
        funcs=[select,disable,active]
        return word,choices_list,choices_back,funcs

    def add_link(self,pos:tuple,text,url,fg='#50B0F4',font:tuple=('微软雅黑',12),anchor='nw'):#绘制超链接
        def turn_red(event):
            self.itemconfig(link,fill='red')
            self['cursor']='hand2'
        def turn_back(event):
            self.itemconfig(link,fill=fg)
            self['cursor']='arrow'
        def go_url(event):
            webopen(url)
        link=self.create_text(pos,text=text,fill=fg,font=font,anchor=anchor)
        font=self.itemcget(link,'font')+' underline'
        self.itemconfig(link,font=font)
        bbox=self.bbox(link)
        back=self.create_rectangle(bbox,width=0)
        self.tkraise(link)
        self.tag_bind(link,'<Enter>',turn_red)
        self.tag_bind(link,'<Leave>',turn_back)
        self.tag_bind(link,'<Button-1>',go_url)
        self.tag_bind(back,'<Enter>',turn_red)
        self.tag_bind(back,'<Leave>',turn_back)
        self.tag_bind(back,'<Button-1>',go_url)
        return link

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
        waitbar1=self.create_arc(bbox,outline=fg,extent=5,start=90,width=bd,style='arc')
        start()
        return waitbar1,ok

    def add_labelframe(self,widgets:tuple=(),title='',fg='#A8A8A8',bg=''):#绘制标题框
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
        balls=[]
        ball_bbox=(pos[0],pos[1],pos[0]+5,pos[1]+5)
        for b in range(1,6):
            ball=self.create_oval(ball_bbox,fill=fg,outline=fg,state='hidden')
            balls.append(ball)
        start()
        return back,balls,stop

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
        bbox=self.bbox(main)
        x1,y1,x2,y2=bbox[0]-3,bbox[1]-3,bbox[0]+width+3,bbox[3]+3
        back=self.create_rectangle((x1,y1,x2,y2),fill=bg,outline=fg)
        self.tkraise(main)
        button_text,button_back,button_funcs=self.add_button((x2+3,y1+3),'∨',fg,bg,'#CCCCCC',1,activefg,activebg,'#7a7a7a',font=font,command=open_box)
        start_x=bbox[0]#起始x位置
        height=bbox[3]+3#变量y位置
        box_tagname='combobox>'+str(main)+'>'+str(back)#绑定独立的tag名称
        info=[]
        for i in content:
            choice=self.create_text((start_x+2,height+2),text=i,fill=fg,font=(font[0],10),anchor='nw',width=width-4)
            pos=self.bbox(choice)
            h=pos[3]-pos[1]+4
            cho_back=self.create_rectangle((start_x,height,start_x+width,height+h),outline=fg,fill=bg)
            self.tkraise(choice)
            height+=h+2
            self.tag_bind(choice,'<Enter>',lambda event,back=cho_back:button_in(back))
            self.tag_bind(choice,'<Leave>',lambda event,back=cho_back:button_out(back))
            self.tag_bind(cho_back,'<Enter>',lambda event,back=cho_back:button_in(back))
            self.tag_bind(cho_back,'<Leave>',lambda event,back=cho_back:button_out(back))
            self.tag_bind(choice,'<Button>',lambda event,_text=i,back=cho_back:choose_this(back,_text))
            self.tag_bind(cho_back,'<Button>',lambda event,_text=i,back=cho_back:choose_this(back,_text))
            info.append((back,i))
            self.addtag_withtag(box_tagname,choice)
            self.addtag_withtag(box_tagname,cho_back)
        self.itemconfig(box_tagname,state='hidden')
        funcs=[select,disable,active]
        return main,back,box_tagname,funcs

    def add_progressbar(self,pos:tuple,width=250,fg='#1E1E27',bg='#0078D7',percentage=True,text=''):#绘制进度条
        def goto(num:int):
            if not 0<=num<=100:
                return
            pw=width*num//100
            self.delete(pro_tagname)
            new_progressbar=self.create_rectangle((pos[0],pos[1],pos[0]+pw,pos[1]+15),fill=bg,outline=bg)
            self.tkraise(text)
            self.addtag_withtag(pro_tagname,new_progressbar)
            if percentage==True:
                self.itemconfig(text,text=str(num)+'%')
            self.update()
        bbox=(pos[0],pos[1],pos[0]+width,pos[1]+15)
        back=self.create_rectangle((bbox),outline=fg,fill='#CCCCCC')
        progressbar=self.create_rectangle((pos[0],pos[1],pos[0],pos[1]+15),outline=bg,fill=bg)
        pro_tagname='progressbar>'+str(back)
        self.addtag_withtag(progressbar,pro_tagname)
        #是否显示默认文本
        if percentage==True:
            text=self.create_text((pos[0]+width//2,pos[1]),anchor='n',text='0%',fill=fg,font='微软雅黑 10')
        else:
            text=self.create_text((pos[0]+width//2,pos[1]),anchor='n',text=text,fill=fg,font='微软雅黑 10')
        return back,pro_tagname,text,goto

    def add_table(self,pos:tuple,outline='#E1E1E1',fg='black',bg='white',data=[['1','2','3'],['a','b','c']],minwidth=100,font=('微软雅黑',12),headbg='#d9ebf9'):#绘制表格
        def get_max_height(widths:dict):
            height=0
            for i in widths.values():
                height=i[1] if i[1]>height else height
            #重新绘制
            for back in widths.keys():
                self.delete(widths[back][0])
                x1,y1,x2=widths[back][2]
                y2=y1+height
                newback=self.create_rectangle((x1,y1,x2,y2),outline=outline,fill=bg)
                self.tkraise(widths[back][3])
            return height
        title_num=len(data[0])#获取表头个数
        end_x,end_y=pos#起始位置
        height=0
        line_width={}#获取每列的固定宽度
        count=1
        for i in data[0]:
            title=self.create_text((end_x,end_y),anchor='nw',text=i,fill=fg,font=font)
            bbox=self.bbox(title)
            if bbox[2]-bbox[0]<=minwidth:
                width=minwidth
            else:
                width=bbox[2]-bbox[0]
            line_width[count]=width
            height=bbox[3]-bbox[1]
            self.create_rectangle((end_x,end_y,end_x+width,end_y+height),outline=outline,fill=headbg)
            end_x=end_x+width+2
            count+=1
            self.tkraise(title)
        end_y=pos[1]+height+2
        for line in data[1:]:
            count=1
            a_dict={}
            end_x=pos[0]
            height=0
            for a in line:
                width=line_width[count]
                cont=self.create_text((end_x,end_y),anchor='nw',text=a,fill=fg,width=width,font=font)
                bbox=self.bbox(cont)
                height=bbox[3]-bbox[1]
                back=self.create_rectangle((end_x,end_y,end_x+width,end_y+height),outline=outline,fill=bg)
                self.tkraise(cont)
                a_dict[count]=(back,height,(end_x,end_y,end_x+width),cont)#(end_x,end_y,width)为重新绘制确定位置范围
                end_x=end_x+width+2
                count+=1
            height=get_max_height(a_dict)
            end_y=end_y+height+2
        return None

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
        bbox=self.bbox(state)
        d=int(bbox[3]-bbox[1])#获得绘制半径
        width=bbox[2]-bbox[0]#获取绘制宽度
        self.move(state,d,0)
        back=self.create_polygon((pos[0]+d,pos[1],pos[0],pos[1]+d/2,pos[0]+d,pos[1]+d,pos[0]+d+width,pos[1]+d,pos[0]+d*2+width,pos[1]+d/2,
        pos[0]+d+width,pos[1],pos[0]+d,pos[1]),fill=bg,outline=fg,width=2,joinstyle='miter')
        self.tkraise(state)
        self.tag_bind(state,'<Button-1>',__on_click)
        self.tag_bind(back,'<Button-1>',__on_click)
        return state,back

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
        bbox=self.bbox(entry)
        height=bbox[3]-bbox[1]
        font=(font[0],font[1]//3)
        button1=self.add_button((pos[0]+width+2,pos[1]+3),text='▲',linew=1,activefg=activefg,activebg=activebg,font=font,command=updata)
        button2=self.add_button((pos[0]+width+2,pos[1]-5+height),text='▼',linew=1,activefg=activefg,activebg=activebg,font=font,anchor='sw',command=downdata)
        datanum=TinUINum()
        datanum.num=data.index(now)#记录数据位置
        maxnum=len(data)-1#最大位置
        return wentry,button1,button2

    def add_scalebar(self,pos:tuple,width=200,fg='#4258cc',activefg='#aeb5d7',bg='#99a3d5',data=(1,2,3,4,5),start=1,command=None):#绘制调节框
        def mousedown(event):
            scale.startx=self.canvasx(event.x)
        def drag(event):
            move=self.canvasx(event.x)-scale.startx
            if self.canvasx(event.x)<pos[0] or self.canvasx(event.x)>pos[0]+width:
                return
            self.move(button,move,0)
            self.delete(name)
            active=self.create_line((pos[0],pos[1],move+scale.startx,pos[1]),fill=fg,width=3,tags=name)
            scale.startx=self.canvasx(event.x)
        def check(event):
            end=int(self.canvasx(event.x))
            if end<pos[0]:end=pos[0]
            if end>pos[0]+width:end=pos[0]+width
            rend=min(dash,key=lambda x:abs(x-end))
            num=dash.index(rend)
            if command!=None:
                command(data[num])
        def checkval(event):
            move=self.canvasx(event.x)
            self.coords(button,move,pos[1]-15,move+10,pos[1]+17)
            self.coords(name,pos[0],pos[1],move,pos[1])
            check(event)
        def select(num):
            self.coords(button,dash[num],pos[1]-15,dash[num]+10,pos[1]+17)
            self.coords(name,pos[0],pos[1],dash[num],pos[1])
        def disable():
            self.itemconfig(button,state='disable',fill='#7a7a7a')
            self.itemconfig(back,state='disable')
            self.itemconfig(name,state='disable',fill='#7a7a7a')
        def _active():
            self.itemconfig(button,state='normal',fill=fg)
            self.itemconfig(back,state='normal')
            self.itemconfig(name,state='normal',fill=fg)
        scale=TinUINum()#记录数据结构体
        back=self.create_line((pos[0],pos[1],pos[0]+width,pos[1]),fill=bg,width=3)
        self.tag_bind(back,'<ButtonRelease-1>',checkval)
        dash_t=width//(len(data)-1)
        s=pos[0]#调节线段起点
        dash=[s]#调节线段的终点位置
        for i in data[1:]:
            s+=dash_t
            dash.append(s)
        del s
        active=self.create_line((pos[0],pos[1],dash[start],pos[1]),fill=fg,width=3)
        name='scaleactive'+str(active)
        self.tag_bind(name,'<ButtonRelease-1>',checkval)
        self.addtag_withtag(name,active)#为重绘绑定tag名称
        button=self.create_rectangle((dash[start],pos[1]-15,dash[start]+10,pos[1]+17),width=0,fill=fg)
        self.tag_bind(button,'<Enter>',lambda event:self.itemconfig(button,fill=activefg))
        self.tag_bind(button,'<Leave>',lambda event:self.itemconfig(button,fill=fg))
        self.tag_bind(button,'<Button-1>',mousedown)
        self.tag_bind(button,'<B1-Motion>',drag)
        self.tag_bind(button,'<ButtonRelease-1>',check)#矫正位置
        funcs=[select,disable,_active]
        return name,back,button,funcs

    def add_info(self,pos:tuple,font='微软雅黑 9',fg='#0078d4',bg='white',info_text='',info_font=('微软雅黑','12'),info_width=200,info_fg='black'):#绘制提示框
        def showinfo(event):
            self.itemconfig(infotagname,state='normal')
        def hideinfo(event):
            self.itemconfig(infotagname,state='hidden')
        text=self.create_text(pos,anchor='nw',text='?',font=font,fill=fg)
        bbox=self.bbox(text)
        back=self.create_oval((bbox[0]-2,bbox[1]-2,bbox[2]+2,bbox[3]+2),fill=bg,outline=fg,width=2)
        self.tkraise(text)
        self.tag_bind(back,'<Enter>',showinfo)
        self.tag_bind(back,'<Leave>',hideinfo)
        self.tag_bind(text,'<Enter>',showinfo)
        self.tag_bind(text,'<Leave>',hideinfo)
        info=self.create_text((bbox[2]+10,(bbox[3]+bbox[1])//2),anchor='nw',text=info_text,font=info_font,fill=info_fg,width=info_width)
        ibbox=self.bbox(info)
        info_back=self.create_rectangle((ibbox[0]-2,ibbox[1]-2,ibbox[2]+2,ibbox[3]+2),width=1,fill=bg,outline=fg)
        self.tkraise(info)
        infotagname='info'+str(info)+str(info_back)
        self.addtag_withtag(infotagname,info)
        self.addtag_withtag(infotagname,info_back)
        self.itemconfig(infotagname,state='hidden')
        return text,back,infotagname

    def add_menubar(self,cid='all',bind='<Button-3>',font='微软雅黑 12',fg='#ecf3e8',bg='#2b2a33',activefg='#ecf3e8',activebg='#616161',cont=(('command',print),'-'),tran='white'):#绘制菜单
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
            menu.geometry(f'{winw+5}x{winh+5}+{x}+{y}')
            menu.deiconify()
            menu.focus_set()
        self.tag_bind(cid,bind,show)
        menu=Toplevel(self)
        menu.overrideredirect(True)
        menu.withdraw()
        bar=TinUI(menu,bg=tran)
        bar.pack(fill='both',expand=True)
        wind=TinUINum()#记录数据
        backs=[]#按钮
        funcs=[]#按钮函数接口
        seps=[]#分割线
        widths=[]#寻找最宽位置
        for i in cont:#添加菜单内容
            if i=='-':
                sep=bar.add_separate((5,endy()),100,fg=activebg)
                seps.append(sep)
            else:
                button=bar.add_button((5,endy()),i[0],fg,bg,bg,3,activefg,activebg,activebg,font,command=lambda event,i=i:(i[1](event),menu.withdraw()))
                backs.append(button[1])
                funcs.append(button[2])
                pos=bar.bbox(button[1])
                width=pos[2]-pos[0]
                widths.append(width)
        repaint()
        readyshow()
        #绘制圆角边框
        bbox=bar.bbox('all')
        start=bbox[2]-bbox[0]
        gomap=((start,bbox[1]),(bbox[2],bbox[1]),(bbox[2],bbox[3]),(bbox[0],bbox[3]),(bbox[0],bbox[1]),(start,bbox[1]))
        mback=bar.create_polygon(gomap,fill=bg,outline=bg,width=5)
        bar.lower(mback)
        menu.bind('<FocusOut>',lambda event:menu.withdraw())
        menu.attributes('-transparent',tran)
        return menu,bar,funcs



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

if __name__=='__main__':
    a=Tk()
    a.geometry('700x700+5+5')

    b=TinUI(a,bg='white')
    b.pack(fill='both',expand=True)
    m=b.add_title((600,0),'TinUI is a test project for futher tin using')
    m1=b.add_title((0,680),'test TinUI scrolled',size=2,angle=24)
    b.add_paragraph((20,290),'''     TinUI是基于tkinter画布开发的界面UI布局方案，作为tkinter拓展和TinEngine的拓展而存在。目前，TinUI尚处于开发阶段。如果想要使用完整的TinUI，敬请期待。''',
    angle=-18)
    b.add_paragraph((20,100),'下面的段落是测试画布的非平行字体显示效果，也是TinUI的简单介绍')
    b.add_button((250,450),'测试按钮',activefg='white',activebg='red',command=test,anchor='center')
    b.add_checkbutton((80,430),'允许TinUI测试',command=test1)
    b.add_label((10,220),'这是由画布TinUI绘制的Label组件')
    b.add_entry((250,300),350,'这里用来输入')
    b.add_separate((20,200),600)
    b.add_radiobutton((50,480),300,'sky is blue, water is blue, too. So, what is your heart',('red','blue','black'),command=test1)
    b.add_link((400,500),'TinGroup知识库','http://tinhome.baklib-free.com/')
    _,ok1=b.add_waitbar1((500,220),bg='#CCCCCC')
    b.add_button((500,270),'停止等待动画',activefg='cyan',activebg='black',command=test2)
    bu1=b.add_button((700,200),'停止点状滚动条',activefg='white',activebg='black',command=test3)[1]
    bu2=b.add_button((700,250),'nothing button 2')[1]
    bu3=b.add_button((700,300),'nothing button 3')[1]
    b.add_labelframe((bu1,bu2,bu3),'box buttons')
    _,_,ok2=b.add_waitbar2((600,400))
    b.add_combobox((600,550),text='你有多大可能去珠穆朗玛峰',content=('20%','40%','60%','80%','100%','1000%'))
    b.add_button((600,480),text='测试进度条（无事件版本）',command=test4)
    _,_,_,progressgoto=b.add_progressbar((600,510))
    b.add_table((180,630),data=(('a','space fans over the world','c'),('you\ncan','2','3'),('I','II','have a dream, then try your best to get it!')))
    b.add_paragraph((300,810),text='上面是一个表格')
    b.add_onoff((600,100))
    b.add_spinbox((680,100))
    b.add_scalebar((680,50),command=test5)
    scale_text=b.add_label((890,50),text='当前选值：2')
    b.add_info((680,140),info_text='this is info widget in TinUI')
    mtb=b.add_paragraph((0,720),'测试菜单（右键单击）')
    b.add_menubar(mtb,cont=(('command',print),('menu',test1),'-',('TinUI文本移动',test)))

    a.mainloop()
