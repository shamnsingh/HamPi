# Main file responsible for synchronous stream processing.
from ..matcher.matcher import *
from ..mySDR.mySDR import *
from ..fmDemod.fmDemod import *
from ..myAudio.myAudio import *
from ..db.db import *
import Queue
import threading, time
from ..utils.dbScrape import *
from ..utils.parser import *
import sys, os
from ..execute.executor import *

from numpy import *
from matplotlib.pyplot import *

from Tkinter import Tk, Frame, BOTH, Label
from ttk import Frame, Button, Style

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.parent = parent
        self.initUI()

    def run(self):
        t_action = threading.Thread(target = self.action, args=())
        t_action.start()

    def action(self):
        args = parse(sys.argv[1])
        progress = open(sys.argv[2], 'w')

        myMatcher = matcher(args['match_thres'], args['m'], args['fs'])
        myExecutor = executor()
        Q_record = Queue.Queue()
        Q_process = Queue.Queue()

        sdr = mySDR()
        sdr.set_up(args['fs'], args['fc'] - args['offset'], args['gain'])

        # Initiate database responsible for acquiring query data.
        database = db([], args['t'], args['m'], args['cutoff'], sdr, Q_record, fmDemod(), myAudio())

        t_record = threading.Thread(target = database.recordContinously, args = (progress,))
        t_record.start()

        time.sleep(args['process_delay'])

        # Stores data_ds in Q_process.
        t_process = threading.Thread(target = database.processContinously, args = (Q_process, progress, args['buff_size'], args['taps']))
        t_process.start()

        time.sleep(args['matcher_delay'])

        myMatcher.match_Queue(Q_process, myExecutor)
   
    def close(self):
        print 'Exiting...'
        os._exit(0)

    def initUI(self):
        self.parent.title("HamPi")
        self.pack(fill=BOTH, expand=2)

        # self.parent.title("Process button")
        self.style = Style()
        self.style.theme_use("default")

        self.pack(fill=BOTH, expand=1)

        processButton = Button(self, text="Process", command=self.run)
        processButton.place(x=60, y=10)

        quitButton = Button(self, text="Quit", command=self.close)
        quitButton.place(x=140, y=10)

rcParams['figure.max_open_warning'] = 200

def usage():
    print 'python -m lib.process.py [args_file] [progress_file] [debug_file]'

if (len(sys.argv) != 3):
    usage()
    exit(0)

root = Tk()
root.geometry("300x50")
app = Example(root)
root.mainloop()

# Hackish listener that exits from keyboard interrupt.
#try:
#    while (True):
#        continue
#except KeyboardInterrupt:
#    print 'Exiting...'
#    os._exit(0)
