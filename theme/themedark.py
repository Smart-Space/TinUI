from typing import Union
from window import *
#winui3
#部分组件无法展示

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
            outline='#9a9a9a',onoutline='#b2b8f2',
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
                headbg='#202020',*arg,**kw)

    def add_onoff(self,pos,*arg,**kw):
        return self.ui.add_onoff(pos,
                fg='#cccccc',bg='#1d1d1d',
                onfg='#000000',onbg='#b2b8f2',
                                 *arg,**kw)

    def add_spinbox(self,pos,*arg,**kw):
        return self.ui.add_spinbox(pos,
              fg='#ffffff',bg='#1f1f1f',line='#303030',
              activefg='#c0c0c0',activebg='#2c2c2c',
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
            fg='#e6e6e6',bg='#323233',line='#3d3d3e',
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
                bg='#202020',fg='#9a9a9a',buttonbg='#303030',
                activefg='#cccccc',activebg='#303030',
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
             activefg='#e8e8e8',activebg='#323232',
             line='#303030',linew=1,activeline='#303030',
                           *arg,**kw)

    def add_expander(self,pos,*arg,**kw):
        return self.ui.add_expander(pos,
                tfg='#ffffff',tbg='#2b2b2b',
                bg='#272727',sep='#1d1d1d',
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
                fg='#cfcfcf',bg='#2d2d2d',outline='#303030',
                activefg='#ffffff',activebg='#3a3a3a',
                onfg='#000000',onbg='#a8ade4',
                *arg,**kw)
    
    def add_menubutton(self,pos,*arg,**kw):
        return self.ui.add_menubutton(pos,
                fg='#ffffff',bg='#2d2d2d',line='#303030',
                activefg='#ffffff',activebg='#3f3f40',activeline='#3f3f3f',
                *arg,**kw)
    
    def add_barbutton(self,pos,*arg,**kw):
        return self.ui.add_barbutton(pos,
                fg='#ffffff',bg='#202020',line='#202020',
                activefg='#cecece',activebg='#2d2d2d',activeline='#2d2d2d',sepcolor='#323232',
                *arg,**kw)

    def add_flyout(self,fid,*arg,**kw):
        return self.ui.add_flyout(fid,
                line='#b0b0b0',bg='#2c2c2c',
                *arg,**kw)


def end():
    bbox=u.bbox('all')
    if bbox==None:
        return (5,5)
    return (5,bbox[3]+10)

r=win()


u=r.u
du=TinUIDark(u)
u['background']='#202020'
x=TinUIXml(du)

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
#splitview
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
#listbox
du.add_listbox(end(),data=('first','second','third',
'some thing between three and four called bleem','forth','fifth',
'some thins behind five\nwhich we can not find it\nfor-\never'))
#inkcanvas
canvas=du.add_canvas(end())[0]
canvas.create_text((100,20),text='TinUI canvas',font='微软雅黑 12')
canvas.create_line((20,50,180,50),fill='#202020',width=5)
#pipspager
du.add_pipspager(end(),num=5)
#tabview
ntb=du.add_notebook(end())[-2]
for i in range(1,4):
    ntb.addpage('test'+str(i),'t'+str(i))
ntvdict=ntb.getvdict()
num=1
for i in ntvdict:
    ui=ntvdict[i][0]
    uxml=TinUIXml(TinUIDark(ui))
    xml=f'''
<tinui><line><button text='这是第{num}个BasicTinUI组件' command='print'></button></line>
<line><label text='TinUI的标签栏视图'></label><label text='每个都是单独页面'></label></line>
</tinui>'''
    uxml.loadxml(xml)
    num+=1
#ratingcontrol
du.add_ratingbar(end())
#radiobutton
du.add_radiobox(end(),command=print)
#expander
du.add_notecard(end())
#pivot
du.add_pivot(end())
#button
du.add_button2(end(),'button2')
#expander
du.add_expander(end())
#animation interop
wffunc=du.add_waitframe((end()[0],end()[1]+200))[3]
wffunc.start()
#listview
du.add_listview(end(),num=10)
#treeview
du.add_treeview(end())
#togglebutton
du.add_togglebutton(end(),text='状态开关按钮')
#swipecontrol
du.add_swipecontrol(end(),text='SwipeControl')
#timepicker
du.add_picker(end())
#dropdownbutton
du.add_menubutton(end(),text='menubutton')
#appbarbutton
du.add_barbutton(end())
#flyout
flylabel = du.add_label(end(),text='Flyout控件-左键单击')[-1]
du.add_flyout(flylabel,anchor='ne')

u.add_back(end())
r.r.title('TinUI dark theme')
r.go()
