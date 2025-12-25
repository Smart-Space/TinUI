from window import win

def close(e):
    func.close_all()

def expand(e):
    func.open_all()

a=win()
u=a.u
u.add_button((10,5),'全部关闭',command=close)
u.add_button((100,5),'全部展开',command=expand)
func=u.add_treeview((5, 40))[-2]

a.go()
