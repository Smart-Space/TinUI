from typing import Union
from window import *
#winui3
#部分组件无法展示

class TinUIDark:
    '''
    这是TinUI黑暗模式的托管类，不是继承类
    调用时这需要注意文本和数据，样式类参数无需理会
    '''

    def __init__(self,ui:Union[TinUI,BasicTinUI]):
        self.ui=ui
        self.label='dark'

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
            linew=2,outline='#9a9a9a',onoutline='#b2b8f2',
                          *arg,**kw)

    def add_separate(self,pos,*arg,**kw):
        return self.ui.add_separate(pos,fg='#323232',
                             *arg,**kw)

    def add_radiobutton(self,pos,*arg,**kw):
        return self.ui.add_radiobutton(pos,
                  fg='#ffffff',bg='#1d1d1d',
                  activefg='#000000',activebg='#b2b8f2',
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
                    fg='#b2b8f2',bg='#202020',okcolor='#b2b8f2',
                                    *arg,**kw)

    def add_combobox(self,pos,*arg,**kw):
        return self.ui.add_combobox(pos,
               fg='#cfcfcf',bg='#2d2d2d',
               activefg='#ffffff',activebg='#393939',
                                    *arg,**kw)

    def add_progressbar(self,pos,*arg,**kw):
        return self.ui.add_progressbar(pos,
                fg='#9a9a9a',bg='#b2b8f2',back='#202020',
                fontc='#0000ff',*arg,**kw)

    def add_table(self,pos,*arg,**kw):
        return self.ui.add_table(pos,
                outline='#9a9a9a',fg='#ffffff',bg='#2d2d2d',
                headbg='#b2b8f2',*arg,**kw)

    def add_onoff(self,pos,*arg,**kw):
        return self.ui.add_onoff(pos,
                fg='#cccccc',bg='#1d1d1d',
                onfg='#000000',onbg='#b2b8f2',
                                 *arg,**kw)

    def add_spinbox(self,pos,*arg,**kw):
        return self.ui.add_spinbox(pos,
              fg='#ffffff',bg='#2d2d2d',
              activefg='#b8b8b8',activebg='#393939',
                                   *arg,**kw)

    def add_scalebar(self,pos,*arg,**kw):
        return self.ui.add_scalebar(pos,
                fg='#b2b8f2',bg='#9a9a9a',activefg='#c2d1fa',
                                    *arg,**kw)

    def add_info(self,pos,*arg,**kw):
        return self.ui.add_info(pos,
           fg='#b2b8f2',bg='#2d2d2d',info_fg='#ffffff',
                                *arg,**kw)

    def add_menubar(self,uid,*arg,**kw):
        return self.ui.add_menubar(uid,
            fg='#e6e6e6',bg='#323233',
            activefg='#ffffff',activebg='#3d3d3e',*arg,**kw)

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
                                   *arg,**kw)

    def add_scrollbar(self,pos,widget,*arg,**kw):
        return self.ui.add_scrollbar(pos,widget,
                bg='#2e2e2e',color='#9f9f9f',
                oncolor='#a0a0a0',*arg,**kw)


def end():
    bbox=u.bbox('all')
    if bbox==None:
        return (5,5)
    return (5,bbox[3]+10)

r=win()

u=r.u
du=TinUIDark(u)
u['background']='#202020'

#button
du.add_button(end(),text='dark theme')
#checkbox
du.add_checkbutton(end(),text='test checkbutton')
#textblock
du.add_label(end(),text='test label')
#textbox
du.add_entry(end(),text='test entry',width=200)
#appbarseparator
du.add_separate(end(),width=200)
#radiobutton
du.add_radiobutton(end(),width=250,text='test radiobutton',
                  choices=('1','2','3','4','5'))
#hyperlinkbutton
du.add_link(end(),text='test link',url='smart-space.com.cn')
#progressring
du.add_waitbar1(end())
#infobar
labelframey=end()[1]+30
lb1=du.add_button((5,labelframey),text='labelframe button1')[1]
lb2=du.add_button(end(),text='labelframe button2')[-1]
lb3=du.add_button(end(),text='labelframe button3')[-1]
du.add_labelframe((lb1,lb2,lb3),title='labelframe')
#progressbar
du.add_waitbar2(end())
#combobox
du.add_combobox(end(),text='test combobox',
               content=('1','2','3','4','5'))
#progressbar
du.add_progressbar((end()[0],end()[1]+130))[3](75)
#treeview
du.add_table(end(),
data=[['t1','t2','t3'],['tinui','table','test'],['1','2','3']])
#toggleswitch
du.add_onoff(end())
#numberbutton
du.add_spinbox(end(),data=('1','2','3','4','5'))
#slider
du.add_scalebar(end())
#teachingtip
du.add_info(end(),info_text='info test')
#menubar
u.add_back(end())
l1=du.add_label(end(),text='menubar test label')[-1]
du.add_menubar(l1,
cont=(('test1',print),('test2',print),'-',('test3',print)))
#tooltip
l2=du.add_label(end(),text='tooltip test label')[-1]
du.add_tooltip(l2,text='test tooltip')
#progressbar
du.add_waitbar3(end())
#richeditbox
textx,texty=end()
text=du.add_textbox((textx,texty),linew=2)[0]
text['insertbackground']='#e0e0e0'
#richtextbox
du.add_scrollbar((textx+205,texty),text)

u.add_back(end())
r.r.title('TinUI light theme')
r.go()
