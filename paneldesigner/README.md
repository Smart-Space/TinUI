# TinUI 面板设计器（panel designer）

纯 HTML + CSS + JavaScript 实现的可视化设计器，用于编辑 TinUI 的**面板模式**布局
（`<tinui layout='panel'>`），并导出可直接被 `TinUIXml.loadxml()` 解析的 XML。

无需构建、无需依赖，直接用浏览器打开 `index.html` 即可。

## 界面

- **左侧**
  - `面板`：`expandpanel` / `verticalpanel` / `horizonpanel` / `cardpanel` / `sash`
  - `控件`：`TinUI` 中全部可作为面板子项的控件（带 `layout` 方法），按用途分组：
    - 文本：`title`、`paragraph`、`label`、`link`
    - 按钮：`button`、`button2`、`togglebutton`、`menubutton`、`segmentbutton`、`barbutton`、
      `checkbutton`、`radiobutton`、`radiobox`、`pivot`、`navigation`、`breadcrumb`
    - 输入：`entry`、`passwordbox`、`textbox`、`combobox`、`spinbox`、`picker`、`scalebar`、`labels`
    - 显示：`progressbar`、`waitbar1`、`waitbar3`、`waitframe`、`ratingbar`、`onoff`、
      `separate`、`image`、`table`、`listbox`、`listview`、`treeview`、`ui`、`pipspager`、
      `notebook`、`expander`
    - 共 40 个；条目只有文字（无图标），点击加入或拖拽到画布
  - `结构树`：完整层级，**可直接选中被控件覆盖的面板**
- **中间**：模拟窗口，按 `TinUIPanel.update_layout` 的规则实时排布
  - 多数控件在画布中按外观近似绘制；难以用 HTML 还原的控件
    （`picker`、`labels`、`image`、`ui`、`pipspager`、`listview`、`waitframe`）
    用**虚线矩形 + 中心控件名**代替；
    `treeview` 则按 `content` 的嵌套层级绘制缩进树
- **右侧**：属性面板
  - 布局约束：`size` / `min_size` / `weight` / `index`
  - 控件属性：默认参数 + `anchor`，并可通过「添加参数」补充任意参数（如 `fg`、`font`、`command`），
    每行右侧的 `✕` 可移除参数；数字 / 颜色 / 枚举 / 布尔参数会自动使用对应编辑器
  - 面板属性：`padding`、`spacing`、`min_width`、`card_width` 等；
    `bd` 是**圆角大小**（对齐 `BasePanel` 的 `bd=9`，即 `TinUI` 面板默认圆角），
    `line` + `linew` 才是边框颜色与宽度
  - 根设置：`root` 类型、`margin`

## 操作

- 点击左侧面板/控件即可添加到当前选中的容器；也可拖拽到画布中某个面板上。
- 点击画布中的元素选中；**按住 `Alt` 点击**可在被覆盖的面板之间循环选中。
  左侧结构树与底部面包屑同样可以选择任意节点。
- 未设置 `size` / `weight` 时，控件与嵌套面板都按各自的固有尺寸排列
  （嵌套面板的固有尺寸由其子项推出），可用右侧 `size` 或 `weight` 覆盖。
- 选中纵向 / 横向面板的子项后，拖动选中框边缘的方块可直接调整 `size`。
- 快捷键：`Delete` 删除、`Ctrl+D` 复制、`Alt+↑/↓` 上移/下移、`Esc` 取消选择。
- 右侧属性改动会实时反映到中间画布，并同步到导出的 XML。

## 导出

点击右上角 **导出 XML**，会得到形如：

```xml
<tinui layout='panel' root='horizon' padding='5,5,5,5' spacing='5' bg='#ffffff' ...>
  <child size='150'>
    <verticalpanel bg='#e0f7fa' spacing='5'>
      <child><button2 text='打开' anchor='nw'/></child>
    </verticalpanel>
  </child>
  <child weight='1'>
    <cardpanel card_width='120' card_height='80' ...>
      <child><label text='卡片 A' anchor='center'/></child>
    </cardpanel>
  </child>
</tinui>
```

导出时会检查常见非法结构（如 `expandpanel` 子项数量不为 1、`sash` 不在纵向/横向面板内）并给出提示。

## 说明

- `padding` 会强制规范为 4 个值（`上,右,下,左`），因为 `TinUIPanel` 解包时要求恰好 4 项。
- 布尔参数（如 `draggable`）导出为 `'true'` / `'false'`。
- 面板的 `bg` 默认留空（透明）。这与 `TinUIPanel` 一致：`BasePanel.fix_bg`
  在 `bg` 为空时直接返回，不绘制任何图元，且「单有边框颜色无效」。
  需要底色时在右侧「背景 bg」自行填写；画布上透明面板以斜纹示意。
- 面板的 `bd` 是圆角半径而非边框宽度；`BasePanel` 用 `create_polygon(width=bd)`
  描边画出圆角背景，故未设 `linew` 时没有边框线，只在四角内收。
- 控件导出时若填写了 `标签名 name`，会作为元素文本内容，对应 `TinUIXml.tags[name]`。
- 只有 `TinUI.add_*` 中定义了 `uid.layout(...)` 的控件才能作为面板子项，共 40 个，与
  `docs/controls/` 中的控件一一核对。面板模式**不支持**、因此未收录的控件：
  - `menubar`：`TinUIXml.noload` 直接跳过
  - `back`、`flyout`、`labelframe`、`tooltip`：`TinUIXml.panel_flow_tags`，载入时抛 `ValueError`
  - `scrollbar`、`notecard`、`accentbutton`、`warningbutton`、`toolbutton`：没有 `uid.layout`，
    `__build_control` 会抛「不支持作为面板子项」
  - `waitbar2`、`info`、`swipecontrol`、`canvas`：仅见于 `docs/controls/`，
    `TinUI.py` 中已无对应实现（文档滞后）
- `treeview` 的 `content` 形如 `(标题, (子项…))` 可嵌套，纯字符串为叶子节点。
- 留空的数值参数不会导出（沿用 `TinUI` 默认值）；自行添加的非默认参数留空同样不导出。
- 暂未提供 `animate` / `duration`：当前 `TinUIPanel` 在根面板首次布局时会在
  `animate_layout → get_rect` 处因背景坐标不足报错，故默认不导出该选项。
