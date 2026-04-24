"""
<TinUI theme dual preview for BasicTinUI.>
    Copyright (C) <2021-present>  <smart-space>
基于GPLv3和额外的LPGLv3许可发布
"""

from tkinter import Tk

from tinui import TinUI, BasicTinUI, TinUIXml

from tinuilight import TinUILight
from tinuidark import TinUIDark


def _build_demo(ui: BasicTinUI, theme_, title: str, width: int):
    def end(pad=10):
        bbox = ui.bbox("all")
        if bbox is None:
            return (pad, pad)
        return (pad, bbox[3] + 10)

    theme = theme_(ui)

    theme.add_title(end(), text=title)
    theme.add_paragraph(
        end(),
        text="BasicTinUI",
    )

    theme.add_button(end(), text="TinUI theme button")
    theme.add_checkbutton(end(), text="test checkbutton")
    theme.add_label(end(), text="test label")
    theme.add_entry(end(), text="test entry", width=width - 40)
    theme.add_separate(end(), width=width - 20)
    theme.add_radiobutton(end(), width - 20, "test radiobutton", ("1", "2", "3", "4", "5"))
    theme.add_link(end(), text="test link", url="smart-space.com.cn")
    theme.add_waitbar1(end())

    labelframey = end()[1] + 30
    lb1 = theme.add_button((10, labelframey), text="labelframe button1")[1]
    lb2 = theme.add_button(end(), text="labelframe button2")[-1]
    lb3 = theme.add_button(end(), text="labelframe button3")[-1]
    theme.add_labelframe((lb1, lb2, lb3), title="labelframe")

    theme.add_combobox(end(), text="test combobox", content=("1", "2", "3", "4", "5"))
    theme.add_progressbar((end()[0], end()[1] + 130), width=width - 20)[4](75)
    theme.add_table(
        end(),
        data=[["t1", "t2", "t3"], ["tinui", "table", "test"], ["1", "2", "3"]],
    )
    theme.add_onoff(end())
    theme.add_spinbox(end(), data=("1", "2", "3", "4", "5"))
    theme.add_scalebar(end())
    theme.add_info(end(), info_text="info test")

    ui.add_back(end())
    l1 = theme.add_label(end(), text="menubar test label")[-1]
    theme.add_menubar(l1, cont=(("test1", print), ("test2", print), "-", ("test3", print)))
    l2 = theme.add_label(end(), text="tooltip test label")[-1]
    theme.add_tooltip(l2, text="test tooltip")

    theme.add_waitbar3(end())
    textx, texty = end()
    text = theme.add_textbox((textx, texty), width=width - 40)[0]
    theme.add_scrollbar((textx + width - 35, texty), text)
    theme.add_listbox(
        end(),
        data=(
            "first",
            "second",
            "third",
            "some thing between three and four called bleem",
            "forth",
            "fifth",
            "some thins behind five\nwhich we can not find it\nfor-\never",
        ),
    )
    theme.add_pipspager(end(), num=5)

    ntb = theme.add_notebook(end(), width=width - 20, height=200)[-2]
    for i in range(1, 4):
        ntb.addpage("test" + str(i), "t" + str(i))
    ntvdict = ntb.getvdict()
    num = 1
    for i in ntvdict:
        sub_ui = ntvdict[i][0]
        uxml = TinUIXml(theme_(sub_ui))
        xml = f"""
<tinui>
    <line><button text='这是第{num}个BasicTinUI组件' command='print'></button></line>
    <line><label text='TinUI的标签栏视图'></label><label text='每个都是单独页面'></label></line>
</tinui>"""
        uxml.loadxml(xml)
        num += 1

    theme.add_ratingbar(end())
    theme.add_radiobox(end(), command=print)
    theme.add_notecard(end())
    theme.add_pivot(end())
    theme.add_button2(end(), "button2")
    theme.add_accentbutton(end(), "accentbutton")
    theme.add_warningbutton(end(), "warningbutton")
    theme.add_toolbutton(end(), "", icon="\uE90F")
    theme.add_expander(end())
    theme.add_listview(end(), num=8, width=width - 20, height=240)
    theme.add_treeview(end(), width=width - 20, height=220)
    theme.add_togglebutton(end(), text="状态开关按钮")
    theme.add_picker(end())
    theme.add_menubutton(end(), text="menubutton")
    theme.add_barbutton(end())
    flylabel = theme.add_label(end(), text="Flyout控件(左键单击)")[-1]
    theme.add_flyout(flylabel, anchor="ne")
    bdf = theme.add_breadcrumb(end())[-2]
    for i in range(1, 4):
        bdf.add(f"item{i}")
    theme.add_segmentbutton(end(), content=("tkinter", "TinUI", "Others"))
    theme.add_navigation(end())


def _sync_mousewheel(parent: TinUI, child: BasicTinUI):
    def _on_mousewheel(event):
        parent.event_generate("<MouseWheel>", state=event.state, delta=event.delta)

    child.bind("<MouseWheel>", _on_mousewheel, True)


def main():
    root = Tk()
    root.title("TinUI Light/Dark Dual Theme")
    root.geometry("800x720+200+100")

    main_ui = TinUI(root)
    main_ui.pack(fill="both", expand=True)

    margin = 10
    gutter = 20
    column_width = 350

    left_ui = BasicTinUI(main_ui, width=column_width, height=600)
    right_ui = BasicTinUI(main_ui, width=column_width, height=600)
    left_ui.TINUIFONT = main_ui.TINUIFONT
    left_ui.TINUIFONTSIZE = main_ui.TINUIFONTSIZE
    right_ui.TINUIFONT = main_ui.TINUIFONT
    right_ui.TINUIFONTSIZE = main_ui.TINUIFONTSIZE

    left_window = main_ui.create_window(
        (margin, margin),
        window=left_ui,
        width=column_width,
        height=600,
        anchor="nw",
    )
    right_window = main_ui.create_window(
        (margin + column_width + gutter, margin),
        window=right_ui,
        width=column_width,
        height=600,
        anchor="nw",
    )

    _build_demo(left_ui, TinUILight, "TinUILight", column_width-50)
    _build_demo(right_ui, TinUIDark, "TinUIDark", column_width-50)

    _sync_mousewheel(main_ui, left_ui)
    _sync_mousewheel(main_ui, right_ui)

    left_bbox = left_ui.bbox("all")
    right_bbox = right_ui.bbox("all")
    left_height = left_bbox[3] + margin if left_bbox else 600
    right_height = right_bbox[3] + margin if right_bbox else 600
    main_ui.itemconfig(left_window, height=left_height)
    main_ui.itemconfig(right_window, height=right_height)
    main_ui.config(scrollregion=main_ui.bbox("all"))

    root.mainloop()


if __name__ == "__main__":
    main()
