"""
TinUIXml简易设计编辑器

注意！！！这只是测试文件，不保证随TinUI正式版本进行维护，
仅作为对TinUIXml和BasicTinUI设计模式 show_location() 的测试。
本代码文件本身不具备xml文本和python代码专用编辑能力。

本文件可作为开发TinUIXml编辑器或通过绝对坐标设计TinUI界面的参考，
不附带TinUI开发能力，不要单纯依靠本程序开发TinUI及python应用。
"""
from window import *
from tkinter import Tk,Toplevel
from tkinter.ttk import Button
from tkinter.scrolledtext import ScrolledText
from tkinter.simpledialog import askinteger
import re
import idlelib.colorizer as idc
import idlelib.percolator as idp


def show_location(state:bool=True,color='red',command=None):
    #在设计时反馈鼠标所在的绝对位置
    if not state:
        displayui.unbind('<Enter>')
        displayui.unbind('<Motion>')
        displayui.unbind('<Leave>')
        return
    displayui.locx=None
    displayui.locy=None
    def entercall(e):
        bbox=displayui.bbox('all')
        width=displayui.winfo_width()
        height=displayui.winfo_height()
        if bbox==None:
            _width=0
            _height=0
        else:
            _width=bbox[2]-bbox[0]
            _height=bbox[3]-bbox[1]
        if _width>width:
            width=_width
        if _height>height:
            height=_height
        displayui.loclx=displayui.create_line((0,0,width,0),width=2,dash=(5,5),fill=color)
        displayui.locly=displayui.create_line((0,0,0,height),width=2,dash=(5,5),fill=color)
    def motioncall(e):#鼠标在界面中滑动
        if displayui.loclx!=None:
            x=displayui.canvasx(e.x)
            y=displayui.canvasy(e.y)
            displayui.moveto(displayui.loclx,0,y)
            displayui.moveto(displayui.locly,x,0)
            if command!=None:command(x,y)
    def leavecall(e):
        displayui.delete(displayui.loclx)
        displayui.delete(displayui.locly)
        displayui.loclx=None
        displayui.locly=None
    displayui.bind('<Enter>',entercall)
    displayui.bind('<Motion>',motioncall)
    displayui.bind('<Leave>',leavecall)

loclines=False#坐标十字线是否存在
def if_location(e):#是否显示坐标十字线
    global loclines
    loclines=e
    if loclines:
        tinui.itemconfig(loctext,state='normal')
        show_location(command=getloc)
    else:
        tinui.itemconfig(loctext,text='x:? y:?')
        show_location(False)

def getloc(x,y):
    tinui.itemconfig(loctext,text=f'x:{x} y:{y}')


def inxml(e):#注入xml界面
    xml=text.get(1.0,'end')
    duixml.funcs=dict()
    duixml.datas=dict()
    duixml.tags=dict()
    result=re.findall("self\.(.*?)\[.(.*?).\]",xml,re.M|re.S)
    print(result)
    for i in result:
        if i[0]=='funcs':
            duixml.funcs[i[1]]=None
        elif i[0]=='datas':
            duixml.datas[i[1]]=(None,None)
    displayui.delete('all')
    duixml.clean()
    duixml.loadxml(xml)
    rescroll()
    reset_marks()

def write(text):
    textbox.insert('end',text)
def pycode(e):#获取IDO代码
    inxml(e)
    pycodew.deiconify()
    textbox.configure(state='normal')
    textbox.delete(1.0,'end')
    uixml=text.get(1.0,'end')
    result=re.findall(r"self\.(.*?)\[.(.*?).\]",uixml,re.M|re.S)
    textbox.result=result
    write('''# u = TinUI(root)
# x = TinUIXml(u)
# xml=file.read()

''')
    write('''# in
''')
    for i in result:
        if i[0]=='funcs':
            write(f'x.funcs["{i[1]}"] = {i[1]}\n')
        elif i[0]=='datas':
            write(f'x.datas["{i[1]}"] = {i[1]}\n')
    write('''
# during
x.loadxml(xml)

# out
''')
    for tag in duixml.tags.keys():
        write(f'{tag} = x.tags["{tag}"]\n')
    textbox.configure(state='disabled')

def copy_pycode(e):#复制
    textbox.clipboard_clear()
    copyText = textbox.get(1.0,'end')
    textbox.clipboard_append(copyText)
def highlight(e):#标注funcs,datas等重点
    havefunc,havedata=False,False
    textbox.configure(state='normal')
    write('\n#TinUIXml导入重点：\n')
    for i in textbox.result:
        if i[0]=='funcs':
            if havefunc==False:
                havefunc=True
                write('#函数/方法(funcs)：\n')
            write(f'#  {i[1]}(...)\n')
        elif i[0]=='datas':
            if havedata==False:
                havedata=True
                write('#数据(datas)：\n')
            write(f'#  {i[1]}=...\n')
    havetag=False
    for tag in duixml.tags.keys():
        if havetag==False:
            havetag=True
            write('\n#TinUIXml导出重点：\n')
        write(f'#  {tag}\n')
    textbox.configure(state='disabled')

now_mark=None#mark_index
def open_markw(e):
    markw.deiconify()
def del_mark(e):#删除选定标记点
    global now_mark
    if now_mark==None:
        return
    listbox.delete(now_mark)
    displayui.delete(mark_points[now_mark][1])
    del mark_points[now_mark]
    now_mark=None
def add_mark(e):#手动添加标记点
    x=askinteger('手动添加标记点','横坐标：',parent=markw)
    if x==None:
        return
    y=askinteger('手动添加标记点','纵坐标：',parent=markw)
    if y==None:
        return
    __set_mark(x,y)
def sel_mark(name):#选定标记点
    global now_mark
    if name.index==0:
        now_mark=None
    else:
        if now_mark!=None:
            displayui.itemconfigure(mark_points[now_mark][1],outline='black',fill="black")
        now_mark=name.index
        displayui.itemconfigure(mark_points[now_mark][1],outline='red',fill='red')

def __set_mark(x,y):
    mark=displayui.create_oval((x,y,x+3,y+3),outline='black',fill="black")
    mark_points.append(((x,y),mark))
    listbox.add(f'({x} , {y})')
def set_mark(e):#绘制标记点
    __set_mark(e.x,e.y)
def reset_marks():#重新绘制标记点
    if len(mark_points)==0:
        return
    index=1
    for i in mark_points[1:]:
        mark=displayui.create_oval((i[0][0],i[0][1],i[0][0]+3,i[0][1]+3),outline='black',fill="black")
        mark_points[index]=(i[0],mark)
        index+=1


root=Tk()


root.geometry('1200x700')
root.title('TinUIXml设计测试')

initial_xml='''<!--TinUIXml编辑-->
<tinui>
<line>
    <line>
        <title text='back'></title>
    </line>
    <line>
        <paragraph text='TinUI的背景控件，用来呈现不同控件组的层次。' width='580'></paragraph>
    </line>
    <line>
    <paragraph text=' ' width='580'></paragraph>
    </line>
    <line anchor='w'>
    <paragraph text='下方就是back'>p1</paragraph>
    <button2 text='本按钮与左边文字构成控件组'>b1</button2>
    <back uids='("b1","p1")' bg='yellow' fg='yellow'></back>
    </line>
</line>
</tinui>'''
tinui=BasicTinUI(root,bg='#f3f3f3')
tinui.pack(expand=True,fill='both')

textids=tinui.add_textbox((0,0),400,700,font='微软雅黑 13',scrollbar=True)
text=textids[0]
textid=textids[-1]
text.insert(1.0,initial_xml)

rp=ExpandPanel(tinui)
hp=HorizonPanel(tinui,spacing=5)
rp.set_child(hp)

vp=VerticalPanel(tinui)
hp.add_child(vp,400)
ep1=ExpandPanel(tinui)
vp.add_child(ep1,700,weight=1)
ep1.set_child(textid)

ep=ExpandPanel(tinui)
hp.add_child(ep,weight=1)

vp2=VerticalPanel(tinui)
ep.set_child(vp2)

top=HorizonPanel(tinui,spacing=5)
vp2.add_child(top,50)
btn=tinui.add_button2((0,0),text='导入xml',command=inxml,anchor='w')[-1]
top.add_child(btn,70)
btn=tinui.add_button2((0,0),text='python代码',command=pycode,anchor='w')[-1]
top.add_child(btn,100)
ctk=tinui.add_checkbutton((0,0),text='启用十字线定位',command=if_location,anchor='w')[-1]
top.add_child(ctk,150)
loctext=tinui.add_paragraph((0,0),text='x: y:',anchor='w')
top.add_child(loctext)

top.add_child(ExpandPanel(tinui),weight=1)

btn=tinui.add_button2((0,0),text='打开标记点管理窗口',command=open_markw,anchor='e')[-1]
top.add_child(btn,300)

uiep=ExpandPanel(tinui)
vp2.add_child(uiep,weight=1)

displayui,rescroll,duixml,uiid=tinui.add_ui((0,0),width=870,height=630,scrollbar='True')
uiep.set_child(uiid)

def update(e):
    rp.update_layout(5,5,e.width-5,e.height-5)
tinui.bind('<Configure>',update)


#Python代码弹窗窗口
pycodew=Toplevel()
pycodew.title("Python代码")
# 设置窗口大小
window_width = 520
window_height = 550
# 获取屏幕大小
screen_width = pycodew.winfo_screenwidth()
screen_height = pycodew.winfo_screenheight()
# 计算窗口居中的x和y坐标
x_coordinate = int((screen_width/2) - (window_width/2))
y_coordinate = int((screen_height/2) - (window_height/2))
# 设置窗口的位置和大小，并禁止改变尺寸
pycodew.geometry("{}x{}+{}+{}".format(window_width, window_height,
                                      x_coordinate, y_coordinate))
pycodew.resizable(width=False, height=False)  # 禁止改变窗口大小
pctinui=BasicTinUI(pycodew)
pctinui.pack(fill='both',expand=True)
pycodew.protocol("WM_DELETE_WINDOW", lambda: pycodew.withdraw())  # 忽略关闭窗口的协议
pycodew.withdraw()
pctinuix=TinUIXml(pctinui)

xmlf=open(os.path.dirname(__file__)+r'\xmltestpage\pytest.xml','r',encoding='utf-8')
xml=xmlf.read()
xmlf.close()
pctinuix.environment(globals())
pctinuix.loadxml(xml)
textbox=pctinuix.tags['textbox'][0]
idc.color_config(textbox)
p = idp.Percolator(textbox)
d = idc.ColorDelegator()
p.insertfilter(d)


#==========
#标记点管理页面
markw = Toplevel(root)
markw.title("标记点管理")
markw.geometry("400x600")
markw.resizable(width=False, height=False)  # 禁止改变窗口大小
markw.protocol("WM_DELETE_WINDOW", lambda: markw.withdraw())  # 忽略关闭窗口的协议
markui=BasicTinUI(markw)
markui.pack(fill='both',expand=True)
markw.withdraw()
markuix=TinUIXml(markui)

xmlf=open(os.path.dirname(__file__)+r'\xmltestpage\marks.xml','r',encoding='utf-8')
xml=xmlf.read()
xmlf.close()
markuix.environment(globals())
markuix.loadxml(xml)
listbox=markuix.tags['listbox'][-2]
mark_points=[((None,None),None)]#与listbox内列表同步更新，[((x,y), point_uid), ...]
displayui.bind('<Button-3>',set_mark)

if __name__=='__main__':
    root.mainloop()
