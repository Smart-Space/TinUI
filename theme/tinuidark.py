from typing import Union
from tinui import TinUI, BasicTinUI, TinUITheme

class TinUIDark(TinUITheme):
    '''
    这是TinUI黑暗模式的托管类，不是继承类
    调用时这需要注意文本和数据，样式类参数无需理会
    '''

    def __init__(self,ui:Union[TinUI,BasicTinUI]):
        super().__init__(ui,'tinui-dark-theme')
        self.label='dark'
        self.ui['background']='#202020'
    
    def add_title(self,pos,*arg,**kw):
        return self.ui.add_title(pos,*arg,**{
            **{'fg':'#ffffff'},
            **kw})
    
    def add_paragraph(self,pos,*arg,**kw):
        return self.ui.add_paragraph(pos,*arg,**{
            **{'fg':'#ffffff'},
            **kw})

    def add_button(self,pos,*arg,**kw):
        return self.ui.add_button(pos,*arg,**{
            **{
                'fg':'#ffffff','bg':'#2d2d2d',
                'activefg':'#e8e8e8','activebg':'#323232',
                'line':'#303030','linew':1,'activeline':'#303030',
            },**kw})

    def add_checkbutton(self,pos,*arg,**kw):
        return self.ui.add_checkbutton(pos,*arg,**{
            **{
                'fontfg':'#ffffff','fg':'#989898','bg':'#1d1d1d',
                'activefg':'#9E9E9E','activebg':'#2a2a2a',
                'onfg':'black','onbg':'#4CC2FF',
            },**kw})

    def add_label(self,pos,*arg,**kw):
        return self.ui.add_label(pos,*arg,**{
            **{
                'fg':'#ffffff','bg':'#202020',
                'outline':'#202020',
            },**kw})

    def add_entry(self,pos,*arg,**kw):
        return self.ui.add_entry(pos,*arg,**{
            **{
                'fg':'#ffffff','bg':'#2d2d2d',
                'activefg':'#ffffff','activebg':'#323232',
                'onfg':'#ffffff','onbg':'#1f1f1f',
                'line':'#303030','activeline':'#303030',
                'outline':'#9a9a9a','onoutline':'#4CC2FF','insert':'#e0e0e0',
            },**kw})

    def add_separate(self,pos,*arg,**kw):
        return self.ui.add_separate(pos,*arg,**{
            **{
                'fg':'#323232',
            },**kw})

    def add_radiobutton(self,pos,*arg,**kw):
        return self.ui.add_radiobutton(pos,*arg,**{
            **{
                'fg':'#f2f2f2','bg':'#2b2b2b',
                'activefg':'#ffffff','activebg':'#373737',
            },**kw})

    def add_link(self,pos,*arg,**kw):
        return self.ui.add_link(pos,*arg,**{
            **{
                'fg':'#99EBFF',
                'activefg':'#99EBFF','activebg':'#2d2d2d',
            },**kw})

    def add_waitbar1(self,pos,*arg,**kw):
        # return self.ui.add_waitbar1(pos,*arg,**{
        #     **{
        #         'fg':'#b2b8f2','bg':'#202020','okfg':'#b2b8f2','bd':5,
        #     },**kw})
        ...

    def add_labelframe(self,uids:tuple,*arg,**kw):
        return self.ui.add_labelframe(uids,*arg,**{
            **{
                'fg':'#1D1D1D','bg':'#272727',
            },**kw})

    def add_waitbar2(self,pos,*arg,**kw):
        # return self.ui.add_waitbar2(pos,*arg,**{
        #     **{
        #         'fg':'#b2b8f2','bg':'#202020','okcolor':'#6ccb5f',
        #     },**kw})
        ...

    def add_combobox(self,pos,*arg,**kw):
        return self.ui.add_combobox(pos,*arg,**{
            **{
                'fg':'#cfcfcf','bg':'#2d2d2d','outline':'#303030',
                'activefg':'#ffffff','activebg':'#323232','activeline':'#303030',
                'onfg':'#cecece','onbg':'#272727','online':'#303030',
                'listfg':'#ffffff','listactivefg':'#ffffff','listactivebg':'#383838',
                'listonfg':'#D1D1D1','listonbg':'#343434','listsel':'#383838',
                'scrollbg':'#2c2c2c','scrollcolor':'#9f9f9f','scrollon':'#a0a0a0',
            },**kw})

    def add_progressbar(self,pos,*arg,**kw):
        return self.ui.add_progressbar(pos,*arg,**{
            **{
                'fg':'#9a9a9a','bg':'#4CC2FF','back':'#202020',
                'fontc':'#0000ff',
            },**kw})

    def add_table(self,pos,*arg,**kw):
        return self.ui.add_table(pos,*arg,**{
            **{
                'outline':'#9a9a9a','fg':'#ffffff','bg':'#2d2d2d',
                'headbg':'#202020',
            },**kw})

    def add_onoff(self,pos,*arg,**kw):
        return self.ui.add_onoff(pos,*arg,**{
            **{
                'fg':'#cccccc','bg':'#1d1d1d',
                'activefg':'#cfcfcf','activebg':'#2a2a2a',
                'onactivefg':'#000000','onactivebg':'#47B1E8',
                'onfg':'#000000','onbg':'#4CC2FF',
            },**kw})

    def add_spinbox(self,pos,*arg,**kw):
        return self.ui.add_spinbox(pos,**{
            **{
              'fg':'#ffffff','bg':'#2d2d2d','line':'#303030',
              'activefg':'#c0c0c0','activebg':'#323232',
              'boxfg':'#cfcfcf','boxbg':'#2c2c2c',
              'boxactivefg':'#d2d2d2','boxactivebg':'#383838',
              'onfg':'#9f9f9f','onbg':'#343434',
            },**kw})

    def add_image(self,pos,*arg,**kw):
        return self.ui.add_image(pos,*arg,**kw)

    def add_scalebar(self,pos,*arg,**kw):
        return self.ui.add_scalebar(pos,*arg,**{
            **{
                'fg':'#4CC2FF','bg':'#9a9a9a','activefg':'#4BB5EC',
                'buttonbg':'#454545','buttonoutline':'#353535',
            },**kw})

    def add_info(self,pos,*arg,**kw):
        # return self.ui.add_info(pos,*arg,**{
        #     **{
        #         'fg':'#b2b8f2','bg':'#2d2d2d','info_fg':'#ffffff',
        #     },**kw})
        ...

    def add_menubar(self,uid,*arg,**kw):
        return self.ui.add_menubar(uid,*arg,**{
            **{
                'fg':'#ffffff','bg':'#2c2c2c','line':'#3d3d3d',
                'activefg':'#ffffff','activebg':'#383838','activeline':'#383838',
                'onfg':'#ffffff','onbg':'#343434','online':'#343434',
            },**kw})

    def add_tooltip(self,uid,*arg,**kw):
        return self.ui.add_tooltip(uid,*arg,**{
            **{
                'fg':'#e8e8e8','bg':'#353535',
            },**kw})

    def add_waitbar3(self,pos,*arg,**kw):
        return self.ui.add_waitbar3(pos,*arg,**{
            **{
                'fg':'#4CC2FF','bg':'#202020','okcolor':'#4CC2FF',
            },**kw})

    def add_textbox(self,pos,*arg,**kw):
        return self.ui.add_textbox(pos,*arg,**{
            **{
                'fg':'#ffffff','bg':'#2d2d2d',
                'outline':'#9a9a9a','onoutline':'#4CC2FF',
                'scrollbg':'#2e2e2e','scrollcolor':'#9f9f9f','scrollon':'#a0a0a0',
            },**kw})

    def add_scrollbar(self,pos,widget,*arg,**kw):
        return self.ui.add_scrollbar(pos,widget,*arg,**{
            **{
                'bg':'#2e2e2e','color':'#9f9f9f','oncolor':'#a0a0a0',
            },**kw})

    def add_listbox(self,pos,*arg,**kw):
        return self.ui.add_listbox(pos,*arg,**{
            **{
                'bg':'#2b2b2b','fg':'white',
                'activefg':'#ffffff','activebg':'#373737',
                'onfg':'#ffffff','onbg':'#333333','sel':'#115990',
                'scrollbg':'#2e2e2e','scrollcolor':'#9f9f9f','scrollon':'#a0a0a0',
            },**kw})

    # def add_canvas(self,pos,*arg,**kw):
    #     return self.ui.add_canvas(pos,*arg,**{
    #         **{
    #             'outline':'#808080','linew':1,
    #             'scrollbg':'#2e2e2e','scrollcolor':'#9f9f9f','scrollon':'#a0a0a0',
    #         },**kw})
    
    def add_pipspager(self,pos,*arg,**kw):
        return self.ui.add_pipspager(pos,*arg,**{
            **{
                'bg':'#202020','fg':'#9a9a9a',
                'buttonfg':'#9f9f9f','buttonbg':'#2c2c2c',
                'activefg':'#cfcfcf','activebg':'#2c2c2c',
                'buttononfg':'#cfcfcf','buttononbg':'#2c2c2c',
            },**kw})

    def add_notebook(self,pos,*arg,**kw):
        return self.ui.add_notebook(pos,*arg,**{
            **{
                'color':'#202020','fg':'#cccccc','bg':'#202020',
                'activefg':'#cfcfcf','activebg':'#2d2d2d',
                'onfg':'#ffffff','onbg':'#282828',
                'scrollbg':'#2e2e2e','scrollcolor':'#9f9f9f','scrollon':'#a0a0a0',
            },**kw})

    def add_ratingbar(self,pos,*arg,**kw):
        return self.ui.add_ratingbar(pos,*arg,**{
            **{
                'fg':'#cccccc','bg':'#202020',
                'onfg':'#4CC2FF','onbg':'#4CC2FF',
            },**kw})

    def add_radiobox(self,pos,*arg,**kw):
        return self.ui.add_radiobox(pos,*arg,**{
            **{
                'fontfg':'#ffffff','fg':'#939393','bg':'#2a2a2a',
                'activefg':'#959595','activebg':'#2a2a2a',
                'onfg':'#4CC2FF','onbg':'#000000',
            },**kw})

    def add_notecard(self,pos,*arg,**kw):
        return self.ui.add_notecard(pos,*arg,**{
            **{
                'tfg':'#ffffff','tbg':'#2b2b2b','fg':'#ffffff',
                'bg':'#272727','sep':'#1d1d1d',
            },**kw})

    def add_pivot(self,pos,*arg,**kw):
        return self.ui.add_pivot(pos,*arg,**{
            **{
                'fg':'#a6a6a6','bg':'',
                'activefg':'#ffffff','activecolor':'#4CC2FF',
            },**kw})

    def add_button2(self,pos,*arg,**kw):
        return self.ui.add_button2(pos,*arg,**{
            **{
                'fg':'#ffffff','bg':'#2d2d2d',
                'activefg':'#ffffff','activebg':'#323232',
                'line':'#303030','linew':1,'activeline':'#202020',
                'onfg':'#cecece','onbg':'#272727','online':'#303030',
            },**kw})
    
    def add_accentbutton(self,pos,*arg,**kw):
        return self.ui.add_accentbutton(pos,*arg,**{
            **{
                'fg':'#000000','bg':'#4CC2FF',
                'activefg':'#000000','activebg':'#47B1E8',
                'line':'#5AC7FF','linew':1,'activeline':'#2B80CA',
                'onfg':'#215069','onbg':'#42A1D2','online':'#42A1D2',
            },**kw})
    
    def add_warningbutton(self,pos,*arg,**kw):
        return self.ui.add_warningbutton(pos,*arg,**{
            **{
                'fg':'#000000','bg':'#FF99A4',
                'activefg':'#000000','activebg':"#F57F90",
                'line':"#FC8290",'linew':1,'activeline':"#BD233A",
                'onfg':"#751F2C",'onbg':"#E96F81",'online':"#D83C5E",
            },**kw})
    
    def add_toolbutton(self,pos,*arg,**kw):
        return self.ui.add_toolbutton(pos,*arg,**{
            **{
                'fg':'#FFFFFF','bg':'#202020',
                'activefg':'#FFFFFF','activebg':'#2D2D2D',
                'line':'#202020','linew':1,'activeline':'#2D2D2D',
                'onfg':'#CECECE','onbg':'#292929','online':'#292929',
            },**kw})

    def add_expander(self,pos,*arg,**kw):
        return self.ui.add_expander(pos,*arg,**{
            **{
                'tfg':'#ffffff','tbg':'#2b2b2b',
                'bg':'#272727','sep':'#1d1d1d',
                'buttonfg':'#ffffff','buttonbg':'#2b2b2b','buttonline':'#2b2b2b',
                'activefg':'#ffffff','activebg':'#373737','activeline':'#373737',
                'onfg':'#ffffff','onbg':'#333333','online':'#333333',
            },**kw})

    def add_waitframe(self,pos,*arg,**kw):
        return self.ui.add_waitframe(pos,*arg,**{
            **{
                'fg':'#2d2d2d','bg':'#323232',
            },**kw})

    def add_listview(self,pos,*arg,**kw):
        return self.ui.add_listview(pos,*arg,**{
            **{
                'bg':'#202020','activebg':'#2d2d2d','oncolor':'#4CC2FF',
                'scrobg':'#2e2e2e','scroc':'#9a9a9a','scrooc':'#9f9f9f',
            },**kw})

    def add_treeview(self,pos,*arg,**kw):
        return self.ui.add_treeview(pos,*arg,**{
            **{
                'fg':'#ffffff','bg':'#202020',
                'onfg':'#ffffff','onbg':'#2d2d2d',
                'oncolor':'#4CC2FF','signcolor':'#9f9f9f',
            },**kw})

    def add_togglebutton(self,pos,*arg,**kw):
        return self.ui.add_togglebutton(pos,*arg,**{
            **{
                'fg':'#ffffff','bg':'#2d2d2d','line':"#303030",
                'activefg':'#000000','activebg':'#4CC2FF','activeline':'#5AC7FF',
            },**kw})
    
    def add_swipecontrol(self,pos,*arg,**kw):
        # return self.ui.add_swipecontrol(pos,*arg,**{
        #     **{
        #         'fg':'#ffffff','bg':'#202020','line':'#2d2d2d',
        #         'data':{'left':({'text':'✔️\nok','fg':'#000000','bg':'#a9a9a9','command':print},),
        #         'right':({'text':'❌\nclose'},)},
        #     },**kw})
        ...

    def add_picker(self,pos,*arg,**kw):
        return self.ui.add_picker(pos,*arg,**{
            **{
                'fg':'#cfcfcf','bg':'#2d2d2d','outline':'#3c3c3c',
                'activefg':'#ffffff','activebg':'#323232',
                'onfg':'#000000','onbg':'#4CC2FF',
                'buttonfg':'#ffffff','buttonbg':'#2d2d2d',
                'buttonactivefg':'#ffffff','buttonactivebg':'#383838',
                'buttononfg':'#ffffff','buttononbg':'#343434',
            },**kw})
    
    def add_menubutton(self,pos,*arg,**kw):
        return self.ui.add_menubutton(pos,*arg,**{
            **{
                'fg':"#ffffff",'bg':'#2d2d2d','line':'#3d3d3d',
                'activefg':'#ffffff','activebg':'#323232','activeline':'#202020',
                'onfg':'#cecece','onbg':'#272727','online':'#303030',
                'menuonfg':'#ffffff','menuonbg':'#383838','menuonline':'#383838',
            },**kw})
    
    def add_barbutton(self,pos,*arg,**kw):
        return self.ui.add_barbutton(pos,*arg,**{
            **{
                'fg':'#ffffff','bg':'#202020',
                'line':'#202020',
                'activefg':'#cecece','activebg':'#2d2d2d',
                'onfg':'#cecece','onbg':'#292929',
                'online':'#292929','sepcolor':'#e5e5e5',
            },**kw})

    def add_flyout(self,fid,*arg,**kw):
        return self.ui.add_flyout(fid,*arg,**{
            **{
                'line':'#b0b0b0','bg':'#2c2c2c',
            },**kw})

    def add_back(self,pos,*arg,**kw):
        return self.ui.add_back(pos,*arg,**{
            **{
                'fg':'#202020','bg':'#202020',
            },**kw})
    
    def add_breadcrumb(self,pos,*arg,**kw):
        return self.ui.add_breadcrumb(pos,*arg,**{
            **{
                'fg':'#ffffff','bg':'#202020','activefg':'#cccccc'
            },**kw})
    
    def add_segmentbutton(self,pos,*arg,**kw):
        return self.ui.add_segmentbutton(pos,*arg,**{
            **{
                'fg':'#FFFFFF','bg':'#1D1D1D',
                'activefg':'#FFFFFF','activebg':'#2A2A2A',
                'onbg':'#3A3A3A',
                'line':'#303030','sign':'#4CC2FF'
        },**kw})

    def add_navigation(self,pos,*arg,**kw):
        return self.ui.add_navigation(pos,*arg,**{
            **{
                'fg':'#FFFFFF','bg':'#202020',
                'activefg':'#FFFFFF','activebg':'#2C2C2C',
                'onfg':'#FFFFFF','onbg':'#2C2C2C','oncolor':'#4CC2FF'
            },**kw})
