import os.path as op
from tkinter import filedialog
from tkinter import (Tk, StringVar, IntVar, filedialog,
                     S, W, BOTH, X, LEFT, RIGHT, CENTER, SUNKEN,
                     Label, Entry, Button, Radiobutton, Frame)

from heudiconv.utils import get_known_heuristics_with_descriptions as heuristics

class MainApp(object):

    def __init__(self, master, title="HeuDiConv", window_size='250x500'):
        self.master = master
        master.title(title)
        master.geometry(window_size)
        # master.iconbitmap(/path/to/img) # to get rid of sketchy ? icon
        self.heuristics = list(heuristics().keys())
        self.mainWindow(master)

    def mainWindow(self, master):
        # GUI variables
        self.dcmdir = StringVar()
        self.heuristic = StringVar()
        self.process = IntVar(value=999) # valid values: 0, 1, 2
        self.builtins = IntVar(value=999) # valid values: 0 - len(self.heuristics)

        self.info = Label(master,
                          text="Heuristic DICOM Converter",
                          font=("Sytem", 11, "bold"))
        self.info.pack(anchor=CENTER, pady=10)

        self.label1 = Label(master, text="Step 1: DICOM directory path")
        self.label1.pack(anchor=W, pady=10)

        self.dcm_entry = Entry(master, textvariable=self.dcmdir)
        self.dcm_entry.pack(fill=BOTH)

        self.dir_button = Button(master, text="Browse", command=self.get_dcmdir)
        self.dir_button.pack(anchor=W)

        self.label2 = Label(master, text="Step 2: Conversion heuristic")
        self.label2.pack(anchor=W, pady=10)

        self.heuristic_entry = Entry(master, textvariable=self.heuristic)

        self.heuristic_entry.pack(fill=BOTH)

        self.use_new = Radiobutton(master,
                                   text="Generate new heuristic",
                                   variable=self.process,
                                   command=self._clear_frame,
                                   value=0)
        self.use_new.pack(anchor=W)

        self.use_custom = Radiobutton(master,
                                      text="Use custom heuristic",
                                      variable=self.process,
                                      command=self.get_heuristic,
                                      value=1)
        self.use_custom.pack(anchor=W)

        self.use_builtin = Radiobutton(master,
                                       text="Use builtin heuristic",
                                       variable=self.process,
                                       command=self.toggle_heuristics,
                                       value=2)
        self.use_builtin.pack(anchor=W)

        # frame to house built-in heuristics, hidden unless chosen
        self.frame = Frame(bd=1, relief=SUNKEN)

        self.builtin_heuristics = []
        for i, heuristic in enumerate(self.heuristics):
            self.builtin_heuristics.append(Radiobutton(self.frame,
                                                       text=heuristic,
                                                       variable=self.builtins,
                                                       value=i))
            self.builtin_heuristics[i].pack(anchor=W)

        self.run_button = Button(master,
                                 text="Run",
                                 command=self._run)
        self.close_button = Button(master, text="Exit", command=master.quit)
        self.fix_style()


    def get_dcmdir(self):
        self.dcmdir.set(filedialog.askdirectory())
        return


    def get_heuristic(self):
        self._clear_frame()
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
            self.frame.pack(anchor=CENTER, pady=10)
            self.fix_style()
        else:
            self.frame.pack_forget()
            self.builtins.set(None)
        return


    def fix_style(self):
        self.run_button.pack_forget()
        self.run_button.pack(side=LEFT, expand=True, fill=X, anchor=S)
        self.close_button.pack_forget()
        self.close_button.pack(side=RIGHT, expand=True, fill=X, anchor=S)
        return


    def _run(self):
        """Runs based on submission requests"""
        # debug
        # print(self.dcmdir_text.get(), self.process.get(), self.builtins.get())
        if not self.dcmdir.get():
            print("No DICOM directory specified")
            return

        if self.process.get() == 999:
            print("Heuristic option not specified")
            return

        if self.process.get() == 2 and self.builtins.get() == 999:
            print("Builtin heuristic not specified")
            return

        return


    def _clear_frame(self):
        self.frame.pack_forget()


def main():
    window = Tk()
    app = MainApp(window)
    window.mainloop()

if __name__ == '__main__':
    main()
