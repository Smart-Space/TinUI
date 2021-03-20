# TinUI

## 项目类型

TinUI是一个基于tkinter（Python）的拓展组件，可以绘制虚拟组件。

TinUI基于tkinter的画布（Canvas），可以作为整个窗口的唯一控件。TinUI能够通过自身绘制出功能组件和文字，也可以使用画布功能添加组件。使用TinUI，可以使界面设计和代码设计分离，此外，TinUI绘制的虚拟组件速度更快，样式更加丰富。

目前，TinUI处于完善阶段。

## 依赖

TinEngine有以下第三方依赖项（实际上是TinEngine的）：

1. PIL（pillow）
2. pywin32（win32gui）
3. requests

## TinEngine支持

TinUI允许插入TinEngine的TinText控件，用以渲染Tin标记语言富文本。