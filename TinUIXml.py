"""
<TinUIXml, the xml layout engine of TinUI.>
    Copyright (C) <2021-present>  <smart-space>
基于GPLv3和额外的LPGLv3许可发布
"""

import uuid
from typing import TYPE_CHECKING, Union
from xml.etree import ElementTree as ET

if TYPE_CHECKING:
    from .TinUI import BasicTinUI, TinUI, TinUITheme


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
    def __init__(self):
        self.data = {}

    def __setitem__(self, key, fun):
        if key in self.data:
            self.data[key].function = fun
        else:
            self.data[key] = TinUIXmlFunc(fun)

    def __getitem__(self, key):
        return self.data[key]

    def __delitem__(self, key):
        self.data.pop(key)

    def __or__(self, other):
        if not isinstance(other, dict):
            return NotImplemented
        # 创建一个新的TinUIXmlFuncDict实例，合并self和other的内容
        new_dict = TinUIXmlFuncDict()
        new_dict.update(other)
        return new_dict

    def update(self, other):
        for key, value in other.items():
            self[key] = value

    def clear(self):
        self.data.clear()

    def __repr__(self):
        return f"{type(self).__name__}({self.data})"


class TinUIXml:  # TinUI的xml渲染方式
    """为TinUI提供更加方便的平面方式，使用xml
    TinUITheme基类无法直接使用，只能够重写TinUI或BasicTinUI的样式后才能够使用，参考 /theme 中的样式重写范例
    """

    def __init__(self, ui: Union["BasicTinUI", "TinUI", "TinUITheme"]):
        self.ui = ui
        if isinstance(ui, TinUIThemeBase):
            self.realui = ui.ui
        else:
            self.realui = ui
        self.noload = ("", "menubar")  # 当前不解析的标签
        self.intargs = (
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
        )  # 需要转为数字的参数
        self.scale_int = (
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
        self.dataargs = (
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
        )  # 需要转为数据结构的参数
        self.funcs = TinUIXmlFuncDict()  # 内部调用方法集合
        self.datas = {}  # 内部数据结构集合
        self.tags = {}  # 内部组件tag集合
        origin = self.__scale_value(5)
        self.xendx, self.xendy = origin, origin  # 横向最宽原点
        self.yendx, self.yendy = origin, origin  # 纵向最低原点

    def __scale_value(self, value: Union[int, float]):
        return self.realui.scale_value(value)

    def __attrib2kws(self, args: dict, ignorecmd):  # 将部分特定参数转化为正确类型
        for key in args:
            if key in self.intargs:
                args[key] = int(args[key])
                if key in self.scale_int:
                    args[key] = self.__scale_value(args[key])
            elif key in self.dataargs:
                if key == "command" and ignorecmd:
                    # 忽略command参数，允许开发者稍后定义
                    exec(f"{args[key]} = None")
                args[key] = eval(args[key])
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
        x=5,
        y=5,
        padx=5,
        pady=5,
        anchor="nw",
        ftags: list = [],
        ignorecmd=False,
    ):  # 根据xml的<line>逐行渲染TinUI组件
        last_y = y
        linex = None  # 纵块中的最大宽度
        padx = int(line.get("padx", padx))
        pady = int(line.get("pady", pady))
        _x = line.get("x", None)
        _x = self.__scale_value(int(_x)) if _x else x
        xendx = x = _x
        _y = line.get("y", None)
        _y = self.__scale_value(int(_y)) if _y else y
        xendy = y = _y
        padx = self.__scale_value(padx)
        pady = self.__scale_value(pady)
        allanchor = line.get("anchor", anchor)
        lineanchor = line.get("lineanchor", "")  # 整个模块的对齐方向
        ftag = "ftag-" + str(uuid.uuid1().hex)
        ftags.append(ftag)
        for i in line.iterfind("*"):  # 只检索直接子元素
            if i.tag == "line":
                liney, newlinex = self.__load_line(
                    i, xendx, xendy, padx, pady, allanchor, ftags, ignorecmd
                )
                if liney > self.yendy - pady:  # 在同一位置判断纵向大小
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
                    olds = eval(i.attrib["uids"])
                    news = []
                    for tag in olds:
                        uid = self.__tags2uid(tag)
                        news.append(uid)
                    i.attrib["uids"] = tuple(news)
            elif i.tag == "labelframe":  # 同back
                if "widgets" in i.attrib:
                    olds = eval(i.attrib["widgets"])
                    news = []
                    for tag in olds:
                        uid = self.__tags2uid(tag)
                        news.append(uid)
                    i.attrib["widgets"] = str(tuple(news))
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
            tagall = eval(f"self.ui.add_{i.tag}(**attrib)")
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
            return last_y, xendx
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
        return last_y, xendx

    def loadxml(self, xml: str):  # 从xml字符串载入窗口组件
        self.xendx, self.xendy = 5, 5  # 横向最宽原点
        self.yendx, self.yendy = 5, 5  # 纵向最低原点
        root = ET.fromstring(xml)
        if root.tag != "tinui":  # 严格控制规范
            return
        for line in root.findall("line"):
            y, _ = self.__load_line(line, y=self.yendy)
            if y > self.yendy - 5:
                self.yendy = y + 5

    def environment(
        self, dict_item: dict
    ):  # 在funcs和datas中加入默认标识内容，一般为globals()或locals()
        self.funcs = self.funcs | dict_item
        self.datas = self.datas | dict_item

    def clean(self):  # 清空TinUI
        self.realui.clean_windows()
        self.funcs.clear()
        self.datas.clear()
        self.tags.clear()
        self.xendx, self.xendy = 5, 5  # 横向最宽原点
        self.yendx, self.yendy = 5, 5  # 纵向最低原点
