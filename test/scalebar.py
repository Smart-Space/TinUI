from window import win

def s(e):
    funcs[0](2)
def di(e):
    funcs[1]()
def ac(e):
    funcs[2]()
def show(val):
    u.itemconfig(text,text=f'选择的值为：{val}')

a=win()
u=a.u
u.add_button((2,5),'选定第三个选项',command=s)
u.add_button((180,5),'禁用',command=di)
u.add_button((250,5),'激活',command=ac)
_,_,_,funcs,_=u.add_scalebar((100,50),direction='y',width=200,data=range(101),command=show)
text=u.create_text((5,80),text='选择的值为：None',font='微软雅黑')

a.go()
