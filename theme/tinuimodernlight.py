# 由chatglm-4生成，作者小改。作为范例，不会维护
from typing import Union
import sys
try:
    from tinui import TinUI, BasicTinUI, TinUITheme
except:
    sys.path.append('../')
    from TinUI import TinUI, BasicTinUI, TinUITheme


class TinUIModernLight(TinUITheme):
    def __init__(self, ui: Union[TinUI, BasicTinUI]):
        super().__init__(ui, 'tinui-modern-light-theme')
        self.label = 'modern-light'
        self.ui['background'] = '#ffffff'
        
    def add_button(self, pos, *arg, **kw):
        return self.ui.add_button(pos, fg='#ffffff', bg='#007bff', 
                                  activefg='#ffffff', activebg='#0056b3', 
                                  line='#007bff', linew=1, activeline='#0056b3', 
                                  *arg, **kw)
                                  
    def add_checkbutton(self, pos, *arg, **kw):
        return self.ui.add_checkbutton(pos, 
            fontfg='#555555', fg='#555555', bg='#ffffff', 
            activefg='#555555', activebg='#f0f0f0', 
            onfg='#ffffff', onbg='#007bff', 
            *arg, **kw)

    def add_label(self, pos, *arg, **kw):
        return self.ui.add_label(pos, fg='#333333', bg='#ffffff', 
                                 outline='#ffffff', *arg, **kw)

    def add_entry(self, pos, *arg, **kw):
        return self.ui.add_entry(pos, fg='#333333', bg='#ffffff', 
                                 activefg='#000000', activebg='#ffffff', 
                                 line='#cccccc', activeline='#007bff', 
                                 outline='#cccccc', onoutline='#007bff', 
                                 insert='#000000', *arg, **kw)

    def add_separate(self, pos, *arg, **kw):
        return self.ui.add_separate(pos, fg='#e6e6e6', *arg, **kw)

    def add_radiobutton(self, pos, *arg, **kw):
        return self.ui.add_radiobutton(pos, 
                                       fg='#333333', bg='#ffffff', 
                                       activefg='#000000', activebg='#f0f0f0', 
                                       *arg, **kw)

    def add_link(self, pos, *arg, **kw):
        return self.ui.add_link(pos, fg='#007bff', 
                                activefg='red', activebg='#eaeaea', 
                                *arg, **kw)

    def add_waitbar1(self, pos, *arg, **kw):
        return self.ui.add_waitbar1(pos, fg='#007bff', 
                                    bg='#ffffff', okfg='#007bff', bd=5, 
                                    *arg, **kw)

    def add_labelframe(self, uids: tuple, *arg, **kw):
        return self.ui.add_labelframe(uids, fg='#333333', bg='#ffffff', 
                                      *arg, **kw)

    def add_waitbar2(self, pos, *arg, **kw):
        return self.ui.add_waitbar2(pos, 
                                    fg='#007bff', bg='#ffffff', okcolor='#0f7b0f', 
                                    *arg, **kw)

    def add_combobox(self, pos, *arg, **kw):
        return self.ui.add_combobox(pos, 
                                    fg='#333333', bg='#ffffff', 
                                    activefg='#333333', activebg='#ededee', 
                                    *arg, **kw)

    def add_progressbar(self, pos, *arg, **kw):
        return self.ui.add_progressbar(pos, 
                                       fg='#555555', bg='#007bff', back='#ffffff', 
                                       fontc='#79b8f8', *arg, **kw)

    def add_table(self, pos, *arg, **kw):
        return self.ui.add_table(pos, 
                                 outline='#dadad8', fg='black', bg='white', 
                                 headbg='#f4f4f2', *arg, **kw)

    def add_onoff(self, pos, *arg, **kw):
        return self.ui.add_onoff(pos, 
                                 fg='#5a5a5a', bg='#ededed', 
                                 onfg='#ffffff', onbg='#007bff', 
                                 *arg, **kw)

    def add_spinbox(self, pos, *arg, **kw):
        return self.ui.add_spinbox(pos, 
                                   fg='#333333', bg='#fefefe', line='#e5e5e5', 
                                   activefg='#333333', activebg='#fafafa', 
                                   onfg='#555555', onbg='#f3f3f3', 
                                   boxfg='#5f5f5f', boxbg='#f9f9f9', 
                                   boxactivefg='#5b5b5b', boxactivebg='#f0f0f0', 
                                   *arg, **kw)

    def add_scalebar(self, pos, *arg, **kw):
        return self.ui.add_scalebar(pos, 
                                    fg='#3b50ba', bg='#555555', activefg='#3b50ba', 
                                    buttonbg='#ffffff', buttonoutline='#cccccc', 
                                    *arg, **kw)

    def add_info(self, pos, *arg, **kw):
        return self.ui.add_info(pos, 
                                fg='#007bff', bg='#f9f9f9', info_fg='#333333', 
                                *arg, **kw)

    def add_menubar(self, uid, *arg, **kw):
        return self.ui.add_menubar(uid, 
                                   fg='#333333', bg='#ffffff', line='#e6e6e6', 
                                   activefg='#000000', activebg='#f0f0f0', activeline='#f0f0f0', 
                                   *arg, **kw)

    def add_tooltip(self, uid, *arg, **kw):
        return self.ui.add_tooltip(uid, fg='#333333', bg='#efefef', 
                                   *arg, **kw)

    def add_waitbar3(self, pos, *arg, **kw):
        return self.ui.add_waitbar3(pos, 
                                    fg='#007bff', bg='#ffffff', okcolor='#007bff', 
                                    *arg, **kw)

    def add_textbox(self, pos, *arg, **kw):
        return self.ui.add_textbox(pos, fg='#333333', bg='white', 
                                   outline='#cccccc', onoutline='#007bff', 
                                   scrollbg='#f9f9f9', scrollcolor='#cccccc', scrollon='#cccccc', 
                                   *arg, **kw)

    def add_scrollbar(self, pos, widget, *arg, **kw):
        return self.ui.add_scrollbar(pos, widget, 
                                     bg='#f9f9f9', color='#cccccc', 
                                     oncolor='#aaaaaa', *arg, **kw)

    def add_listbox(self, pos, *arg, **kw):
        return self.ui.add_listbox(pos, 
                                   bg='#ffffff', fg='black', activebg='#f0f0f0', sel='#007bff', 
                                   scrollbg='#f9f9f9', scrollcolor='#cccccc', scrollon='#cccccc', 
                                   *arg, **kw)

    def add_canvas(self, pos, *arg, **kw):
        return self.ui.add_canvas(pos, 
                                  outline='#cccccc', linew=1, 
                                  scrollbg='#f9f9f9', scrollcolor='#cccccc', scrollon='#cccccc', 
                                  *arg, **kw)

    def add_pipspager(self, pos, *arg, **kw):
        return self.ui.add_pipspager(pos, 
                                     bg='#ffffff', fg='#555555', 
                                     buttonfg='#555555', buttonbg='#f9f9f9', 
                                     activefg='#333333', activebg='#f9f9f9', 
                                     buttononfg='#333333', buttononbg='#f9f9f9', 
                                     *arg, **kw)

    def add_notebook(self, pos, *arg, **kw):
        return self.ui.add_notebook(pos, 
                                    color='#ffffff', fg='#555555', bg='#ffffff', 
                                    activefg='#333333', activebg='#f0f0f0', 
                                    onfg='#333333', onbg='#f9f9f9', 
                                    scrollbg='#f9f9f9', scrollcolor='#cccccc', scrollon='#cccccc', 
                                    *arg, **kw)

    def add_radiobox(self, pos, *arg, **kw):
        return self.ui.add_radiobox(pos, 
                                    fontfg='black', fg='#555555', bg='#ffffff', 
                                    activefg='#333333', activebg='#f0f0f0', 
                                    onfg='#007bff', onbg='#ffffff', 
                                    *arg, **kw)

    def add_ratingbar(self, pos, *arg, **kw):
        return self.ui.add_ratingbar(pos, 
                                     fg='#555555', bg='#ffffff', 
                                     onfg='#007bff', onbg='#007bff', 
                                     *arg, **kw)

    def add_notecard(self, pos, *arg, **kw):
        return self.ui.add_notecard(pos, 
                                    tfg='#333333', tbg='#fbfbfb', fg='#333333', 
                                    bg='#f4f4f4', sep='#e5e5e5', 
                                    *arg, **kw)

    def add_pivot(self, pos, *arg, **kw):
        return self.ui.add_pivot(pos, 
                                 fg='#555555', bg='', 
                                 activefg='#000000', activecolor='#007bff', 
                                 *arg, **kw)

    def add_button2(self, pos, *arg, **kw):
        return self.ui.add_button2(pos, fg='#333333', bg='#ffffff', 
                                   activefg='#000000', activebg='#f0f0f0', 
                                   line='#cccccc', linew=1, activeline='#cccccc', 
                                   onfg='#555555', onbg='#f5f5f5', online='#e5e5e5', 
                                   *arg, **kw)

    def add_expander(self, pos, *arg, **kw):
        return self.ui.add_expander(pos, 
                                    tfg='#333333', tbg='#ffffff', 
                                    bg='#f4f4f4', sep='#e5e5e5', 
                                    buttonfg='#333333', buttonbg='#ffffff', buttonline='#ffffff', 
                                    activefg='#000000', activebg='#f0f0f0', activeline='#f0f0f0', 
                                    onfg='#555555', onbg='#f5f5f5', online='#e5e5e5', 
                                    *arg, **kw)

    def add_waitframe(self, pos, *arg, **kw):
        return self.ui.add_waitframe(pos, 
                                     fg='#ffffff', bg='#f6f6f6', 
                                     *arg, **kw)

    def add_listview(self, pos, *arg, **kw):
        return self.ui.add_listview(pos, 
                                    bg='#ffffff', activebg='#f0f0f0', oncolor='#007bff', 
                                    scrobg='#f8f8f8', scroc='#cccccc', scrooc='#aaaaaa', 
                                    *arg, **kw)

    def add_treeview(self, pos, *arg, **kw):
        return self.ui.add_treeview(pos, 
                                    fg='#333333', bg='#ffffff', 
                                    onfg='#333333', onbg='#f0f0f0', 
                                    oncolor='#007bff', signcolor='#aaaaaa', 
                                    *arg, **kw)

    def add_togglebutton(self, pos, *arg, **kw):
        return self.ui.add_togglebutton(pos, 
                                        fg='#333333', bg='#ffffff', line='#cccccc', 
                                        activefg='#f3f4fd', activebg='#007bff', activeline='#5360de', 
                                        *arg, **kw)

    def add_swipecontrol(self, pos, *arg, **kw):
        return self.ui.add_swipecontrol(pos, 
                                        fg='#333333', bg='#ffffff', line='#ffffff', 
                                        data={'left':({'text':'✔️\nok','fg':'#202020','bg':'#bcbcbc','command':print},), 
                                              'right':({'text':'❌\nclose'},)}, 
                                        *arg, **kw)

    def add_picker(self, pos, *arg, **kw):
        return self.ui.add_picker(pos, 
                                  fg='#333333', bg='#ffffff', 
                                  outline='#ececec', activefg='#333333', 
                                  activebg='#f0f0f0', onfg='#eaecfb', onbg='#007bff', 
                                  buttonfg='#333333', buttonbg='#ffffff', 
                                  buttonactivefg='#333333', buttonactivebg='#f0f0f0', 
                                  *arg, **kw)

    def add_menubutton(self, pos, *arg, **kw):
        return self.ui.add_menubutton(pos, 
                                      fg='#333333', bg='#ffffff', line='#cccccc', 
                                      activefg='#000000', activebg='#f0f0f0', activeline='#cccccc', 
                                      onfg='#555555', onbg='#f5f5f5', online='#e5e5e5', 
                                      menuonfg='#000000', menuonbg='#f0f0f0', menuonline='#f0f0f0', 
                                      *arg, **kw)

    def add_barbutton(self, pos, *arg, **kw):
        return self.ui.add_barbutton(pos, 
                                     fg='#666666', bg='#ffffff', line='#ffffff', 
                                     activefg='#000000', activebg='#f0f0f0', activeline='#f0f0f0', 
                                     onfg='#555555', onbg='#ededed', online='#ededed', sepcolor='#e5e5e5', 
                                     *arg, **kw)

    def add_flyout(self, fid, *arg, **kw):
        return self.ui.add_flyout(fid,
                                  line='#e6e6e6', bg='#ffffff',
                                  *arg, **kw)
