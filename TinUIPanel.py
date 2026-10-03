import time

try:
    from .TinUI import BasicTinUI, TinUIString
except Exception as err:
    from TinUI import BasicTinUI, TinUIString

# 动画进行中标记
_ANIMATING = False
# 动画代次
_ANIM_GEN = 0


class BasePanel:
    """面板的基类"""

    def __init__(self, canvas:BasicTinUI, bg='', bd=9, line='', linew=0):
        self.canvas = canvas
        self.bg = bg
        self.line = line
        self._scale = canvas.scale_value
        self.bd = self._scale(bd, True)
        linew = self._scale(linew)
        self.linew_mask = (linew, linew, -linew, linew, -linew, -linew, linew, -linew)
        self.bg1 = self.canvas.create_polygon(0, 0, 0, 0, fill=line, outline=line, width=self.bd) # outline
        self.rect = f'panel-{self.bg1}'
        self.canvas.addtag_withtag(self.rect, self.bg1)
        self.bg2 = self.canvas.create_polygon(0, 0, 0, 0, fill=bg, outline=bg, width=self.bd, tags=self.rect) # back
        # 记录最近一次外框，供动画获取当前矩形（bg 为空时 fix_bg 不写 coords）
        self._last_rect = None
        self._bg_cache = None
        # 尺寸过渡动画配置
        self.animation_enabled = True
        self.animation_duration = 180  # 毫秒
        self.animation_interval = 16   # 目标帧间隔（毫秒）
        # 自适应帧率。单帧布局超预算时临时拉长间隔，有余量时缓慢回落
        # 时长始终由 perf_counter 决定
        self.animation_adaptive = True
        self.animation_interval_max = 66  # 帧间隔上限
        self._anim_cur_interval = self.animation_interval
        self._anim_id = None
        self._anim_start = None
        self._anim_target = None
        self._anim_duration = 0
        self._anim_t0 = 0.0

    def fix_bg(self, x1, y1, x2, y2):
        self._last_rect = (x1, y1, x2, y2)
        if not self.bg:
            return
        coords = (x1+self.bd/2, y1+self.bd/2, x2-self.bd/2, y1+self.bd/2, x2-self.bd/2, y2-self.bd/2, x1+self.bd/2, y2-self.bd/2)
        if coords == self._bg_cache:  # 坐标未变则跳过两次 coords 调用
            return
        self._bg_cache = coords
        backcoords = tuple(x+y for x, y in zip(coords, self.linew_mask))
        self.canvas.coords(self.bg2, backcoords)
        self.canvas.coords(self.bg1, coords)

    def destroy(self):
        self.stop_animation()
        self.canvas.delete(self.rect)

    def get_rect(self):
        """返回当前外框 (x1, y1, x2, y2)。"""
        if self._last_rect is not None:
            return self._last_rect
        coords = self.canvas.coords(self.bg1)
        if coords:
            return (coords[0]-self.bd/2, coords[1]-self.bd/2, coords[4]+self.bd/2, coords[5]+self.bd/2)
        return (0, 0, 0, 0)

    def stop_animation(self):
        if self._anim_id is not None:
            self.canvas.after_cancel(self._anim_id)
            self._anim_id = None
        self._anim_target = None

    def animate_layout(self, x1, y1, x2, y2, duration=None):
        """将面板尺寸从当前矩形线性过渡到目标矩形，每帧调用 update_layout。"""
        global _ANIM_GEN
        target = (x1, y1, x2, y2)
        start = self.get_rect()
        if duration is None:
            duration = self.animation_duration
        if (not self.animation_enabled) or duration <= 0 or start == target:
            self.stop_animation()
            self.update_layout(*target)
            return
        if self._anim_id is not None:
            self.canvas.after_cancel(self._anim_id)
            self._anim_id = None
        _ANIM_GEN += 1  # 新一段动画
        self._anim_start = start
        self._anim_target = target
        self._anim_duration = duration
        self._anim_cur_interval = self.animation_interval
        self._anim_t0 = time.perf_counter()
        self._anim_tick()  # 首帧同步执行，避免闪烁

    def _adapt_interval(self, cost):
        """按单帧布局耗时自适应帧间隔"""
        base = self.animation_interval
        if not self.animation_adaptive:
            self._anim_cur_interval = base
            return
        hi = min(self.animation_interval_max, max(base, self._anim_duration))
        cost_ms = cost * 1000.0
        if cost_ms > base:
            # 布局耗时已超过一帧预算：按实测耗时拉长，避免帧堆积
            target = cost_ms * 1.3
            self._anim_cur_interval = min(hi, max(self._anim_cur_interval * 1.25, target))
        else:
            # 有富余：缓慢向目标帧间隔回落
            self._anim_cur_interval = max(base, self._anim_cur_interval * 0.85)

    def _anim_tick(self):
        global _ANIMATING
        if self._anim_target is None:
            return
        t = (time.perf_counter() - self._anim_t0) / (self._anim_duration / 1000.0)
        final = t >= 1.0
        if final:
            t = 1.0
        s, e = self._anim_start, self._anim_target
        cur = tuple(round(a + (b - a) * t) for a, b in zip(s, e))
        _ANIMATING = not final
        t_frame = time.perf_counter()
        try:
            self.update_layout(*cur)
        finally:
            _ANIMATING = False
        self._adapt_interval(time.perf_counter() - t_frame)
        if final:
            self._anim_id = None
            self._anim_target = None
        else:
            interval = max(1, int(self._anim_cur_interval))
            self._anim_id = self.canvas.after(interval, self._anim_tick)


class ExpandablePanel(BasePanel):
    """可扩展面板的基类（VerticalPanel和HorizonPanel的父类）"""

    def __init__(self, canvas, padding=(0, 0, 0, 0), min_width=0, min_height=0, bg='', bd=9, line='', linew=0):
        super().__init__(canvas, bg, bd, line, linew)
        self.children = []
        self.padding = tuple(self._scale(i) for i in padding)
        self.min_width = self._scale(min_width)
        self.min_height = self._scale(min_height)
        self.spacing = 0
        # Tier 2：动画期间冻结子元素固有尺寸，避免每帧重复 bbox / get_max_size
        # 形如 {id(child): (_ANIM_GEN, size)}，非动画期间不使用
        self._metric_cache = {}

    def _measure_cached(self, child, measure):
        """动画帧内缓存子元素的固有尺寸；最后一帧（_ANIMATING=False）总是重新测量。"""
        if not _ANIMATING:
            return measure(child)
        key = id(child)
        entry = self._metric_cache.get(key)
        if entry is not None and entry[0] == _ANIM_GEN:
            return entry[1]
        value = measure(child)
        self._metric_cache[key] = (_ANIM_GEN, value)
        return value

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
                child[0].destroy()
            else:
                self.canvas.delete(child[0])
        self.children.clear()
    
    def destroy(self):
        self.stop_animation()
        self.clear_children()
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
            child[0].destroy()
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
        self, canvas, child=None, padding=(0, 0, 0, 0), min_width=0, min_height=0, bg='', bd=9, line='', linew=0
    ):
        super().__init__(canvas, bg, bd, line, linew)
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
                self.child.destroy()
            else:
                self.canvas.delete(self.child)
    
    def destroy(self):
        self.stop_animation()
        self.clear_children()
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
                if not _ANIMATING:
                    self.canvas.tag_raise(self.child.rect, self.rect)
            elif isinstance(self.child, TinUIString):
                # 注意：expand=True 不是文本重排，而是控件的填充/居中布局（entry、button 等
                # 在 expand=False 时会锚到左上角），因此动画中间帧也必须传 True。
                self.child.layout(content_x1, content_y1, content_x2, content_y2, True)
                if not _ANIMATING:
                    self.canvas.tag_raise(self.child, self.rect)


class VerticalPanel(ExpandablePanel):
    def __init__(
        self, canvas, padding=(0, 0, 0, 0), spacing=0, min_width=0, min_height=0, bg='', bd=9, line='', linew=0
    ):
        super().__init__(canvas, padding, min_width, min_height, bg, bd, line, linew)
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

    def _child_height(self, child):
        """子元素固有高度"""
        return self._measure_cached(child, self._measure_child_height)

    def _measure_child_height(self, child):
        if isinstance(child, TinUIString):
            bbox = self.canvas.bbox(child)
            return (bbox[3] - bbox[1]) if bbox else 0
        if isinstance(child, HorizonPanel):
            return child.get_max_size()
        return self._scale(100)

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
        last = len(self.children) - 1
        items = []
        for i, (child, height, min_height, weight) in enumerate(self.children):
            spacing = self.spacing if i < last else 0
            if not height:
                height = self._child_height(child)
            items.append((child, height, min_height, weight, spacing))
            if weight > 0:
                total_weight += weight
            else:
                fixed_size += max(height, min_height) + spacing
        # 计算剩余空间
        remaining_height = max(0, content_height - fixed_size)
        current_y = content_y1
        for child, height, min_height, weight, spacing in items:
            # 计算元素高度
            if weight > 0 and total_weight > 0:
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
                if not _ANIMATING:
                    self.canvas.tag_raise(child.rect, self.rect)
            elif isinstance(child, TinUIString):
                child.layout(content_x1, current_y, content_x2, child_y2)
                if not _ANIMATING:
                    self.canvas.tag_raise(child, self.rect)
            current_y += actual_height + spacing
            # 如果已经超出面板底部，停止布局
            if current_y >= content_y2:
                break


class HorizonPanel(ExpandablePanel):
    def __init__(
        self, canvas, padding=(0, 0, 0, 0), spacing=0, min_width=0, min_height=0, bg='', bd=9, line='', linew=0
    ):
        super().__init__(canvas, padding, min_width, min_height, bg, bd, line, linew)
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

    def _child_width(self, child):
        """子元素固有宽度（仅在 width 缺省时调用一次；动画帧内走缓存）。"""
        return self._measure_cached(child, self._measure_child_width)

    def _measure_child_width(self, child):
        if isinstance(child, TinUIString):
            bbox = self.canvas.bbox(child)
            return (bbox[2] - bbox[0]) if bbox else 0
        if isinstance(child, VerticalPanel):
            return child.get_max_size()
        return self._scale(100)

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
        last = len(self.children) - 1
        items = []
        for i, (child, width, min_width, weight) in enumerate(self.children):
            spacing = self.spacing if i < last else 0
            if not width:
                width = self._child_width(child)
            items.append((child, width, min_width, weight, spacing))
            if weight > 0:
                total_weight += weight
            else:
                fixed_size += max(width, min_width) + spacing
        remaining_width = max(0, content_width - fixed_size)
        current_x = content_x1
        for child, width, min_width, weight, spacing in items:
            if weight > 0 and total_weight > 0:
                proportional_width = remaining_width * weight / total_weight
                actual_width = max(proportional_width, min_width)
            else:
                actual_width = max(width, min_width)
            child_x2 = current_x + actual_width
            if child_x2 > content_x2:
                child_x2 = content_x2
            if issubclass(child.__class__, BasePanel):
                child.update_layout(current_x, content_y1, child_x2, content_y2)
                if not _ANIMATING:
                    self.canvas.tag_raise(child.rect, self.rect)
            elif isinstance(child, TinUIString):
                child.layout(current_x, content_y1, child_x2, content_y2)
                if not _ANIMATING:
                    self.canvas.tag_raise(child, self.rect)
            current_x += actual_width + spacing
            if current_x >= content_x2:
                break


class CardPanel(ExpandablePanel):
    """卡片面板：子元素以固定宽高网格/流式排列，高度随内容自适应（无限）"""
    def __init__(self, canvas, card_width=100, card_height=100, padding=(0, 0, 0, 0), h_spacing=5, v_spacing=5, min_width=0, bg='', bd=9, line='', linew=0):
        # min_height 固定为 0，高度完全由内容决定
        super().__init__(canvas, padding, min_width, 0, bg, bd, line, linew)
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
                if not _ANIMATING:
                    self.canvas.tag_raise(child.rect, self.rect)
            elif isinstance(child, TinUIString):
                child.layout(child_x1, child_y1, child_x2, child_y2)
                if not _ANIMATING:
                    self.canvas.tag_raise(child, self.rect)


class PanelSash(BasePanel):
    """
    面板拉伸条
    用于动态调整 HorizontalPanel 或 VerticalPanel 中相邻子元素的尺寸或权重
    """
    def __init__(self, parent_panel, bg='#cccccc', bd=0, line='', linew=0, draggable=True):
        # 传入的 parent_panel 必须是 VerticalPanel 或 HorizonPanel
        super().__init__(parent_panel.canvas, bg, bd, line, linew)
        self.parent = parent_panel
        
        # 判断方向
        if isinstance(parent_panel, HorizonPanel):
            self.orientation = 'h'
            self.cursor = 'sb_h_double_arrow'
        elif isinstance(parent_panel, VerticalPanel):
            self.orientation = 'v'
            self.cursor = 'sb_v_double_arrow'
        else:
            raise ValueError("PanelSash 仅能在 HorizonPanel 或 VerticalPanel 中使用")

        self._drag_data = {}

        # 绑定鼠标事件
        if draggable:
            self.canvas.tag_bind(self.rect, '<ButtonPress-1>', self.start_drag)
            self.canvas.tag_bind(self.rect, '<B1-Motion>', self.on_drag)
            self.canvas.tag_bind(self.rect, '<Enter>', self.on_enter)
            self.canvas.tag_bind(self.rect, '<Leave>', self.on_leave)

    def update_layout(self, x1, y1, x2, y2):
        self.fix_bg(x1, y1, x2, y2)

    def on_enter(self, _):
        self.canvas.config(cursor=self.cursor)

    def on_leave(self, _):
        self.canvas.config(cursor='')

    def _get_child_size(self, child):
        """获取相邻元素的当前像素尺寸（宽度或高度）"""
        if issubclass(child.__class__, BasePanel):
            coords = self.canvas.coords(child.rect)
            if not coords or len(coords) < 6:
                return 0
            # 还原真实的宽高：消除 self.bd/2 导致的坐标偏移
            if self.orientation == 'h':
                return coords[4] - coords[0] + child.bd
            else:
                return coords[5] - coords[1] + child.bd
        elif isinstance(child, TinUIString):
            bbox = self.canvas.bbox(child)
            if not bbox:
                return 0
            if self.orientation == 'h':
                return bbox[2] - bbox[0]
            else:
                return bbox[3] - bbox[1]
        return 0

    def start_drag(self, event):
        idx = -1
        for i, c in enumerate(self.parent.children):
            if c[0] == self:
                idx = i
                break
        
        # 必须存在于父组件中，且不能是首尾元素（需要有相邻的左右/上下元素才能拉伸）
        if idx <= 0 or idx >= len(self.parent.children) - 1:
            self._drag_data = {}
            return

        self._drag_data['idx'] = idx
        self._drag_data['start_x'] = event.x
        self._drag_data['start_y'] = event.y

        # 获取左右或上下元素的配置和实时像素大小
        left_child = self.parent.children[idx-1]
        right_child = self.parent.children[idx+1]
        
        self._drag_data['left_px'] = self._get_child_size(left_child[0])
        self._drag_data['right_px'] = self._get_child_size(right_child[0])
        self._drag_data['left_cfg'] = left_child
        self._drag_data['right_cfg'] = right_child

    def on_drag(self, event):
        if not self._drag_data:
            return

        idx = self._drag_data['idx']
        # 计算鼠标移动的差值
        delta = event.x - self._drag_data['start_x'] if self.orientation == 'h' else event.y - self._drag_data['start_y']

        left_c, left_size, left_min, left_weight = self._drag_data['left_cfg']
        right_c, right_size, right_min, right_weight = self._drag_data['right_cfg']

        left_px = self._drag_data['left_px']
        right_px = self._drag_data['right_px']

        # 确保尺寸至少为1，避免挤压到负数或 0 导致错位
        actual_left_min = max(left_min, 1)
        actual_right_min = max(right_min, 1)

        # 限制 delta，避免相邻元素被压缩到超出最小限制
        max_negative_delta = actual_left_min - left_px  
        max_positive_delta = right_px - actual_right_min 

        if delta < max_negative_delta:
            delta = max_negative_delta
        if delta > max_positive_delta:
            delta = max_positive_delta

        if delta == 0:
            return

        new_left_size = left_size
        new_left_weight = left_weight
        new_right_size = right_size
        new_right_weight = right_weight

        # 策略计算
        if left_weight == 0 and right_weight == 0:
            # 双固定尺寸
            curr_l_size = left_px if left_size == 0 else left_size
            curr_r_size = right_px if right_size == 0 else right_size
            new_left_size = curr_l_size + delta
            new_right_size = curr_r_size - delta

        elif left_weight > 0 and right_weight > 0:
            # 双权重分配
            total_weight = left_weight + right_weight
            total_px = left_px + right_px
            new_l_px = left_px + delta
            
            if total_px > 0:
                new_left_weight = (new_l_px / total_px) * total_weight
                new_right_weight = total_weight - new_left_weight

        elif left_weight == 0 and right_weight > 0:
            # 左固定，右权重
            curr_l_size = left_px if left_size == 0 else left_size
            new_left_size = curr_l_size + delta

        elif left_weight > 0 and right_weight == 0:
            # 左权重，右固定
            curr_r_size = right_px if right_size == 0 else right_size
            new_right_size = curr_r_size - delta

        # 更新父组件的子元素列表 tuple (child, size, min_size, weight)
        self.parent.children[idx-1] = (left_c, new_left_size, left_min, new_left_weight)
        self.parent.children[idx+1] = (right_c, new_right_size, right_min, new_right_weight)

        # 反算触发父组件局部重绘
        p_coords = self.canvas.coords(self.parent.rect)
        if p_coords:
            bd = self.parent.bd
            x1 = p_coords[0] - bd/2
            y1 = p_coords[1] - bd/2
            x2 = p_coords[4] + bd/2
            y2 = p_coords[5] + bd/2
            self.parent.update_layout(x1, y1, x2, y2)


# 此行（不含）以下代码不受GPLv3、LGPLv3许可证的限制，可以自由使用、修改、分发等。
if __name__ == "__main__":
    from tkinter import Tk
    from ctypes import windll
    shcore = windll.shcore
    shcore.SetProcessDpiAwareness(2)
    scale_factor = shcore.GetScaleFactorForDevice(0) / 100
    # scale_factor = 1

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

    ep = ExpandPanel(b)

    ct = b.add_passwordbox((0,0),width=100)[-1]
    ep.set_child(ct)
    hp.add_child(ep, weight=1)

    v1 = VerticalPanel(b, bg='#e0f7fa')
    hp.add_child(v1, size=150, min_size=50) # 左侧面板，固定宽度150，不能拉伸小于50

    # 添加拉伸条
    sash1 = PanelSash(hp, bg='#999999')
    hp.add_child(sash1, size=5)

    # 包含中间卡片的带权重的面板
    card = CardPanel(b, bg='#fff3e0', v_spacing=10)
    hp.add_child(card, weight=1) # 中间面板，自适应填充权重
    
    sash2 = PanelSash(hp, bg='#999999', draggable=False) # 不可拖动的分隔条
    hp.add_child(sash2, size=5)
    
    # 放入右侧固定尺寸的面板
    v2 = VerticalPanel(b, bg='#f1f8e9')
    hp.add_child(v2, size=150)

    for i in range(10):
        vp = VerticalPanel(b, bg='#f1f8e9', line='#e5e5e5', linew=1)
        button = b.add_button2((0,0), text=f"Button{i}", anchor='center', command=lambda e, v=vp: (card.remove_child(v),b.event_generate("<Configure>",x=0,y=0,width=b.winfo_width(),height=b.winfo_height())))[-1]
        vp.add_child(button)
        vp.add_child(b.add_paragraph((0,0), text=f"Paragraph{i}", anchor='center'))
        card.add_child(vp)

    # 尺寸过渡演示：在“充满画布”与“内缩”之间线性过渡整棵面板树
    def toggle_anim():
        w, h = b.winfo_width(), b.winfo_height()
        if rp.get_rect() != (5, 5, w - 5, h - 5):
            rp.animate_layout(5, 5, w - 5, h - 5)
        else:
            rp.animate_layout(60, 60, w - 60, h - 60)

    b.add_button2((10, 10), text="尺寸过渡动画", anchor='center', command=lambda e: toggle_anim())

    def update(e):
        rp.update_layout(5, 5, e.width - 5, e.height - 5)

    b.bind("<Configure>", update)
    a.mainloop()