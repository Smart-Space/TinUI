from window import win

def active(e):
    funcs[1]()
def disable(e):
    funcs[0]()

a=win()
u=a.u
_,_,funcs,_=u.add_link((5,5),'Smart-Space个人网站','https://smart-space.com.cn/')
u.add_button((5,40),'禁用链接',command=disable)
u.add_button((120,40),'恢复链接',command=active)
a.go()
