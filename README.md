# TinUI

![](https://github.com/Smart-Space/TinUI/raw/main/image/LOGO.png)

## 项目类型

TinUI是一个基于tkinter（Python/tcl/tk）的拓展组件（Widget），可以绘制虚拟组件。

TinUI基于tkinter的画布（Canvas），可以作为整个窗口的唯一控件。TinUI能够通过自身绘制出功能组件和文字，也可以使用画布功能添加组件。使用TinUI，可以使界面设计和代码设计分离，此外，TinUI绘制的虚拟组件速度更快，样式更加丰富。

目前，TinUI还处于完善阶段。

## 依赖

目前，TinUI没有依赖项目。

---

## 创建TinUI

```python
tinui=TinUI(root,bg='white',update=True,update_time=1000)
'''
update:bool::是否实时更新滚动画面
update_time:int::每次更新滚动画面的间隔（毫秒）
**kw::Canvas的参数
'''
```



---

## 基础函数

> ==一般地==，会将每个函数的名称以及定义、参数内容、函数绘制说明列出来。
>
> 所有函数均会返回主要画布对象。

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

### add_button(self,pos:tuple,text:str,fg='black',bg='#E1E1E1',activefg='black',activebg='#E5F1FB',font=('微软雅黑',12),command=None,anchor='nw')

- pos::位置
- text::标题文字
- fg::文字颜色
- bg::按钮颜色
- activefg::相应鼠标的文本颜色
- activebg::相应鼠标的按钮颜色
- font::字体名称+大小
- command::绑定的函数。该函数**必须要有event参数**，因为TinUI的按钮会传递点击事件的event
- anchor::对齐方向

绘制一个按钮。这个按钮会响应鼠标的离开和进入事件，被单击时也会调用绑定的函数。

### return: button_text, button_back

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

### return: label

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI%E5%A4%8D%E9%80%89%E6%A1%86.gif)

---

### add_checkbutton(self,pos:tuple,text:str,fg='black',fill='lightgreen',font=('微软雅黑',12),command=None,anchor='nw')

- pos::位置
- text::标题文字
- fg::文字颜色
- fill::选中的标识填充
- font::字体名称+大小
- command::绑定的函数。该函数**必须要有event参数**，因为TinUI的按钮会传递点击事件的event
- anchor::对齐方向

绘制一个复选框。这个复选框会响应鼠标的离开和进入事件，被单击时也会调用绑定的函数，并且会根据当前样式更改点击后的样式。

### return: check_text, check_mark

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI%E5%A4%8D%E9%80%89%E6%A1%86.gif)

---

### add_entry(self,pos:tuple,width:int,height:int,text:str='',fg='black',bg='white',font=('微软雅黑',12),anchor='nw')

- pos::位置
- width::宽度
- height::高度
- text::初始文字
- fg::文字颜色
- bg::背景颜色
- font::字体
- anchor::对齐方向

绘制一个单行输入框。这是一个伪绘制组件，其实就是简化了Entry控件的导入。

通过`entry.get()`获取值。

### return: entry

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI%E5%8D%95%E9%80%89%E6%A1%86.gif)

---

### add_separate(self,pos:tuple,width:int,direction='x',fg='grey',anchor='nw')

- pos::位置
- width::长度
- direction::方向。“x”或“y”（横向 或 纵向）
- fg::颜色
- anchor::对齐方向

绘制一条分割线。

### return: separate

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI%E5%A4%8D%E9%80%89%E6%A1%86.gif)

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

### return: text, choices_text_list, choices_back

> text::文本提示画布对象
>
> choices_text_list::可选框的文本画布对象
>
> choices_back::可选框的背景方框画布对象

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI%E5%8D%95%E9%80%89%E6%A1%86.gif)

---

### add_link(self,pos:tuple,text,url,fg='#50B0F4',font=('微软雅黑',12),anchor='nw')

- pos::位置
- text::链接文本
- url::链接
- fg::文本颜色
- font::字体
- anchor::对齐方向

绘制一个超链接文本。

### return: link

![](https://github.com/Smart-Space/TinUI/raw/main/image/%E8%B6%85%E9%93%BE%E6%8E%A5.gif)

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

### return: waitbar1,ok

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

### return: label,frame

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

### return: back,balls:list,stop

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

### return: main,back,box_tagname

> main::显示框文字
>
> back::显示框背景
>
> box_tagname::所有选项框的tag名称

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI%E7%BB%84%E5%90%88%E6%A1%86.gif)

---

### add_progressbar(self,pos:tuple,width=250,fg='#3B3B3B',bg='#63ADE5',percentage=True,text='')

- pos::位置
- width::宽度
- fg::文本以及边框颜色
- bg::填充颜色
- percentage::是否显示进度文本，如果为False，则显示参数text的内容
- text::当不显示进度文本时，进度条上的文本内容

绘制一个进度条。

### return: back,pro_tagname,text,goto

> back::背景矩形边框
>
> pro_tagname::进度框矩形所代表的tag名称
>
> text::进度条文本
>
> goto::进度改变函数：goto(num:int)，其中，num∈[0,100]。这将改变进度条的值

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI进度条.gif)

---

### add_table(self,pos:tuple,outline='#E1E1E1',fg='black',bg='white',data=[['1','2','3'],['a','b','c']],minwidth=100,font=('微软雅黑',12))

- pos::位置
- outline::边框颜色
- fg::文本颜色
- bg::文本背景颜色
- data::表格数据。格式：((title,...,...),(content1,...,...),(content2,...,...),...)
- minwidth::单元格最小宽度
- font::字体

绘制一个表格。

### return: None

> 表格组件绘制较复杂，涉及到列宽度、行最大高度等内容，目前没有返回内容

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

### return: state, back

> state::文本内容。“off”或“on”的画布对象

![](https://github.com/Smart-Space/TinUI/raw/main/image/TinUI开关.gif)