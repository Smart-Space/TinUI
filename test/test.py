from window import win

def dop(cont):
    print(f'输入框内容为：{cont}')

a=win()
u=a.u

u.add_button((5,5),text='one')
u.add_button((55,5),text='two1')
u.add_button((55,40),text='two2')
u.add_button((110,5),text='three')

u.add_entry((5,180),350,'这里用来输入',command=dop)

a.go()
