from window import *
from tkinter import Tk

def get1(event):
    lb1=x.tags['lb1'][0]
    entry=x.tags['en'][0]
    u.itemconfig(lb1,text=entry.get())

xml='''
<tinui>
<line>
<button text="获取输入值" font='宋体 16' command='self.funcs["get1"]'></button>
<entry width='200'>en</entry>
</line>
<line>
<button text="hi, this is a xml TinUI test" command='self.funcs["p"]'></button>
</line>
<line x='100'>
<label text='&lt;输入内容显示]' outline=''>lb1</label>
</line>
</tinui>
'''

a=Tk()
u=TinUI(a)
x=TinUIXml(u)
x.funcs={'p':print,'get1':get1}
x.loadxml(xml)
u.pack(fill='both',expand=True)
a.mainloop()
