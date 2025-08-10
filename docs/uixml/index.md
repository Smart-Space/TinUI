---
title: TinUIXml
nav_order: 6
---
# TinUIXml
`TinUIXml`允许通过xml语言来绘制TinUI组件。

> `menubar`不支持使用xml布局。

```python
class TinUIXml():#TinUI的xml渲染方式
    '''为TinUI提供更加方便的平面方式，使用xml
    TinUITheme基类无法直接使用，只能够重写TinUI或BasicTinUI的样式后才能够使用，参考 /theme 中的样式重写范例
    '''

    def __init__(self,ui:Union[BasicTinUI,TinUITheme]):
        #BasicTinUI包括TinUI
        #TinUITheme为样式基础类，继承类也可
```