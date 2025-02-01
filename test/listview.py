from window import win

def additem(e):
    funcs.add()
def deleteitem(e):
    funcs.delete(1)
def print__(name):
    print(name)

a=win()
u=a.u
funcs=u.add_listview((10,5),command=print__)[-2]

lvitems=funcs.getitems()
lvcontent=(
    ('BasicTinUI','TinUI框架渲染核心','https://tinui.smart-space.com.cn'),
    ('TinUI','基于tkinter的现代元素控件框架','https://smart-space.com.cn/project/TinUI/index.html'),
    ('CSDN','中文IT技术交流平台','https://www.csdn.net/'),
    ('TinText','新版TinML实现平台','https://tintext.smart-space.com.cn/'),
    ('Smart-Space','个人开发者名称','https://smart-space.com.cn')
    )
for i in range(0,5):
    lvitems[i][2].loadxml(f'''<tinui>
    <line>
    <line>
    <title text='{lvcontent[i][0]}'></title>
    <link text='相关链接' url='{lvcontent[i][2]}'></link>
    </line>
    <line>
    <label text='{lvcontent[i][1]}'></label>
    <button2 text='test'></button2>
    </line>
    </line>
    </tinui>''')

u.add_button((5,320),'添加元素',command=additem)
u.add_button((120,320),'删除第二个元素',command=deleteitem)

a.go()
