"""
<TinUIXml, the xml layout engine of TinUI.>
    Copyright (C) <2021-present>  <smart-space>
基于GPLv3和额外的LPGLv3许可发布
"""

import ast
import itertools
import re
from typing import TYPE_CHECKING, Optional, Union
from xml.etree import ElementTree as ET

if TYPE_CHECKING:
    from .TinUI import BasicTinUI, TinUI, TinUITheme

# xml中self.funcs["key"]/self.datas["key"]形式的取值
FUNCSDATA_PATTERN = re.compile(r"^self\.(funcs|datas)\[(['\"])(.*?)\2\]$", re.S)

# ftag是画布上的临时标签名，同一进程内唯一
_FTAG_COUNTER = itertools.count()


class TinUIThemeBase:
    """TinUITheme的标记基类

    TinUIXml需要在运行期识别TinUITheme的样式包装对象（见TinUIXml.__init__）。
    将该标记基类置于本模块，TinUIXml便可在不导入TinUI.py的情况下完成该判断，
    依赖方向固定为 TinUI.py -> TinUIXml.py。
    """


class TinUIXmlFunc:
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        if self.function is None:
            return None
        return self.function(*args, **kwargs)


class TinUIXmlFuncDict:
    def __init__(self, default: Optional[dict] = None):
        self.data = {}
        # environment()绑定的原始字典，按引用持有，不做复制；
        # 后绑定者优先，同一对象重复绑定只保留最后一次
        self.defaults = [default] if default is not None else []

    def __setitem__(self, key, fun):
        if key in self.data:
            self.data[key].function = fun
        else:
            self.data[key] = TinUIXmlFunc(fun)

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        for namespace in reversed(self.defaults):
            if key in namespace:
                return namespace[key]
        raise KeyError(key)

    def __delitem__(self, key):
        if key in self.data:
            self.data.pop(key)
        elif key in self:
            # 绑定的字典不可删改，用空实现遮蔽该名
            self.data[key] = TinUIXmlFunc(None)
        else:
            raise KeyError(key)

    def __contains__(self, key):
        if key in self.data:
            return True
        return any(key in namespace for namespace in self.defaults)

    def __or__(self, other):
        if not isinstance(other, dict):
            return NotImplemented
        # 创建一个新的TinUIXmlFuncDict实例，合并self和other的内容
        new_dict = TinUIXmlFuncDict()
        new_dict.defaults = list(self.defaults)
        new_dict.update(self.data)
        new_dict.update(other)
        return new_dict

    def update(self, other):
        for key, value in other.items():
            self[key] = value

    def clear(self):
        self.data.clear()
        self.defaults.clear()

    def __repr__(self):
        return f"{type(self).__name__}({self.data})"


class TinUIXml:  # TinUI的xml渲染方式
    """为TinUI提供更加方便的平面方式，使用xml
    TinUITheme基类无法直接使用，只能够重写TinUI或BasicTinUI的样式后才能够使用，参考 /theme 中的样式重写范例
    """

    # 以下参数表为类级常量，不随实例重复构建；如需改写可在实例上直接赋值覆盖
    noload = frozenset(("", "menubar"))  # 当前不解析的标签
    intargs = frozenset(  # 需要转为数字的参数
        (
            "width",
            "linew",
            "bd",
            "r",
            "minwidth",
            "maxwidth",
            "start",
            "padx",
            "pady",
            "info_width",
            "height",
            "num",
            "delay",
        )
    )
    scale_int = frozenset(  # 需要转为数字且随缩放变化的参数
        (
            "width",
            "linew",
            "r",
            "minwidth",
            "maxwidth",
            "padx",
            "pady",
            "info_width",
            "height",
        )
    )
    dataargs = frozenset(  # 需要转为数据结构的参数
        (
            "size",
            "command",
            "choices",
            "widgets",
            "content",
            "percentage",
            "data",
            "cont",
            "scrollbar",
            "widget",
            "offset",
        )
    )
    # ===== 面板模式（根节点 <tinui layout='panel'>）=====
    # 面板标签集合
    panel_tags = frozenset(
        ("expandpanel", "verticalpanel", "horizonpanel", "cardpanel", "sash")
    )
    # 各面板标签允许的构造参数；数值只做类型转换，缩放交由面板内部完成
    panel_attrs = {
        "expandpanel": ("padding", "min_width", "min_height", "bg", "bd", "line", "linew"),
        "verticalpanel": ("padding", "spacing", "min_width", "min_height", "bg", "bd", "line", "linew"),
        "horizonpanel": ("padding", "spacing", "min_width", "min_height", "bg", "bd", "line", "linew"),
        "cardpanel": ("card_width", "card_height", "padding", "h_spacing", "v_spacing", "min_width", "bg", "bd", "line", "linew"),
        "sash": ("bg", "bd", "line", "linew", "draggable"),
    }
    panel_number_args = frozenset(
        ("bd", "linew", "spacing", "min_width", "min_height", "card_width", "card_height", "h_spacing", "v_spacing")
    )
    panel_tuple_args = frozenset(("padding",))
    panel_bool_args = frozenset(("draggable",))
    # 根面板类型映射
    panel_root_types = {
        "expand": "expandpanel",
        "vertical": "verticalpanel",
        "horizon": "horizonpanel",
        "card": "cardpanel",
    }
    # 面板模式暂不支持的流式标签
    panel_flow_tags = frozenset(("line", "back", "labelframe", "flyout", "tooltip"))

    def __init__(self, ui: Union["BasicTinUI", "TinUI", "TinUITheme"]):
        self.ui = ui
        if isinstance(ui, TinUIThemeBase):
            self.realui = ui.ui
        else:
            self.realui = ui
        self.funcs = TinUIXmlFuncDict()  # 内部调用方法集合
        self.datas = {}  # 内部数据结构集合
        self.tags = {}  # 内部组件tag集合
        origin = self.__origin()
        self.xendx, self.xendy = origin, origin  # 横向最宽原点
        self.yendx, self.yendy = origin, origin  # 纵向最低原点
        # 面板模式状态
        self._panel_root = None  # 隐式根面板
        self._panel_bind_id = None  # <Configure>绑定id
        self._panel_margin = origin  # 根面板距画布边缘
        self._panel_animate = False  # 是否使用尺寸过渡动画
        self._panel_duration = 0  # 动画时长（毫秒）

    def __scale_value(self, value: Union[int, float]):
        return self.realui.scale_value(value)

    def __origin(self):  # 版面原点，需随TINUISCALE同步，故不缓存为实例属性
        return self.__scale_value(5)

    def __eval_data(self, value):
        """
        将xml中的字符串转为python对象。
        `self.funcs["key"]`/`self.datas["key"]`下标与Python字面量走快路径，
        其余写法（如lambda等任意表达式）仍由eval求值
        """
        if not isinstance(value, str):  # 已被back/labelframe等转换过的结构，直接透传
            return value
        matched = FUNCSDATA_PATTERN.fullmatch(value)
        if matched is not None:
            return getattr(self, matched[1])[matched[3]]
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            return eval(value)

    def __attrib2kws(self, args: dict, ignorecmd):  # 将部分特定参数转化为正确类型
        for key in args:
            if key in self.intargs:
                args[key] = int(args[key])
                if key in self.scale_int:
                    args[key] = self.__scale_value(args[key])
            elif key in self.dataargs:
                if key == "command" and ignorecmd:
                    # 忽略command参数，允许开发者稍后定义。
                    # 直接置空而不改动self.funcs，避免注销开发者已注册的回调
                    args[key] = None
                    continue
                args[key] = self.__eval_data(args[key])
        return args

    def __tags2uid(self, tag: str):  # 将self.tags中的内容转为画布uid
        name = self.tags[tag]
        if type(name) != tuple or len(name) == 1:
            uid = name
        else:
            uid = name[-1]
        return uid

    def __load_line(
        self,
        line,
        x=None,
        y=None,
        padx=None,
        pady=None,
        anchor="nw",
        ftags=None,
        ignorecmd=False,
    ):  # 根据xml的<line>逐行渲染TinUI组件，返回(起点x, 起点y, 下边缘, 右边缘)
        # x/y/padx/pady若由父<line>传入，则已是缩放后的画布值，直接沿用；
        # 仅在本层xml显式声明时再做一次缩放，避免嵌套<line>逐层放大
        origin = self.__origin()
        x = origin if x is None else x
        y = origin if y is None else y
        padx = origin if padx is None else padx
        pady = origin if pady is None else pady
        _padx = line.get("padx", None)
        _pady = line.get("pady", None)
        padx = self.__scale_value(int(_padx)) if _padx is not None else padx
        pady = self.__scale_value(int(_pady)) if _pady is not None else pady
        # ftags为本行的祖先链，每个<line>持有独立副本，
        # 避免默认参数/兄弟行/子画布实例之间相互累积
        ftags = list(ftags) if ftags else []
        last_y = y
        linex = None  # 纵块中的最大宽度
        _x = line.get("x", None)
        _x = self.__scale_value(int(_x)) if _x else x
        xendx = x = _x
        _y = line.get("y", None)
        _y = self.__scale_value(int(_y)) if _y else y
        xendy = y = _y
        allanchor = line.get("anchor", anchor)
        lineanchor = line.get("lineanchor", "")  # 整个模块的对齐方向
        ftag = f"ftag-{next(_FTAG_COUNTER)}"
        ftags.append(ftag)
        for i in line.iterfind("*"):  # 只检索直接子元素
            if i.tag == "line":
                _, _, liney, newlinex = self.__load_line(
                    i, xendx, xendy, padx, pady, allanchor, ftags, ignorecmd
                )
                if liney > last_y:  # 在同一位置判断纵向大小
                    last_y = xendy = liney
                if linex == None:  # 判断是否是该纵块的第一个<line>
                    linex = 0
                linex = max(linex, newlinex + padx)
                continue
            if i.tag in self.noload:  # 不渲染的组件
                continue
            # 特殊渲染的组件，有些仅对参数处理，有些需要特殊处理
            elif i.tag == "back":  # 调整uids参数
                if "uids" in i.attrib:
                    olds = self.__eval_data(i.attrib["uids"])
                    news = []
                    for tag in olds:
                        uid = self.__tags2uid(tag)
                        news.append(uid)
                    i.attrib["uids"] = tuple(news)
            elif i.tag == "labelframe":  # 同back
                if "widgets" in i.attrib:
                    olds = self.__eval_data(i.attrib["widgets"])
                    news = []
                    for tag in olds:
                        uid = self.__tags2uid(tag)
                        news.append(uid)
                    i.attrib["widgets"] = tuple(news)
            elif i.tag == "flyout":
                if "fid" in i.attrib:
                    i.attrib["fid"] = self.__tags2uid(i.attrib["fid"])
            elif i.tag == "tooltip":
                if "uid" in i.attrib:
                    i.attrib["uid"] = self.__tags2uid(i.attrib["uid"])
            # 调整内部参数=====
            xendy = y  # 重新获取本行起始纵坐标
            if linex != None:  # 存在纵块
                xendx = linex
                linex = None
            i.attrib["pos"] = (xendx, xendy)
            attrib = self.__attrib2kws(i.attrib, ignorecmd)
            if "anchor" not in i.attrib:
                attrib["anchor"] = allanchor
            # ==========
            tagall = getattr(self.ui, "add_" + i.tag)(**attrib)
            bboxtag = tagall[-1] if isinstance(tagall, tuple) else tagall
            for each_ftag in ftags:
                self.realui.addtag_withtag(each_ftag, bboxtag)
            bbox = self.realui.bbox(bboxtag)
            if not bbox:
                continue
            xendx = bbox[2] + padx  # 获取当前最大x坐标
            last_y = max(last_y, bbox[3] + pady)  # 更新当前最低y坐标
            # ==========
            # 进行特定控件内部xml布局
            if i.tag in ("ui", "expander"):
                # 判断i是否存在子元素
                if len(i) != 0:
                    # 存在子元素，递归渲染
                    tagall[2].__load_line(i, ignorecmd=True)
            elif i.tag == "flyout":
                if len(i) != 0:
                    # 存在子元素，递归渲染
                    tagall[1].__load_line(i, ignorecmd=True)
            # 为内部组件命名
            if i.text != None:
                self.tags[i.text.strip()] = tagall
        # 根据lineanchor调整最后一行的位置
        bbox = self.realui.bbox(ftag)
        if bbox == None:
            self.realui.dtag(ftag)
            return x, y, last_y, xendx
        xcenter = (bbox[0] + bbox[2]) / 2
        ycenter = (bbox[1] + bbox[3]) / 2
        if lineanchor == "":
            dx = 0
            dy = 0
        elif lineanchor == "nw":
            dx = x - bbox[0]
            dy = y - bbox[1]
        elif lineanchor == "n":
            dx = x - xcenter
            dy = y - bbox[1]
        elif lineanchor == "ne":
            dx = x - bbox[2]
            dy = y - bbox[1]
        elif lineanchor == "e":
            dx = x - bbox[2]
            dy = y - ycenter
        elif lineanchor == "se":
            dx = x - bbox[2]
            dy = y - bbox[3]
        elif lineanchor == "s":
            dx = x - xcenter
            dy = y - bbox[3]
        elif lineanchor == "sw":
            dx = x - bbox[0]
            dy = y - bbox[3]
        elif lineanchor == "w":
            dx = x - bbox[0]
            dy = y - ycenter
        elif lineanchor == "center":
            dx = x - xcenter
            dy = y - ycenter
        else:
            raise ValueError(f"Invalid lineanchor value: {lineanchor}")
        self.realui.move(ftag, dx, dy)
        bbox = self.realui.bbox(ftag)
        xendx = bbox[2] + padx
        last_y = bbox[3] + pady
        self.realui.dtag(ftag)
        return x, y, last_y, xendx

    # ===== 面板模式实现 =====
    def __panel_classes(self):
        # 运行期惰性导入，避免 TinUI模块 -> TinUIXml模块 -> TinUIPanel模块 -> TinUI模块 的循环导入
        try:
            from .TinUIPanel import (
                ExpandPanel,
                VerticalPanel,
                HorizonPanel,
                CardPanel,
                PanelSash,
            )
        except ImportError:
            from TinUIPanel import (
                ExpandPanel,
                VerticalPanel,
                HorizonPanel,
                CardPanel,
                PanelSash,
            )
        return ExpandPanel, VerticalPanel, HorizonPanel, CardPanel, PanelSash

    def __panel_number(self, value):
        value = value.strip()
        return float(value) if ("." in value or "e" in value.lower()) else int(value)

    def __panel_kwargs(self, elem, key):
        """提取面板构造参数。数值仅做类型转换，缩放由面板内部完成，避免二次缩放。"""
        kwargs = {}
        for name in self.panel_attrs.get(key, ()):
            if name not in elem.attrib:
                continue
            raw = elem.attrib[name]
            if name in self.panel_tuple_args:
                kwargs[name] = tuple(
                    int(p) for p in re.split(r"[,\s]+", raw.strip()) if p
                )
            elif name in self.panel_bool_args:
                kwargs[name] = raw.strip().lower() in ("true", "1", "yes", "on")
            elif name in self.panel_number_args:
                kwargs[name] = self.__panel_number(raw)
            else:
                kwargs[name] = raw
        return kwargs

    def __split_child(self, elem):
        """解析<child>包装，返回(内层元素, size, min_size, weight, index)。

        未使用<child>包装时，直接返回该元素本身与默认约束。
        注意：ExpandablePanel.add_child 会缩放 size，但不缩放 min_size，
        因此 min_size 需在此按缩放后的画布单位传入。
        """
        if elem.tag != "child":
            return elem, None, 0, 0, -1
        inner = list(elem)
        if len(inner) != 1:
            raise ValueError("TinUIXml 面板布局：<child> 必须且只能包含一个元素")
        _size = elem.get("size")
        size = int(_size) if _size is not None else None
        _min = elem.get("min_size")
        min_size = self.__scale_value(int(_min)) if _min is not None else 0
        weight = float(elem.get("weight", "0"))
        index = int(elem.get("index", "-1"))
        return inner[0], size, min_size, weight, index

    def __build_control(self, elem):
        """在面板子树中创建一个普通控件，返回可作为面板子项的uid。"""
        attrib = dict(elem.attrib)
        attrib["pos"] = (0, 0)  # 实际位置由面板 update_layout 决定
        attrib = self.__attrib2kws(attrib, False)
        add = getattr(self.ui, "add_" + elem.tag, None)
        if add is None:
            raise ValueError(f"TinUIXml 面板布局：未知控件标签 <{elem.tag}>")
        tagall = add(**attrib)
        uid = tagall[-1] if isinstance(tagall, tuple) else tagall
        if not hasattr(uid, "layout"):
            raise ValueError(f"TinUIXml 面板布局：<{elem.tag}> 不支持作为面板子项")
        if elem.text is not None:
            name = elem.text.strip()
            if name:
                self.tags[name] = tagall
        return uid

    def __build_item(self, elem, parent_panel):
        if elem.tag in self.panel_tags:
            return self.__build_panel(elem, parent_panel)
        if elem.tag in self.panel_flow_tags:
            raise ValueError(f"TinUIXml 面板布局暂不支持流式标签 <{elem.tag}>")
        return self.__build_control(elem)

    def __build_panel(self, elem, parent_panel):
        """递归构建面板节点；parent_panel 供 PanelSash 定位，可为 None。"""
        ExpandPanel, VerticalPanel, HorizonPanel, CardPanel, PanelSash = (
            self.__panel_classes()
        )
        tag = elem.tag
        if tag == "sash":
            if len(elem) != 0:
                raise ValueError("TinUIXml 面板布局：<sash> 不能包含子元素")
            if parent_panel is None:
                raise ValueError("TinUIXml 面板布局：<sash> 必须位于面板内部")
            kwargs = self.__panel_kwargs(elem, "sash")
            kwargs["parent_panel"] = parent_panel
            return PanelSash(**kwargs)
        cls = {
            "expandpanel": ExpandPanel,
            "verticalpanel": VerticalPanel,
            "horizonpanel": HorizonPanel,
            "cardpanel": CardPanel,
        }[tag]
        panel = cls(self.realui, **self.__panel_kwargs(elem, tag))
        children = list(elem)
        if tag == "expandpanel":
            if len(children) != 1:
                raise ValueError(
                    "TinUIXml 面板布局：<expandpanel> 必须且只能包含一个子项"
                )
            inner, _, _, _, _ = self.__split_child(children[0])
            panel.set_child(self.__build_item(inner, panel))
            return panel
        for child_elem in children:
            inner, size, min_size, weight, index = self.__split_child(child_elem)
            item = self.__build_item(inner, panel)
            if tag == "cardpanel":
                panel.add_child(item, index=index)
            else:
                panel.add_child(
                    item, size=size, min_size=min_size, weight=weight, index=index
                )
        return panel

    def __layout_panels(self):
        """按当前画布尺寸重新排布根面板。"""
        if self._panel_root is None:
            return
        margin = self._panel_margin
        rect = (
            margin,
            margin,
            self.realui.winfo_width() - margin,
            self.realui.winfo_height() - margin,
        )
        if self._panel_animate:
            self._panel_root.animate_layout(*rect, duration=self._panel_duration)
        else:
            self._panel_root.update_layout(*rect)

    def __on_panel_configure(self, _=None):
        self.__layout_panels()

    def __load_panel_root(self, root):
        """加载 <tinui layout='panel'>：构建一个铺满画布的隐式根面板。"""
        ExpandPanel, VerticalPanel, HorizonPanel, CardPanel, PanelSash = (
            self.__panel_classes()
        )
        root_type = root.get("root", "expand").strip().lower()
        if root_type not in self.panel_root_types:
            raise ValueError(f"TinUIXml 面板布局：未知的 root 类型 '{root_type}'")
        key = self.panel_root_types[root_type]
        cls = {
            "expandpanel": ExpandPanel,
            "verticalpanel": VerticalPanel,
            "horizonpanel": HorizonPanel,
            "cardpanel": CardPanel,
        }[key]
        panel = cls(self.realui, **self.__panel_kwargs(root, key))
        children = list(root)
        if key == "expandpanel":
            if len(children) != 1:
                raise ValueError(
                    "TinUIXml 面板布局：root='expand' 必须且只能包含一个子项"
                )
            inner, _, _, _, _ = self.__split_child(children[0])
            panel.set_child(self.__build_item(inner, panel))
        else:
            for child_elem in children:
                inner, size, min_size, weight, index = self.__split_child(child_elem)
                item = self.__build_item(inner, panel)
                if key == "cardpanel":
                    panel.add_child(item, index=index)
                else:
                    panel.add_child(
                        item, size=size, min_size=min_size, weight=weight, index=index
                    )
        self._panel_root = panel
        self._panel_margin = self.__scale_value(int(root.get("margin", "5")))
        animate = root.get("animate", "false").strip().lower()
        self._panel_animate = animate in ("true", "1", "yes", "on")
        self._panel_duration = int(root.get("duration", "180"))
        self._panel_bind_id = self.realui.bind(
            "<Configure>", self.__on_panel_configure, add="+"
        )
        self.realui.update_idletasks()
        self.__layout_panels()

    def __destroy_panels(self):
        """销毁当前面板树并解除尺寸监听。"""
        if self._panel_root is not None:
            try:
                self._panel_root.stop_animation()
                self._panel_root.destroy()
            finally:
                self._panel_root = None
        if self._panel_bind_id is not None:
            try:
                self.realui.unbind("<Configure>", self._panel_bind_id)
            except Exception:
                pass
            self._panel_bind_id = None

    def loadxml(self, xml: str):  # 从xml字符串载入窗口组件
        self.__destroy_panels()
        origin = self.__origin()
        # xendx/xendy:横向最宽一行的左起点与右边缘
        # yendx/yendy:纵向最低一行的上起点与下边缘，yendy同时作为下一行的y起点
        self.xendx, self.xendy = origin, origin
        self.yendx, self.yendy = origin, origin
        root = ET.fromstring(xml)
        if root.tag != "tinui":  # 严格控制规范
            return
        if root.get("layout", "").strip().lower() == "panel":  # 面板模式分支
            self.__load_panel_root(root)
            return
        for line in root.findall("line"):
            startx, starty, bottomy, rightx = self.__load_line(line, y=self.yendy)
            if rightx > self.xendy:  # 记录横向最宽原点
                self.xendx, self.xendy = startx, rightx
            if bottomy > self.yendy - origin:  # 记录纵向最低原点
                self.yendx, self.yendy = starty, bottomy + origin

    def environment(
        self, dict_item: dict
    ):  # 在funcs和datas中加入默认标识内容，一般为globals()或locals()
        # funcs按引用绑定dict_item，不复制其中的条目，多次调用叠加且后者优先；
        # datas允许开发者写入（datas.update等），故仍持有其浅拷贝
        if isinstance(self.funcs, TinUIXmlFuncDict):
            self.funcs.defaults = [
                d for d in self.funcs.defaults if d is not dict_item
            ]
            self.funcs.defaults.append(dict_item)
        else:  # 开发者以普通dict替换了funcs
            self.funcs.update(dict_item)
        self.datas.update(dict_item)

    def clean(self):  # 清空TinUI
        self.__destroy_panels()
        self.realui.clean_windows()
        self.funcs.clear()
        self.datas.clear()
        self.tags.clear()
        origin = self.__origin()
        self.xendx, self.xendy = origin, origin  # 横向最宽原点
        self.yendx, self.yendy = origin, origin  # 纵向最低原点
