from window import win

def additem(e):
    funcs.add('new item new item new item new item new item')
def deleteitem(e):
    funcs.delete(1)
def print__(name):
    print(name,name.index)

a=win()
u=a.u
_,_,funcs,_=u.add_listbox((5,5),data=(),command=print__)

u.add_button((5,300),'添加元素',command=additem)
#u.add_button((120,300),'删除第二个元素'+'\uE755',font='{Segoe MDL2} 12',command=deleteitem)
u.add_button((120,300),'删除第二个元素',command=deleteitem)

a.go()
