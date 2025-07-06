from window import win

index=-1
def additem(e):
    uixml = funcs.add()[-2]
    uixml.loadxml(onexml)
def deleteitemthis(e):
    funcs.delete(index)
def add10(e):
    for i in range(0,10):
        additem(e)
def deleteitem(e):
    funcs.delete(1)
def deleteitem1(e):
    funcs.delete(0)
def deleteall(e):
    funcs.clear()
def print__(name):
    global index
    index=name
    print(name)
def getnowon(e):
    print(funcs.getsel())
def selectnext(e):
    num = len(funcs.getitems())
    now = funcs.getsel()
    if now < num:
        funcs.select(now+1)

a=win()
u=a.u
funcs=u.add_listview((10,5),command=print__)[-2]

onexml='''<tinui>
<line>
<title text='listview'></title>
<line>
<label text='列表视图'></label>
</line>
</line>
</tinui>
'''

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
u.add_button((5,370),'删除元素',command=deleteitemthis)
u.add_button((5,420),'获取选中元素',command=getnowon)
u.add_button((5,470),'选择下一个',command=selectnext)
u.add_button((120,320),'删除第一个元素',command=deleteitem1)
u.add_button((120,370),'删除第二个元素',command=deleteitem)
u.add_button((120,420),'清空元素',command=deleteall)
u.add_button((120,470),'增加十个',command=add10)

a.go()
