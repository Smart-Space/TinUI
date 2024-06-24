from window import *
from tkinter import Tk

def get1(event):
    lb1=x.tags['lb1'][0]
    entry=x.tags['en'][0]
    print(lb1,entry.get())
    u.itemconfig(lb1,text=entry.get())

xml='''
<tinui>
<line x='5' y='44' anchor='w'>
    <button text="获取输入值" font='宋体 16' command='self.funcs["get1"]'></button>
    <entry width='200'>en</entry>
    <line anchor='nw'>
        <button text="获取输入值" font='宋体 16' command='self.funcs["get1"]'></button>
        <entry width='200'>en</entry>
    </line>
    <line anchor='nw'>
        <button text="获取输入值" font='宋体 16' command='self.funcs["get1"]'></button>
        <entry width='200'>en</entry>
    </line>
</line>
<line>
    <button text="hi, this is a xml TinUI test" command='print'></button>
</line>
<line x='100'>
    <label text='&lt;输入内容显示]' outline=''>lb1</label>
</line>
</tinui>
'''

a=Tk()
u=TinUI(a)
x=TinUIXml(u)
x.environment(globals())
x.loadxml(xml)
u.pack(fill='both',expand=True)
a.mainloop()
