"""
TinUIXml 面板布局模式测试

覆盖内容：
- 横向面板：固定尺寸 / 权重 / <sash> / 嵌套纵向面板
- 卡片面板：网格排列
- 根类型：expand / vertical / horizon / card
- 无背景面板（bg=''）的矩形测量
- <Configure> 尺寸重排
- 重复 loadxml 替换旧面板树
- clean() 后无面板残留，且不误删开发者自己的 <Configure> 绑定
- 流程模式（<line>）回归
- 若干非法结构的报错

运行：
    python tuxmlpanel.py          # 自动测试后退出
    python tuxmlpanel.py --show   # 保留窗口查看效果
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from tkinter import Tk

from TinUI import BasicTinUI, TinUIXml

# ========== 测试用 xml ==========
PANEL_XML = """
<tinui layout='panel' root='horizon' spacing='5' bg='#ffffff' padding='5,5,5,5'>
  <child size='150' min_size='50'>
    <verticalpanel bg='#e0f7fa' spacing='3'>
      <child weight='1'>
        <button2 text='a' command='self.funcs["cb"]'>btnA</button2>
      </child>
      <child>
        <paragraph text='hello'/>
      </child>
    </verticalpanel>
  </child>
  <child size='5'>
    <sash bg='#999999'/>
  </child>
  <child weight='1'>
    <cardpanel card_width='120' card_height='80' v_spacing='10'>
      <child><paragraph text='card1'/></child>
      <child><paragraph text='card2'/></child>
    </cardpanel>
  </child>
</tinui>
"""

EXPAND_XML = """
<tinui layout='panel' root='expand' margin='10'>
  <child weight='1'>
    <horizonpanel spacing='4' bg='#f0f0f0'>
      <child weight='1'><paragraph text='left'/></child>
      <child weight='2'><paragraph text='right'/></child>
    </horizonpanel>
  </child>
</tinui>
"""

VERTICAL_XML = """
<tinui layout='panel' root='vertical' spacing='2'>
  <child size='100'><paragraph text='a'/></child>
  <child weight='1'><paragraph text='b'/></child>
</tinui>
"""

CARD_XML = """
<tinui layout='panel' root='card' card_width='100' card_height='60' h_spacing='4' v_spacing='4'>
  <child><paragraph text='1'/></child>
  <child><paragraph text='2'/></child>
  <child><paragraph text='3'/></child>
</tinui>
"""

NOBG_XML = """
<tinui layout='panel' root='vertical'>
  <child weight='1'><paragraph text='transparent'/></child>
</tinui>
"""

FLOW_XML = """
<tinui>
  <line>
    <button text='one'/>
  </line>
</tinui>
"""

# ========== 辅助 ==========
cb_calls = []


def cb(event=None):
    cb_calls.append(event)


def make_tinui(root):
    """创建 BasicTinUI + TinUIXml，返回 (canvas, xml)。"""
    b = BasicTinUI(root, bg="white")
    b.set_scale(1.0)
    b.pack(fill="both", expand=True)
    root.update()
    x = TinUIXml(b)
    x.environment(globals())
    return b, x


def assert_rect(panel, name):
    x1, y1, x2, y2 = panel.get_rect()
    assert x2 > x1 and y2 > y1, f"{name} 矩形无效: {(x1, y1, x2, y2)}"


def expect_value_error(x, xml, tip):
    try:
        x.loadxml(xml)
    except ValueError:
        return
    raise AssertionError(f"应当抛出 ValueError: {tip}")


# ========== 用例 ==========
def test_horizon(root):
    b, x = make_tinui(root)
    x.loadxml(PANEL_XML)
    root.update()
    assert x._panel_root is not None, "未创建根面板"
    hr = x._panel_root
    assert len(hr.children) == 3, f"根横向面板应有3个子项，实际{len(hr.children)}"
    assert_rect(hr, "横向根面板")
    assert "btnA" in x.tags, "控件命名未登记到 tags"
    # 命令绑定可解析、可调用
    before = len(cb_calls)
    x.funcs["cb"]("invoke")
    assert len(cb_calls) == before + 1
    # 卡片网格
    card = hr.children[2][0]
    assert type(card).__name__ == "CardPanel"
    assert len(card.children) == 2
    # 尺寸重排
    live = hr.get_rect()
    root.geometry("500x400")
    root.update()
    resized = hr.get_rect()
    assert resized != live, "Configure 未触发重排"
    assert resized[2] < live[2], "缩小窗口后面板矩形未变小"
    x.clean()
    assert x._panel_root is None, "clean 未销毁面板"
    b.destroy()


def test_expand(root):
    b, x = make_tinui(root)
    x.loadxml(EXPAND_XML)
    root.update()
    assert x._panel_root is not None
    child = x._panel_root.child
    assert type(child).__name__ == "HorizonPanel"
    assert len(child.children) == 2
    x.clean()
    b.destroy()


def test_vertical(root):
    b, x = make_tinui(root)
    x.loadxml(VERTICAL_XML)
    root.update()
    vp = x._panel_root
    assert type(vp).__name__ == "VerticalPanel"
    assert len(vp.children) == 2
    assert vp.children[0][1] == 100, "size 应由 add_child 记录"
    assert vp.children[1][3] == 1.0, "weight 应被记录"
    x.clean()
    b.destroy()


def test_card(root):
    b, x = make_tinui(root)
    x.loadxml(CARD_XML)
    root.update()
    cp = x._panel_root
    assert type(cp).__name__ == "CardPanel"
    assert len(cp.children) == 3
    assert_rect(cp, "卡片根面板")
    x.clean()
    b.destroy()


def test_nobg(root):
    b, x = make_tinui(root)
    x.loadxml(NOBG_XML)
    root.update()
    vp = x._panel_root
    # 无背景时依旧能通过 get_rect() 得到有效矩形
    assert_rect(vp, "无背景面板")
    x.clean()
    b.destroy()


def test_flow(root):
    b, x = make_tinui(root)
    x.loadxml(FLOW_XML)
    root.update()
    assert x._panel_root is None, "流程模式不应创建面板"
    x.clean()
    b.destroy()


def test_replace_and_bind(root):
    """重复加载替换旧树；clean 不误删用户自己的 Configure 绑定。"""
    b, x = make_tinui(root)
    user_hits = []
    b.bind("<Configure>", lambda e: user_hits.append(1), add="+")

    x.loadxml(VERTICAL_XML)
    root.update()
    first_root = x._panel_root
    assert first_root is not None and x._panel_bind_id is not None

    x.loadxml(EXPAND_XML)
    root.update()
    assert x._panel_root is not first_root, "重复加载未替换旧面板树"

    hits_before = len(user_hits)
    x.clean()
    root.geometry("720x520")
    root.update()
    assert len(user_hits) > hits_before, "面板清理误删了用户 Configure 绑定"
    assert x._panel_root is None and x._panel_bind_id is None

    # clean 后仍可使用流程模式
    x.loadxml(FLOW_XML)
    root.update()
    assert x._panel_root is None
    b.destroy()


def test_errors(root):
    b, x = make_tinui(root)
    expect_value_error(x, "<tinui layout='panel' root='expand'></tinui>", "expand 根缺少子项")
    expect_value_error(x, "<tinui layout='panel' root='nope'></tinui>", "未知 root 类型")
    expect_value_error(
        x,
        "<tinui layout='panel' root='horizon'><child size='5'><sash><x/></sash></child></tinui>",
        "sash 含子元素",
    )
    expect_value_error(
        x,
        "<tinui layout='panel' root='expand'><child><line/></child></tinui>",
        "面板内使用流式标签",
    )
    expect_value_error(
        x,
        "<tinui layout='panel' root='vertical'><child><paragraph text='a'/><paragraph text='b'/></child></tinui>",
        "child 含多个元素",
    )
    b.destroy()


TESTS = (
    test_horizon,
    test_expand,
    test_vertical,
    test_card,
    test_nobg,
    test_flow,
    test_replace_and_bind,
    test_errors,
)


def main():
    root = Tk()
    root.geometry("800x600")
    root.title("TinUIXml面板布局测试")
    root.update()
    for case in TESTS:
        case(root)
        print(f"  [ok] {case.__name__}")
    if "--show" in sys.argv:
        root.deiconify()
        root.mainloop()
    else:
        root.destroy()
    print(f"{len(TESTS)} 项面板布局测试全部通过")


if __name__ == "__main__":
    main()
