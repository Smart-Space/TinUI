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
import re
import idlelib.colorizer as idc
import idlelib.percolator as idp


loclines=False#坐标十字线是否存在
def if_location(e):#是否显示坐标十字线
    global loclines
    loclines=e
    if loclines:
        tinui.itemconfig(loctext,state='normal')
        displayui.show_location(command=getloc)
    else:
        tinui.itemconfig(loctext,text='x:? y:?',state='hidden')
        displayui.show_location(False)

def getloc(x,y):
    tinui.itemconfig(loctext,text=f'x:{x} y:{y}')


def inxml(e):#注入xml界面
    xml=text.get(1.0,'end')
    duixml.funcs=dict()
    duixml.datas=dict()
    duixml.tags=dict()
    result=re.findall("self\.(.*?)\[.(.*?).\]'",xml,re.M|re.S)
    for i in result:
        if i[0]=='funcs':
            duixml.funcs[i[1]]=None
        elif i[0]=='datas':
            duixml.datas[i[1]]=(None,None)
    duixml.yendy=5
    duixml.clean()
    duixml.loadxml(xml)
    rescroll()

def write(text):
    textbox.insert('end',text)
def pycode(e):#获取IDO代码
    inxml(e)
    pycodew.deiconify()
    textbox.configure(state='normal')
    textbox.delete(1.0,'end')
    uixml=text.get(1.0,'end')
    result=re.findall("self\.(.*?)\[.(.*?).\]'",uixml,re.M|re.S)
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


root=Tk()
root.geometry('1300x700+5+5')
root.title('TinUIXml设计测试')
root.resizable(False,False)

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
text=ScrolledText(root,font='微软雅黑 13')
text.place(x=0,y=0,width=400,height=700)
text.insert(1.0,initial_xml)
tinui=TinUI(root,update=False,bg='#f3f3f3')
tinui.place(x=401,y=0,width=899,height=700)
tinui.vbar.pack_forget()
tinui.hbar.pack_forget()
x=TinUIXml(tinui)
x.environment(globals())

xmlf=open(os.path.dirname(__file__)+r'\xmltestpage\main.xml','r',encoding='utf-8')
xml=xmlf.read()
xmlf.close()

x.loadxml(xml)
displayui,rescroll,duixml,_=x.tags['xmlui']
loctext=x.tags['loctext']
tinui.itemconfig(loctext,state='hidden')
tinui.bind('<Enter>',lambda e:tinui.focus())


#弹窗窗口
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

if __name__=='__main__':
    root.mainloop()
