---
title: TinUI样式
nav_order: 5
---
# TinUI样式

TinUI自定义配色类`TinUITheme`是所有TinUI配色样式的基类，所有继承该类的TinUI样式类应当实现完整的TinUI控件配色支持，而保留各控件的其余参数。此外，通过继承`TinUITheme`类，新的TinUI样式类可以直接结合`TinUIXml`使用。

`TinUITheme`的定义如下：

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

使用示例见开源TinUI代码库见 `theme\tinuilight.py`等。

> TinUI只维护`tinuilight.py`和`tinuidark.py`。