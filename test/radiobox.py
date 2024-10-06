from window import win


def di(e):
    funcs.disable()
def ac(e):
    funcs.active()

a=win()
u=a.u
u.add_button((180,5),'禁用',command=di)
u.add_button((250,5),'激活',command=ac)
_,funcs,_=u.add_radiobox((5,50),content=('1','','2'))

a.go()
