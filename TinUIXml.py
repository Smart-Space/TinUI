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

    def loadxml(self, xml: str):  # 从xml字符串载入窗口组件
        origin = self.__origin()
        # xendx/xendy:横向最宽一行的左起点与右边缘
        # yendx/yendy:纵向最低一行的上起点与下边缘，yendy同时作为下一行的y起点
        self.xendx, self.xendy = origin, origin
        self.yendx, self.yendy = origin, origin
        root = ET.fromstring(xml)
        if root.tag != "tinui":  # 严格控制规范
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
        self.realui.clean_windows()
        self.funcs.clear()
        self.datas.clear()
        self.tags.clear()
        origin = self.__origin()
        self.xendx, self.xendy = origin, origin  # 横向最宽原点
        self.yendx, self.yendy = origin, origin  # 纵向最低原点
