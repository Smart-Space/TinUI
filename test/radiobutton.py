from window import win

def s(e):
    funcs[0](2)
def di(e):
    funcs[1]()
def ac(e):
    funcs[2]()

a=win()
u=a.u
u.add_button((2,5),'选定第三个选项',command=s)
u.add_button((180,5),'禁用',command=di)
u.add_button((250,5),'激活',command=ac)
_,_,_,funcs,_=u.add_radiobutton((5,50),width=200,text='test radio button',choices=('1','2','3','4','5','6'))

a.go()
