# 由chatglm-4生成，作者小改。作为范例，不会维护
from typing import Union
import sys
try:
    from tinui import TinUI, BasicTinUI, TinUITheme
except:
    sys.path.append('../')
    from TinUI import TinUI, BasicTinUI, TinUITheme



class TinUIModernDark(TinUITheme):
    '''
    这是TinUI现代黑暗模式的托管类，不是继承类
    调用时需要注意文本和数据，样式类参数无需理会
    '''

    def __init__(self, ui: Union[TinUI, BasicTinUI]):
        super().__init__(ui, 'tinui-modern-dark-theme')
        self.label = 'modern-dark'
        self.ui['background'] = '#1e1e1e'

    def add_button(self, pos, *arg, **kw):
        return self.ui.add_button(pos, fg='#d9d9d9', bg='#2a2a2a', activefg='#ffffff', activebg='#3c3c3c', line='#424242', linew=1, activeline='#525252', *arg, **kw)

    def add_checkbutton(self, pos, *arg, **kw):
        return self.ui.add_checkbutton(pos, fontfg='#d9d9d9', fg='#8c8c8c', bg='#212121', activefg='#9c9c9c', activebg='#2a2a2a', onfg='#010101', onbg='#3b78e7', *arg, **kw)

    def add_label(self, pos, *arg, **kw):
        return self.ui.add_label(pos, fg='#d9d9d9', bg='#1e1e1e', outline='#1e1e1e', *arg, **kw)

    def add_entry(self, pos, *arg, **kw):
        return self.ui.add_entry(pos, fg='#cfcfcf', bg='#2a2a2a', activefg='#e6e6e6', activebg='#212121', line='#424242', activeline='#525252', outline='#8c8c8c', onoutline='#3b78e7', insert='#e0e0e0', *arg, **kw)

    def add_separate(self, pos, *arg, **kw):
        return self.ui.add_separate(pos, fg='#3c3c3c', *arg, **kw)

    def add_radiobutton(self, pos, *arg, **kw):
        return self.ui.add_radiobutton(pos, fg='#f2f2f2', bg='#2a2a2a', activefg='#ffffff', activebg='#3c3c3c', *arg, **kw)

    def add_link(self, pos, *arg, **kw):
        return self.ui.add_link(pos, fg='#3b78e7', activefg='#3b78e7', activebg='#2a2a2a', *arg, **kw)

    def add_waitbar1(self, pos, *arg, **kw):
        return self.ui.add_waitbar1(pos, fg='#3b78e7', bg='#1e1e1e', okfg='#3b78e7', bd=5, *arg, **kw)

    def add_labelframe(self, uids: tuple, *arg, **kw):
        return self.ui.add_labelframe(uids, fg='#d9d9d9', bg='#212121', *arg, **kw)

    def add_waitbar2(self, pos, *arg, **kw):
        return self.ui.add_waitbar2(pos, fg='#3b78e7', bg='#1e1e1e', okcolor='#6ccb5f', *arg, **kw)

    def add_combobox(self, pos, *arg, **kw):
        return self.ui.add_combobox(pos, fg='#cfcfcf', bg='#2a2a2a', outline='#424242', activefg='#ffffff', activebg='#3c3c3c', scrollbg='#212121', scrollcolor='#8c8c8c', scrollon='#9c9c9c', *arg, **kw)

    def add_progressbar(self, pos, *arg, **kw):
        return self.ui.add_progressbar(pos, fg='#8c8c8c', bg='#3b78e7', back='#1e1e1e', fontc='#0000ff', *arg, **kw)

    def add_table(self, pos, *arg, **kw):
        return self.ui.add_table(pos, outline='#8c8c8c', fg='#d9d9d9', bg='#2a2a2a', headbg='#1e1e1e', *arg, **kw)

    def add_onoff(self, pos, *arg, **kw):
        return self.ui.add_onoff(pos, fg='#cfcfcf', bg='#212121', onfg='#000000', onbg='#3b78e7', *arg, **kw)

    def add_spinbox(self, pos, *arg, **kw):
        return self.ui.add_spinbox(pos, fg='#d9d9d9', bg='#2a2a2a', line='#424242', activefg='#c0c0c0', activebg='#3c3c3c', boxfg='#cfcfcf', boxbg='#212121', boxactivefg='#d2d2d2', boxactivebg='#323232', onfg='#8c8c8c', onbg='#2a2a2a', *arg, **kw)

    def add_scalebar(self, pos, *arg, **kw):
        return self.ui.add_scalebar(pos, fg='#3b78e7', bg='#8c8c8c', activefg='#3b78e7', buttonbg='#3c3c3c', buttonoutline='#424242', *arg, **kw)

    def add_info(self, pos, *arg, **kw):
        return self.ui.add_info(pos, fg='#3b78e7', bg='#2a2a2a', info_fg='#d9d9d9', *arg, **kw)

    def add_menubar(self, uid, *arg, **kw):
        return self.ui.add_menubar(uid, fg='#d9d9d9', bg='#212121', line='#8c8c8c', activefg='#ffffff', activebg='#3c3c3c', activeline='#3c3c3c', *arg, **kw)

    def add_tooltip(self, uid, *arg, **kw):
        return self.ui.add_tooltip(uid, fg='#e8e8e8', bg='#3c3c3c', *arg, **kw)

    def add_waitbar3(self, pos, *arg, **kw):
        return self.ui.add_waitbar3(pos, fg='#3b78e7', bg='#1e1e1e', okcolor='#3b78e7', *arg, **kw)

    def add_textbox(self, pos, *arg, **kw):
        return self.ui.add_textbox(pos, fg='#d9d9d9', bg='#2a2a2a', outline='#8c8c8c', onoutline='#3b78e7', scrollbg='#212121', scrollcolor='#8c8c8c', scrollon='#9c9c9c', *arg, **kw)

    def add_scrollbar(self, pos, widget, *arg, **kw):
        return self.ui.add_scrollbar(pos, widget, bg='#212121', color='#8c8c8c', oncolor='#9c9c9c', *arg, **kw)

    def add_listbox(self, pos, *arg, **kw):
        return self.ui.add_listbox(pos, bg='#2a2a2a', fg='white', activebg='#3b78e7', sel='#465097', scrollbg='#212121', scrollcolor='#8c8c8c', scrollon='#9c9c9c', *arg, **kw)

    def add_canvas(self, pos, *arg, **kw):
        return self.ui.add_canvas(pos, outline='#8c8c8c', linew=1, scrollbg='#212121', scrollcolor='#8c8c8c', scrollon='#9c9c9c', *arg, **kw)

    def add_pipspager(self, pos, *arg, **kw):
        return self.ui.add_pipspager(pos, bg='#1e1e1e', fg='#8c8c8c', buttonfg='#9c9c9c', buttonbg='#212121', activefg='#d9d9d9', activebg='#212121', buttononfg='#d9d9d9', buttononbg='#212121', *arg, **kw)

    def add_notebook(self, pos, *arg, **kw):
        return self.ui.add_notebook(pos, color='#1e1e1e', fg='#d9d9d9', bg='#1e1e1e', activefg='#ffffff', activebg='#3c3c3c', onfg='#d9d9d9', onbg='#212121', scrollbg='#212121', scrollcolor='#8c8c8c', scrollon='#9c9c9c', *arg, **kw)

    def add_ratingbar(self, pos, *arg, **kw):
        return self.ui.add_ratingbar(pos, fg='#cfcfcf', bg='#1e1e1e', onfg='#3b78e7', onbg='#3b78e7', *arg, **kw)

    def add_radiobox(self, pos, *arg, **kw):
        return self.ui.add_radiobox(pos, fontfg='#d9d9d9', fg='#8c8c8c', bg='#2a2a2a', activefg='#9c9c9c', activebg='#2a2a2a', onfg='#3b78e7', onbg='#000000', *arg, **kw)

    def add_notecard(self, pos, *arg, **kw):
        return self.ui.add_notecard(pos, tfg='#d9d9d9', tbg='#2a2a2a', fg='#d9d9d9', bg='#212121', sep='#1d1d1d', *arg, **kw)

    def add_pivot(self, pos, *arg, **kw):
        return self.ui.add_pivot(pos, fg='#8c8c8c', bg='', activefg='#ffffff', activecolor='#3b78e7', *arg, **kw)

    def add_button2(self, pos, *arg, **kw):
        return self.ui.add_button2(pos, fg='#d9d9d9', bg='#2a2a2a', activefg='#ffffff', activebg='#3c3c3c', line='#424242', linew=1, activeline='#1e1e1e', onfg='#cecece', onbg='#212121', online='#424242', *arg, **kw)

    def add_expander(self, pos, *arg, **kw):
        return self.ui.add_expander(pos, tfg='#d9d9d9', tbg='#2a2a2a', bg='#212121', sep='#1d1d1d', buttonfg='#d9d9d9', buttonbg='#2a2a2a', buttonline='#2a2a2a', activefg='#ffffff', activebg='#3c3c3c', activeline='#3c3c3c', onfg='#d9d9d9', onbg='#232323', online='#3c3c3c', *arg, **kw)

    def add_waitframe(self, pos, *arg, **kw):
        return self.ui.add_waitframe(pos, fg='#2a2a2a', bg='#3c3c3c', *arg, **kw)

    def add_listview(self, pos, *arg, **kw):
        return self.ui.add_listview(pos, bg='#1e1e1e', activebg='#2a2a2a', oncolor='#3b78e7', scrobg='#212121', scroc='#8c8c8c', scrooc='#9c9c9c', *arg, **kw)

    def add_treeview(self, pos, *arg, **kw):
        return self.ui.add_treeview(pos, fg='#d9d9d9', bg='#1e1e1e', onfg='#d9d9d9', onbg='#2a2a2a', oncolor='#3b78e7', signcolor='#8c8c8c', *arg, **kw)

    def add_togglebutton(self, pos, *arg, **kw):
        return self.ui.add_togglebutton(pos, fg='#d9d9d9', bg='#2a2a2a', line='#424242', activefg='#000000', activebg='#3b78e7', activeline='#3b78e7', *arg, **kw)
    
    def add_swipecontrol(self, pos, *arg, **kw):
        return self.ui.add_swipecontrol(pos, fg='#d9d9d9', bg='#1e1e1e', line='#2a2a2a', data={'left':({'text':'✔️\nok','fg':'#000000','bg':'#a9a9a9','command':print},),'right':({'text':'❌\nclose'},)}, *arg, **kw)

    def add_picker(self, pos, *arg, **kw):
        return self.ui.add_picker(pos, fg='#cfcfcf', bg='#2a2a2a', outline='#424242', activefg='#ffffff', activebg='#3c3c3c', onfg='#000000', onbg='#3b78e7', buttonfg='#d9d9d9', buttonbg='#2a2a2a', buttonactivefg='#ffffff', buttonactivebg='#3c3c3c', *arg, **kw)
    
    def add_menubutton(self, pos, *arg, **kw):
        return self.ui.add_menubutton(pos, fg='#d9d9d9', bg='#2a2a2a', line='#424242', activefg='#ffffff', activebg='#3c3c3c', activeline='#1e1e1e', onfg='#cecece', onbg='#212121', online='#424242', menuonfg='#d9d9d9', menuonbg='#3c3c3c', menuonline='#3c3c3c', *arg, **kw)
    
    def add_barbutton(self, pos, *arg, **kw):
        return self.ui.add_barbutton(pos, fg='#d9d9d9', bg='#1e1e1e', line='#1e1e1e', activefg='#cecece', activebg='#2a2a2a', activeline='#2a2a2a', onfg='#cecece', onbg='#232323', online='#232323', sepcolor='#e5e5e5', *arg, **kw)

    def add_flyout(self, fid, *arg, **kw):
        return self.ui.add_flyout(fid, line='#b0b0b0', bg='#212121', *arg, **kw)

