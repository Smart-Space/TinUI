---
title: TinUI对话框
nav_order: 3
---
# TinUI对话框

TinUI对话框由`TinUIDialog`类实现，但是一般情况下不应当直接使用，而是使用基于此实现的若干对话框交互函数，例如：

```python
from tinui import show_msg
```

不过，`show_msg`也只是一个“朴素”的信息提示框，一般情况下应当导入以下对话框函数：

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

以 `show_msg`为例：

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

> TinUI-5.35版本开始，对话框可通过键盘按键交互：
>
> - 左右选择按钮
> - 空格或回车触发按钮
> - **注意**，输入类对话框只有回车确定功能

---

## 自定义对话框

除了TinUI自带的对话框，你可以在查看`TinUIDialog`的源码并理解后直接使用`Dialog`类，定义你希望对话框出现和交互的行为。当然，还有一个稍微简单的办法，就是使用TinUIDialog提供的基于TinUIXml自定义布局的封装。

```python
def initial_xml_load(self,title,xml,funcdict:dict={},data:dict={},yestext='OK',notext='Cancel',yescallback=None,nocallback=None,nonecallback=None,tinuitheme=None):
    """
    title...
    xml - 你希望使用的TinUIXml内容
    funcdict - 函数字典
    data - 数据字典
    yestext...
    notext...
    yescallback - 确认按钮按下后的回调函数
    nocallback - 取消按钮按下后的回调函数
    nonecallback - 直接关闭对话框的回调函数
    tinuitheme - 继承TinUITheme的样式类
    """
    ...
```

虽然TinUI的很多控件可以通过回调函数进行操作，而且理论上弹窗只需要一个回调函数就可以了，因为TinUIDialog会先执行回调函数后再关闭对话框，并返回对话框选项（`True`,`False`,`None`）。但是，都已经自定义了，所以不同的关闭行为对应不同的回调函数。但也因此，这三个参数完全可以指向一个回调函数。

最重要的一点，自定义TinUIDialog是三步走：

```python
d=Dialog(root,'xml')# 初始化
d.initial_xml_load(...)# 注入参数
dr=d.initial_xml_init()# 显示
```

`TinUIDialog.py`中给出的示例是：

```python
xml_data = 0
def xml_func(e):
    global xml_data
    xml_data = 1
    
func_dict = {'func':xml_func}

d=Dialog(root,'xml')

d.initial_xml_load('test xml dialog','<tinui><line>'
'<button text="click to change data value" command="self.funcs[\'func\']"></button>'
'</line></tinui>',
funcdict=func_dict,yescallback=lambda:print('yes'),nocallback=lambda:print('no'),nonecallback=lambda:print('none'))

dr=d.initial_xml_init()

if dr:
    print(f'yes with {xml_data}')
elif dr==False:
    print(f'no with {xml_data}')
elif dr==None:
    print(f'none with {xml_data}')
```

点击按钮会改变后台的`xml_data`，不同的关闭方式会先输出不同的文本，然后再输出包含关闭方式和`xml_data`值的文本。