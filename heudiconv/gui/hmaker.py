#!/usr/bin/env python

from heudiconv.gui.main import MainApp
from tkinter import (Tk, StringVar, IntVar, filedialog,
                     S, W, BOTH, X, LEFT, RIGHT, CENTER, SUNKEN,
                     Label, Entry, Button, Radiobutton, Frame, Toplevel)

class HeuristicGenie(MainApp):

    def __init__(self,
                 master,
                 dicominfo,
                 title="HeuristicGenie",
                 window_size='500x500',
                 **kwargs):
        """Inherit from main GUI but increase size"""
        self.dicominfo = dicominfo
        super(HeuristicGenie, self).__init__(master, title, window_size, **kwargs)

    def mainWindow(self, master):
        print("My info shows me a", self.dicominfo)
        self.close_button = Button(master, text="Exit", command=master.quit)
        self.close_button.pack()

        #
