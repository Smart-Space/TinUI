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