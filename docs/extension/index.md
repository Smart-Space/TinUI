---
title: TinUI拓展
nav_order: 4
---
# TinUI拓展

TinUI的拓展功能可以通过`from tinui import extension`导入。

> 这部分不是TinUI开发的重点

## 控件按钮化

```python
buttonlize(tinui,uid,bg='#fbfbfb',line='#CCCCCC',activebg='#f5f5f5',activeline='#e5e5e5',command=None)
```

- tinui - TinUI控件所属的TinUI或BasicTinUI

- uid - 元素名称或代码

- bg - 背景颜色

- line - 边框颜色

- activebg - 响应背景色

- activeline - 响应边框颜色

- command - 响应函数

> 注意，如果元素控件组(`uid`)中含有按钮之类的响应点击的控件，点击时会同时触发控件响应函数和该函数。
