---
title: TinUI面板布局
nav_order: 7
---
# TinUI面板布局

TinUI中有四个可用面板类，分别管理拓展、纵向、横向、卡片式面板布局；以及一个辅助面板类，面板拉伸条。

---

## 通用面板类参数

```python
class BasePanel:
    """面板的基类"""

    def __init__(self, canvas:BasicTinUI, bg='', bd=9, line='', linew=0):
        ...
```

- bg::背景颜色
- bd::圆角大小（高DPI下自动适配）
- line::边框颜色
- linew::边框宽度（高DPI下自动适配）

面板相关颜色只有在背景色不为空时才展示，单有边框颜色无效。

---

## ExpandPanel

```python
class ExpandPanel(BasePanel):
    def __init__(self, canvas, child=None, padding=(0, 0, 0, 0), min_width=0, min_height=0, bg='', bd=9):
        ...
```

### set_padding(padding)

设置内边距，四元组(top, right, bottom, left)。

### set_min_size(min_width, min_height)

设置最小尺寸。

### set_child(child)

设置托管元素。

### clear_children()

删除下辖所有元素。

### destroy()

删除下辖所有元素，删除自身背景。

### update_layout(x1, y1, x2, y2)

设置布局区域，一般使用如下方法，将ExpandPanel作为TinUI框架的根面板：

```python
b=BasicTinUI(a,bg='white')
b.pack(fill='both',expand=True)

rp=ExpandPanel(b)

def update(e):
    rp.update_layout(5,5,e.width-5,e.height-5)

b.bind('<Configure>',update)
```

---

## VerticalPanel

```python
class VerticalPanel(ExpandablePanel):
    def __init__(self, canvas, padding=(0, 0, 0, 0), spacing=0, min_width=0, min_height=0, bg='', bd=9):
        ...
```

`set_padding`,`set_min_size`,`update_layout`同ExpandPanel。

### set_padding(padding)

设置内边距，四元组(top, right, bottom, left)。

### set_spacing(spacing)

设置元素间间距。

### set_min_size(min_width, min_height)

设置最小尺寸。

### clear_children()

删除下辖所有元素。

### destroy()

删除下辖所有元素，删除自身背景。

### add_child(child, size=None, min_size=0, weight=0, index=-1)

若`size`未指定，当`child`是控件时，获取对应方向上的尺寸；如果是横向面板，则获取最大控件高度；否则为`100`，**注意**，每次布局时都会重新获取控件元素的尺寸，将增大计算负荷。

当`weight>0`时，该元素的尺寸将根据剩余空间按比例分配，否则其固定尺寸。

使用`index`参数控制控件插入的顺序，默认在末尾插入（除了`-1`，插入逻辑同python列表插入）。

### remove_child(index)

删除位置在`index`的托管元素。

如果`index`不是int而是元素uid或者面板，则删除指定元素或面板，不存在则会报错。

### pop_child(index)

不再管理位置在`index`的托管元素，并返回这个元素。

如果`index`不是int而是元素uid或者面板，则取消指定元素或面板的托管，不存在则会报错。

---

## HorizonPanel

同VerticalPanel，但`add_child`未指定`size`时，判断纵向面板最大控件宽度。

---

## CardPanel

```python
class CardPanel(ExpandablePanel):
    def __init__(self, canvas, card_width=100, card_height=100, padding=(0, 0, 0, 0), h_spacing=5, v_spacing=5, min_width=0, bg='', bd=9):
 		...
```

- card_width::卡片宽度
- card_height::卡片高度
- h_spacing::水平间距
- v_spacing::垂直间距

### set_card_size(width, height)

调整卡片尺寸。

### set_spacing(horizontal=None, vertical=None)

设置卡片间距。

### add_child(child, index=-1)

在指定位置插入托管元素。

---

## PanelSash

```python
class PanelSash(BasePanel):
    """
    面板拉伸条
    用于动态调整 HorizontalPanel 或 VerticalPanel 中相邻子元素的尺寸或权重
    """
    def __init__(self, parent_panel, bg='#cccccc', bd=0, line='', linew=0, draggable=True):
```

直接作为子元素添加进纵向面板或者横向面板，其`parent_panel`与加入该面板的上级面板需要一致。

`draggable`参数控制拉伸条是否允许被拖动，如果为`False`，则可当作面板分割线使用。

- 当相邻元素为固定尺寸时，调整尺寸；
- 均为权重时，调整权重系数；
- 权重与固定尺寸相邻，则调整尺寸。