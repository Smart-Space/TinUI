from window import win

def flash(e):
    funcs[0]()
def on(e):
    funcs[1]()
def off(e):
    funcs[2]()
def ac(e):
    funcs[4]()
def di(e):
    funcs[3]()

a=win()
u=a.u
u.add_button((2,5),'切换状态',command=flash)
u.add_button((80,5),'选定',command=on)
u.add_button((160,5),'取消选定',command=off)
u.add_button((260,5),'disable',command=di)
u.add_button((340,5),'active',command=ac)
_,_,funcs,_=u.add_checkbutton((2,50),'测试checkbutton')
a.go()