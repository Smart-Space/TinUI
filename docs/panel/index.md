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
    def __init__(self, canvas, child=None, padding=(0, 0, 0, 0), min_width=0, min_height=0, bg='', bd=9):
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
    def __init__(self, canvas, padding=(0, 0, 0, 0), spacing=0, min_width=0, min_height=0, bg='', bd=9):
        ...
```

`set_padding`,`set_min_size`,`update_layout`同ExpandPanel。

### set_spacing(spacing)

设置元素间间距。

### clear_children()

删除下辖所有元素。

### add_child(child, size=None, min_size=0, weight=0, index=-1)

若`size`未指定，当`child`是控件时，获取对应方向上的尺寸；如果是横向面板，则获取最大控件高度；否则为`100`，**注意**，每次布局时都会重新获取控件元素的尺寸，将增大计算负荷。

当`weight>0`时，该元素的尺寸将根据剩余空间按比例分配，否则其固定尺寸。

使用`index`参数控制控件插入的顺序，默认在末尾插入（除了`-1`，插入逻辑同python列表插入）。

### remove_child(index)

删除位置在`index`的托管元素。

### pop_child(index)

不再管理位置在`index`的托管元素，并返回这个元素。

---

## HorizonPanel

同VerticalPanel，但`add_child`未指定`size`是，判断纵向面板最大控件宽度。