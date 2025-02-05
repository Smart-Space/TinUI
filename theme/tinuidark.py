from typing import Union
import sys
sys.path.append('../')
from TinUI import TinUI, BasicTinUI, TinUITheme, TinUIXml

class TinUIDark(TinUITheme):
    '''
    这是TinUI黑暗模式的托管类，不是继承类
    调用时这需要注意文本和数据，样式类参数无需理会
    '''

    def __init__(self,ui:Union[TinUI,BasicTinUI]):
        super().__init__(ui,'tinui-dark-theme')
        self.label='dark'
        self.ui['background']='#202020'

    def add_button(self,pos,*arg,**kw):
        return self.ui.add_button(pos,fg='#ffffff',bg='#2d2d2d',
             activefg='#e8e8e8',activebg='#323232',
             line='#303030',linew=1,activeline='#303030',
                           *arg,**kw)

    def add_checkbutton(self,pos,*arg,**kw):
        return self.ui.add_checkbutton(pos,
            fontfg='#ffffff',fg='#999999',bg='#1d1d1d',
                  activefg='#9c9c9c',activebg='#2a2a2a',
                  onfg='#010101',onbg='#a3a8dc',
                                *arg,**kw)

    def add_label(self,pos,*arg,**kw):
        return self.ui.add_label(pos,fg='#ffffff',bg='#202020',
                          outline='#202020',*arg,**kw)

    def add_entry(self,pos,*arg,**kw):
        return self.ui.add_entry(pos,fg='#cfcfcf',bg='#2d2d2d',
            activefg='#e6e6e6',activebg='#1f1f1f',
            line='#303030',activeline='#303030',
            outline='#9a9a9a',onoutline='#b2b8f2',insert='#e0e0e0',
                          *arg,**kw)

    def add_separate(self,pos,*arg,**kw):
        return self.ui.add_separate(pos,fg='#323232',
                             *arg,**kw)

    def add_radiobutton(self,pos,*arg,**kw):
        return self.ui.add_radiobutton(pos,
                  fg='#f2f2f2',bg='#2b2b2b',
                  activefg='#ffffff',activebg='#373737',
                                *arg,**kw)

    def add_link(self,pos,*arg,**kw):
        return self.ui.add_link(pos,fg='#d7d9f9',
           activefg='#d7d9f9',activebg='#2d2d2d',
                                *arg,**kw)

    def add_waitbar1(self,pos,*arg,**kw):
        return self.ui.add_waitbar1(pos,fg='#b2b8f2',
                                   bg='#202020',okfg='#b2b8f2',bd=5,
                                   *arg,**kw)

    def add_labelframe(self,uids:tuple,*arg,**kw):
        return self.ui.add_labelframe(uids,fg='#ffffff',bg='#272727',
                                      *arg,**kw)

    def add_waitbar2(self,pos,*arg,**kw):
        return self.ui.add_waitbar2(pos,
                    fg='#b2b8f2',bg='#202020',okcolor='#6ccb5f',
                                    *arg,**kw)

    def add_combobox(self,pos,*arg,**kw):
        return self.ui.add_combobox(pos,
               fg='#cfcfcf',bg='#2d2d2d',outline='#303030',
               activefg='#ffffff',activebg='#393939',
               scrollbg='#2c2c2c',scrollcolor='#9f9f9f',scrollon='#a0a0a0',
                                    *arg,**kw)

    def add_progressbar(self,pos,*arg,**kw):
        return self.ui.add_progressbar(pos,
                fg='#9a9a9a',bg='#b2b8f2',back='#202020',
                fontc='#0000ff',*arg,**kw)

    def add_table(self,pos,*arg,**kw):
        return self.ui.add_table(pos,
                outline='#9a9a9a',fg='#ffffff',bg='#2d2d2d',
                headbg='#202020',*arg,**kw)

    def add_onoff(self,pos,*arg,**kw):
        return self.ui.add_onoff(pos,
                fg='#cccccc',bg='#1d1d1d',
                onfg='#000000',onbg='#b2b8f2',
                                 *arg,**kw)

    def add_spinbox(self,pos,*arg,**kw):
        return self.ui.add_spinbox(pos,
              fg='#ffffff',bg='#2d2d2d',line='#303030',
              activefg='#c0c0c0',activebg='#323232',
              boxfg='#cfcfcf',boxbg='#2c2c2c',
              boxactivefg='#d2d2d2',boxactivebg='#383838',
              onfg='#9f9f9f',onbg='#343434',
                                   *arg,**kw)

    def add_scalebar(self,pos,*arg,**kw):
        return self.ui.add_scalebar(pos,
                fg='#b2b8f2',bg='#9a9a9a',activefg='#b2b8f2',
                buttonbg='#454545',buttonoutline='#303030',
                                    *arg,**kw)

    def add_info(self,pos,*arg,**kw):
        return self.ui.add_info(pos,
           fg='#b2b8f2',bg='#2d2d2d',info_fg='#ffffff',
                                *arg,**kw)

    def add_menubar(self,uid,*arg,**kw):
        return self.ui.add_menubar(uid,
            fg='#ffffff',bg='#2c2c2c',line='#b3b3b3',
            activefg='#ffffff',activebg='#383838',activeline='#383838',*arg,**kw)

    def add_tooltip(self,uid,*arg,**kw):
        return self.ui.add_tooltip(uid,fg='#e8e8e8',bg='#353535',
                                   *arg,**kw)

    def add_waitbar3(self,pos,*arg,**kw):
        return self.ui.add_waitbar3(pos,
            fg='#b2b8f2',bg='#202020',okcolor='#b2b8f2',
                                    *arg,**kw)

    def add_textbox(self,pos,*arg,**kw):
        return self.ui.add_textbox(pos,fg='#ffffff',bg='#2d2d2d',
              outline='#9a9a9a',onoutline='#b2b8f2',
              scrollbg='#2e2e2e',scrollcolor='#9f9f9f',scrollon='#a0a0a0',
                                   *arg,**kw)

    def add_scrollbar(self,pos,widget,*arg,**kw):
        return self.ui.add_scrollbar(pos,widget,
                bg='#2e2e2e',color='#9f9f9f',
                oncolor='#a0a0a0',*arg,**kw)

    def add_listbox(self,pos,*arg,**kw):
        return self.ui.add_listbox(pos,
                bg='#2b2b2b',fg='white',activebg='#b4bbea',sel='#465097',
                scrollbg='#2e2e2e',scrollcolor='#9f9f9f',scrollon='#a0a0a0',
                                   *arg,**kw)

    def add_canvas(self,pos,*arg,**kw):
        return self.ui.add_canvas(pos,
                outline='#808080',linew=1,
                scrollbg='#2e2e2e',scrollcolor='#9f9f9f',scrollon='#a0a0a0',
                                  *arg,**kw)

    def add_pipspager(self,pos,*arg,**kw):
        return self.ui.add_pipspager(pos,
                bg='#202020',fg='#9a9a9a',
                buttonfg='#9f9f9f',buttonbg='#2c2c2c',
                activefg='#cfcfcf',activebg='#2c2c2c',
                buttononfg='#cfcfcf',buttononbg='#2c2c2c',
                                     *arg,**kw)

    def add_notebook(self,pos,*arg,**kw):
        return self.ui.add_notebook(pos,
                color='#202020',fg='#cccccc',bg='#202020',
                activefg='#cfcfcf',activebg='#2d2d2d',
                onfg='#ffffff',onbg='#282828',
                scrollbg='#2e2e2e',scrollcolor='#9f9f9f',scrollon='#a0a0a0',
                                    *arg,**kw)

    def add_ratingbar(self,pos,*arg,**kw):
        return self.ui.add_ratingbar(pos,
                fg='#cccccc',bg='#202020',
                onfg='#b2b8f2',onbg='#b2b8f2',
                                     *arg,**kw)

    def add_radiobox(self,pos,*arg,**kw):
        return self.ui.add_radiobox(pos,
                fontfg='#ffffff',fg='#939393',bg='#2a2a2a',
                activefg='#959595',activebg='#2a2a2a',
                onfg='#a3a8dc',onbg='#000000',
                                    *arg,**kw)

    def add_notecard(self,pos,*arg,**kw):
        return self.ui.add_notecard(pos,
                tfg='#ffffff',tbg='#2b2b2b',fg='#ffffff',
                bg='#272727',sep='#1d1d1d',
                                    *arg,**kw)

    def add_pivot(self,pos,*arg,**kw):
        return self.ui.add_pivot(pos,
                fg='#a6a6a6',bg='',
                activefg='#ffffff',activecolor='#5969e0',
                                 *arg,**kw)

    def add_button2(self,pos,*arg,**kw):
        return self.ui.add_button2(pos,fg='#ffffff',bg='#2d2d2d',
             activefg='#ffffff',activebg='#323232',
             line='#303030',linew=1,activeline='#202020',
             onfg='#cecece',onbg='#272727',online='#303030',
                           *arg,**kw)

    def add_expander(self,pos,*arg,**kw):
        return self.ui.add_expander(pos,
                tfg='#ffffff',tbg='#2b2b2b',
                bg='#272727',sep='#1d1d1d',
                buttonfg='#ffffff',buttonbg='#2b2b2b',buttonline='#2b2b2b',
                activefg='#ffffff',activebg='#373737',activeline='#373737',
                onfg='#ffffff',onbg='#333333',online='#333333',
                                    *arg,**kw)

    def add_waitframe(self,pos,*arg,**kw):
        return self.ui.add_waitframe(pos,
                fg='#2d2d2d',bg='#323232',
                                     *arg,**kw)

    def add_listview(self,pos,*arg,**kw):
        return self.ui.add_listview(pos,
                bg='#202020',activebg='#2d2d2d',oncolor='#b2b8f2',
                scrobg='#2e2e2e',scroc='#9a9a9a',scrooc='#9f9f9f',
                                    *arg,**kw)

    def add_treeview(self,pos,*arg,**kw):
        return self.ui.add_treeview(pos,
                fg='#ffffff',bg='#202020',
                onfg='#ffffff',onbg='#2d2d2d',
                oncolor='#b2b8f2',signcolor='#9f9f9f',
                *arg,**kw)

    def add_togglebutton(self,pos,*arg,**kw):
        return self.ui.add_togglebutton(pos,
                fg='#ffffff',bg='#2d2d2d',line='#303030',
                activefg='#000000',activebg='#b2b8f2',activeline='#b8bef3',
                *arg,**kw)
    
    def add_swipecontrol(self,pos,*arg,**kw):
        return self.ui.add_swipecontrol(pos,
                fg='#ffffff',bg='#202020',line='#2d2d2d',
                data={'left':({'text':'✔️\nok','fg':'#000000','bg':'#a9a9a9','command':print},),
                'right':({'text':'❌\nclose'},)},
                *arg,**kw)

    def add_picker(self,pos,*arg,**kw):
        return self.ui.add_picker(pos,
                fg='#cfcfcf',bg='#2d2d2d',outline='#3c3c3c',
                activefg='#ffffff',activebg='#323232',
                onfg='#000000',onbg='#a8ade4',
                buttonfg='#ffffff',buttonbg='#2d2d2d',
                buttonactivefg='#ffffff',buttonactivebg='#343434',
                *arg,**kw)
    
    def add_menubutton(self,pos,*arg,**kw):
        return self.ui.add_menubutton(pos,
                fg='#ffffff',bg='#2d2d2d',line='#303030',
                activefg='#ffffff',activebg='#323232',activeline='#202020',
                onfg='#cecece',onbg='#272727',online='#303030',
                menuonfg='#ffffff',menuonbg='#383838',menuonline='#383838',
                *arg,**kw)
    
    def add_barbutton(self,pos,*arg,**kw):
        return self.ui.add_barbutton(pos,
                fg='#ffffff',bg='#202020',line='#202020',
                activefg='#cecece',activebg='#2d2d2d',activeline='#2d2d2d',
                onfg='#cecece',onbg='#292929',online='#292929',sepcolor='#e5e5e5',
                *arg,**kw)

    def add_flyout(self,fid,*arg,**kw):
        return self.ui.add_flyout(fid,
                line='#b0b0b0',bg='#2c2c2c',
                *arg,**kw)
