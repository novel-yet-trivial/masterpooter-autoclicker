#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Documentation is like sex.
#   When it's good, it's very good.
#   When it's bad, it's better than nothing.
#   When it lies to you, it may be a while before you realize something's wrong.
#
#   from: https://www.reddit.com/r/linuxmint/comments/5mgde1/does_anyone_know_of_an_autoclicker_with_hotkeys/
#   Reddit user: masterpooter
#

# before running this program, run:
# $ sudo apt-get install -y python-xlib python-tk


from Xlib.display import Display
from Xlib import X, XK
from Xlib.ext.xtest import fake_input
import Tkinter as tk
import random
import os
import time


_display = Display(os.environ['DISPLAY'])
def click():
    fake_input(_display, X.ButtonPress, 1)
    #_display.sync()
    #time.sleep(0.25)
    fake_input(_display, X.ButtonRelease, 1)
    _display.sync()

START = "Start"
STOP = "Stop"
class GUI(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.pos = None
        self.last = 0


        lbl = tk.Label(self, text="Delay")
        lbl.grid(row=0, column=0, sticky='w')
        self.delay = tk.IntVar(self, 2000)
        ent = tk.Entry(self, textvariable=self.delay, width=8)
        ent.grid(row=0, column=1)

        lbl = tk.Label(self, text="Interval")
        lbl.grid(row=1, column=0, sticky='w')
        self.interval = tk.IntVar(self, 1000)
        ent = tk.Entry(self, textvariable=self.interval, width=8)
        ent.grid(row=1, column=1)

        lbl = tk.Label(self, text="Random +/-")
        lbl.grid(row=2, column=0, sticky='w')
        self.rand = tk.IntVar(self, 250)
        ent = tk.Entry(self, textvariable=self.rand, width=8)
        ent.grid(row=2, column=1)

        self.status = tk.Label(self, text='ready')
        self.status.grid(row=3, column=0, columnspan=2)

        self.button = tk.Button(self, text=START, command=self.toggle)
        self.button.grid(row=4, column=0, columnspan=2)

        self.mouse_mon()

    def toggle(self, value=None):
        if value == START or self.button['text'] == STOP:
            self.button['text'] = START
            self.status.config(text="Ready")
        elif value == STOP or self.button['text'] == START:
            self.button['text'] = STOP
            self.run()

    def run(self):
        try:
            if time.time() - self.last > self.delay.get() / 1000.:
                if self.button['text'] == STOP:
                    self.status.config(text="Running")
                    click()
                    rand = self.rand.get()
                    if rand:
                        rand = random.randrange(rand*2) - rand
                    self.after(self.interval.get() + rand, self.run)
            else:
                self.after(100, self.run)
        except Exception as e:
            self.toggle(START)
            self.status.config(text="ERROR")
            raise

    def mouse_mon(self):
        pos = self.winfo_pointerx(), self.winfo_pointery()
        if pos != self.pos:
            self.pos = pos
            self.last = time.time()
            if self.button['text'] == STOP:
                self.status.config(text="Paused")
        self.after(50, self.mouse_mon)

def main():
    root = tk.Tk()
    root.title("masterpooter")
    win = GUI(root)
    win.pack()
    root.mainloop()

if __name__ == "__main__":
    main()
