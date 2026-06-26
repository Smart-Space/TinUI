from window import win

def additem(e):
    funcs.add('new item new item new item new item new item', 2)
def getitem(e):
    print(funcs.get())
def deleteitem(e):
    funcs.delete(1)
def deleteall(e):
    funcs.clear()
def print__(name):
    print(name,name.index)

a=win()
u=a.u
_,_,funcs,_=u.add_listbox((5,5),data=(),command=print__)

u.add_button((5,300),'添加元素',command=additem)
u.add_button((5,350),'获取选定',command=getitem)
u.add_button((120,300),'删除第二个元素',command=deleteitem)
u.add_button((120,350),'清空元素',command=deleteall)
a.go()
