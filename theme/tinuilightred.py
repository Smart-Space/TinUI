# generate by 豆包
from typing import Union
import sys
sys.path.append('../')
from TinUI import TinUI, BasicTinUI, TinUITheme, TinUIXml


class TinUILightRed(TinUITheme):
    def __init__(self, ui: Union[TinUI, BasicTinUI]):
        super().__init__(ui, 'tinui-light-red-theme')
        self.label = 'light-red'
        self.ui['background'] = '#fef0f0'

    def add_button(self, pos, *arg, **kw):
        return self.ui.add_button(pos, fg='#7f0000', bg='#ffe4e1',
                                  activefg='#b22222', activebg='#ffc0cb',
                                  line='#ff9999', linew=1, activeline='#ff9999',
                                  *arg, **kw)

    def add_checkbutton(self, pos, *arg, **kw):
        return self.ui.add_checkbutton(pos,
                                       fontfg='#b22222', fg='#ff6347', bg='#ffe4e1',
                                       activefg='#ff6347', activebg='#ffd1dc',
                                       onfg='white', onbg='#ff0000',
                                       *arg, **kw)

    def add_label(self, pos, *arg, **kw):
        return self.ui.add_label(pos, fg='#b22222', bg='#fef0f0',
                                 outline='#fef0f0', *arg, **kw)

    def add_entry(self, pos, *arg, **kw):
        return self.ui.add_entry(pos, fg='#ff4500', bg='#ffe4e1',
                                 activefg='#b22222', activebg='#ffffff',
                                 line='#ff9999', activeline='#ff9999',
                                 outline='#ff6347', onoutline='#ff0000', insert='#000000',
                                 *arg, **kw)

    def add_separate(self, pos, *arg, **kw):
        return self.ui.add_separate(pos, fg='#ff9999',
                                    *arg, **kw)

    def add_radiobutton(self, pos, *arg, **kw):
        return self.ui.add_radiobutton(pos,
                                       fg='#b22222', bg='#ffe4e1',
                                       activefg='#990000', activebg='#ffc0cb',
                                       *arg, **kw)

    def add_link(self, pos, *arg, **kw):
        return self.ui.add_link(pos, fg='#ff0000',
                                activefg='red', activebg='#ffe4e1',
                                *arg, **kw)

    def add_waitbar1(self, pos, *arg, **kw):
        return self.ui.add_waitbar1(pos, fg='#ff0000',
                                    bg='#fef0f0', okfg='#ff0000', bd=5,
                                    *arg, **kw)

    def add_labelframe(self, uids: tuple, *arg, **kw):
        return self.ui.add_labelframe(uids, fg='#b22222', bg='#fbe9e7',
                                      *arg, **kw)

    def add_waitbar2(self, pos, *arg, **kw):
        return self.ui.add_waitbar2(pos,
                                    fg='#ff0000', bg='#fef0f0', okcolor='#ff0000',
                                    *arg, **kw)

    def add_combobox(self, pos, *arg, **kw):
        return self.ui.add_combobox(pos,
                                    fg='#b22222', bg='#ffe4e1', outline='#ff9999',
                                    activefg='#b22222', activebg='#ffe4e1',
                                    scrollbg='#f5f5f5', scrollcolor='#9e9e9e', scrollon='#757575',
                                    *arg, **kw)

    def add_progressbar(self, pos, *arg, **kw):
        return self.ui.add_progressbar(pos,
                                       fg='#ff6347', bg='#ff0000', back='#fef0f0',
                                       fontc='#ffb6c1', *arg, **kw)

    def add_table(self, pos, *arg, **kw):
        return self.ui.add_table(pos,
                                 outline='#ff9999', fg='black', bg='white',
                                 headbg='#ffe4e1', *arg, **kw)

    def add_onoff(self, pos, *arg, **kw):
        return self.ui.add_onoff(pos,
                                 fg='#ff4500', bg='#ffe4e1',
                                 onfg='#ffffff', onbg='#ff0000',
                                 *arg, **kw)

    def add_spinbox(self, pos, *arg, **kw):
        return self.ui.add_spinbox(pos,
                                   fg='#b22222', bg='#ffe4e1', line='#ff9999',
                                   activefg='#990000', activebg='#ffd1dc',
                                   onfg='#ff6347', onbg='#ffe4e1',
                                   boxfg='#ff4500', boxbg='#ffe4e1',
                                   boxactivefg='#7f0000', boxactivebg='#ffe4e1',
                                   *arg, **kw)

    def add_scalebar(self, pos, *arg, **kw):
        return self.ui.add_scalebar(pos,
                                    fg='#ff0000', bg='#ff6347', activefg='#ff0000',
                                    buttonbg='#ffffff', buttonoutline='#ff9999',
                                    *arg, **kw)

    def add_info(self, pos, *arg, **kw):
        return self.ui.add_info(pos,
                                fg='#ff0000', bg='#ffe4e1', info_fg='#b22222',
                                *arg, **kw)

    def add_menubar(self, uid, *arg, **kw):
        return self.ui.add_menubar(uid,
                                   fg='#b22222', bg='#ffe4e1', line='#ff9999',
                                   activefg='#990000', activebg='#ffe4e1', activeline='#ffe4e1', *arg, **kw)

    def add_tooltip(self, uid, *arg, **kw):
        return self.ui.add_tooltip(uid, fg='#b22222', bg='#ffe4e1',
                                   *arg, **kw)

    def add_waitbar3(self, pos, *arg, **kw):
        return self.ui.add_waitbar3(pos,
                                    fg='#ff0000', bg='#fef0f0', okcolor='#ff0000',
                                    *arg, **kw)

    def add_textbox(self, pos, *arg, **kw):
        return self.ui.add_textbox(pos, fg='#b22222', bg='white',
                                   outline='#ff6347', onoutline='#ff0000',
                                   scrollbg='#ffe4e1', scrollcolor='#8d8d8d', scrollon='#8a8a8a',
                                   *arg, **kw)

    def add_scrollbar(self, pos, widget, *arg, **kw):
        return self.ui.add_scrollbar(pos, widget,
                                     bg='#ffe4e1', color='#8d8d8d',
                                     oncolor='#8a8a8a', *arg, **kw)

    def add_listbox(self, pos, *arg, **kw):
        return self.ui.add_listbox(pos,
                                   bg='#ffe4e1', fg='black', activebg='#ffc0cb', sel='#ff9999',
                                   scrollbg='#ffe4e1', scrollcolor='#8d8d8d', scrollon='#8a8a8a',
                                   *arg, **kw)

    def add_canvas(self, pos, *arg, **kw):
        return self.ui.add_canvas(pos,
                                  outline='#808080', linew=1,
                                  scrollbg='#ffe4e1', scrollcolor='#8d8d8d', scrollon='#8a8a8a',
                                  *arg, **kw)

    def add_pipspager(self, pos, *arg, **kw):
        return self.ui.add_pipspager(pos,
                                     bg='#fef0f0', fg='#ff6347',
                                     buttonfg='#ff4500', buttonbg='#ffe4e1',
                                     activefg='#7f0000', activebg='#ffe4e1',
                                     buttononfg='#7f0000', buttononbg='#ffe4e1',
                                     *arg, **kw)

    def add_notebook(self, pos, *arg, **kw):
        return self.ui.add_notebook(pos,
                                    color='#fef0f0', fg='#ff4500', bg='#fef0f0',
                                    activefg='#7f0000', activebg='#ffe4e1',
                                    onfg='#b22222', onbg='#ffe4e1',
                                    scrollbg='#ffe4e1', scrollcolor='#8d8d8d', scrollon='#8a8a8a',
                                    *arg, **kw)

    def add_radiobox(self, pos, *arg, **kw):
        return self.ui.add_radiobox(pos,
                                    fontfg='black', fg='#ff6347', bg='#ffe4e1',
                                    activefg='#ff0000', activebg='#ffd1dc',
                                    onfg='#ff0000', onbg='#ffffff',
                                    *arg, **kw)

    def add_ratingbar(self, pos, *arg, **kw):
        return self.ui.add_ratingbar(pos,
                                     fg='#ff4500', bg='#fef0f0',
                                     onfg='#ff0000', onbg='#ff0000',
                                     *arg, **kw)

    def add_notecard(self, pos, *arg, **kw):
        return self.ui.add_notecard(pos,
                                    tfg='#b22222', tbg='#ffe4e1', fg='#b22222',
                                    bg='#fbe9e7', sep='#ff9999',
                                    *arg, **kw)

    def add_pivot(self, pos, *arg, **kw):
        return self.ui.add_pivot(pos,
                                 fg='#ff4500', bg='',
                                 activefg='#000000', activecolor='#ff0000',
                                 *arg, **kw)

    def add_button2(self, pos, *arg, **kw):
        return self.ui.add_button2(pos, fg='#b22222', bg='#ffe4e1',
                                   activefg='#990000', activebg='#ffc0cb',
                                   line='#ff9999', linew=1, activeline='#ff9999',
                                   onfg='#ff4500', onbg='#ffe4e1', online='#ff9999',
                                   *arg, **kw)

    def add_expander(self, pos, *arg, **kw):
        return self.ui.add_expander(pos,
                                    tfg='#b22222', tbg='#ffe4e1',
                                    bg='#fbe9e7', sep='#ff9999',
                                    buttonfg='#b22222', buttonbg='#ffe4e1', buttonline='#ffe4e1',
                                    activefg='#990000', activebg='#ffd1dc', activeline='#ffd1dc',
                                    onfg='#b22222', onbg='#ffe4e1', online='#ffe4e1',
                                    *arg, **kw)

    def add_waitframe(self, pos, *arg, **kw):
        return self.ui.add_waitframe(pos,
                                     fg='#ffe4e1', bg='#ffd1dc',
                                     *arg, **kw)

    def add_listview(self, pos, *arg, **kw):
        return self.ui.add_listview(pos,
                                    bg='#fef0f0', activebg='#ffe4e1', oncolor='#ff0000',
                                    scrobg='#ffe4e1', scroc='#868686', scrooc='#898989',
                                    *arg, **kw)

    def add_treeview(self, pos, *arg, **kw):
        return self.ui.add_treeview(pos,
                                    fg='#b22222', bg='#fef0f0',
                                    onfg='#b22222', onbg='#ffe4e1',
                                    oncolor='#ff0000', signcolor='#8a8a8a',
                                    *arg, **kw)

    def add_togglebutton(self, pos, *arg, **kw):
        return self.ui.add_togglebutton(pos,
                                        fg='#b22222', bg='#ffe4e1', line='#ff9999',
                                        activefg='#ffe4e1', activebg='#ff0000', activeline='#ff0000',
                                        *arg, **kw)

    def add_swipecontrol(self, pos, *arg, **kw):
        return self.ui.add_swipecontrol(pos,
                                        fg='#b22222', bg='#fef0f0', line='#ffe4e1',
                                        data={'left': ({'text': '✔️\nok', 'fg': '#202020', 'bg': '#ffc0cb', 'command': print},),
                                              'right': ({'text': '❌\nclose'},)},
                                        *arg, **kw)

    def add_picker(self, pos, *arg, **kw):
        return self.ui.add_picker(pos,
                                  fg='#b22222', bg='#ffe4e1',
                                  outline='#ffe4e1', activefg='#b22222',
                                  activebg='#ffe4e1', onfg='#ffe4e1', onbg='#ff0000',
                                  buttonfg='#b22222', buttonbg='#ffe4e1',
                                  buttonactivefg='#b22222', buttonactivebg='#ffe4e1',
                                  *arg, **kw)

    def add_menubutton(self, pos, *arg, **kw):
        return self.ui.add_menubutton(pos,
                                      fg='#b22222', bg='#ffe4e1', line='#ff9999',
                                      activefg='#990000', activebg='#ffc0cb', activeline='#ff9999',
                                      onfg='#ff4500', onbg='#ffe4e1', online='#ff9999',
                                      menuonfg='#990000', menuonbg='#ffe4e1', menuonline='#ffe4e1',
                                      *arg, **kw)

    def add_barbutton(self, pos, *arg, **kw):
        return self.ui.add_barbutton(pos,
                                     fg='#ff4500', bg='#fef0f0', line='#fef0f0',
                                     activefg='#990000', activebg='#ffe4e1', activeline='#ffe4e1',
                                     onfg='#ff4500', onbg='#ffe4e1', online='#ffe4e1', sepcolor='#ff9999',
                                     *arg, **kw)

    def add_flyout(self, fid, *arg, **kw):
        return self.ui.add_flyout(fid,
                                  line='#ff9999', bg='#ffe4e1',
                                  *arg, **kw)
