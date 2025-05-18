from window import win



a=win()
u=a.u
pivot = u.add_pivot((5,5))[-2]
u.add_button((10,80),text='选择第二个',command=lambda e:pivot.select(1))

a.go()
