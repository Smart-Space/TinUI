---
sort: 2
---
# TinUI控件

## BasicTinUI

`BasicTinUI`是TinUI的核心组件，也是`TinUI`的基类，负责实现对各控件的呈现与管理。

```python
from tinui import BasicTinUI
tinui = BasicTinUI(root, bg='white')
```

### clean_windows()

使用`tinui.clean_windows()`清除浮出控件的子窗口，开发者可以手动销毁子窗口。

## TinUI
```python
from tinui import BasicTinUI, TinUI
tinui = TinUI(root, bg='white', update=True, update_time=1000)
'''
update:bool::是否实时更新滚动画面
update_time:int::每次更新滚动画面的间隔（毫秒）
**kw::Canvas的参数
'''
```

`TinUI`基于`BasicTinUI`，二者用法完全相同，但是二者有以下区别：

| 项目          | BasicTinUI | TinUI |
| ------------- | ---------- | ----- |
| TinUI绘制组件 | √          | √     |
| 自动刷新      | ×          | √     |
| 滚动条支持    | ×          | √     |
| 窗口主组件    | ×          | √     |
| 主窗口        | ×          | √     |
| 区域渲染组件  | √          | ×     |

> 表格中部分功能只是建议，并非不行。

## TinUI支持的控件

TinUI中的大部分控件均是通过`tkinter.Canvas`创建的，并且能够在一个画布中呈现多个控件，因此，TinUI的控件创建方法均为`add_<control-name>`。

TinUI有如下几类控件：

- [文本类](./1.text)
- [按钮类](./2.button)
- [输入类](./3.input)
- [选择类](./4.select)
- [框架类](./5.frame)
- [图像类](./6.image)
- [菜单类](./7.menu)
- [功能类](./8.function)

> 一般地，`tinui.add_<control-name>(...)`的最后一个返回值为该控件整体在画布中的ID。
