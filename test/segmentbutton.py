from window import win


def callback(mode):
    u.itemconfig(t,text=f'当前模式：{mode}')

def set_default(e):
    select(1)

a=win()
u=a.u
select=u.add_segmentbutton((5,5),content=('节能','均衡','高性能'),command=callback)[-2].select
t=u.add_paragraph((5,100),text='当前模式：节能')
select(0)
u.add_button((5,140),text='默认',command=set_default)

a.go()
