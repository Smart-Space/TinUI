from window import win

def mnone(e):
    u.add_image((10,40),100,200,'none','LOGO.png')

def mfill(e):
    u.add_image((190,40),100,200,'fill','LOGO.png')

def muniform(e):
    u.add_image((300,40),100,200,'uniform','LOGO.png')


a=win()
u=a.u
u.add_button((10,5),'None',command=mnone)
u.add_button((190,5),'Fill',command=mfill)
u.add_button((350,5),'Uniform',command=muniform)

a.go()
