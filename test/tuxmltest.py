from window import *
from tkinter import Tk
from tkinter.ttk import Button
from tkinter.scrolledtext import ScrolledText

def inxml():
    xml=text.get(1.0,'end')
    x.yendy=5
    x.clean()
    x.loadxml(xml)

root=Tk()
root.geometry('1000x700+5+5')
root.title('TinUIXml设计测试')

text=ScrolledText(root,width=50,font='微软雅黑 13')
text.pack(side='left',fill='y',expand=True)
Button(root,text='导入xml',command=inxml).pack()
tinui=TinUI(root,bg='white',width=480,height=650)
tinui.pack(side='right',expand=True)
x=TinUIXml(tinui)

root.mainloop()
