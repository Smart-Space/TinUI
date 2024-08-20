"""
TinUI风格对话框
"""
from tkinter import Tk, Toplevel

try:
    from .TinUI import BasicTinUI
except:
    from TinUI import BasicTinUI



class Dialog(Toplevel):
    """
    TinUI对话框基础类
    """

    def __init__(self,master,dialogtype='normal',**options):
        super().__init__(master,**options)
        self.withdraw()
        
        self.tinui=BasicTinUI(self)
        self.tinui.pack(fill='both',expand=True)

        self.type=dialogtype#对话框类型

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
            pass
        elif self.type=='info':
            self.tinui['bg']='#ffffff'
            icon_uid=self.tinui.add_paragraph((5,5),text='\uE946',fg='#5969e0',font='{Segoe Fluent Icons} 14',anchor='w')
            self.tinui.addtag_withtag('content',icon_uid)
        elif self.type=='success':
            self.tinui['bg']='#dff6dd'
            icon_uid=self.tinui.add_paragraph((5,5),text='\uE73E',fg='#0f7b0f',font='{Segoe Fluent Icons} 14',anchor='w')
            self.tinui.addtag_withtag('content',icon_uid)
        elif self.type=='warning':
            self.tinui['bg']='#fff4ce'
            icon_uid=self.tinui.add_paragraph((5,5),text='\uE7BA',fg='#9d5d00',font='{Segoe Fluent Icons} 14',anchor='w')
            self.tinui.addtag_withtag('content',icon_uid)
        elif self.type=='error':
            self.tinui['bg']='#fde7e9'
            icon_uid=self.tinui.add_paragraph((5,5),text='\uEA39',fg='#c42b1c',font='{Segoe Fluent Icons} 14',anchor='w')
            self.tinui.addtag_withtag('content',icon_uid)
        elif self.type=='question':
            self.tinui['bg']='#ffffff'
            icon_uid1=self.tinui.add_paragraph((5,5),text='\uEA3A',fg='#5969e0',font='{Segoe Fluent Icons} 14',anchor='w')
            icon_uid2=self.tinui.add_paragraph((5,5),text='\uF142',fg='#5969e0',font='{Segoe Fluent Icons} 14',anchor='w')
            self.tinui.addtag_withtag('content',icon_uid1)
            self.tinui.addtag_withtag('content',icon_uid2)

        content_uid=self.tinui.add_paragraph((35,5),text=content,anchor='w')
        self.tinui.addtag_withtag('content',content_uid)
        content_bbox=self.tinui.bbox('content')
        btn_width=(content_bbox[2]-content_bbox[0])/2
        button_width=btn_width-10 if btn_width>110 else 100
        button_endy=self._endy()+15
        yesbutton_uid=self.tinui.add_button2(((content_bbox[0]+content_bbox[2])/2-5,button_endy),text=YES,minwidth=button_width,command=lambda e:self.return_msg(True),anchor='ne')[-1]
        nobutton_uid=self.tinui.add_button2(((content_bbox[0]+content_bbox[2])/2+5,button_endy),text=NO,minwidth=button_width,command=lambda e:self.return_msg(False),anchor='nw')[-1]
        self.tinui.add_back((),(yesbutton_uid,nobutton_uid),bg='#f3f3f3',fg='#f3f3f3',linew=9)

        return self.load_window()
    
    def return_msg(self,val):
        #返回消息
        self.result=val
        self.destroy()
        self.master.focus_set()

    def initial_input(self,title,content,yestext='OK',notext='Cancel'):
        """
        初始化对话框-输入类
        """
        YES=yestext
        NO=notext

        self.tinui['bg']='#ffffff'
        
        self.title(title)
        self.protocol('WM_DELETE_WINDOW',lambda:self.return_input(None))
        
        self.tinui.add_paragraph((5,5),text=content)
        content_bbox=self.tinui.bbox('all')
        entry_width=content_bbox[2]-content_bbox[0]
        width=entry_width if entry_width>200 else 200
        self.entry=self.tinui.add_entry((5,self._endy()+5),width=width)[-2]# tinui entry widget, funcs
        bbox=self.tinui.bbox('all')
        btn_width=(bbox[2]-bbox[0])/2
        button_width=btn_width-10 if btn_width>110 else 100
        button_endy=self._endy()+15
        yesbutton_uid=self.tinui.add_button2(((bbox[0]+bbox[2])/2-5,button_endy),text=YES,minwidth=button_width,command=lambda e:self.return_input(self.entry.get()),anchor='ne')[-1]
        nobutton_uid=self.tinui.add_button2(((bbox[0]+bbox[2])/2+5,button_endy),text=NO,minwidth=button_width,command=lambda e:self.return_input(None),anchor='nw')[-1]
        self.tinui.add_back((),(yesbutton_uid,nobutton_uid),bg='#f3f3f3',fg='#f3f3f3',linew=9)

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

        self.tinui['bg']='#ffffff'

        self.title(title)
        self.protocol('WM_DELETE_WINDOW',lambda:self.return_choice(None))

        self.tinui.add_paragraph((5,5),text=content)
        content_bbox=self.tinui.bbox('all')

        if self.type=='listbox':
            self.tinui.add_listbox(((content_bbox[0]+content_bbox[2])/2,self._endy()+5),data=choices,command=self.return_choice,anchor='n')

        bbox=self.tinui.bbox('all')
        btn_width=(bbox[2]-bbox[0])/2
        button_width=btn_width-10 if btn_width>110 else 100
        button_endy=self._endy()+15
        yesbutton_uid=self.tinui.add_button2(((bbox[0]+bbox[2])/2-5,button_endy),text=YES,minwidth=button_width,command=lambda e:self.return_choice(True),anchor='ne')[-1]
        nobutton_uid=self.tinui.add_button2(((bbox[0]+bbox[2])/2+5,button_endy),text=NO,minwidth=button_width,command=lambda e:self.return_choice(None),anchor='nw')[-1]
        self.tinui.add_back((),(yesbutton_uid,nobutton_uid),bg='#f3f3f3',fg='#f3f3f3',linew=9)

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

        self.transient(self.master)
        self.focus_set()
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

        return self.result



def show_msg(master,title,content):
    """
    显示消息对话框
    """
    dialog=Dialog(master,'normal')
    return dialog.initial_msg(title,content)

def show_info(master,title,content,yestext='OK',notext='Cancel'):
    """
    显示信息对话框
    """
    dialog=Dialog(master,'info')
    return dialog.initial_msg(title,content,yestext,notext)

def show_success(master,title,content,yestext='OK',notext='Cancel'):
    """
    显示成功对话框
    """
    dialog=Dialog(master,'success')
    return dialog.initial_msg(title,content,yestext,notext)


def show_warning(master,title,content,yestext='OK',notext='Cancel'):
    """
    显示警告对话框
    """
    dialog=Dialog(master,'warning')
    return dialog.initial_msg(title,content,yestext,notext)

def show_error(master,title,content,yestext='OK',notext='Cancel'):
    """
    显示错误对话框
    """
    dialog=Dialog(master,'error')
    return dialog.initial_msg(title,content,yestext,notext)

def show_question(master,title,content,yestext='YES',notext='NO'):
    """
    显示询问对话框
    """
    dialog=Dialog(master,'question')
    return dialog.initial_msg(title,content,yestext,notext)


def ask_string(master,title,content,yestext='OK',notext='Cancel'):
    """
    输入字符串对话框
    """
    dialog=Dialog(master,'string')
    return dialog.initial_input(title,content,yestext,notext)

def ask_integer(master,title,content,yestext='OK',notext='Cancel'):
    """
    输入整数对话框
    """
    dialog=Dialog(master,'integer')
    return dialog.initial_input(title,content,yestext,notext)

def ask_float(master,title,content,yestext='OK',notext='Cancel'):
    """
    输入浮点数对话框
    """
    dialog=Dialog(master,'float')
    return dialog.initial_input(title,content,yestext,notext)

def ask_choice(master,title,content,choices,yestext='OK',notext='Cancel'):
    """
    选择列表对话框
    """
    dialog=Dialog(master,'listbox')
    return dialog.initial_choice(title,content,choices,yestext,notext)



#test
if __name__=='__main__':
    root=Tk()
    root.iconbitmap('LOGO.ico')
    a=show_msg(root,'test','hello world!')
    # print(a)
    show_info(root,'test','show information\nhello world!')
    show_success(root,'test','Success!\nhello world! hello world! hello world! hello world!')
    show_warning(root,'test','this is a warning\nhello world!')
    show_error(root,'test','something is wrong\nhello world! hello world! hello world! hello world!')
    show_question(root,'test','Do you want to continue?')
    b=ask_string(root,'test','input something input something input something input something')
    ask_integer(root,'test','input integer')
    ask_float(root,'test','input float')
    # print(b)
    c=ask_choice(root,'test','choose one',('a','b','c'))
    # print(c)
    root.mainloop()