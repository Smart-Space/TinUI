from window import win

def select(e):
    funcs[0](2)
def disable(e):
    funcs[1]()
def active(e):
    funcs[2]()

a=win()
u=a.u
u.add_button((2,5),'选定第三个值',command=select)
u.add_button((150,5),'禁用',command=disable)
u.add_button((220,5),'启用',command=active)
_,_,_,funcs,_=u.add_combobox((2,50),text='test combobox',content=('1','2','3','4','5'))

a.go()
