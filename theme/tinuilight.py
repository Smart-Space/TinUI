from typing import Union
from tinui import TinUI, BasicTinUI, TinUITheme

class TinUILight(TinUITheme):
    '''
    这是TinUI明亮模式的托管类，不是继承类
    调用时这需要注意文本和数据，样式类参数无需理会
    '''

    def __init__(self,ui:Union[TinUI,BasicTinUI]):
        super().__init__(ui,'tinui-light-theme')
        self.label='light'
        self.ui['background']='#f3f3f3'
    
    def add_title(self,pos,*arg,**kw):
        return self.ui.add_title(pos,*arg,**{
            **{'fg':'#000000'},**kw})

    def add_paragraph(self,pos,*arg,**kw):
        return self.ui.add_paragraph(pos,*arg,**{
            **{'fg':'#000000'},**kw})

    def add_button(self,pos,*arg,**kw):
        return self.ui.add_button(pos,*arg,**{
            **{
                'fg':'#1b1b1b','bg':'#fbfbfb',
                'activefg':'#1a1a1a','activebg':'#f6f6f6',
                'line':'#cccccc','linew':1,'activeline':'#cccccc'
            },**kw})

    def add_checkbutton(self,pos,*arg,**kw):
        return self.ui.add_checkbutton(pos,*arg,**{
            **{
                'fontfg':'#1a1a1a','fg':'#868686','bg':'#ededed',
                'activefg':'#868686','activebg':'#e5e5e5',
                'onfg':'white','onbg':'#0067C0'
            },**kw})

    def add_label(self,pos,*arg,**kw):
        return self.ui.add_label(pos,*arg,**{
            **{
                'fg':'#1a1a1a','bg':'#f3f3f3',
                'outline':'#f3f3f3'
            },**kw})

    def add_entry(self,pos,*arg,**kw):
        return self.ui.add_entry(pos,*arg,**{
            **{
                'fg':'#1b1b1b','bg':'#fbfbfb',
                'activefg':'#1a1a1a','activebg':'#f6f6f6',
                'onfg':'#000000','onbg':'#ffffff',
                'line':'#e5e5e5','activeline':'#e5e5e5',
                'outline':'#868686','onoutline':'#0067C0','insert':'#000000'
            },**kw})

    def add_separate(self,pos,*arg,**kw):
        return self.ui.add_separate(pos,*arg,**{
            **{'fg':'#e5e5e5'},**kw})


    def add_radiobutton(self,pos,*arg,**kw):
        return self.ui.add_radiobutton(pos,*arg,**{
            **{
                'fg':'#1a1a1a','bg':'#f2f2f2',
                'activefg':'#191919','activebg':'#e9e9e9',
            },**kw})

    def add_link(self,pos,*arg,**kw):
        return self.ui.add_link(pos,*arg,**{
            **{
                'fg':'#003E92',
                'activefg':'#001A68','activebg':'#eaeaea',
            },**kw})

    def add_waitbar1(self,pos,*arg,**kw):
        # return self.ui.add_waitbar1(pos,*arg,**{
        #     **{
        #         'fg':'#3041d8',
        #         'bg':'#f3f3f3',
        #         'okfg':'#3041d8',
        #         'bd':5
        #     },**kw})
        ...

    def add_labelframe(self,uids:tuple,*arg,**kw):
        return self.ui.add_labelframe(uids,*arg,**{
            **{
                'fg':'#E5E5E5','bg':'#f4f4f4',
            },**kw})

    def add_waitbar2(self,pos,*arg,**kw):
        # return self.ui.add_waitbar2(pos,*arg,**{
        #     **{
        #         'fg':'#3041d8','bg':'#f3f3f3','okcolor':'#0f7b0f',
        #     },**kw})
        ...

    def add_combobox(self,pos,*arg,**kw):
        return self.ui.add_combobox(pos,*arg,**{
            **{
                'fg':'#1a1a1a','bg':'#fbfbfb',
                'outline':'#c8c8c8',
                'activefg':'#1a1a1a','activebg':'#f6f6f6',
                'activeline':'#cccccc',
                'onfg':'#5d5d5d','onbg':'#f5f5f5','online':'#e5e5e5',
                'listfg':'#1a1a1a','listactivefg':'#191919','listactivebg':'#F0F0F0',
                'listonfg':'#5C5C5C','listonbg':'#F3F3F3','listsel':'#F0F0F0',
                'scrollbg':'#f9f9f9','scrollcolor':'#999999','scrollon':'#89898b',
            },**kw})

    def add_progressbar(self,pos,*arg,**kw):
        return self.ui.add_progressbar(pos,*arg,**{
            **{
                'fg':'#868686','bg':'#0067C0','back':'#f3f3f3',
                'fontc':'#79b8f8',
            },**kw})

    def add_table(self,pos,*arg,**kw):
        return self.ui.add_table(pos,*arg,**{
            **{
                'outline':'#dadad8','fg':'black','bg':'white',
                'headbg':'#f4f4f2',
            },**kw})

    def add_onoff(self,pos,*arg,**kw):
        return self.ui.add_onoff(pos,*arg,**{
            **{
                'fg':'#5a5a5a','bg':'#ededed',
                'activefg':'#575757','activebg':'#e5e5e5',
                'onactivefg':'#ffffff','onactivebg':'#1975c5',
                'onfg':'#FFFFFF','onbg':'#0067c0',
            },**kw})

    def add_spinbox(self,pos,*arg,**kw):
        return self.ui.add_spinbox(pos,*arg,**{
            **{
                'fg':'#1b1b1b','bg':'#fefefe','line':'#e5e5e5',
                'activefg':'#1a1a1a','activebg':'#fafafa',
                'onfg':'#868686','onbg':'#f3f3f3',
                'boxfg':'#5f5f5f','boxbg':'#f9f9f9',
                'boxactivefg':'#5b5b5b','boxactivebg':'#f0f0f0',
            },**kw})

    def add_image(self,pos,*arg,**kw):
        return self.ui.add_image(pos,*arg,**kw)

    def add_scalebar(self,pos,*arg,**kw):
        return self.ui.add_scalebar(pos,*arg,**{
            **{
                'fg':'#0067C0','bg':'#868686','activefg':'#1A76C6',
                'buttonbg':'#ffffff','buttonoutline':'#cccccc',
            },**kw})

    def add_info(self,pos,*arg,**kw):
        # return self.ui.add_info(pos,*arg,**{
        #     **{
        #         'fg':'#0078d4','bg':'#f9f9f9','info_fg':'#1a1a1a',
        #     },**kw})
        ...
    
    def add_menubar(self,uid,*arg,**kw):
        return self.ui.add_menubar(uid,*arg,**{
            **{
                'fg':'#1a1a1a','bg':'#f9f9f9','line':'#dfdfdf',
                'activefg':'#191919','activebg':'#f0f0f0','activeline':'#f0f0f0',
                'onfg':'#191919','onbg':'#f3f3f3','online':'#f3f3f3',
            },**kw})

    def add_tooltip(self,uid,*arg,**kw):
        return self.ui.add_tooltip(uid,*arg,**{
            **{
                'fg':'#1a1a1a','bg':'#efefef',
            },**kw})

    def add_waitbar3(self,pos,*arg,**kw):
        return self.ui.add_waitbar3(pos,*arg,**{
            **{
                'fg':'#0067C0','bg':'#f3f3f3','okcolor':'#0067C0',
            },**kw})

    def add_textbox(self,pos,*arg,**kw):
        return self.ui.add_textbox(pos,*arg,**{
            **{
                'fg':'#1a1a1a','bg':'white',
                'outline':'#868686','onoutline':'#0067C0',
                'scrollbg':'#f9f9f9','scrollcolor':'#8d8d8d','scrollon':'#8a8a8a',
            },**kw})

    def add_scrollbar(self,pos,widget,*arg,**kw):
        return self.ui.add_scrollbar(pos,widget,*arg,**{
            **{
                'bg':'#f9f9f9','color':'#8d8d8d',
                'oncolor':'#8a8a8a',
            },**kw})

    def add_listbox(self,pos,*arg,**kw):
        return self.ui.add_listbox(pos,*arg,**{
            **{
                'fg':'#1a1a1a','bg':'#f2f2f2',
                'activefg':'#191919','activebg':'#e9e9e9',
                'onfg':'#191919','onbg':'#ececec','sel':'#91C1E6',
                'scrollbg':'#f9f9f9','scrollcolor':'#8d8d8d','scrollon':'#8a8a8a',
            },**kw})

    # def add_canvas(self,pos,*arg,**kw):
    #     return self.ui.add_canvas(pos,*arg,**{
    #         **{
    #             'outline':'#808080','linew':1,
    #             'scrollbg':'#f9f9f9','scrollcolor':'#8d8d8d','scrollon':'#8a8a8a',
    #         },**kw})

    def add_pipspager(self,pos,*arg,**kw):
        return self.ui.add_pipspager(pos,*arg,**{
            **{
                'bg':'#f3f3f3','fg':'#868686',
                'buttonfg':'#8a8a8a','buttonbg':'#f9f9f9',
                'activefg':'#5f5f5f','activebg':'#f9f9f9',
                'buttononfg':'#5f5f5f','buttononbg':'#f9f9f9',
            },**kw})

    def add_notebook(self,pos,*arg,**kw):
        return self.ui.add_notebook(pos,*arg,**{
            **{
                'color':'#f3f3f3','fg':'#5d5d5d','bg':'#f3f3f3',
                'activefg':'#595959','activebg':'#eaeaea',
                'onfg':'#1a1a1a','onbg':'#f9f9f9',
                'scrollbg':'#f9f9f9','scrollcolor':'#8d8d8d','scrollon':'#8a8a8a',
            },**kw})
    
    def add_ratingbar(self,pos,*arg,**kw):
        return self.ui.add_ratingbar(pos,*arg,**{
            **{
                'fg':'#5d5d5d','bg':'#f3f3f3',
                'onfg':'#0067C0','onbg':'#0067C0',
            },**kw})

    def add_radiobox(self,pos,*arg,**kw):
        return self.ui.add_radiobox(pos,*arg,**{
            **{
                'fontfg':'black','fg':'#8b8b8b','bg':'#ededed',
                'activefg':'#898989','activebg':'#e5e5e5',
                'onfg':'#0067C0','onbg':'#ffffff',
            },**kw})

    def add_notecard(self,pos,*arg,**kw):
        return self.ui.add_notecard(pos,*arg,**{
            **{
                'tfg':'#1b1b1b','tbg':'#fbfbfb','fg':'#1a1a1a',
                'bg':'#f4f4f4','sep':'#e5e5e5',
            },**kw})

    def add_pivot(self,pos,*arg,**kw):
        return self.ui.add_pivot(pos,*arg,**{
            **{
                'fg':'#616161','bg':'',
                'activefg':'#000000','activecolor':'#0067C0',
            },**kw})

    def add_button2(self,pos,*arg,**kw):
        return self.ui.add_button2(pos,*arg,**{
            **{
                'fg':'#1b1b1b','bg':'#fbfbfb',
                'activefg':'#1a1a1a','activebg':'#f6f6f6',
                'line':'#cccccc','linew':1,'activeline':'#cccccc',
                'onfg':'#5d5d5d','onbg':'#f5f5f5','online':'#e5e5e5',
            },**kw})
    
    def add_accentbutton(self,pos,*arg,**kw):
        return self.ui.add_accentbutton(pos,*arg,**{
            **{
                'fg':'#FFFFFF','bg':'#0067C0',
                'activefg':'#FFFFFF','activebg':'#1975C5',
                'line':'#1473C5','linew':1,'activeline':'#2B80CA',
                'onfg':'#C2DAEF','onbg':'#3183CA','online':'#3183CA',
            },**kw})
    
    def add_toolbutton(self,pos,*arg,**kw):
        return self.ui.add_toolbutton(pos,*arg,**{
            **{
                'fg':'#1A1A1A','bg':'#F3F3F3',
                'activefg':'#191919','activebg':'#EAEAEA',
                'line':'#F3F3F3','linew':1,'activeline':'#EAEAEA',
                'onfg':'#5A5A5A','onbg':'#EDEDED','online':'#EDEDED',
            },**kw})

    def add_expander(self,pos,*arg,**kw):
        return self.ui.add_expander(pos,*arg,**{
            **{
                'tfg':'#1b1b1b','tbg':'#fbfbfb',
                'bg':'#f4f4f4','sep':'#e5e5e5',
                'buttonfg':'#1b1b1b','buttonbg':'#fbfbfb','buttonline':'#fbfbfb',
                'activefg':'#1a1a1a','activebg':'#f2f2f2','activeline':'#f2f2f2',
                'onfg':'#1a1a1a','onbg':'#f5f5f5','online':'#f5f5f5',
            },**kw})

    def add_waitframe(self,pos,*arg,**kw):
        return self.ui.add_waitframe(pos,*arg,**{
            **{
                'fg':'#fbfbfb','bg':'#f6f6f6',
            },**kw})

    def add_listview(self,pos,*arg,**kw):
        return self.ui.add_listview(pos,*arg,**{
            **{
                'bg':'#f3f3f3','activebg':'#eaeaea','oncolor':'#0067C0',
                'scrobg':'#f8f8f8','scroc':'#868686','scrooc':'#898989',
            },**kw})

    def add_treeview(self,pos,*arg,**kw):
        return self.ui.add_treeview(pos,*arg,**{
            **{
                'fg':'#1a1a1a','bg':'#f3f3f3',
                'onfg':'#1a1a1a','onbg':'#eaeaea',
                'oncolor':'#0067C0','signcolor':'#8a8a8a',
            },**kw})

    def add_togglebutton(self,pos,*arg,**kw):
        return self.ui.add_togglebutton(pos,*arg,**{
            **{
                'fg':'#1b1b1b','bg':'#fbfbfb','line':'#cccccc',
                'activefg':'#f3f4fd','activebg':'#0067C0','activeline':'#2B80CA',
            },**kw})
    
    def add_swipecontrol(self,pos,*arg,**kw):
        # return self.ui.add_swipecontrol(pos,*arg,**{
        #     **{
        #         'fg':'#1a1a1a','bg':'#f3f3f3','line':'#fbfbfb',
        #         'data':{'left':({'text':'✔️\nok','fg':'#202020','bg':'#bcbcbc','command':print},),
        #         'right':({'text':'❌\nclose'},)},
        #     },**kw})
        ...
    
    def add_picker(self,pos,*arg,**kw):
        return self.ui.add_picker(pos,*arg,**{
            **{
                'fg':'#1b1b1b','bg':'#fbfbfb',
                'outline':'#ececec','activefg':'#1b1b1b',
                'activebg':'#f6f6f6','onfg':'#eaecfb','onbg':'#0067C0',
                'buttonfg':'#1a1a1a','buttonbg':'#fbfbfb',
                'buttonactivefg':'#1a1a1a','buttonactivebg':'#f0f0f0',
                'buttononfg':'#1a1a1a','buttononbg':'#f3f3f3',
            },**kw})
    
    def add_menubutton(self,pos,*arg,**kw):
        return self.ui.add_menubutton(pos,*arg,**{
            **{
                'fg':'#1b1b1b','bg':'#fbfbfb','line':'#CCCCCC',
                'activefg':'#1a1a1a','activebg':'#f6f6f6','activeline':'#cccccc',
                'onfg':'#5d5d5d','onbg':'#f5f5f5','online':'#e5e5e5',
                'menuonfg':'#191919','menuonbg':'#f0f0f0','menuonline':'#f0f0f0',
            },**kw})
    
    def add_barbutton(self,pos,*arg,**kw):
        return self.ui.add_barbutton(pos,*arg,**{
            **{
                'fg':'#636363','bg':'#f3f3f3','line':'#f3f3f3',
                'activefg':'#191919','activebg':'#eaeaea','activeline':'#eaeaea',
                'onfg':'#5a5a5a','onbg':'#ededed','online':'#ededed','sepcolor':'#e5e5e5',
            },**kw})

    def add_flyout(self,fid,*arg,**kw):
        return self.ui.add_flyout(fid,*arg,**{
            **{
                'line':'#dcdcdc','bg':'#f9f9f9',
            },**kw})
    
    def add_back(self,pos,*arg,**kw):
        return self.ui.add_back(pos,*arg,**{
            **{
                'fg':'#f3f3f3','bg':'#f3f3f3',
            },**kw})
    
    def add_breadcrumb(self,pos,*arg,**kw):
        return self.ui.add_breadcrumb(pos,*arg,**{
            **{
                'fg':'#1a1a1a','bg':'#f3f3f3','activefg':'#5c5c5c'
            },**kw})
    
    def add_segmentbutton(self,pos,*arg,**kw):
        return self.ui.add_segmentbutton(pos,*arg,**{
            **{
                'fg':'#191919','bg':'#EDEDED',
                'activefg':'#181818','activebg':'#E5E5E5',
                'onbg':'#FAFAFA',
                'line':'#E5E5E5','sign':'#0067C0'
        },**kw})

    def add_navigation(self,pos,*arg,**kw):
        return self.ui.add_navigation(pos,*arg,**{
            **{
                'fg':'#1A1A1A','bg':'#F3F3F3',
                'activefg':'#191919','activebg':'#E9E9E9',
                'onfg':'#191919','onbg':'#E9E9E9','oncolor':'#0067C0'
            },**kw})
