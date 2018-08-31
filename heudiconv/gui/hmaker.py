#!/usr/bin/env python

import csv
import platform
import os.path as op
# TODO: remove unused
from tkinter import (Tk, StringVar, IntVar, filedialog, Canvas, Label,
                     Entry, Button, Radiobutton, Frame, Checkbutton, Scrollbar)

from heudiconv.gui.main import MainApp

MOUSEWHEEL = ["<MouseWheel>"]
if platform.system().lower().startswith("linux"):
    MOUSEWHEEL = ["<Button-4>", "<Button-5>"]

class InfoButton(Checkbutton, object):
    """Checkbutton with IntVar variable attached"""
    def __init__(self, var=0, **kwargs):
        self.val= IntVar(value=var)
        super(InfoButton, self).__init__(variable=self.val, **kwargs)


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
        self.target_series = []
        super(HeuristicGenie, self).__init__(master, title, window_size, **kwargs)


    def mainWindow(self, master):
        self.gen_infoframe()

        self.select_button = Button(master,
                                    text="Generate Heuristic",
                                    command=self._create_heuristic)
        self.select_button.pack(side='left', expand=True, fill='x', anchor='s')
        self.close_button = Button(master, text="Exit", command=master.quit)
        self.close_button.pack(side='right', expand=True, fill='x', anchor='s')


    def gen_infoframe(self):
        self.canvasframe = Frame(self.master,
                                 bd=1,
                                 relief='sunken')
        self.canvasframe.pack()

        # TODO: adjust dynamically based on input
        infocanvas = Canvas(self.canvasframe,
                            width=450,
                            height=450,
                            scrollregion=(0,0,2300,2300))
        self.bind_mousewheel(infocanvas)

        scrollx = Scrollbar(self.canvasframe,
                            orient='horizontal',
                            command=infocanvas.xview)
        scrollx.pack(side='bottom', fill='x')


        scrolly = Scrollbar(self.canvasframe,
                            orient='vertical',
                            command=infocanvas.yview)
        scrolly.pack(side='right', fill='y')

        infocanvas.configure(xscrollcommand=scrollx.set,
                             yscrollcommand=scrolly.set,
                             scrollregion=infocanvas.bbox("all"))
        infocanvas.pack(side='left', expand=True, fill='both')

        infoframe = Frame(infocanvas)
        infoframe.pack()
        infocanvas.create_window((0, 0), window=infoframe, anchor='n')

        # TODO: make scrollable
        self.series_choices = []
        row = 0
        for i, series in enumerate(self.dicominfo):
            col = 1
            if i >= 1:
                # add tick box
                self.series_choices.append(InfoButton(master=infoframe))
                self.series_choices[i-1].grid(row=row, column=col-1)

            for val in series:
                label = Label(infoframe, text=val)
                label.grid(row=row, column=col)
                col += 2
            row += 1

        # pack after everything
        # self.infocanvas.pack(side='left', expand=True, fill=BOTH)

    def bind_mousewheel(self, canvas):
        for but in MOUSEWHEEL:
            self.master.bind_all(but,
                                 lambda event: canvas.yview_scroll(int(-1 * event.delta/200), "units"))


    def read_infofile(self, infofile):
        if not infofile or not op.exists(infofile):
            return None
        with open(infofile, 'rt') as fp:
            reader = csv.reader(fp, delimiter='\t')
            return [series for series in reader]


    def _create_heuristic(self):
        for i, opt in enumerate(self.series_choices):
            if opt.val.get() == 1:
                self.target_series.append(self.dicominfo[i+1])  # first is column names

        for s in self.target_series:
            print(s[2])

        self.master.quit()

def main():
    infofile = '/code/scratch/test/voice2/.heudiconv/voice969/info/dicominfo.tsv'
    window = Tk()
    app = HeuristicGenie(window, infofile)
    window.mainloop()


if __name__ == '__main__':
    main()
