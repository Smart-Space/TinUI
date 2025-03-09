# TinUI

![](https://github.com/Smart-Space/TinUI/raw/main/image/LOGO.png)

---

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI明亮样式.gif)![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI黑暗样式.gif)

---

## 项目类型

TinUI是一个基于tkinter（Python/tcl/tk）的拓展组件（Widget），可以绘制具有现代化样式的控件。

TinUI基于tkinter的画布（Canvas），可以作为整个窗口的唯一控件。TinUI能够通过自身绘制出功能组件和文字，也可以使用画布功能添加组件。使用TinUI，可以使界面设计和代码设计分离，此外，TinUI绘制的虚拟组件速度更快，样式更加丰富。

目前，TinUI可用于常规tkinter窗口开发。

## 依赖

目前，TinUI没有依赖项目。

## 开源协议

TinUI使用GPLv3（GPL）作为开源协议。

非商业软件，TinUI部分代码必须开源，即使源码被修改。开源的TinUI部分代码必须采用同样的开源协议——GPL，并且注明开发者 Smart-Space（Junming Zhang），以及GitHub/TinUI的开源代码库：https://github.com/Smart-Space/TinUI/

商业软件，需要添加TinUI的gpl-3.0.md的开源许可，为自身使用TinUI做出声明，并且公开TinUI部分的代码。此外，需要注明开发者Smart-Space（Junming Zhang）对TinUI的版权所有，以及GitHub/TinUI的开源代码库：https://github.com/Smart-Space/TinUI/

> 自TinUI-**5.11**起，TinUI支持LGPL-3中的额外许可

## 简单示例

以下是一段简易TinUI代码示例：

```python
from tkinter import Tk
#from tinui.TinUI import TinUI #导入TinUI
from tinui import TinUI

def dop(cont):#处理输入框返回事件
    print(f'输入框内容为：{cont}')

r=Tk()
r.geometry('500x500+10+10')

ui=TinUI(r)
ui.pack(fill='both',expand=True)#填充窗口

#绘制若干个按钮
ui.add_button((5,5),text='one')
ui.add_button((55,5),text='two1')
ui.add_button((55,40),text='two2')
ui.add_button((110,5),text='three')

#绘制一个输入框，并绑定到处理函数：dop
ui.add_entry((5,180),350,'这里用来输入',command=dop)

r.mainloop()
```

## 更新日志

[TinUI更新日志](https://tinui.smart-space.com.cn/changelog/ChangeLog.txt)。

## 贡献者

[TinUI贡献者列表](https://tinui.smart-space.com.cn/contributors)。

---

# Class: TinUI(BasicTinUI)

TinUI模块的主类，基于 `Class: BasicTinUI`。

## 创建TinUI

```python
tinui=TinUI(root,bg='white',update=True,update_time=1000)
'''
update:bool::是否实时更新滚动画面
update_time:int::每次更新滚动画面的间隔（毫秒）
**kw::Canvas的参数
'''
```

## 基础函数

> - ==一般地==，会将每个函数的名称以及定义、参数内容、函数绘制说明列出来。
> 
> 所有函数均会返回主要画布对象。`TinUI.add_...(...)`。
> 
> - 除了 `title`, `paragraph`, `separate`, `menubar`, `labelframe`, `tooltip`, `back`等组件，其余组件的最后一个返回值均为整个组件的画布 `tag_name`，返回值变量为 `uid`。

### clean_windows()

清除浮出控件的子窗口，需要开发者手动释放子窗口。

---

### show_location(state=True,color='red',command=None)

state::是否显示十字坐标确定线

color::线条颜色

command::反馈函数，应当接受两个参数，`x`, `y`

启用十字定位并反馈鼠标所在位置的坐标。

---

### add_title(self,pos:tuple,text:str,fg='black',font='微软雅黑',size=1,anchor='nw',**kw)

- pos::位置
- text::标题文字
- fg::文本颜色
- font::文本字体
- size::文本字体大小。依据字典：`{0:20,1:18,2:16,3:14,4:12}`
- anchor::对齐方向

绘制一个大字体标题。

### return: title

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI%E8%B5%B7%E6%AD%A5.gif)

---

### add_paragraph(self,pos:tuple,text:str,fg='black',font=('微软雅黑',12),side='left',width=500,anchor='nw',**kw)

- pos::位置
- text::标题文字
- fg::文本颜色
- font::字体名称+大小
- side::对齐方向
- width::一行允许的最大字符宽度
- anchor::对齐方向

绘制一个段落。

### return: paragraph

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI%E8%B5%B7%E6%AD%A5.gif)

---

### add_button(self,pos:tuple,text:str,fg='black',bg='#CCCCCC',line='#CCCCCC',linew=3,activefg='black',activebg='#999999',activeline='#7a7a7a',font=('微软雅黑',12),minwidth=0,maxwidth=0,command=None,anchor='nw')

- pos::位置
- text::标题文字
- fg::文字颜色
- bg::按钮颜色
- line::边框颜色
- linew::边框宽度
- activefg::响应鼠标的文本颜色
- activebg::响应鼠标的按钮颜色
- activeline::响应鼠标的边框颜色
- font::字体名称+大小
- minwidth::最小宽度，为0忽略
- maxwidth::最大宽度，为0忽略
- command::绑定的函数。该函数**必须要有event参数**，因为TinUI的按钮会传递点击事件的event
- anchor::对齐方向

绘制一个按钮。这个按钮会响应鼠标的离开和进入事件，被单击时也会调用绑定的函数。

### return: button_text, button_back, funcs, uid

> button_text::按钮文本
> 
> button_back::按钮背景
> 
> funcs
> 
> > `funcs[0]|funcs.change_command(new_func)`::为按钮绑定新函数
> > 
> > `funcs[1]|funcs.disable(fg='#7a7a7a',bg='#cccccc')`::禁用按钮
> > 
> > `funcs[2]|funcs.active()`::激活按钮

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI%E6%8C%89%E9%92%AE.gif)

---

### add_label(self,pos:tuple,text:str,fg='black',bg='#f0f0f0',outline='grey',font=('微软雅黑',12),anchor='nw')

- pos::位置
- text::标题文字
- fg::文字颜色
- bg::背景色
- outline::边框颜色
- font::字体名称+大小
- anchor::对齐方向

绘制一个类Label组件。

### return: label, back, uid

> label::文本
>
> back::背景元素

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI标签.gif)

---

### add_checkbutton(self,pos:tuple,text:str,fontfg='black',fg='#868686',bg='#ededed',activefg='#868686',activebg='#e5e5e5',onfg='white',onbg='#334ac0',font=('微软雅黑',12),command=None,anchor='nw')

- pos::位置
- text::标题文字
- fontfg::文本颜色
- fg::复选框边框颜色
- bg::复选框背景颜色
- activefg::响应鼠标边框颜色
- activebg::响应鼠标背景颜色
- onfg::选定时文本图标颜色
- obbg::选定时背景颜色
- font::字体名称+大小
- command::绑定的函数。该函数**必须要有选定状态参数，True/False，代表操作后按钮代表的状态**
- anchor::对齐方向

绘制一个复选框。这个复选框会响应鼠标的离开和进入事件，被单击时也会调用绑定的函数，并且会根据当前样式更改点击后的样式。

### return: check_text, check_mark, funcs, uid

> check_text::复选框文本
> 
> check_mark::复选框矩形标记部件，除边框
> 
> funcs
> 
> > `funcs[0]|funcs.flash()`::切换复选框状态
> > 
> > `funcs[1]|funcs.on()`::选定
> > 
> > `funcs[2]|funcs.off()`::取消选定
> > 
> > `funcs[3]|funcs.disable()`::禁用
> > 
> > `funcs[4]|funcs.active()`::激活

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI复选框.gif)

---

### add_entry(self,pos:tuple,width:int,text:str='',fg='#606060',bg='#f6f6f6',activefg='#1b1b1b',activebg='#ffffff',line='#e5e5e5',activeline='#e5e5e5',insert='#808080',font=('微软雅黑',12),outline='#868686',onoutline='#3041d8',icon='>',anchor='nw',call='→',command=None)

- pos::位置
- width::宽度
- text::初始文字
- fg::文字颜色
- bg::背景颜色
- activefg::激活时字体颜色
- activebg::激活时背景色
- line::边框颜色
- activeline::激活时边框颜色
- insert::光标颜色
- font::字体
- outline::提示线颜色
- onoutline::获取焦点时的提示线颜色
- icon::内容为空时，右侧显示的字符
- anchor::对齐方向
- call::回调按钮文本，仅command存在时可用
- command::回调函数，可以通过按钮或回车键调用，函数需要接受text参数

绘制一个单行输入框。这是一个半绘制组件，其实就是简化了Entry控件的导入。

通过 `entry.get()`获取值。

### return: entry, funcs, uid

> entry::输入框类（控件）
> 
> funcs
> 
> > `funcs.get()`::获取输入内容
> > 
> > `funcs.error(errorline='#c42b1c')`::显示错误样式
> > 
> > `funcs.normal()`::回复正常样式
> > 
> > `funcs.disable()`::禁用输入框

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI输入框.gif)

---

### add_separate(self,pos:tuple,width:int,direction='x',fg='grey',anchor='nw')

- pos::位置
- width::长度
- direction::方向。“x”或“y”（横向 或 纵向）
- fg::颜色
- anchor::对齐方向

绘制一条分割线。

### return: separate

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI分割线.gif)

---

### add_radiobutton(self,pos:tuple,width,text='',choices=('choose me'),fg='#1a1a1a',bg='#f2f2f2',font=('微软雅黑',12),activefg='#3c3c3c',activebg='#e9e9e9',command=None,anchor='nw')

- pos::位置
- width::整体宽度
- text::单选框文本提示
- choices::选项（list, set, map...）
- fg::文本和边框颜色
- bg::选项背景色
- font::字体
- activefg::选中字体和边框颜色
- activebg::选中背景颜色
- command::回调函数，有并且仅有一个参数，即该按钮所显示的文本
- anchor::对齐方向

绘制一个单选框，竖式排列。

### return: text, choices_text_list, choices_back, funcs, uid

> text::文本提示画布对象
> 
> choices_text_list::可选框的文本画布对象
> 
> choices_back::可选框的背景方框画布对象
> 
> funcs
> 
> > `funcs[0]|funcs.select(num)`::选定一个选项
> > 
> > `funcs[1]|funcs.disable()`::禁用
> > 
> > `funcs[2]|funcs.active()`::激活

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI单选框.gif)

---

### add_link(self,pos:tuple,text,url,fg='#4f62ca',activefg='red',activebg='#eaeaea',font:tuple=('微软雅黑',12),anchor='nw')

- pos::位置
- text::网页链接 **或者** 要执行的函数，函数需要接受 `event`参数
- url::链接或执行函数，当command为None时执行
- fg::文本颜色
- activefg::响应鼠标时文本颜色
- activebg::响应鼠标时背景颜色
- font::字体
- anchor::对齐方向
- command::目标函数，必须接受一个参数，链接目标（网页链接）字符串

绘制一个链接文本，指向网页或者执行函数或者指向目标函数。

### return: link, funcs, uid

![](https://github.com/Smart-Space/TinUI/raw/main/image/%E8%B6%85%E9%93%BE%E6%8E%A5.gif)

> link::链接文本
> 
> funcs
> 
> > `funcs[0]|funcs.disable(fg='#b0b0b0')`::禁用链接
> > 
> > `funcs[1]|funcs.active()`::恢复链接

---

### add_waitbar1(self,pos:tuple,fg='#0078D7',bg='',okfg='lightgreen',okbg='',bd=5,r=20,anchor='nw')

- pos::位置
- fg::边框颜色
- bg::内部填充颜色
- okfg::完成时边框颜色
- okbg::完成时内部填充颜色
- bd::外框宽度
- r::半径
- anchor::对齐方向

绘制一个扇形等待框。

### return: waitbar1, ok, uid

> waitbar1::该画布对象
> 
> ok::停止等待动画的函数。当你完成你需要等待的任务后，你可以调用此函数，停止等待动画

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI%E7%AD%89%E5%BE%851.gif)

---

### add_labelframe(self,widgets:tuple=(),title='',font='微软雅黑 10',fg='#A8A8A8',bg=''）

- widgets::需要标题框囊括的画布对象
- title::标题
- font::字体
- fg::边框及标题颜色
- bg::背景色

绘制一个标题框，以包含所制定的所有画布对象。

### return: label, back, outline, uid

> label::标题文本
> 
> back::背景元素
> 
> outline::边框元素

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI%E6%A0%87%E9%A2%98%E8%BE%B9%E6%A1%86.gif)

---

### add_waitbar2(self,pos:tuple,width:int=200,fg='#3041d8',bg='#f3f3f3',okcolor='#0f7b0f',anchor='nw')

- pos::位置
- width::宽度
- fg::点状颜色
- bg::背景颜色
- okcolor::完成时背景填充颜色
- anchor::对齐方向

绘制一个点状运动的等待框。

### return: back, balls:list, stop, uid

> back::背景矩形画布对象
> 
> balls::五个圆形画布对象的列表
> 
> stop::停止等待动画的函数。当你完成你需要等待的任务后，你可以调用此函数，停止等待动画

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI%E7%AD%89%E5%BE%852.gif)

---

### add_combobox(self,pos:tuple,width:int=200,height:int=200,text='',content:tuple=(),fg='#1a1a1a',bg='#f8f8f8',outline='#c8c8c8',activefg='#191919',activebg='#f1f1f1',scrollbg='#f0f0f0',scrollcolor='#999999',scrollon='#89898b',tran='#01FF11',font=('微软雅黑',12),anchor='nw',command=None)

- pos::位置
- width::组合框显示区宽度
- height::下拉框高度
- text::组合框显示区初始文字
- content::拥有组合框所包含的内容的元组
- fg::组合框文本、边框颜色
- bg::组合框背景色
- outline::下拉框边框颜色
- activefg::组合框选定时文本、边框颜色
- activebg::组合框选定时文本、边框背景色
- scrollbg::滚动条背景色
- scrollcolor::滚动条颜色
- scrollon::滚动条标识颜色
- font::字体
- anchor::对齐方向
- command::当某一刻选择框被点击回调的函数。该函数需要接受一个参数：该选项框的文本内容。

绘制一个组合框。

### return: main, back, bar, funcs, uid

> main::显示框文字
> 
> back::显示框背景
> 
> bar::载有选项listview控件的BasicTinUI
> 
> funcs
> 
> > `funcs[0]|funcs.select(num)`::选定选值，第一个值是0
> > 
> > `funcs[1]|funcs.disable(fg='#9d9d9d',bg='#f5f5f5')`::禁用
> > 
> > `funcs[2]|funcs.active()`::激活

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI%E7%BB%84%E5%90%88%E6%A1%86.gif)

---

### add_progressbar(self,pos:tuple,width=250,fg='#868686',bg='#334ac0',back='#f3f3f3',fontc='#79b8f8',percentage=True,text='',anchor='nw')

- pos::位置
- width::宽度
- fg::边框颜色
- bg::填充颜色
- back::未被填充的背景颜色
- fontc::字体颜色
- percentage::是否显示进度文本，如果为False，则显示参数text的内容
- text::当不显示进度文本时，进度条上的文本内容
- anchor::对齐方向

绘制一个进度条。

不提供进度动画，动画效果需要自己实现，参考 `TinUI.py`的 `test4()`函数。

### return: back, pro_tagname, text, goto, funcs, uid

> back::背景矩形边框
> 
> pro_tagname::进度框矩形所代表的tag名称
> 
> text::进度条文本
> 
> goto::改变进度：goto(num:int)，其中，num∈[0,100]。这将改变组件进度指示
> 
> funcs
> 
> > `funcs[0]|funcs.now_running()`::恢复常规样式
> > 
> > `funcs[1]|funcs.now_paused(fg='#868686',bg='#9d5d00',fontc='#cdcdcd')`::改为暂停样式
> > 
> > `funcs[2]|funcs.now_error(fg='#868686',bg='#c42b1c',fontc='#cdcdcd')`::改为因错误暂停样式

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI进度条.gif)

---

### add_table(self,pos:tuple,outline='#E1E1E1',fg='black',bg='white',data=[['1','2','3'],['a','b','c']],minwidth=100,maxwidth=300,font=('微软雅黑',12),headbg='#d9ebf9',anchor='nw')

- pos::位置
- outline::边框颜色
- fg::文本颜色
- bg::文本背景颜色
- data::表格数据。格式：((title,...,...),(content1,...,...),(content2,...,...),...)
- minwidth::单元格最小宽度
- maxwidth::单元格最大宽度
- font::字体
- headbg::表头背景色
- anchor::对齐方向

绘制一个表格。

### return: uid

> 表格组件绘制较复杂，涉及到列宽度、行最大高度等内容，目前只返回整体画布tag

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI表格.gif)

---

### add_onoff(self,pos:tuple,fg='#575757',bg='#e5e5e5',onfg='#FFFFFF',onbg='#3041d8',anchor='nw',command=None)

- pos::位置
- fg::关闭状态下的文本、边框颜色
- bg::关闭状态下的背景颜色
- onfg::开启状态下的文本颜色
- onbg::开启状态下的边框、背景颜色
- anchor::对齐方向
- command::当被点击时调用的函数，函数只有一个参数：布尔值。调用参数True表示开启，False表示关闭

绘制一个开关。

### return: state, back, outline, funcs, uid

> state::开关标识符
> 
> back::背景
> 
> outline::边框，与背景为同一个类型，比背景尺寸稍大
> 
> funcs
> 
> > `funcs.on`::开启
> > 
> > `funcs.off`::关闭
> > 
> > `funcs.active`::启用
> > 
> > `fucns.disable(dfg='#f0f0f0',dbg='#bfbfbf')`::禁用

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI开关.gif)

---

### add_spinbox(self,pos:tuple,width=150,data=('1','2','3'),now='',fg='#1b1b1b',bg='#fefefe',line='#e5e5e5',activefg='#1a1a1a',activebg='#fafafa',onfg='#868686',onbg='#f3f3f3',boxfg='#5f5f5f',boxbg='#f9f9f9',boxactivefg='#5b5b5b',boxactivebg='#f0f0f0',font=('微软雅黑',12),anchor='nw',command=None)

- pos::位置
- width::宽度
- data::可选值的内容。格式：(ele1,ele2,ele3...)
- now::当前显示值。如果为空或不在data中，则显示第一个值
- fg::文本颜色
- bg::输入框背景色
- activefg::按钮响应文本颜色
- activebg::按钮响应背景色
- onfg::点击时按钮文本颜色
- onbg::点击时按钮背景色
- boxactivefg::响应鼠标进入按钮文本颜色
- boxactivebg:: 响应鼠标进入按钮背景色
- boxfg:: 按钮文本颜色
- boxbg:: 按钮背景颜色
- font::输入框字体，同时会影响按钮字体
- anchor::对齐方向
- command::选值时响应的函数，必须接受一个参数，这个参数是当前选定的值

> `command`返回值为 `string:TinUIString`，`string`为值本身，来自于 `data`。
> 
> `string.num`为值在 `data`中的索引，从 `0`开始。

绘制一个选值框。

### return: wentry, button1, button2, back, outline, button, uid

> wentry::输入框组件
> 
> button1::上调按钮
> 
> button2::下调按钮
> 
> back::背景元素
> 
> outline::边框元素
> 
> button::打开调节框的按钮

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI选值框.gif)

---

### add_scalebar(self,pos:tuple,width=200,fg='#4554dc',activefg='#4554dc',bg='#868686',buttonbg='#ffffff',buttonoutline='#cccccc',data=(1,2,3,4,5),start=1,anchor='nw',command=None)

- pos::位置
- width::长度（宽度）
- fg::选值覆盖部分颜色
- activefg::滑动按钮激活颜色
- bg::选值未覆盖部分颜色
- buttonbg::按钮背景色
- buttonoutline::按钮边框色
- data::选值范围
- start::初始位置，第一个位置是0，第二个位置是1……
- command::选值完成后调用该函数，必须接受一个参数，这个参数为data中的一个值

绘制一个滑动调节框。

### return: name, back, button, funcs, uid

> name::选值覆盖区域的tag名称
> 
> back::选值未覆盖区域的画布对象
> 
> button::选值滑动按钮
> 
> funcs
> 
> > `funcs[0]|funcs.select(num)`::选定选值，第一个值是0
> > 
> > `funcs[1]|funcs.disable()`::禁用
> > 
> > `funcs[2]|funcs._active()`::激活

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI调节框.gif)

---

### add_info(self,pos:tuple,info='info',font='微软雅黑 9',fg='#0078d4',bg='white',info_text='',info_font=('微软雅黑','12'),info_width=200,info_fg='black',width=400,anchor='nw')

- pos::位置
- font::标识符字体
- fg::标识符颜色
- bg::气泡提示组件背景色
- info_text::提示文本
- info_font::提示文本字体
- info_width::提示文本每一行的宽度
- info_fg::提示文本颜色
- width::文本宽度
- anchor::对齐方向

绘制一个气泡提示框组件。

### return: text, back, uid

> text::标识符文本
> 
> back::标识符背景边框

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI气泡提示.gif)

---

### add_menubar(self,cid='all',bind='\<Button-3\>',font='微软雅黑 12',fg='#1b1b1b',bg='#fbfbfc',line='#cccccc',activefg='#191919',activebg='#f0f0f0',activeline='#f0f0f0',cont=(('command',print('')),'-'),tran='#01FF11')

- cid::绑定的画布对象
- bind::绑定事件的类型
- font::菜单字体
- fg::字体颜色
- bg::背景颜色
- line::边框颜色，分割线颜色
- activefg::选定时字体颜色
- activebg::选定时菜单选项颜色
- activeline::选定时菜单选项边框颜色
- cont::菜单内容
- tran::透明色

> cont的格式如下：
> 
> ```
> (('名称',绑定的函数（接受event参数）),#常规格式
> '-',#分割线
> ...,
> )
> ```

为绑定的画布对象被指定事件激活后，显示菜单。

### return: menu, bar, funcs

> menu::菜单窗口（Toplevel）
> 
> bar::菜单窗口中的TinUI
> 
> funcs::所有菜单按钮的函数集，每一个元素为每一个TinUI按钮的函数集

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI菜单.gif)

---

### add_tooltip(self,uid,text='',fg='#3b3b3b',bg='#e7e7e7',outline='#3b3b3b',font='微软雅黑 12',tran='#01FF11',delay=0,width=400)

- uid::画布对象
- text::提示文本
- fg::字体颜色
- bg::背景色
- outline::边框颜色
- font::字体
- tran::透明色
- delay::延时显示时间，以秒为单位
- width::文本宽度

绘制一个信息提示窗口。

### return: get_return

> get_return::函数，获取toti（提示窗口）和bar（其中的TinUI）

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI窗口提示.gif)

---

### add_back(self,pos:tuple,uids:tuple=(),fg='',bg='',linew=0)

- pos::起始位置，可用(0,0)忽略
- uids::包含的所有画布对象，优先考虑该参数，若只有一个元素，使用 `(id,)`表示
- fg::边框颜色
- bg::背景色
- linew::边框宽度

绘制一个背景框或间隔框，优先考虑 `uids`参数。

### return: back

> 效果见tooltip控件中绑定的label控件背景。

---

### add_waitbar3(self,pos:tuple,width:int=200,fg='#3041d8',bg='#f3f3f3',okcolor='#0f7b0f',anchor='nw')

- pos::起始位置
- width::宽度
- fg::动画块颜色
- bg::背景色
- okcolor::完成时的颜色
- anchor::对齐方向

绘制一个带状等待框。

### return: back, bar, stop, uid

> back::背景框
> 
> bar::动画块
> 
> stop::停止等待动画的函数。当你完成你需要等待的任务后，你可以调用此函数，停止等待动画

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI等待3.gif)

---

### add_textbox(self,pos:tuple,width:int=200,height:int=200,text:str='',anchor='nw',font='微软雅黑 12',fg='black',bg='white',linew=3,scrollbar=False,outline='#63676b',onoutline='#3041d8',scrollbg='#f0f0f0',scrollcolor='#999999',scrollon='#89898b')

- pos::起始位置
- width::宽度
- height::高度
- text::预置文本
- anchor::对齐方向
- font::字体
- fg::文本
- bg::背景色
- linew::边框宽度
- scrollbar::是否添加纵向滚动条
- outline::边框颜色
- onoutline::响应鼠标边框颜色
- scrollbg::滚动条背景色
- scrollcolor::滚动条颜色
- scrollon::滚动条响应颜色

绘制一个文本编辑框。

### return: textbox, funcs, uid

> textbox::Text控件
> 
> funcs
> 
> > `funcs.get(start='1.0',end='end')`::获取输入
> > 
> > `funcs.delete(start='1.0',end='end')`::删除内容
> > 
> > `funcs.config(**kw)`::设置Text属性

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI文本框.gif)

---

### add_scrollbar(self,pos:tuple,widget,height:int=200,direction='y',bg='#f0f0f0',color='#999999',oncolor='#89898b')

- pos::起始位置
- widget::绑定滑动的组件，Text、Canvas、Treeview、Listbox等
- height::长度
- direction::方向，x或y，大小写无关
- bg::背景色
- color::滚动条闲置颜色
- oncolor::滚动条激活颜色

为显示区域可变的组件绘制一个滚动条。

### return: top, bottom, back, sc, uid

> top::上（左）标识
> 
> bottom::下（右）标识
> 
> back::背景
> 
> sc::滚动块

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI滚动条.gif)

---

### add_listbox(self,pos:tuple,width:int=200,height:int=200,font='微软雅黑 12',data=('a','b','c'),bg='#f2f2f2',fg='black',activebg='#e9e9e9',sel='#b4bbea',scrollbg='#f0f0f0',scrollcolor='#999999',scrollon='#89898b',anchor='nw',command=None)

- pos::起始位置
- width::列表框宽度而非框架宽度
- height::列表框高度而非框架高度
- font::字体
- data::选项
- bg::背景颜色
- fg::文本颜色
- activebg::响应鼠标背景色
- sel::被选中的背景颜色
- scrollbg::滚动条背景色
- scrollcolor::滚动条颜色
- scrollon::滚动条响应颜色
- anchor::对齐方式
- command::回调函数，必须接受一个选项参数 `result`
  - 这个参数来自data，使用 `result.index`获取该选项当前的位置，仅对触发时准确

绘制一个列表框。

### return: box, allback, funcs, uid

> box::绘制列表框功能区的BasicTinUI
>
> allback::背景元素
>
> funcs
>
> > `funcs.add(text:str)`::在尾部添加新选项
> >
> > `funcs.delete(index:int)`::删除指定序数的元素，第一个元素序号为0
> >
> > `funcs.clear()`::清空

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI列表框.gif)

---

### add_canvas(self,pos:tuple,width:int=200,height:int=200,bg='white',outline='#808080',scrollbg='#f0f0f0',scrollcolor='#999999',scrollon='#89898b',linew=1,scrollbar=False,anchor='nw')

- pos::位置
- width::宽度
- height::高度
- bg::背景颜色
- outline::边框颜色
- scrollbg::滚动条背景色
- scrollcolor::滚动条颜色
- scrollon::滚动条响应颜色
- linew::边框宽度
- scrollbar::是否添加滚动条
- anchor::对齐方位

绘制一个画布。

### return: canvas, re_scrollregion, uid

> canvas::画布组件
> 
> re_scrollregion::刷新滚动范围，标记为“all”

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI画布.gif)

---

### add_ui(self,pos:tuple,width:int=200,height:int=200,bg='white',scrollbg='#f0f0f0',scrollcolor='#999999',scrollon='#89898b',scrollbar=False,region='man',anchor='nw')

- pos::位置
- width::宽度
- height::高度
- bg::背景颜色
- scrollbg::滚动条背景色
- scrollcolor::滚动条颜色
- scrollon::滚动条响应颜色
- scrollbar::是否添加滚动条
- region::范围控制，手动“man”或自动“auto”
- anchor::对齐方位

添加一个内嵌BasicTinUI。

### return: ui, re_scrollregion, ui_xml, uid

> ui::BasicTinUI类
> 
> re_scrollregion::刷新滚动范围，如果 `region`参数为“auto”可忽略
> 
> ui_xml::该BasicTinUI类的TinUIXml绑定

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI内置ui.gif)

---

### add_pipspager(self,pos:tuple,width:int=200,height:int=200,bg='#f3f3f3',fg='#898989',buttonfg='#8a8a8a',buttonbg='#f9f9f9',activefg='#5f5f5f',activebg='#f9f9f9',buttononfg='#5f5f5f',buttononbg='#f9f9f9',num:int=2)

- pos::位置
- width::主视图宽度
- height::主视图高度
- bg::背景颜色
- fg::导航栏前景色
- buttonfg:: 按钮文本颜色
- buttonbg::按钮背景颜色
- activefg::响应时按钮文本颜色
- activebg::响应时按钮背景色
- buttononfg:: 点击时按钮文本颜色
- buttononbg:: 点击时按钮背景颜色
- num::视图数量

绘制一个横向翻页视图。

### return: uilist, dotlist, move_to, uid

> uilist::视图列表结构。`[(id-1,tinui-1,tinuixml-1),...]`
> 
> dotlist::导航栏列表结构。`[dot_id-1,...]`
> 
> move_to::需要一个数字参数num，转到第num个视图，第一个视图num为0

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI横向翻页视图.gif)

---

### add_notebook(self,pos:tuple,width:int=400,height:int=400,color='#f3f3f3',fg='#5d5d5d',bg='#f3f3f3',activefg='#595959',activebg='#e9e9e9',onfg='#1a1a1a',onbg='#f9f9f9',scrollbg='#f0f0f0',scrollcolor='#999999',scrollon='#89898b')

- pos::位置
- width::页面宽度
- height::页面高度
- color::视图背景色
- fg::文本颜色
- bg::标签栏标签颜色
- activefg::鼠标进入时提示色
- activebg::鼠标进入时提示色
- onfg::被点击时激活色
- onbg::被点击时激活色
- scrollbg::滚动条背景色
- scrollcolor::滚动条标识符颜色
- scrollon::滚动条响应时颜色

绘制一个标签栏视图。

### return: tbu, scro, back, notebook, uid

> tbu::标签栏BasicTinUI
> 
> scro::滚动条TinUI返回值
> 
> back::背景元素
> 
> notebook::TinUINum函数结构体
> 
> > notebook.addpage(title,flag=None,scrollbar=False,cancancel=True)->flag
> > 
> > `title`标签栏标签标题
> > 
> > `flag`标识符，如果没有给定，会自动生成并返回
> > 
> > `scrollbar`是否使用TinUI，默认BasicTinUI
> > 
> > `cancancel`该页面是否能被删除
> > 
> > notebook.showpage(flag)
> > 
> > `flag`需要显示的页面的标识符
> > 
> > notebook.deletepage(flag)
> > 
> > `flag`需要删除的页面的标识符
> > 
> > notebook.getuis(flag)->(tinui,uixml,uiid)
> > 
> > `flag`页面标识符。返回TinUI组件、TinUIXml绑定、组件的画布对象
> > 
> > notebook.gettitles(flag)->(title,cb,bu)
> > 
> > `flag`页面标识符。返回标题tbu对象、删除键tbu对象、标签tbu对象
> > 
> > notebook.getvdic()->vdict
> > 
> > 返回页面字典
> > 
> > notebook.gettbdict()->tbdict
> > 
> > 返回标签栏字典
> > 
> > notebook.cannew(can=False,newfunc=None)
> > 
> > `can`是否响应&显示新界面按钮
> > 
> > `newfunc`响应函数，如果为None则不执行
> > 
> > notebook.newtitle(flag,title_text='')
> > 
> > `flag`需要更换标题的页面的标识符
> > 
> > `title_text`新标题文本

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI标签栏视图.gif)

---

### add_ratingbar(self,pos:tuple,fg='#585858',bg='#f3f3f3',onfg='#3041d8',onbg='#3041d8',size=12,num:int=5,linew:int=10,command=None)

- pos::位置
- fg::边框颜色
- bg::星级色
- onfg::激活时星级边框
- onbg::激活时星级色
- size::星级字符大小
- num::总共的星级数量
- linew::每一行有多少的星级
- command::回调函数，必须接受一个参数，星级个数（1~...）

绘制一个评星级控件。

### return: bars, uid

> bars::评星级元素列表
> 
> 当只选定一个星级，再次选择第一个星级时，取消选择，command个数为0

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI评星级控件.gif)

---

### add_radiobox(self,pos:tuple,fontfg='black',font='微软雅黑 12',fg='#8b8b8b',bg='#ededed',activefg='#898989',activebg='#e5e5e5',onfg='#3041d8',onbg='#ffffff',content:tuple=('1','','2'),padx=15,pady=10,anchor='nw',command=None)

- pos::位置
- fontfg::文本颜色
- fg::标识符边框颜色
- bg::标识符背景颜色
- activefg::鼠标进入标识符边框颜色
- activebg::鼠标进入标识符背景颜色
- onfg::选定标识符边框颜色
- onbg::选定标识符背景颜色
- content::选择文本内容。如果为空字符串则代表换行
- padx::水平间距
- pady::行间距
- anchor::对齐方向
- command::回调函数，必须接受一个参数，所选选项的文本

绘制一个单选组控件。

### return: boxes, funcs, uid

> boxes::元素组：(标识符背景, 标识符, 文本, 背景元素)
>
> funcs
>
> > `funcs.active()`::激活控件
> >
> > `funcs.disable(fg='#c1c1c1',bg='#f3f3f3')`::禁用控件
> >
> > `funcs.select(index)`::选中第几个参数

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI单选组控件.gif)

---

### add_notecard(self,pos:tuple,title='note',text='note text\nmain content',tfg='black',tbg='#fbfbfb',fg='black',bg='#f4f4f4',sep='#e5e5e5',width=200,font='微软雅黑 12')

- pos::位置
- title::标题文本
- text::内容文本
- tfg::标题文本颜色
- tbg::标题背景色
- fg::内容文本颜色
- bg::内容背景色
- sep::边框、分割线颜色
- width::文本宽度
- font::字体

绘制一个可拖动的便笺。

### return: toptext, content, uid

> toptext::标题文本
> 
> content::内容文本

![](https://raw.githubusercontent.com/Smart-Space/TinUI/main/image/TinUI%E4%BE%BF%E7%AC%BA.gif)

---

### add_pivot(self,pos:tuple,fg='#959595',bg='',activefg='#525252',activecolor='#5969e0',content=(('a-title','tag1'),('b-title','tag2'),'',('c-title','tag3')),font='微软雅黑 16',padx=10,pady=10,anchor='nw',command=None)

- pos::位置
- fg::字体颜色
- bg::保留参数，忽略
- activefg::字体激活颜色
- activecolor::提示色
- content::内容，（文本，标签）
- font::字体
- padx::横方向间距
- pady::纵方向间距
- anchor::对齐方向
- command::响应函数，必须接受一个参数，所选选项的标签

绘制一个支点标题。

### return: texts, uid

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI支点标题.gif)

---

### add_button2(self,pos:tuple,text:str,icon=None,compound='left',fg='#1b1b1b',bg='#fbfbfb',line='#CCCCCC',linew=1,activefg='#5d5d5d',activebg='#f5f5f5',activeline='#cccccc',onfg='#5d5d5d',onbg='#f5f5f5',online='#e5e5e5',font=('微软雅黑',12),minwidth=0,maxwidth=0,command=None,anchor='nw')

- pos::位置
- text::标题文字
- icon::Segoe Fluent Icons符号编号，为None忽略
- compound::存在icon时，文本相对于符号的位置，left, right, top, bottom
- fg::文字颜色
- bg::按钮颜色
- line::边框颜色
- linew::边框宽度
- activefg::响应鼠标的文本颜色
- activebg::响应鼠标的按钮颜色
- activeline::响应鼠标的边框颜色
- onfg::鼠标点击时文本颜色
- onbg::鼠标点击时按钮颜色
- online::鼠标点击时边框颜色
- font::字体名称+大小
- minwidth::最小宽度，为0忽略
- maxwidth::最大宽度，为0忽略
- command::绑定的函数。该函数**必须要有event参数**，因为TinUI的按钮会传递点击事件的event
- anchor::对齐方向

绘制一个圆角按钮。

### return: button, back, outline, funcs, uid

> button::按钮文本
> 
> back::背景元素
> 
> outline::边框元素
> 
> funcs
> 
> > funcs.change_command(new_func)
> > 
> > `new_func`切换的新函数
> > 
> > funcs.disable(fg='#9d9d9d',bg='#f5f5f5')
> > 
> > 禁用按钮
> > 
> > funcs.active()
> > 
> > 激活按钮

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI按钮2.gif)

---

### add_expander(self,pos:tuple,title='expand content',tfg='black',tbg='#fbfbfb',bg='#f4f4f4',sep='#e5e5e5',buttonfg='#1b1b1b',buttonbg='#fbfbfb',buttonline='#fbfbfb',activefg='#1a1a1a',activebg='#f2f2f2',activeline='#f2f2f2',onfg='#1a1a1a',onbg='#f5f5f5',online='#f5f5f5',width=200,height=200,scrollbar=False,font='微软雅黑 12')

- pos::位置
- title::标题
- tfg::标题颜色
- tbg::标题背景色
- bg::UI颜色
- sep::大背景色、分割线颜色
- buttonfg:: 按钮文本颜色
- buttonbg:: 按钮背景颜色
- buttonline:: 按钮边框颜色
- activefg:: 按钮响应鼠标文本颜色
- activebg:: 按钮响应鼠标背景颜色
- activeline:: 按钮响应鼠标边框颜色
- onfg:: 按钮点击时文本颜色
- onbg:: 按钮点击时背景颜色
- online:: 按钮点击时边框颜色
- width::控件宽度，文本宽度为
- height::UI高度
- scrollbar::是否添加滚动条（是否使用TinUI）
- font::标题字体

绘制一个可折叠UI。

### return: toptext, ui, ux, uid

> toptext::标题文本
> 
> ui::BasicTinUI或TinUI
> 
> ux::绑定到UI的TinUIXml

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI可折叠UI.gif)

---

### add_waitframe(self,pos:tuple,width=300,height=300,fg='#e0e0e0',bg='#ececee',anchor='nw')

- pos::位置
- width::宽度
- height::盖度
- fg::前景色
- bg::背景色
- anchor::对齐方向

绘制一个元素等待框。

### return: frame, itemfg, itembg, funcs, uid

> frame::元素框控件（BasicTinUI）
> 
> itemfg::标识元素1
> 
> itembg::标识元素2
> 
> funcs
> 
> > `funcs.start()`::开启等待覆盖
> > 
> > `funcs.end()`::结束等待覆盖

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI元素等待框.gif)

---

### add_listview(self,pos:tuple,width=300,height=300,linew=80,bg='#f3f3f3',activebg='#eaeaea',oncolor='#3041d8',scrobg='#f8f8f8',scroc='#999999',scrooc='#89898b',num=5,command=None)

- pos::位置
- width::宽度
- height::高度
- linew::单元素高度
- bg::背景色
- activebg::响应鼠标提示色
- oncolor::选中提示色
- scrobg::滚动条背景色
- scroc::滚动条颜色
- scrooc::滚动条提示色
- num::元素数量
- command::选定时响应函数，需要一个参数：选中项的位次，从0开始

绘制一个列表视图。

### return: ui, scro, items, funcs, uid

> ui::列表框架BasicTinUI
>
> scro::滚动条返回值，`add_scrollbar`
>
> items::元素列表，每个元素为ui返回值，`add_ui`。进返回初始元素列表
>
> funcs
>
> > `funcs.getitems()`获取当前所有元素列表
> >
> > `funcs.getui(index)`获取index对应的`add_ui`返回值
> >
> > `funcs.delete(index)`删除index位的UI元素
> >
> > `funcs.add()`在末尾追加新元素，并且返回`add_ui`返回值
> >
> > `funcs.clear()`清除所有元素

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI列表视图.gif)

---

### add_treeview(self,pos:tuple,fg='#1a1a1a',bg='#f3f3f3',onfg='#1a1a1a',onbg='#eaeaea',oncolor='#3041d8',signcolor='#8a8a8a',width=200,height=300,font='微软雅黑 12',content=(('one',('1','2','3')),'two',('three',('a',('b',('b1','b2','b3')),'c')),'four'),command=None)

- pos::位置
- fg::文本颜色
- bg::背景色
- onfg::选中时文本颜色
- onbg::选中时元素背景色
- oncolor::标识符颜色
- signcolor::滚动条提示色
- width::宽度
- height::高度
- font::字体
- content::内容数据。`(一级,一级,(一级,(二级)),一级)`可嵌套
- command::回调函数，需要一个参数：选中项id的级次从属列表

绘制一个树状图。

### return: items, items_dict, box, uid

> items::所有元素id对应的文本id、背景id，以及可能的伸缩提示文本id的字典
> 
> items_dict::所有含子级元素id对应下一级id的字典
> 
> box::作为树状图父组件的BasicTinUI

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI树状图.gif)

---

### add_image(self,pos:tuple,width=None,height=None,state='fill',imgfile=None,anchor='nw')

- pos::位置
- width::宽度（默认为图片宽度）
- height::高度（默认为图片高度）
- state::尺寸状态（none左上角裁剪，fill填充，uniform等比缩放）
- imgfile::图片文件，支持静态gif和png
- anchor::对齐方向

绘制一个静态图片。

### return: img

> img::图片画布对象，相当于大多数的 `uid`

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI图片1.gif)

---

### add_togglebutton(self,pos:tuple,text:str,fg='#1b1b1b',bg='#fbfbfb',line='#CCCCCC',linew=1,activefg='#f3f4fd',activebg='#3041d8',activeline='#5360de',font=('微软雅黑',12),command=None,anchor='nw')

- pos::位置
- text::文本
- fg::文本颜色
- bg::背景色
- line::边框颜色
- linew::边框宽度
- activefg::开启状态文本颜色
- activebg::开启状态背景色
- activeline::开启状态边框颜色
- font::字体
- command::响应函数，接受一个参数：`True`开启，`False`关闭
- anchor::对齐方向

绘制一个状态开关按钮。

### return: button, back, outline, funcs, uid

> button::文本元素
> 
> back::背景元素
> 
> outline::边框元素
> 
> funcs
> 
> > `funcs.change_command()`::更换响应函数
> > 
> > `funcs.disable(fg='#9d9d9d',bg='#f5f5f5')`::禁用
> > 
> > `funcs.active()`::启用

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI状态开关按钮.gif)

---

### add_swipecontrol(self,pos:tuple,text:str='',height=50,width=400,fg='#1a1a1a',bg='#f3f3f3',line='#fbfbfb',data:dict=,),'right':(,)},font=('微软雅黑',12),anchor='nw')

- pos-位置

- text-文本

- height-高度

- width-宽度

- fg-文本颜色

- bg-背景色

- line-边框颜色

- data-滑动操作元素参数
  
  > data结构：
  > 
  > ```json
  > {
  >     'left':({
  >         'text':'文本',
  >         'fg':'文本颜色',
  >         'bg':'背景颜色',
  >     },
  >             ...,
  >            ),
  >     'right':({
  >         'text':'文本',
  >     },
  >              ...,
  >     )
  > }
  > ```
  > 
  > 其中，字典键值 `left`表示往右滑动显示的左边元素，`right`表示往左滑动显示的右边元素。两者皆可选。
  > 一侧元素以一个数组表示，一个及以上，不超过六个。每个元素以字典表示，文本必选，颜色有默认值。

- font-字体

- anchor-对齐方向

绘制一个滑动控件。

### return: back, backitem

> back::容器BasicTinUI
> 
> backitem::控件的画布元素

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI滑动控件.gif)

---

### add_passwordbox(self,pos:tuple,width:int,fg='#606060',bg='#f6f6f6',activefg='#1b1b1b',activebg='#ffffff',line='#e5e5e5',activeline='#e5e5e5',insert='#808080',font=('微软雅黑',12),outline='#868686',onoutline='#3041d8',anchor='nw',command=None)

- pos-位置
- width-宽度
- fg-文本颜色
- bg-背景色
- activefg-响应时文本颜色
- activebg-响应时背景颜色
- line-边框颜色
- activeline-响应式边框颜色
- insert-光标颜色
- font-字体
- outline-提示线颜色
- onoutline-响应时提示线颜色
- anchor-对齐方向

绘制一个密码输入框。

### return: entry, funcs, uid

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI密码输入框.gif)

---

### add_picker(self,pos:tuple,height=250,fg='#1b1b1b',bg='#fbfbfb',outline='#ececec',activefg='#1b1b1b',activebg='#f6f6f6',onfg='#eaecfb',onbg='#3748d9',buttonfg='#1a1a1a',buttonbg='#f9f9f9',buttonactivefg='#1a1a1a',buttonactivebg='#f3f3f3',font=('微软雅黑',10),text=(('year',60),('season',100),),data=(('2022','2023','2024'),('spring','summer','autumn','winter')),tran='#01FF11',anchor='nw',command=None)

- pos-位置
- height-选择框高度
- fg-文本颜色
- bg-背景色
- outline-边框色
- activefg-选择时文本颜色
- activebg-选择时背景颜色
- onfg-选定时文本颜色
- onbg-选定时背景颜色
- buttonfg-按钮文本颜色
- buttonbg-按钮背景颜色
- buttonactivefg-按钮相应鼠标文本颜色
- buttonactivebg-按钮响应鼠标背景颜色
- font-字体
- text-文本内容，需要与 `data`对应。`((选值文本,元素宽度),...)`
- data-选值内容，需要与 `text`对应
- tran-透明处理规避颜色
- anchor-对齐方向
- command-响应接受函数。需要接受一个参数：所有选值列表，全被选定时触发

绘制一个滚动选值框。

### return: picker, bar, texts, pickerbars, uid

> picker::选择器所在的窗口
> 
> bar::选择器所在的BasicTinUI
> 
> texts::文本元素列表
> 
> pickerbars::元素选择BasicTinUI列表

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI滚动选择框.gif)

---

### add_menubutton(self,pos:tuple,text:str,side='y',fg='#1b1b1b',bg='#fbfbfb',line='#CCCCCC',linew=1,activefg='#1a1a1a',activebg='#f6f6f6',activeline='#cccccc',onfg='#5d5d5d',onbg='#f5f5f5',online='#e5e5e5',menuonfg='#191919',menuonbg='#f0f0f0',menuonline='#f0f0f0',font=('微软雅黑',12),cont=(('command',print),'-'),widget=True,tran='#01FF11')

- pos-位置
- text-文本
- side-展开方向。y：向下展开；x：向右展开
- fg-文本颜色
- bg-背景色
- line-边框颜色
- linew-边框宽度
- activefg-响应状态文本颜色
- activebg-响应状态背景色
- activeline-响应状态边框颜色
- onfg-点击时文本颜色
- onbg-点击时背景颜色
- online-点击时边框颜色
- menuonfg-菜单选项响应文本颜色
- menuonbg-菜单选项响应背景颜色
- menuonline-菜单选项响应边框颜色
- font-字体
- cont-菜单内容
- widget-是否显示下拉标识符
- tran-透明处理规避色

> cont的格式如下：
> 
> ```
> (('名称',绑定的函数（接受event参数）),#常规格式
> '-',#分割线
> ...,
> )
> ```

绘制一个菜单按钮。

### return: text, back, outline, funcs, uid

> text-文本元素，包括标识文本
> 
> back-背景元素
> 
> outline-边框元素
> 
> funcs
> 
> > funcs.disable(fg='#9d9d9d',bg='#f5f5f5')
> > 
> > 禁用按钮
> > 
> > funcs.active()
> > 
> > 激活按钮

<img src="https://github.com/Smart-Space/TinUI/raw/main/image/TinUI菜单按钮.gif" title="" alt="" data-align="inline">

---

### add_barbutton(self,pos:tuple,font='微软雅黑 14',fg='#636363',bg='#f3f3f3',line='#f3f3f3',linew=0,activefg='#191919',activebg='#eaeaea',activeline='#eaeaea',onfg='#5a5a5a',onbg='#ededed',online='#ededed',sepcolor='#e6e6e6',content=(('保存','\uE74E',None),('','\uE792',None),'',('','\uE74D',None)),anchor='nw')

- pos-位置

- font-字体

- fg-文本颜色

- bg-背景颜色

- line-边框颜色

- linew-边框宽度

- activefg-响应时文本颜色

- activebg-响应时背景色

- activeline-响应时边框颜色

- onfg-点击时文本颜色

- onbg-点击时背景颜色

- online-点击时边框颜色

- sepcolor-分割线颜色

- content-按钮内容
  
  > ```python
  > (
  >  ('text','Segoe Fluent Icons code',command),
  >  ...,
  >  '',#分割线
  >  ('text','Segoe Fluent Icons code',command),
  > )
  > ```
  >
  > 文本和图标参数皆可为空，但至少应该有一个是有值的
  
- anchor-对齐方向

绘制一个工具栏按钮组件。

### return: outline, back, buttons, uid

> outline::边框元素
> 
> back::背景板元素
> 
> buttons::按顺序的所有按钮列表，每一个值为 `add_button2()`的返回值

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI工具栏按钮组件.gif)

---

### add_flyout(self, fid, width:int=250, height:int=150, bind='\<Button-1>', line='#dcdcdc', bg='#f9f9f9', anchor='n')

- fid-需要绑定的控件元素
- width-宽度
- height-高度
- bind-绑定的事件
- line-边框颜色
- bg-背景颜色
- anchor-相对于绑定元素的浮出位置，默认在上方

绘制一个浮出ui控件

### renturn: ui, uixml, hide, uid

> ui::浮出元素BasicTinUI
>
> uixml::绑定在ui上的TinUIXml
>
> hide::窗口关闭函数，接受一个event参数，因此可直接绑定在浮出控件内部的按钮等关闭浮出ui的交互控件的回调

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI浮出ui控件.gif)

---

# Class: BasicTinUI

TinUI的基础类，仅提供组件绘制。

`BasicTinUI`的用法与TinUI完全一致，虽然TinUI基于BasicTinUI，但是TinUI更适合作为窗口主组件，以下是二者区别：

| 项目        | BasicTinUI | TinUI |
| --------- | ---------- | ----- |
| TinUI绘制组件 | √          | √     |
| 自动刷新      | ×          | √     |
| 滚动条支持     | ×          | √     |
| 窗口主组件     | ×          | √     |
| 主窗口       | ×          | √     |
| 区域渲染组件    | √          | ×     |

---

# Class: TinUIDialog

TinUIDialog是一个基础类，使用时无需在意，只需要从tinui包中导入相关对话框函数即可。

```python
from tinui import show_msg
```

不过，`show_msg`是一个“朴素”的信息提示框，一般情况下应当导入以下对话框函数：

```python
from tinui import show_info, show_success, show_error,\
    show_warning, show_question,\
    ask_string, ask_integer, ask_float, ask_choice
"""
上述分别对应：
信息提示
成功提示
警告提示
错误提示
问答提示
文本输入
整数输入
浮点输入
单选输入
"""
```

以 `show_msg`为例。

```python
def show_msg(master,title,content,yestext='OK',notext='Cancel',theme='light'):
    """
    master - 父窗口
    title - 标题
    context - 信息内容
    yestext - 确认文本
    notext - 取消文本
    theme - 样式，'light' or 'dark'
    """
    ...
```

对话框只有在“确认按钮”被点击后才返回交互值。

- 对于信息提示对话框，“取消按钮”返回 `False`，关闭窗口返回 `None`。
- 对于输入对话框，“取消按钮”和关闭窗口均返回 `None`。

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI信息提示对话框.gif)

---

# Class: extension

TinUI拓展工具包，通过`from tinui import extension`导入。

`extension`目前含有如下方法：

## buttonlize(tinui,uid,bg='#fbfbfb',line='#CCCCCC',activebg='#f5f5f5',activeline='#e5e5e5',command=None)

- tinui - TinUI控件所属的TinUI或BasicTinUI

- uid - 元素名称或代码

- bg - 背景颜色

- line - 边框颜色

- activebg - 响应背景色

- activeline - 响应边框颜色

- command - 响应函数

> 注意，如果元素控件组(`uid`)中含有按钮之类的响应点击的控件，点击时会同时触发控件响应函数和该函数。

---

# Class: FuncList

TinUI控件使用的方法列表，既可以当做列表获取返回函数，也可以作为函数整体对象执行单个方法。以button为例：

使用button的禁用方法（已获取 `funcs`返回值）。既可以使用 `funcs[1]()`，也可以使用 `funcs.disable()`。方便使用。

> 本文档中比较久之前的函数返回调用，沿用最初列表式结构说明，具体返回的 `FuncList`类见源码。
> 
> 无论怎样，使用 `funcs.<function-name>`是正确的。

---

# Class: TinUITheme

TinUI自定义配色类。可实例化后直接应用于TinUIXml。

```python
class TinUITheme:
    '''
    专门为特有样式的TinUI或BasicTinUI提供的类
    适用于重写样式配色的TinUI或BasicTinUI
    该类允许重写样式的TinUI或BasicTinUI使用TinUIXml
    '''

    def __init__(self,ui,name='tinui-theme'):
        #ui为TinUI框架
```

使用示例见开源TinUI代码库见 `theme\themelight.py`等。

---

# Class: TinUIWidget

创建一个含单个元素控件的BasicTinUI组件。

```python
class TinUIWidget(BasicTinUI):
    '''提供含单个元素控件的TinUI控件，用来在普通tkinter组件中使用'''

    def __init__(self,master,widget_name='ui',**kw):
        BasicTinUI.__init__(self,master,**kw)
        self.func=eval('self.add_'+widget_name)
        self.width=None
        self.height=None
```

## get_size()

获取元素控件尺寸。

## load(*args,**kw)

根据初始化的 `widget_name`，创建元素控件。

## reupdate()

更新尺寸信息，但不会更改控件大小。

---

# Class: TinUIXml

使用xml语言来绘制TinUI组件，当然，也包括BasicTinUI。

> 当前，`menubar`,`tooltip`等组件不支持使用xml布局。

```python
class TinUIXml():#TinUI的xml渲染方式
    '''为TinUI提供更加方便的平面方式，使用xml
    TinUITheme基类无法直接使用，只能够重写TinUI或BasicTinUI的样式后才能够使用，参考 /theme 中的样式重写范例
    '''

    def __init__(self,ui:Union[BasicTinUI,TinUITheme]):
        #BasicTinUI包括TinUI
        #TinUITheme为样式基础类，继承类也可
```

## 基础类变量

self.funcs::xml中涉及到的函数

通常用与 `command`参数。

self.datas::xml中使用的特殊数据结构

通常用于 `data`等参数，但若数据结构不复杂，可以直接在xml中用字符表示。

> 如 '200'，'("1","2","3","4")'等数据结构可以直接在字符串中表示。

self.tags::内部组件tag集合

用于有目标文本的xml-TinUI组件元素的回调。

> 如 `<button text='test'>bu</button>`可以使用 `*.tags['bu']`获取原组件返回值。

## 基本规则

以下是使用 `TinUIXml`中xml字符串的若干规定：

1. 根元素必须是 `<tinui>`

2. 行元素必须是 `<line>`

3. 根元素的直接子集不能有除了行元素的其它元素

4. 行元素可以嵌套

   > 可以如下写法：
   > 
   > ```xml
   > <tinui>
   > <line>
   >       <button text='one'></button>
   > </line>
   > <line>
   >     <button text='two'></button>
   >     <line>
   >         <button text='three'></button>
   >     </line>
   >     <line>
   >         <button text='four'></button>
   >     </line>
   >     <button text='five'></button>
   > </line>
   > </tinui>
   > ```

5. 所有xml使用的函数需要使用字符串中表述为 `self.funcs[...]`

   > 即：
   > 
   > ```xml
   > <button text='one' command='self.funcs["funcstion"]'></button>
   > ```

6. 若需要，如【5】中类似地使用 `self.datas[...]`

7. 若需要使用**整数**定义宽度参数等，也如同 `width='200'`使用

8. 字体使用如 `font="微软雅黑 12"`的写法

9. 控件下没有其它元素，仅少部分含ui框架的控件允许，详见[tkinter-TinUI使用xml编写界面](https://blog.csdn.net/tinga_kilin/article/details/122740802)

## 基本语法

使用 `TinUIXml`，有特殊的语法和协定，详情见CSDN文章：

[tkinter-TinUI使用xml编写界面](https://blog.csdn.net/tinga_kilin/article/details/122740802)。

## 基础函数

### loadxml(xml:str)

xml::xml语言

通过一定规范的Xml字符串来对TinUI（BasicTinUI）进行渲染操作。

### environment(dict_item:dict)

dict_item::一个字典，建议是 `globals()`或 `locals()`

根据本地变量，快速导入 `funcs`和 `datas`。但这样会缺少规范性。

### clean()

清空绑定的TinUI或BasicTinUI，同时会触发 `ui.clean_windows()`。

## 特殊规则组件

部分组件的xml写法有特殊规定。

- back
- labelframe

部分组件的特殊规定，详情见CSDN文章：

[tkinter-TinUI使用xml的特殊组件](https://blog.csdn.net/tinga_kilin/article/details/122740802#_481)。

# 新想法

- 发送issue至GitHub-TinUI储存库
- 发送邮件至tsan-zane@outlook.com或smart-space@qq.com
