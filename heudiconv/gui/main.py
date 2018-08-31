#!/usr/bin/env python

import os
import os.path as op
from functools import partial
from tkinter import (Tk, StringVar, IntVar, filedialog, Label,
                     Entry, Button, Radiobutton, Frame, Checkbutton)

from heudiconv.utils import get_known_heuristics_with_descriptions as heuristics

class MainApp(object):

    def __init__(self, master, title="HeuDiConv", window_size='250x700', **kwargs):
        self.master = master
        master.title(title)
        master.geometry(window_size)
        # master.iconbitmap(/path/to/img) # to get rid of sketchy ? icon
        self.mainWindow(master)

    def mainWindow(self, master):
        # GUI variables
        # TODO: outdir + bids + minmeta
        self.heuristics = list(heuristics().keys())
        self.dcmdir = StringVar(value=os.getcwd())
        self.heuristic = StringVar()
        self.process = IntVar(value=999) # valid values: 0, 1, 2
        self.builtins = IntVar(value=999) # valid values: 0 - len(self.heuristics)
        self.outdir = StringVar(value=os.getcwd())
        self.bids = IntVar()
        self.minmeta = IntVar()

        self.info = Label(master,
                          text="Heuristic DICOM Converter",
                          font=("Sytem", 11, "bold"))
        self.info.pack(anchor='center', pady=10)

        self.label1 = Label(master, text="Step 1: DICOM directory path")
        self.label1.pack(anchor='w', pady=10)

        self.dcm_entry = Entry(master, textvariable=self.dcmdir)
        self.dcm_entry.pack(fill='both')

        self.dir_button = Button(master,
                                 text="Browse",
                                 command=partial(self.set_dir, self.dcmdir))
        self.dir_button.pack(anchor='w')

        self.label2 = Label(master, text="Step 2: Conversion heuristic")
        self.label2.pack(anchor='w', pady=10)

        self.heuristic_entry = Entry(master, textvariable=self.heuristic)
        self.heuristic_entry.pack(fill='both')

        self.use_new = Radiobutton(master,
                                   text="Generate new heuristic",
                                   variable=self.process,
                                   command=self._clear_builtins,
                                   value=0)
        self.use_new.pack(anchor='w')

        self.use_custom = Radiobutton(master,
                                      text="Use custom heuristic",
                                      variable=self.process,
                                      command=self.get_heuristic,
                                      value=1)
        self.use_custom.pack(anchor='w')

        self.use_builtin = Radiobutton(master,
                                       text="Use builtin heuristic",
                                       variable=self.process,
                                       command=self.toggle_heuristics,
                                       value=2)
        self.use_builtin.pack(anchor='w')

        # frame to house built-in heuristics, hidden unless chosen
        self.frame = Frame(bd=1, relief='sunken')

        self.builtin_heuristics = []
        for i, heuristic in enumerate(self.heuristics):
            self.builtin_heuristics.append(Radiobutton(self.frame,
                                                       text=heuristic,
                                                       variable=self.builtins,
                                                       value=i))
            self.builtin_heuristics[i].pack(anchor='w')


        self.frame_bot = Frame()
        self.frame_bot.pack(fill='both')

        self.label3 = Label(self.frame_bot, text="Step 3: Output directory (CWD)")
        self.label3.pack(anchor='w', pady=10)

        self.outdir_entry = Entry(self.frame_bot, textvariable=self.outdir)
        self.outdir_entry.pack(fill='both')

        self.outdir_button = Button(self.frame_bot,
                                    text="Change",
                                    command=partial(self.set_dir, self.outdir))
        self.outdir_button.pack(anchor='w')

        self.label4 = Label(self.frame_bot, text="Step 4: Additional options")
        self.label4.pack(anchor=W, pady=10)

        # bids, minmeta
        self.bids_button = Checkbutton(self.frame_bot,
                                       text="BIDS conversion",
                                       variable=self.bids)
        self.bids_button.pack(anchor='w')

        self.minmeta_button = Checkbutton(self.frame_bot,
                                          text="Condense DICOM metadata",
                                          variable=self.minmeta)
        self.minmeta_button.pack(anchor='w')

        self.run_button = Button(master,
                                 text="Run",
                                 command=self._run)
        self.close_button = Button(master, text="Exit", command=master.quit)
        self.fix_style()


    def set_dir(self, obj):
        obj.set(filedialog.askdirectory())
        return


    def get_heuristic(self):
        self._clear_builtins()
        self.heuristic.set(filedialog.askdirectory())
        return


    def toggle_heuristics(self):
        """Displays or hides frame with built-in heuristics"""
        displayed = True
        try:
            status = self.frame.pack_info()
        except:
            displayed = False

        if not displayed:
            self.frame.pack(anchor='center', pady=10)
            self.fix_style()

        else:
            self.frame.pack_forget()
            self.builtins.set(999)
        return


    def fix_style(self):
        if getattr(self, "frame_bot", None):
            self.frame_bot.pack_forget()
            self.frame_bot.pack(fill=BOTH)
        if (getattr(self, "run_button", None) and
                getattr(self, "close_button", None)):
            self.run_button.pack_forget()
            self.run_button.pack(side=LEFT, expand=True, fill=X, anchor=S)
            self.close_button.pack_forget()
            self.close_button.pack(side=RIGHT, expand=True, fill=X, anchor=S)
        return


    def _run(self):
        """Runs based on submission requests"""
        # catch some run errors
        converter = "dcm2niix"
        self._dcmdir = self.dcmdir.get()
        self._process = self.process.get()
        self._builtins = self.builtins.get()
        self._heuristic = self.heuristic.get()
        self._outdir = self.outdir.get()

        if not self._dcmdir:
            print("No DICOM directory specified")
            return
        elif not op.exists(self._dcmdir):
            print("DICOM directory not found")
            return
        elif self._process == 999:
            print("Heuristic option not specified")
            return
        elif self._process == 1 and not op.exists(self._heuristic):
            print("Heuristic not found")
            return
        elif self._process == 2 and self._builtins == 999:
            return

        # search for files
        self._files = self.search_files(self._dcmdir)
        if not self._files:
            print("No files found")
            return
        else:
            print("Number of files found: %d" % len(self._files))

        # generate heuristic
        if self._process == 0:
            converter = "none"
            self._heuristic = 'convertall'

        elif self._process == 2:
            if self._builtins == 999:
                print("Builtin heuristic not specified")
                return
            self._heuristic = self.heuristics[self._builtins]

        from heudiconv.cli.run import main as runner
        # TODO: add additional arguments
        args = (['--files'] + self._files +
                ['-c', converter,
                 '-f', self._heuristic,
                 '-o', self._outdir])

        if self.bids.get() == 1:
            args.append('-b')

        if self.minmeta.get() == 1:
            args.append('--minmeta')

        # print(' '.join(args))
        runner(args)

        # TODO: if generating heuristic, run again with newly created H
        if convert == "none":
            from heudiconv.gui.hmaker import HeuristicGenie
            hwindow = Tk()
            dicominfo = 2  # replace with dicominfo.tsv
            happ = HeuristicGenie(hwindow, dicominfo) # extract output heuristic from this
            hwindow.mainloop()

        self.master.quit()


    def search_files(self, dirpath):
        """Finds files in a given path

        TODO: add option for further search depth
        """
        return next(os.walk(dirpath))[2]


    def _clear_builtins(self):
        if getattr(self, 'frame'):
            self.frame.pack_forget()
        return


def main():
    window = Tk()
    app = MainApp(window)
    window.mainloop()

if __name__ == '__main__':
    main()
