---
title: TinUI面板布局
nav_order: 7
---
# TinUI面板布局

TinUI中有三个可用面板类，分别管理拓展、纵向、横向面板布局。

---

## ExpandPanel

```python
class ExpandPanel(BasePanel):
    def __init__(self, canvas, child=None, padding=(0, 0, 0, 0), min_width=0, min_height=0):
        ...
```

### set_padding(padding)

设置内边距，四元组(top, right, bottom, left)。

### set_min_size(min_width, min_height)

设置最小尺寸。

### set_child(child)

设置托管元素。

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
    def __init__(self, canvas, padding=(0, 0, 0, 0), spacing=0, min_width=0, min_height=0):
        ...
```

`set_padding`,`set_min_size`,`update_layout`同ExpandPanel。

### set_spacing(spacing)

设置元素间间距。

### add_child(child, size=100, min_size=0, weight=0)

当`weight>0`时，该元素的尺寸将根据剩余空间按比例分配，否则其固定尺寸。

---

## HorizonPanel

同VerticalPanel