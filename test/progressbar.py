from window import win

def run(event):
    from time import sleep
    for button in (b1,ba,bb,bc,bd):
        button[2][1]()
    for i in range(1,101):
        sleep(0.02)
        goto(i)
    for button in (b1,ba,bb,bc,bd):
        button[2][2]()
def to60(event):
    goto(60)
def stop(event):
    funcs[1]()
def error(event):
    funcs[2]()
def normal(event):
    funcs[0]()

a=win()
u=a.u
b1=u.add_button((2,5),'全过程',command=run)
ba=u.add_button((80,5),'固定到60%',command=to60)
bb=u.add_button((180,5),'暂停',command=stop)
bc=u.add_button((240,5),'意外错误',command=error)
bd=u.add_button((340,5),'恢复正常',command=normal)
_,_,_,goto,funcs,_=u.add_progressbar((2,50))
a.go()
