from window import win
import sys
sys.path.append('..')
from TinUI import ExpandPanel, HorizonPanel

def callback(tag):
    if isinstance(tag, bool):
        u.event_generate("<Configure>", width=u.winfo_width(), height=u.winfo_height())
    else:
        textbox[0].delete(1.0, "end")
        textbox[0].insert(1.0, f'{tag}-view')

a=win()
u=a.u
u.config(bg='#FFFFFF')

root=ExpandPanel(u)
hp=HorizonPanel(u,spacing=5)
root.set_child(hp)

textbox=u.add_textbox((0,0))
naview=u.add_navigation((0,0),command=callback)[-1]
hp.add_child(naview)

expand=ExpandPanel(u,padding=(5,5,5,5))
hp.add_child(expand, weight=1)
expand.set_child(textbox[-1])

def update(e):
    root.update_layout(5,5,e.width-5,e.height-5)
u.bind('<Configure>',update)

a.go()
