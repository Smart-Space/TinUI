from window import win,BasicTinUI


def destroy(f):
    print(frames[f])
    frames[f].destroy()


a=win()
u=a.u

tb,_,_=u.add_textbox((5,5),450,400,scrollbar=True)

frames=[]
for i in range(0,15):
    cont=BasicTinUI(tb,width=404,height=54)
    item,_=cont.add_swipecontrol((1,1),text=f'swipe item {i}',data={'right':({'text':'close','fg':'#ffecec','bg':'#ff0000','command':(lambda it=i:destroy(it))},)})
    tb.window_create('end',window=cont)
    item.bind('<Destroy>',lambda e,cont=cont:cont.destroy())
    frames.append(item)

a.go()
