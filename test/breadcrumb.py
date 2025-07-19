from window import win

def step1():
    for i in range(1,5):
        funcs.add(f'item{i}')
def step2():
    funcs.delete()
def step3():
    cid = funcs.get()[1]
    funcs.delete_to(cid)

def unwrap(cids):
    res=[]
    for i in cids:
        res.append(u.itemcget(i,'text'))
    u.itemconfig(t,text='\\'.join(res))

a=win()
u=a.u
funcs=u.add_breadcrumb((250,5),anchor='n',command=unwrap)[-2]

step=1
def nextstep(e):
    global step
    if step==1:
        step1()
        step=2
    elif step==2:
        step2()
        step=3
    elif step==3:
        step3()
        u.delete(b)
b=u.add_button((5,50),'下一步',command=nextstep)[-1]
t=u.add_paragraph((250,55),'HOME',anchor='n')
a.go()
