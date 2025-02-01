from window import win


def disable(e):
    funcs.disable()
def active(e):
    funcs.active()
def on(e):
    funcs.on()
def off(e):
    funcs.off()

a=win()
u=a.u
funcs=u.add_onoff((5,40),command=print)[-2]
u.add_button((5,5),'禁用',command=disable)
u.add_button((80,5),'恢复',command=active)
u.add_button2((160,5),'开启',command=on)
u.add_button2((240,5),'关闭',command=off)

#ctypes.windll.shcore.SetProcessDpiAwareness(1)

a.go()
