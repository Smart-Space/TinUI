"""
TinUI拓展功能包
"""

Extension='TinUI'


def buttonlize(tinui,uid,bg='#fbfbfb',line='#CCCCCC',activebg='#f5f5f5',activeline='#e5e5e5',command=None):#按钮化tinui控件
    def in_button(e):
        tinui.itemconfig(outline,outline=activeline,fill=activeline)
    def out_button(e):
        tinui.itemconfig(back,fill=bg,outline=bg)
        tinui.itemconfig(outline,outline=line,fill=line)
    def on_click(e):
        tinui.itemconfig(back,fill=activebg,outline=activebg)
        tinui.after(500,lambda : out_button(None))
        if command:
            command()

    x1,y1,x2,y2=tinui.bbox(uid)
    x1+=1
    y1+=1
    x2-=1
    y2-=1
    outlinepos=(x1,y1,x2,y1,x2,y2,x1,y2)
    nameid=uid+'-buttonlize'
    outline=tinui.create_polygon(outlinepos,width=9,fill=line,outline=line,tags=nameid)
    back=tinui.create_polygon(outlinepos,width=7,fill=bg,outline=bg,tags=nameid)
    tinui.lower(nameid,uid)

    tinui.tag_bind(nameid,'<Button-1>',on_click)
    tinui.tag_bind(nameid,'<Enter>',in_button)
    tinui.tag_bind(nameid,'<Leave>',out_button)
    tinui.tag_bind(uid,'<Button-1>',on_click)
    tinui.tag_bind(uid,'<Enter>',in_button)
    tinui.tag_bind(uid,'<Leave>',out_button)
