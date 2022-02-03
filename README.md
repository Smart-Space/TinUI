# TinUI

![](https://github.com/Smart-Space/TinUI/raw/main/image/LOGO.png)

## 项目类型

TinUI是一个基于tkinter（Python/tcl/tk）的拓展组件（Widget），可以绘制虚拟组件。

TinUI基于tkinter的画布（Canvas），可以作为整个窗口的唯一控件。TinUI能够通过自身绘制出功能组件和文字，也可以使用画布功能添加组件。使用TinUI，可以使界面设计和代码设计分离，此外，TinUI绘制的虚拟组件速度更快，样式更加丰富。

目前，TinUI可用于常规tkinter窗口开发。

## 依赖

目前，TinUI没有依赖项目。

---

# Class: TinUI(BasicTinUI)

TinUI模块的主类，基于`Class: BasicTinUI`。

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
> - 除了`title`, `paragraph`, `separate`, `menubar`, `labelframe`, `tooltip`, `back`等组件，其余组件的最后一个返回值均为整个组件的画布`tag_name`，返回值变量为`uid`。

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

### add_button(self,pos:tuple,text:str,fg='black',bg='#CCCCCC',line='#CCCCCC',linew=3,activefg='black',activebg='#999999',activeline='#7a7a7a',font=('微软雅黑',12),command=None,anchor='nw')

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
> > `funcs[0](new_func)`::为按钮绑定新函数
> >
> > `funcs[1](fg='#7a7a7a',bg='#cccccc')`::禁用按钮
> >
> > `funcs[2]()`::激活按钮

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

### return: label, uid

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
- command::绑定的函数。该函数**必须要有event参数**，因为TinUI的按钮会传递点击事件的event
- anchor::对齐方向

绘制一个复选框。这个复选框会响应鼠标的离开和进入事件，被单击时也会调用绑定的函数，并且会根据当前样式更改点击后的样式。

### return: check_text, check_mark, funcs, uid

> check_text::复选框文本
>
> check_mark::复选框矩形标记部件
>
> funcs
>
> > `funcs[0]()`::切换复选框状态
> >
> > `funcs[1]()`::选定
> >
> > `funcs[2]()`::取消选定
> >
> > `funcs[3]()`::禁用
> >
> > `funcs[4]()`::激活

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI复选框.gif)

---

### add_entry(self,pos:tuple,width:int,text:str='',fg='black',bg='#cfd3d6',activefg='black',activebg='white',font=('微软雅黑',12),linew=3,outline='#63676b',onoutline='#3041d8',icon='>',anchor='nw')

- pos::位置
- width::宽度
- text::初始文字
- fg::文字颜色
- bg::背景颜色
- activefg::激活时字体颜色
- activebg::激活时背景色
- font::字体
- linew::边框宽度
- outline::输入框边框颜色
- onoutline::获取焦点时的边框颜色
- icon::内容为空时，右侧显示的字符
- anchor::对齐方向

绘制一个单行输入框。这是一个半绘制组件，其实就是简化了Entry控件的导入。

通过`entry.get()`获取值。

### return: entry, uid

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

### add_radiobutton(self,pos:tuple,width,text='',choices=('choose me'),fg='black',bg='white',font=('微软雅黑',12),command=None,anchor='nw')

- pos::位置
- width::整体宽度
- text::单选框文本提示
- choices::选项（list, set, map...）
- fg::文本和边框颜色
- bg::选项背景色
- font::字体
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
> > `funcs[0](num)`::选定一个选项
> >
> > `funcs[1]()`::禁用
> >
> > `funcs[2]()`::激活

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI单选框.gif)

---

### add_link(self,pos:tuple,text,url:Union[str,FunctionType],fg='#4f62ca',activefg='red',activebg='#eaeaea',font:tuple=('微软雅黑',12),anchor='nw')

- pos::位置
- text::网页链接 **或者** 要执行的函数，函数需要接受`event`参数
- url::链接
- fg::文本颜色
- activefg::响应鼠标时文本颜色
- activebg::响应鼠标时背景颜色
- font::字体
- anchor::对齐方向

绘制一个链接文本，指向网页或者执行函数。

### return: link, funcs, uid

![](https://github.com/Smart-Space/TinUI/raw/main/image/%E8%B6%85%E9%93%BE%E6%8E%A5.gif)

> link::链接文本
>
> funcs
>
> > `funcs[0](fg='#b0b0b0')`::禁用链接
> >
> > `funcs[1]()`::恢复链接

---

### add_waitbar1(self,pos:tuple,fg='blue',bg='',okfg='lightgreen',okbg='',bd=2,r=20)

- pos::位置
- fg::边框颜色
- bg::内部填充颜色
- okfg::完成时边框颜色
- okbg::完成时内部填充颜色
- bd::外框宽度
- r::半径

绘制一个扇形等待框。

### return: waitbar1, ok, uid

> waitbar1::该画布对象
>
> ok::停止等待动画的函数。当你完成你需要等待的任务后，你可以调用此函数，停止等待动画

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI%E7%AD%89%E5%BE%851.gif)

---

### add_labelframe(self,widgets:tuple=(),title='',fg='#A8A8A8',bg=''）

- widgets::需要标题框囊括的画布对象
- title::标题
- fg::边框及标题颜色
- bg::背景色

绘制一个标题框，以包含所制定的所有画布对象。

### return: label, frame

> label::标题文本
>
> frame::边框画布对象

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI%E6%A0%87%E9%A2%98%E8%BE%B9%E6%A1%86.gif)

---

### add_waitbar2(self,pos:tuple,width:int=200,fg='grey',bg='white',okcolor='lightgreen')

- pos::位置
- width::宽度
- fg::点状颜色
- bg::背景颜色
- okcolor::完成时背景填充颜色

绘制一个点状运动的等待框。

### return: back, balls:list, stop, uid

> back::背景矩形画布对象
>
> balls::五个圆形画布对象的列表
>
> stop::停止等待动画的函数。当你完成你需要等待的任务后，你可以调用此函数，停止等待动画

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI%E7%AD%89%E5%BE%852.gif)

---

### add_combobox(self,pos:tuple,width:int=200,text='',content:tuple=(),fg='black',bg='white',activefg='#757F87',activebg='#CCE4F7',font=('微软雅黑',12),command=None)

- pos::位置
- width::组合框显示区宽度
- text::组合框显示区初始文字
- content::拥有组合框所包含的内容的元组
- fg::组合框文本、边框颜色
- bg::组合框背景色
- activefg::组合框选定时文本、边框颜色
- activebg::组合框选定时文本、边框背景色
- font::字体
- command::当某一刻选择框被点击回调的函数。该函数需要接受一个参数：该选项框的文本内容。

绘制一个组合框。

### return: main, back, box_tagname, funcs, uid

> main::显示框文字
>
> back::显示框背景
>
> box_tagname::所有选项框的tag名称
>
> funcs
>
> > `funcs[0](num)`::选定选值，第一个值是0
> >
> > `funcs[1]()`::禁用
> >
> > `funcs[2]()`::激活

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI%E7%BB%84%E5%90%88%E6%A1%86.gif)

---

### add_progressbar(self,pos:tuple,width=250,fg='#868686',bg='#334ac0',back='#f3f3f3',fontc='#79b8f8',percentage=True,text='')

- pos::位置
- width::宽度
- fg::边框颜色
- bg::填充颜色
- back::未被填充的背景颜色
- fontc::字体颜色
- percentage::是否显示进度文本，如果为False，则显示参数text的内容
- text::当不显示进度文本时，进度条上的文本内容

绘制一个进度条。

不提供进度动画，动画效果需要自己实现，参考`TinUI.py`的`test4()`函数。

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
> > `funcs[0]()`::恢复常规样式
> >
> > `funcs[1](fg='#868686',bg='#9d5d00',fontc='#cdcdcd')`::改为暂停样式
> >
> > `funcs[2](fg='#868686',bg='#c42b1c',fontc='#cdcdcd')`::改为因错误暂停样式

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI进度条.gif)

---

### add_table(self,pos:tuple,outline='#E1E1E1',fg='black',bg='white',data=[['1','2','3'],['a','b','c']],minwidth=100,font=('微软雅黑',12),headbg='#d9ebf9')

- pos::位置
- outline::边框颜色
- fg::文本颜色
- bg::文本背景颜色
- data::表格数据。格式：((title,...,...),(content1,...,...),(content2,...,...),...)
- minwidth::单元格最小宽度
- font::字体
- headbg::表头背景色

绘制一个表格。

### return: uid

> 表格组件绘制较复杂，涉及到列宽度、行最大高度等内容，目前只返回整体画布tag

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI表格.gif)

---

### add_onoff(self,pos:tuple,fg='#333333',bg='#FFFFFF',onfg='#FFFFFF',onbg='#4258CC',font=('微软雅黑',12),command=None)

- pos::位置
- fg::关闭状态下的文本、边框颜色
- bg::关闭状态下的背景颜色
- onfg::开启状态下的文本颜色
- onbg::开启状态下的边框、背景颜色
- font::字体
- command::当被点击时调用的函数，函数只有一个参数：布尔值。调用参数True表示开启，False表示关闭

绘制一个开关。

### return: state, back, uid

> state::文本内容。“off”或“on”的画布对象

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI开关.gif)

---

### add_spinbox(self,pos:tuple,width=150,data=('1','2','3'),now='',fg='black',bg='',activefg='black',activebg='#E5F1FB',font=('微软雅黑',12),command=None)

- pos::位置
- width::宽度
- data::可选值的内容。格式：(ele1,ele2,ele3...)
- now::当前显示值。如果为空或不在data中，则显示第一个值
- fg::文本颜色
- bg::输入框背景色
- activefg::按钮响应文本颜色
- activebg::按钮响应背景色
- font::输入框字体，同时会影响按钮字体
- command::选值时响应的函数，必须接受一个参数，这个参数是当前选定的值

绘制一个选值框。

### return: wentry, button1, button2, uid

> wentry::输入框组件
>
> button1::上调按钮
>
> button2::下调按钮

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI选值框.gif)

---

### add_scalebar(self,pos:tuple,width=200,fg='#4258cc',activefg='#aeb5d7',bg='#99a3d5',data=(1,2,3,4,5),start=1,command=None)

- pos::位置
- width::长度（宽度）
- fg::选值覆盖部分颜色
- activefg::滑动按钮激活颜色
- bg::选值未覆盖部分颜色
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
> > `funcs[0](num)`::选定选值，第一个值是0
> >
> > `funcs[1]()`::禁用
> >
> > `funcs[2]()`::激活

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI调节框.gif)

---

### add_info(self,pos:tuple,font='微软雅黑 9',fg='#0078d4',bg='white',info_text='',info_font=('微软雅黑','12'),info_width=200,info_fg='black')

- pos::位置
- font::标识符字体
- fg::标识符颜色
- bg::气泡提示组件背景色
- info_text::提示文本
- info_font::提示文本字体
- info_width::提示文本每一行的宽度
- info_fg::提示文本颜色

绘制一个气泡提示框组件。

### return: text, back, infotagname, uid

> text::标识符文本
>
> back::标识符背景边框
>
> infotagname::提示文本以及文本边框背景

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI气泡提示.gif)

---

### add_menubar(self,cid='all',bind='\<Button-3\>',font='微软雅黑 12',fg='#ecf3e8',bg='#2b2a33',activefg='#ecf3e8',activebg='#616161',cont=(('command',print('')),'-'),tran='#01FF11')

- cid::绑定的画布对象
- bind::绑定事件的类型
- font::菜单字体
- fg::字体颜色
- bg::背景颜色
- activefg::选定时字体颜色
- activebg::选定时菜单选项颜色
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

>menu::菜单窗口（Toplevel）
>
>bar::菜单窗口中的TinUI
>
>funcs::所有菜单按钮的函数集，每一个元素为每一个TinUI按钮的函数集

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI菜单.gif)

---

### add_tooltip(self,uid,text='',fg='#3b3b3b',bg='#e7e7e7',font='微软雅黑 12',tran='#01FF11')

- uid::画布对象

- text::提示文本

- fg::字体颜色

- bg::背景色

- font::字体

- tran::透明色


绘制一个信息提示窗口。

### return: toti, bar

> toti::提示窗口（Toplevel）
>
> bar::提示窗口中的TinUI

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI窗口提示.gif)

---

### add_back(self,pos:tuple,uids:tuple=(),fg='',bg='',linew=0)

- pos::起始位置，可用(0,0)忽略

- uids::包含的所有画布对象，优先考虑该参数，若只有一个元素，使用`(id,)`表示

- fg::边框颜色

- bg::背景色

- linew::边框宽度


绘制一个背景框或间隔框，优先考虑`uids`参数。

### return: back

> 效果见tooltip控件中绑定的label控件背景。

---

### add_waitbar3(self,pos:tuple,width:int=200,fg='#3041d8',bg='#f3f3f3',okcolor='lightgreen')

- pos::起始位置
- width::宽度
- fg::动画块颜色
- bg::背景色
- okcolor::完成时的颜色

绘制一个带状等待框。

### return: back, bar, stop, uid

> back::背景框
>
> bar::动画块
>
> stop::停止等待动画的函数。当你完成你需要等待的任务后，你可以调用此函数，停止等待动画

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI等待3.gif)

---

# Class: BasicTinUI

TinUI的基础类，仅提供组件绘制。

`BasicTinUI`的用法与TinUI完全一致，虽然TinUI基于BasicTinUI，但是TinUI更适合作为窗口主组件，以下是二者区别：

| 项目          | BasicTinUI | TinUI |
| ------------- | ---------- | ----- |
| TinUI绘制组件 | √          | √     |
| 自动刷新      | ×          | √     |
| 滚动条支持    | ×          | √     |
| 窗口主组件    | ×          | √     |
| 主窗口        | ×          | √     |
| 区域渲染组件  | √          | ×     |

---

# Class: TinUINum

TinUI中使用数据结构载体，不需要知道。

---

# Class: TinUIXml

使用xml语言来绘制TinUI组件，当然，也包括BasicTinUI。

> 当前，`info`, `menubar`, `labelframe`, `tooltip`等组件不支持使用xml布局。

## 基础类变量

self.funcs::xml中涉及到的函数

通常用与`command`参数。

self.datas::xml中使用的特殊数据结构

通常用于`data`等参数，但若数据结构不复杂，可以直接在xml中用字符表示。

> 如 '200'，'("1","2","3","4")'等数据结构可以直接在字符串中表示。

self.tags::内部组件tag集合

用于有目标文本的xml-TinUI组件元素的回调。

> 如`<button text='test'>bu</button>`可以使用`*.tags['bu']`获取原组件返回值。

## 基本规则

以下是使用`TinUIXml`中xml字符串的若干规定：

1. 根元素必须是`<tinui>`

2. 行元素必须是`<line>`

2. 根元素的直接子集不能有除了行元素的其它元素

3. 行元素可以嵌套

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
    
4. 所有xml使用的函数需要使用字符串中表述为`self.funcs[...]`

    > 即：
    >
    > ```xml
    > <button text='one' command='self.funcs["funcstion"]'></button>
    > ```

5. 若需要，如【5】中类似地使用`self.datas[...]`

7. 若需要使用**整数**定义宽度参数等，也如同`width='200'`使用

6. 字体使用如`font="微软雅黑 12"`的写法

## 基本语法

使用`TinUIXml`，有特殊的语法和协定，详情见CSDN文章：

[tkinter-TinUI使用xml编写界面](https://blog.csdn.net/tinga_kilin/article/details/122740802)。

## 基础函数

### loadxml(xml:str)

xml::xml语言

通过一定规范的Xml字符串来对TinUI（BasicTinUI）进行渲染操作。

### clean()

清空绑定的TinUI或BasicTinUI。

## 特殊规则组件

部分组件的xml写法有特殊规定。

- back

部分组件的特殊规定，详情见CSDN文章：

[tkinter-TinUI使用xml的特殊组件](https://blog.csdn.net/tinga_kilin/article/details/122740802#_481)。