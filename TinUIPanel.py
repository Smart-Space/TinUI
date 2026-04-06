try:
    from .TinUI import BasicTinUI, TinUIString
except Exception as err:
    from TinUI import BasicTinUI, TinUIString


class BasePanel:
    """面板的基类"""

    def __init__(self, canvas:BasicTinUI, bg='', bd=9):
        self.canvas = canvas
        self.bg = bg
        self._scale = canvas.scale_value
        self.bd = self._scale(bd)
        self.rect = self.canvas.create_polygon(0, 0, 0, 0, fill=bg, outline=bg, width=self.bd)

    def fix_bg(self, x1, y1, x2, y2):
        if self.bg:
            coords = (x1+self.bd/2, y1+self.bd/2, x2-self.bd/2, y1+self.bd/2, x2-self.bd/2, y2-self.bd/2, x1+self.bd/2, y2-self.bd/2)
            self.canvas.coords(self.rect, coords)


class ExpandablePanel(BasePanel):
    """可扩展面板的基类（VerticalPanel和HorizonPanel的父类）"""

    def __init__(self, canvas, padding=(0, 0, 0, 0), min_width=0, min_height=0, bg='', bd=9):
        super().__init__(canvas, bg, bd)
        self.children = []
        self.padding = tuple(self._scale(i) for i in padding)
        self.min_width = self._scale(min_width)
        self.min_height = self._scale(min_height)
        self.spacing = 0

    def set_padding(self, padding):
        self.padding = tuple(self._scale(i) for i in padding)

    def set_min_size(self, min_width, min_height):
        self.min_width = self._scale(min_width)
        self.min_height = self._scale(min_height)

    def set_spacing(self, spacing):
        self.spacing = self._scale(spacing)

    def clear_children(self):
        for child in self.children:
            if issubclass(child[0].__class__, BasePanel):
                child[0].clear_children()
            else:
                self.canvas.delete(child[0])
        self.children.clear()
        self.canvas.delete(self.rect)

    def remove_child(self, index):
        if isinstance(index, int):
            child = self.children.pop(index)
        else:
            for i, c in enumerate(self.children):
                if c[0] == index:
                    child = self.children.pop(i)
                    break
        if issubclass(child[0].__class__, BasePanel):
            child[0].clear_children()
        else:
            self.canvas.delete(child[0])

    def pop_child(self, index):
        if isinstance(index, int):
            child = self.children.pop(index)
        else:
            for i, c in enumerate(self.children):
                if c[0] == index:
                    child = self.children.pop(i)
                    break
        return child[0]  # 开发者自己应当（可以）知道返回的对象类型

    def add_child(self, child, size=None, min_size=0, weight=0, index=-1):
        if index == -1:
            index = len(self.children)
        if size:
            size = self._scale(size)
        self.children.insert(index, (child, size, min_size, weight))


class ExpandPanel(BasePanel):
    def __init__(
        self, canvas, child=None, padding=(0, 0, 0, 0), min_width=0, min_height=0, bg='', bd=9
    ):
        super().__init__(canvas, bg, bd)
        self.child = child
        self.padding = tuple(self._scale(i) for i in padding)
        self.min_width = self._scale(min_width)
        self.min_height = self._scale(min_height)
        # self.create_bg("#e0f7fa", "#00838f")

    def set_padding(self, padding):
        self.padding = tuple(self._scale(i) for i in padding)

    def set_min_size(self, min_width, min_height):
        self.min_width = self._scale(min_width)
        self.min_height = self._scale(min_height)

    def set_child(self, child):
        self.child = child
    
    def clear_children(self):
        if self.child:
            if issubclass(self.child.__class__, BasePanel):
                self.child.clear_children()
            else:
                self.canvas.delete(self.child)
        self.canvas.delete(self.rect)

    def update_layout(self, x1, y1, x2, y2):
        # 应用内边距
        top, right, bottom, left = self.padding
        content_x1 = x1 + left
        content_y1 = y1 + top
        content_x2 = x2 - right
        content_y2 = y2 - bottom
        # 确保内容区域不小于最小尺寸
        content_width = max(content_x2 - content_x1, self.min_width)
        content_height = max(content_y2 - content_y1, self.min_height)
        content_x2 = content_x1 + content_width
        content_y2 = content_y1 + content_height
        # 更新背景位置
        self.fix_bg(x1, y1, x2, y2)
        # 更新子元素位置
        if self.child:
            if issubclass(self.child.__class__, BasePanel):
                self.child.update_layout(content_x1, content_y1, content_x2, content_y2)
                self.canvas.tag_raise(self.child.rect, self.rect)
            elif isinstance(self.child, TinUIString):
                self.child.layout(content_x1, content_y1, content_x2, content_y2, True)
                self.canvas.tag_raise(self.child, self.rect)


class VerticalPanel(ExpandablePanel):
    def __init__(
        self, canvas, padding=(0, 0, 0, 0), spacing=0, min_width=0, min_height=0, bg='', bd=9
    ):
        super().__init__(canvas, padding, min_width, min_height, bg, bd)
        self.spacing = self._scale(spacing)
        # self.create_bg("#f1f8e9", "#558b2f")

    def get_max_size(self):
        # 元素最大宽度
        max_size = 0
        for c in self.children:
            if isinstance(c[0], TinUIString):
                bbox = self.canvas.bbox(c[0])
                max_size = max(max_size, bbox[2] - bbox[0])
        return max_size+self.padding[1]+self.padding[3]

    def update_layout(self, x1, y1, x2, y2):
        top, right, bottom, left = self.padding
        content_x1 = x1 + left
        content_y1 = y1 + top
        content_x2 = x2 - right
        content_y2 = y2 - bottom
        content_width = max(content_x2 - content_x1, self.min_width)
        content_height = max(content_y2 - content_y1, self.min_height)
        content_x2 = content_x1 + content_width
        content_y2 = content_y1 + content_height
        # 更新背景位置
        self.fix_bg(x1, y1, x2, y2)
        # 计算总权重和固定尺寸
        total_weight = 0
        fixed_size = 0
        for i, (child, height, min_height, weight) in enumerate(self.children):
            # 计算间距（最后一个元素不加间距）
            spacing = self.spacing if i < len(self.children) - 1 else 0

            if not height:
                if isinstance(child, TinUIString):
                    bbox = self.canvas.bbox(child)
                    height = bbox[3] - bbox[1]
                elif isinstance(child, HorizonPanel):
                    height = child.get_max_size()
                else:
                    height = self._scale(100)

            if weight > 0:
                total_weight += weight
            else:
                actual_height = max(height, min_height)
                fixed_size += actual_height + spacing
        # 计算剩余空间
        remaining_height = max(0, content_height - fixed_size)
        current_y = content_y1
        total_children = len(self.children)
        for i, (child, height, min_height, weight) in enumerate(self.children):
            # 计算间距（最后一个元素不加间距）
            spacing = self.spacing if i < total_children - 1 else 0
            if not height:
                if isinstance(child, TinUIString):
                    bbox = self.canvas.bbox(child)
                    height = bbox[3] - bbox[1]
                elif isinstance(child, HorizonPanel):
                    height = child.get_max_size()
                else:
                    height = self._scale(100)
            # 计算元素高度
            if weight > 0:
                # 按权重分配剩余空间
                proportional_height = remaining_height * weight / total_weight
                actual_height = max(proportional_height, min_height)
            else:
                actual_height = max(height, min_height)
            child_y2 = current_y + actual_height
            # 确保不会超出面板范围
            if child_y2 > content_y2:
                child_y2 = content_y2
            # 更新子元素位置
            if issubclass(child.__class__, BasePanel):
                child.update_layout(content_x1, current_y, content_x2, child_y2)
                self.canvas.tag_raise(child.rect, self.rect)
            elif isinstance(child, TinUIString):
                child.layout(content_x1, current_y, content_x2, child_y2)
                self.canvas.tag_raise(child, self.rect)
            current_y += actual_height + spacing
            # 如果已经超出面板底部，停止布局
            if current_y >= content_y2:
                break


class HorizonPanel(ExpandablePanel):
    def __init__(
        self, canvas, padding=(0, 0, 0, 0), spacing=0, min_width=0, min_height=0, bg='', bd=9
    ):
        super().__init__(canvas, padding, min_width, min_height, bg, bd)
        self.spacing = self._scale(spacing)
        # self.create_bg("#fff3e0", "#f57c00")

    def get_max_size(self):
        # 元素最大宽度
        max_size = 0
        for c in self.children:
            if isinstance(c[0], TinUIString):
                bbox = self.canvas.bbox(c[0])
                max_size = max(max_size, bbox[3] - bbox[1])
        return max_size+self.padding[0]+self.padding[2]

    def update_layout(self, x1, y1, x2, y2):
        top, right, bottom, left = self.padding
        content_x1 = x1 + left
        content_y1 = y1 + top
        content_x2 = x2 - right
        content_y2 = y2 - bottom
        content_width = max(content_x2 - content_x1, self.min_width)
        content_height = max(content_y2 - content_y1, self.min_height)
        content_x2 = content_x1 + content_width
        content_y2 = content_y1 + content_height
        # 更新背景位置
        self.fix_bg(x1, y1, x2, y2)
        total_weight = 0
        fixed_size = 0
        for i, (child, width, min_width, weight) in enumerate(self.children):
            spacing = self.spacing if i < len(self.children) - 1 else 0
            if not width:
                if isinstance(child, TinUIString):
                    bbox = self.canvas.bbox(child)
                    width = bbox[2] - bbox[0]
                elif isinstance(child, VerticalPanel):
                    width = child.get_max_size()
                else:
                    width = self._scale(100)
            if weight > 0:
                total_weight += weight
            else:
                actual_width = max(width, min_width)
                fixed_size += actual_width + spacing
        remaining_width = max(0, content_width - fixed_size)
        current_x = content_x1
        total_children = len(self.children)
        for i, (child, width, min_width, weight) in enumerate(self.children):
            spacing = self.spacing if i < total_children - 1 else 0
            if not width:
                if isinstance(child, TinUIString):
                    bbox = self.canvas.bbox(child)
                    width = bbox[2] - bbox[0]
                elif isinstance(child, VerticalPanel):
                    width = child.get_max_size()
                else:
                    width = self._scale(100)
            if weight > 0:
                proportional_width = remaining_width * weight / total_weight
                actual_width = max(proportional_width, min_width)
            else:
                actual_width = max(width, min_width)
            child_x2 = current_x + actual_width
            if child_x2 > content_x2:
                child_x2 = content_x2
            if issubclass(child.__class__, BasePanel):
                child.update_layout(current_x, content_y1, child_x2, content_y2)
                self.canvas.tag_raise(child.rect, self.rect)
            elif isinstance(child, TinUIString):
                child.layout(current_x, content_y1, child_x2, content_y2)
                self.canvas.tag_raise(child, self.rect)
            current_x += actual_width + spacing
            if current_x >= content_x2:
                break


class CardPanel(ExpandablePanel):
    """卡片面板：子元素以固定宽高网格/流式排列，高度随内容自适应（无限）"""
    def __init__(self, canvas, card_width=100, card_height=100, padding=(0, 0, 0, 0), h_spacing=5, v_spacing=5, min_width=0, bg='', bd=9):
        # min_height 固定为 0，高度完全由内容决定
        super().__init__(canvas, padding, min_width, 0, bg, bd)
        self.card_width = self._scale(card_width)
        self.card_height = self._scale(card_height)
        self.h_spacing = self._scale(h_spacing)
        self.v_spacing = self._scale(v_spacing)

    def set_card_size(self, width, height):
        """动态调整卡片统一尺寸，调整后需重新触发 update_layout"""
        self.card_width = self._scale(width)
        self.card_height = self._scale(height)
    
    def set_spacing(self, horizontal=None, vertical=None):
        if horizontal is not None:
            self.h_spacing = self._scale(horizontal)
        if vertical is not None:
            self.v_spacing = self._scale(vertical)

    def add_child(self, child, index=-1):
        """添加卡片子元素"""
        if index == -1:
            index = len(self.children)
        self.children.insert(index, (child, 0, 0, 0))

    def update_layout(self, x1, y1, x2, _):
        top, right, bottom, left = self.padding
        content_x1 = x1 + left
        content_x2 = x2 - right
        avail_width = content_x2 - content_x1

        cols = max(1, (avail_width + self.h_spacing) // (self.card_width + self.h_spacing))

        num_children = len(self.children)
        rows = (num_children + cols - 1) // cols if num_children > 0 else 1

        total_content_height = rows * self.card_height + max(0, rows - 1) * self.v_spacing
        content_y1 = y1 + top

        self.fix_bg(x1, y1, x2, content_y1 + total_content_height + bottom)

        for i, (child, _, _, _) in enumerate(self.children):
            col = i % cols
            row = i // cols

            child_x1 = content_x1 + col * (self.card_width + self.h_spacing)
            child_y1 = content_y1 + row * (self.card_height + self.v_spacing)
            child_x2 = child_x1 + self.card_width
            child_y2 = child_y1 + self.card_height

            if issubclass(child.__class__, BasePanel):
                child.update_layout(child_x1, child_y1, child_x2, child_y2)
                self.canvas.tag_raise(child.rect, self.rect)
            elif isinstance(child, TinUIString):
                child.layout(child_x1, child_y1, child_x2, child_y2)
                self.canvas.tag_raise(child, self.rect)


# 此行（不含）以下代码不受GPLv3、LGPLv3许可证的限制，可以自由使用、修改、分发等。
if __name__ == "__main__":
    from tkinter import Tk
    from ctypes import windll
    shcore = windll.shcore
    shcore.SetProcessDpiAwareness(2)
    scale_factor = shcore.GetScaleFactorForDevice(0) / 100

    # panel test
    a = Tk()
    a.geometry("800x800+5+5")
    a.title("TinUIPanel")
    a.iconbitmap("LOGO.ico")
    b = BasicTinUI(a, bg="white")
    b.set_scale(scale_factor)
    b.pack(fill="both", expand=True)
    rp = ExpandPanel(b)
    hp = HorizonPanel(b, bg="#fff3e0", bd=0)
    rp.set_child(hp)

    v1 = ExpandPanel(b, bg='#e0f7fa')
    # v1=VerticalPanel(b, bg='#f1f8e9')

    hp.add_child(v1, size=150, weight=1)
    # hp.add_child(v1,size=150)

    cts = b.add_waitbar3((0,0),anchor='center')
    ct = cts[-1]
    cts[-2].start()

    v1.set_child(ct)
    # hp.add_child(ct, weight=1)

    v2 = VerticalPanel(b, bg='#f1f8e9')
    hp.add_child(v2, size=150)

    card = CardPanel(b, bg='#fff3e0', v_spacing=10)
    hp.add_child(card, weight=1)

    for i in range(10):
        vp = VerticalPanel(b, bg='#f1f8e9')
        button = b.add_button2((0,0), text=f"Button{i}", anchor='center', command=lambda e, v=vp: (card.remove_child(v),b.event_generate("<Configure>",x=0,y=0,width=b.winfo_width(),height=b.winfo_height())))[-1]
        vp.add_child(button)
        vp.add_child(b.add_paragraph((0,0), text=f"Paragraph{i}", anchor='center'))
        card.add_child(vp)
    hp.remove_child(v2)

    def update(e):
        rp.update_layout(5, 5, e.width - 5, e.height - 5)

    b.bind("<Configure>", update)
    a.mainloop()