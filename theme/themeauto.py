'''
TinUI自动主题
跟随系统的亮暗模式设置，在TinUILight与TinUIDark之间自动切换
'''

import os
import sys
from typing import Union
import winreg

try:  #作为tinui包的子模块被导入（pip安装）
    from .. import TinUI, BasicTinUI, TinUITheme, TinUIXml
except ImportError:  #源码目录
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    from TinUI import TinUI, BasicTinUI, TinUITheme, TinUIXml

try:  #作为tinui包的子模块被导入
    from .tinuilight import TinUILight
    from .tinuidark import TinUIDark
except ImportError:  #在theme目录中直接运行
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from tinuilight import TinUILight
    from tinuidark import TinUIDark

try:  #演示窗口
    from .window import win
except ImportError:
    from window import win


def get_dark():  #获取系统亮暗模式设置
    registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    reg_keypath = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'
    try:
        reg_key = winreg.OpenKey(registry, reg_keypath)
    except FileNotFoundError:
        return False

    for i in range(1024):
        try:
            value_name, value, _ = winreg.EnumValue(reg_key, i)
            if value_name == 'AppsUseLightTheme':
                return value == 0
        except OSError:
            break
    return False


class TinUIAuto(TinUITheme):
    '''
    这是TinUI自动主题的托管类，不是继承类
    跟随系统的亮暗模式设置，自动使用TinUILight或TinUIDark主题
    '''

    def __init__(self, ui: Union[TinUI, BasicTinUI], accent=None):
        super().__init__(ui, 'tinui-auto-theme')
        self.accent = accent  #强调色，为None时使用各模式自身的默认强调色
        self.dark = get_dark()
        self._theme = self.__build_theme()

    def __build_theme(self):
        '''按照当前的亮暗模式建立对应的亮色或暗色主题'''
        if self.dark:
            return TinUIDark(self.ui, self.accent) if self.accent else TinUIDark(self.ui)
        return TinUILight(self.ui, self.accent) if self.accent else TinUILight(self.ui)

    @property
    def label(self):
        '''当前生效的主题标签，light或dark'''
        return self._theme.label

    @label.setter
    def label(self, value):
        self._theme.label = value

    @property
    def current_theme(self):
        '''当前生效的亮色或暗色主题对象'''
        return self._theme

    def refresh_theme(self, accent=None):
        '''重新读取系统的亮暗模式设置并切换主题，返回切换后的主题标签'''
        self.dark = get_dark()
        if accent is not None:
            self.accent = accent
        self._theme = self.__build_theme()
        return self._theme.label

    def __getattr__(self, name):
        '''TinUIAuto未定义的接口（如各控件的add_xxx）转交给当前生效的主题'''
        theme = self.__dict__.get('_theme')
        if theme is None:
            raise AttributeError(name)
        return getattr(theme, name)


def build_demo(du, u):
    '''在界面上构建自动主题的演示内容'''

    def end():
        '''获取下一个控件的摆放位置'''
        bbox = u.bbox('all')
        if bbox == None:
            return (5, 5)
        return (5, bbox[3] + 10)

    #标题与说明
    du.add_title(end(), 'TinUI Auto Light/Dark Theme', font='微软雅黑 25')
    du.add_label(end(), '2022 By rgzz666', font='微软雅黑 13')
    du.add_label(end(), 'It will get you system light/dark settings.', font='微软雅黑 13')
    du.add_label(end(), 'Then the theme will be light/dark Automaticlly.', font='微软雅黑 13')
    du.add_label(end(), 'It only works on Windows10+', font='微软雅黑 13')
    du.add_link(end(), 'My Site', 'http://rgzz.great-site.net')

    #当前生效的系统模式
    mode = du.add_label(end(), f'Current system mode: {du.label}')[-1]

    def refresh(e):
        '''重新读取系统的亮暗模式设置，之后创建的控件将使用新的配色'''
        u.itemconfig(mode, text=f'Current system mode: {du.refresh_theme()}')

    du.add_button(end(), 'Refresh system light/dark mode', command=refresh)

    #按钮
    du.add_button(end(), 'Button')
    du.add_button2(end(), 'Button2')
    du.add_accentbutton(end(), 'Accent Button')
    du.add_warningbutton(end(), 'Warning Button')
    du.add_toolbutton(end(), 'Tool Button')
    du.add_togglebutton(end(), 'Toggle Button')

    #勾选与选择
    du.add_checkbutton(end(), 'test checkbutton')
    du.add_radiobutton(end(), 250, 'test radiobutton', ('1', '2', '3', '4', '5'))
    du.add_radiobox(end(), content=('1', '', '2'))
    du.add_onoff(end())
    du.add_segmentbutton(end(), content=('A', 'B', 'C'))

    #输入
    du.add_entry(end(), 200, 'test entry')
    du.add_passwordbox(end(), 200)
    du.add_combobox(end(), text='test combobox', content=('1', '2', '3', '4', '5'))
    du.add_picker(end())
    du.add_spinbox(end(), data=('1', '2', '3', '4', '5'))

    #文本
    du.add_label(end(), 'test label')
    du.add_paragraph(end(), 'test paragraph')
    du.add_separate(end(), 200)
    textx, texty = end()
    text = du.add_textbox((textx, texty))[0]
    du.add_scrollbar((textx + 205, texty), text)

    #进度与状态
    du.add_waitbar1(end())
    goto = du.add_progressbar(end())[4]  #设置进度
    goto(60)
    du.add_waitbar3(end())
    du.add_ratingbar(end())
    du.add_scalebar(end())
    du.add_waitframe(end(), width=200, height=100)[3].start()  #开始等待动画

    #列表
    du.add_table(end(), data=[['t1', 't2', 't3'], ['tinui', 'table', 'test'], ['1', '2', '3']])
    du.add_listbox(end(), data=('first', 'second', 'third'))
    du.add_treeview(end())
    du.add_pipspager(end(), num=5)

    #视图
    du.add_notecard(end())
    du.add_expander(end())
    du.add_labels(end())
    du.add_navigation(end())
    du.add_breadcrumb(end())
    du.add_barbutton(end())
    du.add_menubutton(end(), 'Menu Button')

    #菜单栏、提示与浮出
    l1 = du.add_label(end(), 'menubar test label')[-1]
    du.add_menubar(l1, cont=(('test1', print), ('test2', print), '-', ('test3', print)))
    l2 = du.add_label(end(), 'tooltip test label')[-1]
    du.add_tooltip(l2, 'test tooltip')
    l3 = du.add_label(end(), 'flyout test label')[-1]
    du.add_flyout(l3)

    #标签栏，页面内容同样使用自动主题
    ntb = du.add_notebook(end())[-2]
    for i in range(1, 4):
        ntb.addpage(f'test{i}', f'flag{i}')
    for page in ntb.getvdict().values():
        TinUIXml(TinUIAuto(page[0])).loadxml('''<tinui>
<line><label text='TinUIXml与主题联动'></label></line>
</tinui>''')

    #列表视图
    items = du.add_listview(end(), height=200)[2]
    if len(items) > 0:
        items[0][2].loadxml('''<tinui>
<line><title text='listview与主题联动'></title></line>
</tinui>''')

    #分组框
    labelframey = end()[1] + 30
    lb1 = du.add_button((5, labelframey), 'labelframe button1')[-1]
    lb2 = du.add_button(end(), 'labelframe button2')[-1]
    lb3 = du.add_button(end(), 'labelframe button3')[-1]
    du.add_labelframe((lb1, lb2, lb3), title='labelframe')

    du.add_back(end())


if __name__ == '__main__':
    r = win()
    u = r.u
    du = TinUIAuto(u)
    build_demo(du, u)
    r.r.title('TinUI Auto Light/Dark Theme')
    r.go()
