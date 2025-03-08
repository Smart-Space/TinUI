# generate by 豆包
from typing import Union
import sys
try:
    from tinui import TinUI, BasicTinUI, TinUITheme
except:
    sys.path.append('../')
    from TinUI import TinUI, BasicTinUI, TinUITheme

class TinUILightCyan(TinUITheme):
    def __init__(self,ui:Union[TinUI,BasicTinUI]):
        super().__init__(ui,'tinui-light-cyan-theme')
        self.label='light-cyan'
        self.ui['background']='#f0f8ff'

    def add_button(self,pos,*arg,**kw):
        return self.ui.add_button(pos,fg='#1e3799',bg='#e0f7fa',
             activefg='#1976d2',activebg='#b3e5fc',
             line='#80deea',linew=1,activeline='#80deea',
                           *arg,**kw)

    def add_checkbutton(self,pos,*arg,**kw):
        return self.ui.add_checkbutton(pos,
            fontfg='#1976d2',fg='#00acc1',bg='#e0f7fa',
                  activefg='#00acc1',activebg='#b2ebf2',
                  onfg='white',onbg='#00bcd4',
                                *arg,**kw)

    def add_label(self,pos,*arg,**kw):
        return self.ui.add_label(pos,fg='#1976d2',bg='#f0f8ff',
                                 outline='#f0f8ff',*arg,**kw)

    def add_entry(self,pos,*arg,**kw):
        return self.ui.add_entry(pos,fg='#42a5f5',bg='#e0f7fa',
            activefg='#1976d2',activebg='#ffffff',
            line='#80deea',activeline='#80deea',
            outline='#00acc1',onoutline='#0097a7',insert='#000000',
                          *arg,**kw)

    def add_separate(self,pos,*arg,**kw):
        return self.ui.add_separate(pos,fg='#80deea',
                             *arg,**kw)

    def add_radiobutton(self,pos,*arg,**kw):
        return self.ui.add_radiobutton(pos,
                  fg='#1976d2',bg='#e0f7fa',
                  activefg='#1565c0',activebg='#b3e5fc',
                                *arg,**kw)

    def add_link(self,pos,*arg,**kw):
        return self.ui.add_link(pos,fg='#007bff',
           activefg='red',activebg='#e3f2fd',
                                *arg,**kw)

    def add_waitbar1(self,pos,*arg,**kw):
        return self.ui.add_waitbar1(pos,fg='#0097a7',
                                    bg='#f0f8ff',okfg='#0097a7',bd=5,
                                   *arg,**kw)

    def add_labelframe(self,uids:tuple,*arg,**kw):
        return self.ui.add_labelframe(uids,fg='#1976d2',bg='#e8f5e9',
                                      *arg,**kw)

    def add_waitbar2(self,pos,*arg,**kw):
        return self.ui.add_waitbar2(pos,
            fg='#0097a7',bg='#f0f8ff',okcolor='#4caf50',
                                    *arg,**kw)

    def add_combobox(self,pos,*arg,**kw):
        return self.ui.add_combobox(pos,
               fg='#1976d2',bg='#e0f7fa',outline='#80deea',
               activefg='#1976d2',activebg='#e3f2fd',
               scrollbg='#f5f5f5',scrollcolor='#9e9e9e',scrollon='#757575',
                                    *arg,**kw)

    def add_progressbar(self,pos,*arg,**kw):
        return self.ui.add_progressbar(pos,
            fg='#00acc1',bg='#0097a7',back='#f0f8ff',
                  fontc='#b3e5fc',*arg,**kw)

    def add_table(self,pos,*arg,**kw):
        return self.ui.add_table(pos,
                outline='#80deea',fg='black',bg='white',
                headbg='#e0f7fa',*arg,**kw)

    def add_onoff(self,pos,*arg,**kw):
        return self.ui.add_onoff(pos,
                fg='#42a5f5',bg='#e0f7fa',
                onfg='#ffffff',onbg='#00bcd4',
                                 *arg,**kw)

    def add_spinbox(self,pos,*arg,**kw):
        return self.ui.add_spinbox(pos,
              fg='#1976d2',bg='#e0f7fa',line='#80deea',
              activefg='#1565c0',activebg='#e3f2fd',
              onfg='#00acc1',onbg='#e0f7fa',
              boxfg='#42a5f5',boxbg='#e0f7fa',
              boxactivefg='#3949ab',boxactivebg='#d0d0d0',
                                   *arg,**kw)

    def add_scalebar(self,pos,*arg,**kw):
        return self.ui.add_scalebar(pos,
            fg='#0097a7',bg='#00acc1',activefg='#0097a7',
            buttonbg='#ffffff',buttonoutline='#80deea',
                                    *arg,**kw)

    def add_info(self,pos,*arg,**kw):
        return self.ui.add_info(pos,
           fg='#007bff',bg='#e3f2fd',info_fg='#1976d2',
                                *arg,**kw)

    def add_menubar(self,uid,*arg,**kw):
        return self.ui.add_menubar(uid,
            fg='#1976d2',bg='#e3f2fd',line='#80deea',
            activefg='#1565c0',activebg='#e0e0e0',activeline='#e0e0e0',*arg,**kw)

    def add_tooltip(self,uid,*arg,**kw):
        return self.ui.add_tooltip(uid,fg='#1976d2',bg='#e0e0e0',
                                   *arg,**kw)

    def add_waitbar3(self,pos,*arg,**kw):
        return self.ui.add_waitbar3(pos,
            fg='#0097a7',bg='#f0f8ff',okcolor='#0097a7',
                                    *arg,**kw)

    def add_textbox(self,pos,*arg,**kw):
        return self.ui.add_textbox(pos,fg='#1976d2',bg='white',
              outline='#00acc1',onoutline='#0097a7',
              scrollbg='#e0f7fa',scrollcolor='#8d8d8d',scrollon='#8a8a8a',
                                   *arg,**kw)

    def add_scrollbar(self,pos,widget,*arg,**kw):
        return self.ui.add_scrollbar(pos,widget,
                bg='#e0f7fa',color='#8d8d8d',
                 oncolor='#8a8a8a',*arg,**kw)

    def add_listbox(self,pos,*arg,**kw):
        return self.ui.add_listbox(pos,
                bg='#e0f7fa',fg='black',activebg='#b3e5fc',sel='#80deea',
                scrollbg='#e0f7fa',scrollcolor='#8d8d8d',scrollon='#8a8a8a',
                                   *arg,**kw)

    def add_canvas(self,pos,*arg,**kw):
        return self.ui.add_canvas(pos,
                outline='#808080',linew=1,
                scrollbg='#e0f7fa',scrollcolor='#8d8d8d',scrollon='#8a8a8a',
                                  *arg,**kw)

    def add_pipspager(self,pos,*arg,**kw):
        return self.ui.add_pipspager(pos,
                bg='#f0f8ff',fg='#00acc1',
                buttonfg='#42a5f5',buttonbg='#e0f7fa',
                activefg='#3949ab',activebg='#e0f7fa',
                buttononfg='#3949ab',buttononbg='#e0f7fa',
                                     *arg,**kw)

    def add_notebook(self,pos,*arg,**kw):
        return self.ui.add_notebook(pos,
                color='#f0f8ff',fg='#42a5f5',bg='#f0f8ff',
                activefg='#3949ab',activebg='#e3f2fd',
                onfg='#1976d2',onbg='#e3f2fd',
                scrollbg='#e0f7fa',scrollcolor='#8d8d8d',scrollon='#8a8a8a',
                                    *arg,**kw)

    def add_radiobox(self,pos,*arg,**kw):
        return self.ui.add_radiobox(pos,
                fontfg='black',fg='#00acc1',bg='#e0f7fa',
                activefg='#0097a7',activebg='#b2ebf2',
                onfg='#007bff',onbg='#ffffff',
                                    *arg,**kw)

    def add_ratingbar(self,pos,*arg,**kw):
        return self.ui.add_ratingbar(pos,
                fg='#42a5f5',bg='#f0f8ff',
                onfg='#0097a7',onbg='#0097a7',
                                     *arg,**kw)

    def add_notecard(self,pos,*arg,**kw):
        return self.ui.add_notecard(pos,
                tfg='#1976d2',tbg='#e0f7fa',fg='#1976d2',
                bg='#e8f5e9',sep='#80deea',
                                    *arg,**kw)

    def add_pivot(self,pos,*arg,**kw):
        return self.ui.add_pivot(pos,
                fg='#42a5f5',bg='',
                activefg='#000000',activecolor='#0097a7',
                                 *arg,**kw)

    def add_button2(self,pos,*arg,**kw):
        return self.ui.add_button2(pos,fg='#1976d2',bg='#e0f7fa',
             activefg='#1565c0',activebg='#b3e5fc',
             line='#80deea',linew=1,activeline='#80deea',
             onfg='#42a5f5',onbg='#e0f7fa',online='#80deea',
                           *arg,**kw)

    def add_expander(self,pos,*arg,**kw):
        return self.ui.add_expander(pos,
                tfg='#1976d2',tbg='#e0f7fa',
                bg='#e8f5e9',sep='#80deea',
                buttonfg='#1976d2',buttonbg='#e0f7fa',buttonline='#e0f7fa',
                activefg='#1565c0',activebg='#e3f2fd',activeline='#e3f2fd',
                onfg='#1976d2',onbg='#e0f7fa',online='#e0f7fa',
                                    *arg,**kw)

    def add_waitframe(self,pos,*arg,**kw):
        return self.ui.add_waitframe(pos,
                fg='#e0f7fa',bg='#e3f2fd',
                                     *arg,**kw)

    def add_listview(self,pos,*arg,**kw):
        return self.ui.add_listview(pos,
                bg='#f0f8ff',activebg='#e3f2fd',oncolor='#0097a7',
                scrobg='#e0f7fa',scroc='#868686',scrooc='#898989',
                                    *arg,**kw)

    def add_treeview(self,pos,*arg,**kw):
        return self.ui.add_treeview(pos,
                fg='#1976d2',bg='#f0f8ff',
                onfg='#1976d2',onbg='#e3f2fd',
                oncolor='#0097a7',signcolor='#8a8a8a',
                *arg,**kw)

    def add_togglebutton(self,pos,*arg,**kw):
        return self.ui.add_togglebutton(pos,
                fg='#1976d2',bg='#e0f7fa',line='#80deea',
                activefg='#e0f7fa',activebg='#0097a7',activeline='#00838f',
                *arg,**kw)

    def add_swipecontrol(self,pos,*arg,**kw):
        return self.ui.add_swipecontrol(pos,
                fg='#1976d2',bg='#f0f8ff',line='#e0f7fa',
                data={'left':({'text':'✔️\nok','fg':'#202020','bg':'#b2ebf2','command':print},),
                'right':({'text':'❌\nclose'},)},
                *arg,**kw)

    def add_picker(self,pos,*arg,**kw):
        return self.ui.add_picker(pos,
                fg='#1976d2',bg='#e0f7fa',
                outline='#e0e0e0',activefg='#1976d2',
                activebg='#e3f2fd',onfg='#e3f2fd',onbg='#0097a7',
                buttonfg='#1976d2',buttonbg='#e0f7fa',
                buttonactivefg='#1976d2',buttonactivebg='#e0f7fa',
                *arg,**kw)

    def add_menubutton(self,pos,*arg,**kw):
        return self.ui.add_menubutton(pos,
                fg='#1976d2',bg='#e0f7fa',line='#80deea',
                activefg='#1565c0',activebg='#b3e5fc',activeline='#80deea',
                onfg='#42a5f5',onbg='#e0f7fa',online='#80deea',
                menuonfg='#1565c0',menuonbg='#e0e0e0',menuonline='#e0e0e0',
                *arg,**kw)

    def add_barbutton(self,pos,*arg,**kw):
        return self.ui.add_barbutton(pos,
                fg='#42a5f5',bg='#f0f8ff',line='#f0f8ff',
                activefg='#1565c0',activebg='#e3f2fd',activeline='#e3f2fd',
                onfg='#42a5f5',onbg='#e0f7fa',online='#e0f7fa',sepcolor='#80deea',
                *arg,**kw)

    def add_flyout(self,fid,*arg,**kw):
        return self.ui.add_flyout(fid,
                line='#80deea', bg='#e3f2fd',
                *arg,**kw)
