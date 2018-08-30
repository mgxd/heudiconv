#!/usr/bin/env python

import csv
import platform
import os.path as op
# TODO: remove unused
from tkinter import (Tk, StringVar, IntVar, filedialog, Canvas,
                     N, S, E, W, BOTH, X, LEFT, RIGHT, CENTER, SUNKEN, END, BOTTOM,
                     Label, Entry, Button, Radiobutton, Frame, Checkbutton, Scrollbar)

from heudiconv.gui.main import MainApp

MOUSEWHEEL = ["<MouseWheel>"]
if platform.system().lower().startswith("linux"):
    MOUSEWHEEL = ["<Button-4>", "<Button-5>"]


class HeuristicGenie(MainApp):

    def __init__(self,
                 master,
                 infofile,
                 title="HeuristicGenie",
                 window_size='500x500',
                 **kwargs):
        """Inherit from main GUI but increase size and add dicominfo property"""
        self.infofile = infofile
        self.dicominfo = self.read_infofile(self.infofile)
        super(HeuristicGenie, self).__init__(master, title, window_size, **kwargs)


    def mainWindow(self, master):
        self.gen_infoframe()

        self.close_button = Button(master, text="Exit", command=master.quit)
        self.close_button.pack()
        #self.label1.grid(row=1, column=1)

        # self.listbox = Listbox(self.infoframe)
        # self.listbox.pack(fill=BOTH)
        #
        # self.listbox.insert(END, self.dicominfo)


    def gen_infoframe(self):
        self.infoframe = Frame(self.master, bd=1, relief=SUNKEN, width=300, height=300)
        self.infoframe.pack()

        self.infocanvas = Canvas(self.infoframe, width=300, height=300, scrollregion=(0,0,500,500))

        self.bind_mousewheel()

        self.infoscrollx = Scrollbar(self.infoframe,
                                     orient='horizontal',
                                     command=self.infocanvas.xview)
        self.infoscrollx.pack(side='bottom', fill='x')

        self.infoscrolly = Scrollbar(self.infoframe,
                                     orient='vertical',
                                     command=self.infocanvas.yview)
        self.infoscrolly.pack(side='right', fill='y')

        self.infocanvas.configure(xscrollcommand=self.infoscrollx.set)
        self.infocanvas.configure(scrollregion=self.infocanvas.bbox("all"))

        self.series_choices = []
        # TODO: make scrollable
        row = 0
        for i, series in enumerate(self.dicominfo):
            col = 1
            if i >= 1:
                # add tick box
                self.series_choices.append(Checkbutton(self.infocanvas))
                self.series_choices[i-1].grid(row=row, column=col-1)

            for val in series:
                label = Label(self.infocanvas, text=val)
                label.grid(row=row, column=col)
                col += 1
            row += 1

        # pack after everything
        self.infocanvas.pack(side='left', expand=True)

    def bind_mousewheel(self):
        for but in MOUSEWHEEL:
            self.master.bind_all(but,
                                 lambda event: self.infocanvas.xview_scroll(int(-1 * event.delta/200), "units"))

    def read_infofile(self, infofile):
        if not infofile or not op.exists(infofile):
            return None
        with open(infofile, 'rt') as fp:
            reader = csv.reader(fp, delimiter='\t')
            return [series for series in reader]

def main():
    infofile = '/code/scratch/test/voice2/.heudiconv/voice969/info/dicominfo.tsv'
    window = Tk()
    app = HeuristicGenie(window, infofile)
    window.mainloop()


if __name__ == '__main__':
    main()
