"""
TinUI风格对话框
"""
from tkinter import Tk, Toplevel

try:
    from .TinUI import BasicTinUI, TinUIXml
except:
    from TinUI import BasicTinUI, TinUIXml



class Dialog(Toplevel):
    """
    TinUI对话框基础类
    """

    def __init__(self,master,dialogtype='normal',theme='light',**options):
        """
        theme: 'dark' or 'light'
        """
        super().__init__(master,**options)
        self.withdraw()

        if master:
            self.transient(self.master)
        
        self.tinui=BasicTinUI(self)
        self.tinui.pack(fill='both',expand=True)

        self.type=dialogtype#对话框类型

        if theme=='light':
            self.background = '#f3f3f3'
            self.fg = '#000000'
            self.barback = '#f3f3f3'
            self.selback = '#1a1a1a'
            self.buttonargs = {
                'fg':'#1b1b1b',
                'bg':'#fbfbfb',
                'line':'#cccccc',
                'activefg':'#1a1a1a',
                'activebg':'#f6f6f6',
                'activeline':'#cccccc',
                'onfg':'#5d5d5d',
                'onbg':'#f5f5f5',
                'online':'#e5e5e5'
            }
            self.entryargs = {
                'fg':'#606060',
                'bg':'#fbfbfb',
                'activefg':'#1a1a1a',
                'activebg':'#f6f6f6',
                'onfg':'#000000',
                'onbg':'#ffffff',
                'line':'#e5e5e5',
                'activeline':'#e5e5e5',
                'insert':'#000000',
                'outline':'#868686',
                'onoutline':'#3041d8',
            }
            self.listargs = {
                'fg':'#1a1a1a',
                'bg':'#f2f2f2',
                'activefg':'#191919',
                'activebg':'#e9e9e9',
                'onfg':'#191919',
                'onbg':'#ececec',
                'sel':'#b4bbea',
                'scrollbg':'#f9f9f9',
                'scrollcolor':'#8d8d8d',
                'scrollon':'#8a8a8a'
            }
            self.infocolor = '#5969e0'
            self.infoback = '#ffffff'
            self.successcolor = '#0f7b0f'
            self.successback = '#dff6dd'
            self.warningcolor = '#9d5d00'
            self.warningback = '#fff4ce'
            self.errorcolor = '#c42b1c'
            self.errorback = '#fde7e9'
            self.questioncolor = '#5969e0'
            self.questionback = '#ffffff'
        elif theme=='dark':
            self.background = '#202020'
            self.fg = '#ffffff'
            self.barback = '#202020'
            self.selback = '#ffffff'
            self.buttonargs = {
                'fg':'#ffffff',
                'bg':'#2d2d2d',
                'line':'#303030',
                'activefg':'#ffffff',
                'activebg':'#323232',
                'activeline':'#202020',
                'onfg':'#cecece',
                'onbg':'#272727',
                'online':'#303030'
            }
            self.entryargs = {
                'fg':'#cfcfcf',
                'bg':'#2d2d2d',
                'activefg':'#ffffff',
                'activebg':'#323232',
                'onfg':'#ffffff',
                'onbg':'#1f1f1f',
                'line':'#303030',
                'activeline':'#202020',
                'outline':'#9a9a9a',
                'onoutline':'#b2b8f2',
                'insert':'#e0e0e0',
            }
            self.listargs = {
                'bg':'#2d2d2d',
                'fg':'#ffffff',
                'activefg':'#ffffff',
                'activebg':'#373737',
                'onfg':'#ffffff',
                'onbg':'#333333',
                'sel':'#465097',
                'scrollbg':'#2e2e2e',
                'scrollcolor':'#9f9f9f',
                'scrollon':'#a0a0a0'
            }
            self.infocolor = '#4cc2ff'
            self.infoback = '#2c2c2c'
            self.successcolor = '#6ccb5f'
            self.successback = '#393d1b'
            self.warningcolor = '#fce100'
            self.warningback = '#433519'
            self.errorcolor = '#ff99a4'
            self.errorback = '#442726'
            self.questioncolor = '#4cc2ff'
            self.questionback = '#2c2c2c'

        self.resizable(False,False)
        self.tk.call('wm', 'iconbitmap', self._w, '-default', '')
    
    def _endy(self):
        #最低位置
        bbox=self.tinui.bbox('all')
        if bbox:
            return bbox[3]
        else:
            return 0
    
    def initial_msg(self,title,content,yestext='OK',notext='Cancel'):
        """
        初始化对话框-消息类
        """
        YES=yestext
        NO=notext

        self.title(title)
        self.protocol('WM_DELETE_WINDOW',lambda:self.return_msg(None))
        
        # contenty=5
        if self.type=='normal':
            self.tinui['bg']=self.background
        elif self.type=='info':
            self.tinui['bg']=self.infoback
            icon_uid=self.tinui.add_paragraph((5,5),text='\uE946',fg=self.infocolor,font='{Segoe Fluent Icons} 14',anchor='w')
            self.tinui.addtag_withtag('content',icon_uid)
        elif self.type=='success':
            self.tinui['bg']=self.successback
            icon_uid=self.tinui.add_paragraph((5,5),text='\uE73E',fg=self.successcolor,font='{Segoe Fluent Icons} 14',anchor='w')
            self.tinui.addtag_withtag('content',icon_uid)
        elif self.type=='warning':
            self.tinui['bg']=self.warningback
            icon_uid=self.tinui.add_paragraph((5,5),text='\uE7BA',fg=self.warningcolor,font='{Segoe Fluent Icons} 14',anchor='w')
            self.tinui.addtag_withtag('content',icon_uid)
        elif self.type=='error':
            self.tinui['bg']=self.errorback
            icon_uid=self.tinui.add_paragraph((5,5),text='\uEA39',fg=self.errorcolor,font='{Segoe Fluent Icons} 14',anchor='w')
            self.tinui.addtag_withtag('content',icon_uid)
        elif self.type=='question':
            self.tinui['bg']=self.questionback
            icon_uid1=self.tinui.add_paragraph((5,5),text='\uEA3A',fg=self.questioncolor,font='{Segoe Fluent Icons} 14',anchor='w')
            icon_uid2=self.tinui.add_paragraph((5,5),text='\uF142',fg=self.questioncolor,font='{Segoe Fluent Icons} 14',anchor='w')
            self.tinui.addtag_withtag('content',icon_uid1)
            self.tinui.addtag_withtag('content',icon_uid2)

        content_uid=self.tinui.add_paragraph((35,5),text=content,fg=self.fg,anchor='w')
        self.tinui.addtag_withtag('content',content_uid)
        content_bbox=self.tinui.bbox('content')
        btn_width=(content_bbox[2]-content_bbox[0])/2
        button_width=btn_width-10 if btn_width>110 else 100
        button_endy=self._endy()+15
        yesbutton_uid=self.tinui.add_button2(((content_bbox[0]+content_bbox[2])/2-5,button_endy),text=YES,minwidth=button_width,command=lambda e:self.return_msg(True),anchor='ne',**self.buttonargs)[-1]
        yb_coords = self.tinui.coords(yesbutton_uid)
        nobutton_uid=self.tinui.add_button2(((content_bbox[0]+content_bbox[2])/2+5,button_endy),text=NO,minwidth=button_width,command=lambda e:self.return_msg(False),anchor='nw',**self.buttonargs)[-1]
        nb_coords = self.tinui.coords(nobutton_uid)
        self.tinui.add_back((),(yesbutton_uid,nobutton_uid),bg=self.barback,fg=self.barback,linew=9)

        def return_focus(event):
            if now_focus == 'yes':
                self.return_msg(True)
            else:
                self.return_msg(False)
        def focus_left(event):
            nonlocal now_focus
            if now_focus == 'yes':
                return
            now_focus = 'yes'
            self.tinui.coords(focus_button, yb_coords)
        def focus_right(event):
            nonlocal now_focus
            if now_focus == 'no':
                return
            now_focus = 'no'
            self.tinui.coords(focus_button, nb_coords)

        focus_button = self.tinui.create_polygon(yb_coords, width=11, fill=self.barback, outline=self.selback)
        self.tinui.lower(focus_button, yesbutton_uid)
        now_focus = 'yes'
        self.bind('<Return>', return_focus)
        self.bind('<space>', return_focus)
        self.bind('<Left>', focus_left)
        self.bind('<Right>', focus_right)

        self.entryw = None
        return self.load_window()
    
    def return_msg(self,val):
        #返回消息
        self.result=val
        self.destroy()
        self.master.focus_set()
    
    def initial_xml_load(self,title,xml,funcdict:dict=None,data:dict=None,yestext='OK',notext='Cancel'):
        """
        自定义XML内容
        """
        YES=yestext
        NO=notext

        self.tinuixml = TinUIXml(self.tinui)
        self.tinuixml.funcs.update(funcdict)
        self.tinuixml.datas.update(data)

        self.title(title)
        self.protocol('WM_DELETE_WINDOW',lambda:self.return_msg(None))

        self.tinui['bg'] = self.background
        self.tinuixml.loadxml(xml)

        content_bbox=self.tinui.bbox('all')
        btn_width=(content_bbox[2]-content_bbox[0])/2
        button_width=btn_width-10 if btn_width>110 else 100
        button_endy=self._endy()+15
        yesbutton_uid=self.tinui.add_button2(((content_bbox[0]+content_bbox[2])/2-5,button_endy),text=YES,minwidth=button_width,command=lambda e:self.return_msg(True),anchor='ne',**self.buttonargs)[-1]
        yb_coords = self.tinui.coords(yesbutton_uid)
        nobutton_uid=self.tinui.add_button2(((content_bbox[0]+content_bbox[2])/2+5,button_endy),text=NO,minwidth=button_width,command=lambda e:self.return_msg(False),anchor='nw',**self.buttonargs)[-1]
        nb_coords = self.tinui.coords(nobutton_uid)
        self.tinui.add_back((),(yesbutton_uid,nobutton_uid),bg=self.barback,fg=self.barback,linew=9)

        def return_focus(event):
            if now_focus == 'yes':
                self.return_msg(True)
            else:
                self.return_msg(False)
        def focus_left(event):
            nonlocal now_focus
            if now_focus == 'yes':
                return
            now_focus = 'yes'
            self.tinui.coords(focus_button, yb_coords)
        def focus_right(event):
            nonlocal now_focus
            if now_focus == 'no':
                return
            now_focus = 'no'
            self.tinui.coords(focus_button, nb_coords)

        focus_button = self.tinui.create_polygon(yb_coords, width=11, fill=self.barback, outline=self.selback)
        self.tinui.lower(focus_button, yesbutton_uid)
        now_focus = 'yes'
        self.bind('<Return>', return_focus)
        self.bind('<space>', return_focus)
        self.bind('<Left>', focus_left)
        self.bind('<Right>', focus_right)

        self.entryw = None

    def initial_xml_init(self):
        return self.load_window()

    def initial_input(self,title,content,text,yestext='OK',notext='Cancel'):
        """
        初始化对话框-输入类
        """
        YES=yestext
        NO=notext

        self.tinui['bg']=self.background
        
        self.title(title)
        self.protocol('WM_DELETE_WINDOW',lambda:self.return_input(None))
        
        self.tinui.add_paragraph((5,5),text=content,fg=self.fg)
        content_bbox=self.tinui.bbox('all')
        entry_width=content_bbox[2]-content_bbox[0]
        width=entry_width if entry_width>200 else 200
        self.entryw, self.entry=self.tinui.add_entry((5,self._endy()+5),width=width,**self.entryargs)[:-1]# tinui entry widget, funcs
        self.entry.insert(0,str(text))
        bbox=self.tinui.bbox('all')
        btn_width=(bbox[2]-bbox[0])/2
        button_width=btn_width-10 if btn_width>110 else 100
        button_endy=self._endy()+15
        yesbutton_uid=self.tinui.add_button2(((bbox[0]+bbox[2])/2-5,button_endy),text=YES,minwidth=button_width,command=lambda e:self.return_input(self.entry.get()),anchor='ne',**self.buttonargs)[-1]
        yb_coords = self.tinui.coords(yesbutton_uid)
        nobutton_uid=self.tinui.add_button2(((bbox[0]+bbox[2])/2+5,button_endy),text=NO,minwidth=button_width,command=lambda e:self.return_input(None),anchor='nw',**self.buttonargs)[-1]
        self.tinui.add_back((),(yesbutton_uid,nobutton_uid),bg=self.barback,fg=self.barback,linew=9)

        focus_button = self.tinui.create_polygon(yb_coords, width=11, fill=self.barback, outline=self.selback)
        self.tinui.lower(focus_button, yesbutton_uid)
        self.bind('<Return>', lambda e:self.return_input(self.entry.get()))

        return self.load_window()

    def return_input(self,val):
        #返回输入内容
        self.result=val
        if self.result==None:
            pass
        elif self.type=='string':
            pass
        elif self.type=='integer':
            try:
                self.result=int(self.result)
            except:
                return
        elif self.type=='float':
            try:
                self.result=float(self.result)
            except:
                return
        self.destroy()
        self.master.focus_set()
    
    def initial_choice(self,title,content,choices,yestext='OK',notext='Cancel'):
        """
        初始化对话框-选择类
        """
        YES=yestext
        NO=notext
        self.result=None

        self.tinui['bg']=self.background

        self.title(title)
        self.protocol('WM_DELETE_WINDOW',lambda:self.return_choice(None))

        self.tinui.add_paragraph((5,5),text=content,fg=self.fg)
        content_bbox=self.tinui.bbox('all')
        width = max(content_bbox[2]-content_bbox[0], 300)

        if self.type=='listbox':
            self.tinui.add_listbox((5,self._endy()+5),width=width,height=300,data=choices,command=self.return_choice,**self.listargs)

        bbox=self.tinui.bbox('all')
        btn_width=(bbox[2]-bbox[0])/2
        button_width=btn_width-10 if btn_width>110 else 100
        button_endy=self._endy()+15
        yesbutton_uid=self.tinui.add_button2(((bbox[0]+bbox[2])/2-5,button_endy),text=YES,minwidth=button_width,command=lambda e:self.return_choice(True),anchor='ne',**self.buttonargs)[-1]
        yb_coords = self.tinui.coords(yesbutton_uid)
        nobutton_uid=self.tinui.add_button2(((bbox[0]+bbox[2])/2+5,button_endy),text=NO,minwidth=button_width,command=lambda e:self.return_choice(None),anchor='nw',**self.buttonargs)[-1]
        nb_coords = self.tinui.coords(nobutton_uid)
        self.tinui.add_back((),(yesbutton_uid,nobutton_uid),bg=self.background,fg=self.background,linew=9)

        def return_focus(event):
            if now_focus == 'yes':
                self.return_choice(True)
            else:
                self.return_choice(None)
        def focus_left(event):
            nonlocal now_focus
            if now_focus == 'yes':
                return
            now_focus = 'yes'
            self.tinui.coords(focus_button, yb_coords)
        def focus_right(event):
            nonlocal now_focus
            if now_focus == 'no':
                return
            now_focus = 'no'
            self.tinui.coords(focus_button, nb_coords)

        focus_button = self.tinui.create_polygon(yb_coords, width=11, fill=self.barback, outline=self.selback)
        self.tinui.lower(focus_button, yesbutton_uid)
        now_focus = 'yes'
        self.bind('<Return>', return_focus)
        self.bind('<space>', return_focus)
        self.bind('<Left>', focus_left)
        self.bind('<Right>', focus_right)

        self.entryw = None
        return self.load_window()
    
    def return_choice(self,val):
        #返回选择内容
        if val==True:#YES
            if self.result==None:
                return
            self.destroy()
            self.master.focus_set()
        elif val==None:#NO
            self.result=None
            self.destroy()
            self.master.focus_set()
        else:#输入值
            self.result=val

    def load_window(self):
        #获取窗口内所有控件的bbox，窗口居中布局
        bboxall=self.tinui.bbox('all')
        w,h=bboxall[2]-bboxall[0],bboxall[3]-bboxall[1]+1
        screenw=self.winfo_screenwidth()
        screenh=self.winfo_screenheight()
        x,y=(screenw-w)/2,(screenh-h)/2
        self.geometry(f'{w}x{h}+{int(x)}+{int(y)-10}')
        self.deiconify()

        self.tinui.config(scrollregion=bboxall)

        self.focus_set()
        if self.entryw:
            self.entryw.focus_set()
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

        return self.result



def show_msg(master,title,content,theme='light'):
    """
    显示消息对话框
    """
    dialog=Dialog(master,'normal',theme)
    return dialog.initial_msg(title,content)

def show_info(master,title,content,yestext='OK',notext='Cancel',theme='light'):
    """
    显示信息对话框
    """
    dialog=Dialog(master,'info',theme)
    return dialog.initial_msg(title,content,yestext,notext)
def show_success(master,title,content,yestext='OK',notext='Cancel',theme='light'):
    """
    显示成功对话框
    """
    dialog=Dialog(master,'success',theme)
    return dialog.initial_msg(title,content,yestext,notext)

def show_warning(master,title,content,yestext='OK',notext='Cancel',theme='light'):
    """
    显示警告对话框
    """
    dialog=Dialog(master,'warning',theme)
    return dialog.initial_msg(title,content,yestext,notext)

def show_error(master,title,content,yestext='OK',notext='Cancel',theme='light'):
    """
    显示错误对话框
    """
    dialog=Dialog(master,'error',theme)
    return dialog.initial_msg(title,content,yestext,notext)

def show_question(master,title,content,yestext='YES',notext='NO',theme='light'):
    """
    显示询问对话框
    """
    dialog=Dialog(master,'question',theme)
    return dialog.initial_msg(title,content,yestext,notext)


def ask_string(master,title,content,text:str="",yestext='OK',notext='Cancel',theme='light'):
    """
    输入字符串对话框
    """
    dialog=Dialog(master,'string',theme)
    return dialog.initial_input(title,content,text,yestext,notext)

def ask_integer(master,title,content,text:int=0,yestext='OK',notext='Cancel',theme='light'):
    """
    输入整数对话框
    """
    dialog=Dialog(master,'integer',theme)
    return dialog.initial_input(title,content,text,yestext,notext)

def ask_float(master,title,content,text:float="0.0",yestext='OK',notext='Cancel',theme='light'):
    """
    输入浮点数对话框
    """
    dialog=Dialog(master,'float',theme)
    return dialog.initial_input(title,content,text,yestext,notext)

def ask_choice(master,title,content,choices,yestext='OK',notext='Cancel',theme='light'):
    """
    选择列表对话框
    """
    dialog=Dialog(master,'listbox',theme)
    return dialog.initial_choice(title,content,choices,yestext,notext)



if __name__=='__main__':
    root=Tk()
    root.iconbitmap('LOGO.ico')
    a=show_msg(root,'test','hello world!',theme='dark')
    print(a)
    show_info(root,'test','show information\nhello world!',theme='dark')
    show_success(root,'test','Success!\nhello world! hello world! hello world! hello world!',theme='dark')
    show_warning(root,'test','this is a warning\nhello world!',theme='dark')
    show_error(root,'test','something is wrong\nhello world! hello world! hello world! hello world!')
    show_question(root,'test','Do you want to continue?')
    b=ask_string(root,'test','input something input something input something input something')
    print(b)
    ask_integer(root,'test','input integer')
    ask_float(root,'test','input float')
    c=ask_choice(root,'test','choose one',('a','b','c'),theme='dark')
    print(c)
    root.mainloop()