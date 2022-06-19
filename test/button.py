from window import win

def change1(event):
    func[0](test1)
def test1(event):
    print('1')
def change2(event):
    func[0](test2)
def test2(event):
    print('2')

def disable(event):
    func2.disable()
def active(event):
    func2[2]()

a=win()
u=a.u
u.add_button((10,5),'切换到函数1',command=change1)
u.add_button((150,5),'切换到函数2',command=change2)
u.add_button((250,5),'禁止按钮',command=disable)
u.add_button((350,5),'激活按钮',command=active)
_,_,func,_=u.add_button((5,100),'测试按钮',command=test1)
_,_,func2,_=u.add_button((100,100),'测试按钮2',command=test1)

a.go()
