from window import win, extension
from extension import buttonlize

def go(e):
    buttonlize(u,'btllb',command=func)

def func():
    print('click')

a=win()
u=a.u

lb=u.add_label((15,15),text='buttonlized label')[-1]
lb2=u.add_button((15,60),text='buttonlized button',command=print)[-1]

u.addtag_withtag('btllb',lb)
u.addtag_withtag('btllb',lb2)

u.add_button2((15,120),text='buttonlize',command=go)

a.go()
