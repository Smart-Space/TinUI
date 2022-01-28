from window import win

a=win()
u=a.u

u.add_button((5,5),text='one')
u.add_button((55,5),text='two1')
u.add_button((55,40),text='two2')
u.add_button((110,5),text='three')

a.go()
