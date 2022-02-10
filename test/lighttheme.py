from window import *
#winui3
#部分组件无法展示

def end():
    bbox=u.bbox('all')
    if bbox==None:
        return (5,5)
    return (5,bbox[3]+10)

r=win()

u=r.u

#button
u.add_button(end(),text='light theme',fg='#1b1b1b',bg='#fbfbfb',
             activefg='#1a1a1a',activebg='#f6f6f6',
             line='#cccccc',linew=1,activeline='#cccccc')
#checkbox
u.add_checkbutton(end(),text='test checkbutton',fontfg='#1a1a1a',fg='#868686',bg='#ededed',
                  activefg='#868686',activebg='#e5e5e5',
                  onfg='white',onbg='#334ac0')
#textblock
u.add_label(end(),text='test label',fg='#1a1a1a',bg='#f3f3f3',outline='#f3f3f3')
#textbox
u.add_entry(end(),text='test entry',width=200,fg='#606060',bg='#fbfbfb',
            activefg='black',activebg='#fbfbfb',
            linew=2,outline='#868686',onoutline='#3041d8')
#appbarseparator
u.add_separate(end(),200,fg='#e5e5e5')
#radiobutton
#u.add_radiobutton
#hyperlinkbutton
u.add_link(end(),text='test link',url='smart-space.com.cn',
           fg='#4f62ca',
           activefg='red',activebg='#eaeaea')
#progressring
u.add_waitbar1(end(),fg='#3041d8',bg='#f3f3f3',okfg='#3041d8',bd=5)
#u.add_labelframe(...)
#u.add_waitbar2(...)
#combobox
u.add_combobox(end(),text='test combobox',content=('1','2','3','4','5'),
               fg='#1a1a1a',bg='#fbfbfb',
               activefg='#1a1a1a',activebg='#ededee')
#progressbar
u.add_progressbar((end()[0],end()[1]+130),fg='#868686',bg='#334ac0',back='#f3f3f3',
                  fontc='#79b8f8')[3](75)
#treeview
#u.add_table(...)
#toggleswitch
u.add_onoff(end(),fg='#5a5a5a',bg='#ededed',onfg='#ffffff',onbg='#4453db')
#u.add_spinbox(...)
#slider
u.add_scalebar(end(),fg='#3b50ba',bg='#868686',activefg='#aeb5d7')
#u.add_info(...)
#menubar
l1=u.add_label(end(),text='menubar test label')[-1]
u.add_menubar(l1,fg='#1a1a1a',bg='#faf8f9',activefg='#1a1a1a',activebg='#efefef',
              cont=(('test1',print),('test2',print),'-',('test3',print)))
#tooltip
l2=u.add_label(end(),text='tooltip test label')[-1]
u.add_tooltip(l2,text='test tooltip',fg='#1a1a1a',bg='#efefef')
#progressbar
u.add_waitbar3(end(),fg='#3041d8',bg='#f3f3f3',okcolor='#3041d8')
#richeditbox
textx,texty=end()
text=u.add_textbox((textx,texty),fg='#1a1a1a',bg='white',
              outline='#868686',onoutline='#3041d8',linew=2)[0]
#richtextbox
u.add_scrollbar((textx+205,texty),text,bg='#f9f9f9',color='#8d8d8d',
                 oncolor='#8a8a8a')

u.add_back(end())
r.r.title('TinUI light theme')
r.go()
