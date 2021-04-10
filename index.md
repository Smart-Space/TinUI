# TinUI

## 项目类型

TinUI是一个基于tkinter（Python/tcl/tk）的拓展组件，可以绘制虚拟组件。

TinUI基于tkinter的画布（Canvas），可以作为整个窗口的唯一控件。TinUI能够通过自身绘制出功能组件和文字，也可以使用画布功能添加组件。使用TinUI，可以使界面设计和代码设计分离，此外，TinUI绘制的虚拟组件速度更快，样式更加丰富。

目前，TinUI还处于完善阶段。

## 依赖

TinEngine有以下第三方依赖项（实际上是[TinEngine](https://blog.csdn.net/tinga_kilin/category_10332845.html)的）：

1. PIL（pillow）
2. pywin32（win32gui）
3. requests

## TinEngine支持

TinUI允许插入[TinEngine](https://blog.csdn.net/tinga_kilin/category_10332845.html)的TinText控件，用以渲染[Tin标记语言](https://blog.csdn.net/tinga_kilin/category_10332845.html)富文本。

---

## 基础函数

> ==一般地==，会将每个函数的名称以及定义、参数内容、函数绘制说明列出来。
>
> 所有函数均会返回主要画布对象。

### add_title(self,pos:tuple,text:str,fg='black',font='微软雅黑',size=1,**kw)

- pos::位置
- text::标题文字
- fg::文本颜色
- font::文本字体
- size::文本字体大小。依据字典：`{0:20,1:18,2:16,3:14,4:12}`

绘制一个大字体标题。

### add_paragraph(self,pos:tuple,text:str,fg='black',font=('微软雅黑',12),side='left',width=500,**kw)

- pos::位置
- text::标题文字
- fg::文本颜色
- font::字体名称+大小
- side::对齐方向
- width::一行允许的最大字符宽度

绘制一个段落。

### add_button(self,pos:tuple,text:str,fg='black',bg='#E1E1E1',font=('微软雅黑',12),command=None)

- pos::位置
- text::标题文字
- fg::文字颜色
- bg::按钮颜色
- font::字体名称+大小
- command::绑定的函数。该函数**必须要有event参数**，因为TinUI的按钮会传递点击事件的event

绘制一个按钮。这个按钮会响应鼠标的离开和进入事件，被单击时也会调用绑定的函数。

### add_label(self,pos:tuple,text:str,fg='black',bg='#f0f0f0',outline='grey',font=('微软雅黑',12)) 

- pos::位置
- text::标题文字
- fg::文字颜色
- bg::背景色
- outline::边框颜色
- font::字体名称+大小

绘制一个类Label组件。

### add_checkbutton(self,pos:tuple,text:str,fg='black',fill='lightgreen',font=('微软雅黑',12),command=None)

- pos::位置
- text::标题文字
- fg::文字颜色
- fill::选中的标识填充
- font::字体名称+大小
- command::绑定的函数。该函数**必须要有event参数**，因为TinUI的按钮会传递点击事件的event

绘制一个复选框。这个复选框会响应鼠标的离开和进入事件，被单击时也会调用绑定的函数，并且会根据当前样式更改点击后的样式。