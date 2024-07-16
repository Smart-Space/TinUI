from window import win

def getin(*e):
    con=func.get()
    u.itemconfig(p,text='输入内容：'+con)

def renormal(*e):
    func.normal()

def error(*e):
    func.error()

def disable(*e):
    func.disable()

def active(*e):
    func.active()

def insert(*e):
    func.insert(text='insert text')


a=win()
u=a.u
u.add_button((10,5),'获取输入内容',command=getin)
u.add_button((150,5),'禁用输入框',command=disable)
u.add_button((250,5),'恢复输入框',command=renormal)
u.add_button((350,5),'显示错误样式',command=error)
entry,func,_=u.add_entry((180,50),anchor='n',width=300)
p=u.add_paragraph((5,100),text='输入内容：')

u.add_button((10,200),'用active恢复',command=active)
u.add_button((10,250),'插入文本',command=insert)

a.go()
