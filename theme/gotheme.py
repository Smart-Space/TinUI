# 由chat-glm4生成，作者小改。作为示例，不会维护
from typing import Union
from tkinter import Tk, Toplevel
from tinui import TinUI, BasicTinUI, TinUITheme, TinUIXml

from tinuilight import TinUILight
from tinuidark import TinUIDark
from tinuimodernlight import TinUIModernLight
from tinuimoderndark import TinUIModernDark
from tinuidarkorange import TinUIDarkOrange
from tinuidarkpurple import TinUIDarkPurple
from tinuilightcyan import TinUILightCyan
from tinuilightred import TinUILightRed
from tinuisteelblue import TinUISteelBlue


def test(theme):
    def end():
        bbox=u.bbox('all')
        if bbox==None:
            return (5,5)
        return (5,bbox[3]+10)
    
    r=Toplevel()
    r.geometry('500x500')
    u=TinUI(r)
    u.pack(fill='both',expand=True)
    
    du=theme(u)

    #button
    du.add_button(end(),text='TinUI theme')
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
    du.add_progressbar((end()[0],end()[1]+130))[4](75)
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
    text=du.add_textbox((textx,texty))[0]
    #richtextbox
    du.add_scrollbar((textx+205,texty),text)
    #listbox
    du.add_listbox(end(),data=('first','second','third',
    'some thing between three and four called bleem','forth','fifth',
    'some thins behind five\nwhich we can not find it\nfor-\never'))
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
        uxml=TinUIXml(theme(ui))
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
    du.add_accentbutton(end(),'accentbutton')
    #appbarbutton
    du.add_toolbutton(end(),'',icon='\uE90F')
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
    flylabel = du.add_label(end(),text='Flyout控件(左键单击)')[-1]
    du.add_flyout(flylabel,anchor='ne')
    bdf = du.add_breadcrumb(end(),flylabel)[-2]
    for i in range(1,4):
        bdf.add(f'item{i}')
    du.add_segmentbutton(end(),content=('tkinter', 'TinUI', 'Others'))
    du.add_navigation(end())

w = Tk()
w.geometry('500x500+500+100')

ru = BasicTinUI(w)
ru.pack(fill='both',expand=True)

ru.add_button((5,5), text='TinUILight theme', command = lambda e : test(TinUILight))
ru.add_button((220,5), text='TinUIDark theme', command = lambda e : test(TinUIDark))
ru.add_button((5,55), text='TinUIModernLight theme', command = lambda e : test(TinUIModernLight))
ru.add_button((220,55), text='TinUIModernDark theme', command = lambda e : test(TinUIModernDark))
ru.add_button((5,105), text='TinUIDarkOrange theme', command = lambda e : test(TinUIDarkOrange))
ru.add_button((220,105), text='TinUIDarkPurple theme', command = lambda e : test(TinUIDarkPurple))
ru.add_button((5,155), text='TinUILightCyan theme', command = lambda e : test(TinUILightCyan))
ru.add_button((220,155), text='TinUILightRed theme', command = lambda e : test(TinUILightRed))
ru.add_button((5,205), text='TinUISteelBlue theme', command = lambda e : test(TinUISteelBlue))

w.mainloop()
