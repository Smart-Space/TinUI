from window import win


def f(e):
    print('go')

a=win()
xml = a.uixml
xml.funcs['test']=print
xml.loadxml(
'''
<!--TinUIXml编辑-->
<tinui>
<line>
<button text='outside' command='self.funcs["test"]'></button>
    <ui>ui
        <button text='button' command='self.funcs["test"]'></button>
        <button2 text='button2'></button2>
        <line>
            <label text='line1'></label>
        </line>
        <line>
            <label text='line2'></label>
        </line>
    </ui>
</line>
</tinui>

'''
)
xml.tags['ui'][-2].funcs['test']=f


a.go()
