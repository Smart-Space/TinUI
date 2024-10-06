from typing import Union
from window import *
#winui3
#部分组件无法展示

class TinUILight(TinUITheme):
    '''
    这是TinUI明亮模式的托管类，不是继承类
    调用时这需要注意文本和数据，样式类参数无需理会
    '''

    def __init__(self,ui:Union[TinUI,BasicTinUI]):
        super().__init__(ui,'tinui-light-theme')
        self.label='dark'
        self.ui['background']='#f3f3f3'

    def add_button(self,pos,*arg,**kw):
        return self.ui.add_button(pos,fg='#1b1b1b',bg='#fbfbfb',
             activefg='#1a1a1a',activebg='#f6f6f6',
             line='#cccccc',linew=1,activeline='#cccccc',
                           *arg,**kw)

    def add_checkbutton(self,pos,*arg,**kw):
        return self.ui.add_checkbutton(pos,
            fontfg='#1a1a1a',fg='#868686',bg='#ededed',
                  activefg='#868686',activebg='#e5e5e5',
                  onfg='white',onbg='#334ac0',
                                *arg,**kw)

    def add_label(self,pos,*arg,**kw):
        return self.ui.add_label(pos,fg='#1a1a1a',bg='#f3f3f3',
                                 outline='#f3f3f3',*arg,**kw)

    def add_entry(self,pos,*arg,**kw):
        return self.ui.add_entry(pos,fg='#606060',bg='#fbfbfb',
            activefg='#1b1b1b',activebg='#ffffff',
            line='#e5e5e5',activeline='#e5e5e5',
            outline='#868686',onoutline='#3041d8',
                          *arg,**kw)

    def add_separate(self,pos,*arg,**kw):
        return self.ui.add_separate(pos,fg='#e5e5e5',
                             *arg,**kw)

    def add_radiobutton(self,pos,*arg,**kw):
        return self.ui.add_radiobutton(pos,
                  fg='#1a1a1a',bg='#f2f2f2',
                  activefg='#191919',activebg='#e9e9e9',
                                *arg,**kw)

    def add_link(self,pos,*arg,**kw):
        return self.ui.add_link(pos,fg='#4f62ca',
           activefg='red',activebg='#eaeaea',
                                *arg,**kw)

    def add_waitbar1(self,pos,*arg,**kw):
        return self.ui.add_waitbar1(pos,fg='#3041d8',
                                    bg='#f3f3f3',okfg='#3041d8',bd=5,
                                   *arg,**kw)

    def add_labelframe(self,uids:tuple,*arg,**kw):
        return self.ui.add_labelframe(uids,fg='#1a1a1a',bg='#f4f4f4',
                                      *arg,**kw)

    def add_waitbar2(self,pos,*arg,**kw):
        return self.ui.add_waitbar2(pos,
            fg='#3041d8',bg='#f3f3f3',okcolor='#0f7b0f',
                                    *arg,**kw)

    def add_combobox(self,pos,*arg,**kw):
        return self.ui.add_combobox(pos,
               fg='#1a1a1a',bg='#fbfbfb',
               activefg='#1a1a1a',activebg='#ededee',
                                    *arg,**kw)

    def add_progressbar(self,pos,*arg,**kw):
        return self.ui.add_progressbar(pos,
            fg='#868686',bg='#334ac0',back='#f3f3f3',
                  fontc='#79b8f8',*arg,**kw)

    def add_table(self,pos,*arg,**kw):
        return self.ui.add_table(pos,
                outline='#dadad8',fg='black',bg='white',
                headbg='#f4f4f2',*arg,**kw)

    def add_onoff(self,pos,*arg,**kw):
        return self.ui.add_onoff(pos,
                fg='#5a5a5a',bg='#ededed',
                onfg='#ffffff',onbg='#4453db',
                                 *arg,**kw)

    def add_spinbox(self,pos,*arg,**kw):
        return self.ui.add_spinbox(pos,
              fg='#1b1b1b',bg='#ffffff',line='#e5e5e5',
              activefg='#818181',activebg='#f2f2f2',
                                   *arg,**kw)

    def add_scalebar(self,pos,*arg,**kw):
        return self.ui.add_scalebar(pos,
            fg='#3b50ba',bg='#868686',activefg='#3b50ba',
            buttonbg='#ffffff',buttonoutline='#cccccc',
                                    *arg,**kw)

    def add_info(self,pos,*arg,**kw):
        return self.ui.add_info(pos,
           fg='#0078d4',bg='#f9f9f9',info_fg='#1a1a1a',
                                *arg,**kw)

    def add_menubar(self,uid,*arg,**kw):
        return self.ui.add_menubar(uid,
            fg='#1a1a1a',bg='#faf8f9',line='#e3e3e3',
            activefg='#1a1a1a',activebg='#efefef',*arg,**kw)

    def add_tooltip(self,uid,*arg,**kw):
        return self.ui.add_tooltip(uid,fg='#1a1a1a',bg='#efefef',
                                   *arg,**kw)

    def add_waitbar3(self,pos,*arg,**kw):
        return self.ui.add_waitbar3(pos,
            fg='#3041d8',bg='#f3f3f3',okcolor='#3041d8',
                                    *arg,**kw)

    def add_textbox(self,pos,*arg,**kw):
        return self.ui.add_textbox(pos,fg='#1a1a1a',bg='white',
              outline='#868686',onoutline='#3041d8',
              scrollbg='#f9f9f9',scrollcolor='#8d8d8d',scrollon='#8a8a8a',
                                   *arg,**kw)

    def add_scrollbar(self,pos,widget,*arg,**kw):
        return self.ui.add_scrollbar(pos,widget,
                bg='#f9f9f9',color='#8d8d8d',
                 oncolor='#8a8a8a',*arg,**kw)

    def add_listbox(self,pos,*arg,**kw):
        return self.ui.add_listbox(pos,
                bg='#f2f2f2',fg='black',activebg='#e9e9e9',sel='#b4bbea',
                scrollbg='#f9f9f9',scrollcolor='#8d8d8d',scrollon='#8a8a8a',
                                   *arg,**kw)

    def add_canvas(self,pos,*arg,**kw):
        return self.ui.add_canvas(pos,
                outline='#808080',linew=1,
                scrollbg='#f9f9f9',scrollcolor='#8d8d8d',scrollon='#8a8a8a',
                                  *arg,**kw)

    def add_pipspager(self,pos,*arg,**kw):
        return self.ui.add_pipspager(pos,
                bg='#f3f3f3',fg='#868686',buttonbg='#fafafa',
                activefg='#5d5d5d',activebg='#fafafa',
                                     *arg,**kw)

    def add_notebook(self,pos,*arg,**kw):
        return self.ui.add_notebook(pos,
                color='#f3f3f3',fg='#5d5d5d',bg='#f3f3f3',
                activefg='#595959',activebg='#eaeaea',
                onfg='#1a1a1a',onbg='#f9f9f9',
                scrollbg='#f9f9f9',scrollcolor='#8d8d8d',scrollon='#8a8a8a',
                                    *arg,**kw)

    def add_radiobox(self,pos,*arg,**kw):
        return self.ui.add_radiobox(pos,
                fontfg='black',fg='#8b8b8b',bg='#ededed',
                activefg='#898989',activebg='#e5e5e5',
                onfg='#3041d8',onbg='#ffffff',
                                    *arg,**kw)

    def add_ratingbar(self,pos,*arg,**kw):
        return self.ui.add_ratingbar(pos,
                fg='#5d5d5d',bg='#f3f3f3',
                onfg='#3041d8',onbg='#3041d8',
                                     *arg,**kw)

    def add_notecard(self,pos,*arg,**kw):
        return self.ui.add_notecard(pos,
                tfg='#1b1b1b',tbg='#fbfbfb',fg='#1a1a1a',
                bg='#f4f4f4',sep='#e5e5e5',
                                    *arg,**kw)

    def add_pivot(self,pos,*arg,**kw):
        return self.ui.add_pivot(pos,
                fg='#616161',bg='',
                activefg='#000000',activecolor='#5969e0',
                                 *arg,**kw)

    def add_button2(self,pos,*arg,**kw):
        return self.ui.add_button2(pos,fg='#1b1b1b',bg='#fbfbfb',
             activefg='#1a1a1a',activebg='#f6f6f6',
             line='#cccccc',linew=1,activeline='#cccccc',
                           *arg,**kw)

    def add_expander(self,pos,*arg,**kw):
        return self.ui.add_expander(pos,
                tfg='#1b1b1b',tbg='#fbfbfb',
                bg='#f4f4f4',sep='#e5e5e5',
                                    *arg,**kw)

    def add_waitframe(self,pos,*arg,**kw):
        return self.ui.add_waitframe(pos,
                fg='#fbfbfb',bg='#f6f6f6',
                                     *arg,**kw)

    def add_listview(self,pos,*arg,**kw):
        return self.ui.add_listview(pos,
                bg='#f3f3f3',activebg='#eaeaea',oncolor='#3041d8',
                scrobg='#f8f8f8',scroc='#868686',scrooc='#898989',
                                    *arg,**kw)

    def add_treeview(self,pos,*arg,**kw):
        return self.ui.add_treeview(pos,
                fg='#1a1a1a',bg='#f3f3f3',
                onfg='#1a1a1a',onbg='#eaeaea',
                oncolor='#3041d8',signcolor='#8a8a8a',
                *arg,**kw)

    def add_togglebutton(self,pos,*arg,**kw):
        return self.ui.add_togglebutton(pos,
                fg='#1b1b1b',bg='#fbfbfb',line='#cccccc',
                activefg='#f3f4fd',activebg='#3041d8',activeline='#5360de',
                *arg,**kw)
    
    def add_swipecontrol(self,pos,*arg,**kw):
        return self.ui.add_swipecontrol(pos,
                fg='#1a1a1a',bg='#f3f3f3',line='#fbfbfb',
                data={'left':({'text':'✔️\nok','fg':'#202020','bg':'#bcbcbc','command':print},),
                'right':({'text':'❌\nclose'},)},
                *arg,**kw)
    
    def add_picker(self,pos,*arg,**kw):
        return self.ui.add_picker(pos,
                fg='#1b1b1b',bg='#fbfbfb',
                outline='#ececec',activefg='#1b1b1b',
                activebg='#f6f6f6',onfg='#eaecfb',onbg='#3748d9',
                *arg,**kw)
    
    def add_menubutton(self,pos,*arg,**kw):
        return self.ui.add_menubutton(pos,
                fg='#1b1b1b',bg='#fbfbfb',line='#CCCCCC',
                activefg='#5d5d5d',activebg='#f5f5f5',activeline='#e5e5e5',
                *arg,**kw)
    
    def add_barbutton(self,pos,*arg,**kw):
        return self.ui.add_barbutton(pos,
                fg='#636363',bg='#f3f3f3',line='#f3f3f3',
                activefg='#191919',activebg='#eaeaea',activeline='#eaeaea',sepcolor='#e5e5e5',
                *arg,**kw)


def end():
    bbox=u.bbox('all')
    if bbox==None:
        return (5,5)
    return (5,bbox[3]+10)

r=win()

u=r.u
du=TinUILight(u)
u['background']='#f3f3f3'
x=TinUIXml(du)

#button
du.add_button(end(),text='light theme')
#checkbox
du.add_checkbutton(end(),text='test checkbutton')
#textblock
du.add_label(end(),text='test label')
#textbox
du.add_entry(end(),text='test entry',width=200)
#appbarseparator
du.add_separate(end(),width=200)
#splitview
du.add_radiobutton(end(),250,'test radiobutton',('1','2','3','4','5'))
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
du.add_combobox(end(),text='test combobox',content=('1','2','3','4','5'))
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
#richtextbox
du.add_scrollbar((textx+205,texty),text)
#listbox
du.add_listbox(end(),data=('first','second','third',
'some thing between three and four called bleem','forth','fifth',
'some thins behind five\nwhich we can not find it\nfor-\never'))
#inkcanvas
canvas=du.add_canvas(end())[0]
canvas.create_text((100,20),text='TinUI canvas',font='微软雅黑 12')
canvas.create_line((20,50,180,50),fill='#f3f3f3',width=5)
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
    uxml=TinUIXml(TinUILight(ui))
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

u.add_back(end())
r.r.title('TinUI light theme')
r.go()
