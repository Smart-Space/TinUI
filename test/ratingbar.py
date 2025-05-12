from window import win


def func(e):
    f.setrate(2)

a=win()
u=a.u
f = u.add_ratingbar((5,5))[-2]
u.add_button((5,50), text='选择第二个', command=func)

a.go()
