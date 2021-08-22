import sys
sys.path.append('..')
from TinUI import TinUI

from tkinter import Tk

class win:
    def __init__(self):
        self.r=Tk()
        self.r.geometry('500x500+10+10')
        self.u=TinUI(self.r)
        self.u.pack(fill='both',expand=True)
    def go(self):
        self.r.mainloop()
if __name__=='__main__':
    win()
