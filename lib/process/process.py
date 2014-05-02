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

from numpy import *
from matplotlib.pyplot import *

rcParams['figure.max_open_warning'] = 200

def usage():
    print 'python -m lib.process.py [file]'

if (len(sys.argv) != 2):
    usage()
    exit(0)

args = parse(sys.argv[1])
myMatcher = matcher(args['match_thres'], args['m'], args['fs'])
Q_record = Queue.Queue()
Q_process = Queue.Queue()

sdr = mySDR()
sdr.set_up(args['fs'], args['fc'] - args['offset'], args['gain'])

# Initiate database responsible for acquiring query data.
database = db([], args['t'], args['m'], args['cutoff'], sdr, Q_record, fmDemod(), myAudio())

raw_input('ENTER to record continously ...')

t_record = threading.Thread(target = database.recordContinously, args = ())
t_record.start()

time.sleep(args['process_delay'])

# Stores data_ds in Q_process.
t_process = threading.Thread(target = database.processContinously, args = (Q_process,))
t_process.start()

time.sleep(args['matcher_delay'])

# Match the data from the processing Queue to words.
#t_match = threading.Thread(target = myMatcher.match_Queue, args = (Q_process,))
#t_match.start()


try:
    myMatcher.match_Queue(Q_process)
except KeyboardInterrupt:
    print 'Exiting...'
    os._exit(0)

# Hackish listener that exits from keyboard interrupt.
try:
    while (True):
        continue
except KeyboardInterrupt:
    print 'Exiting...'
    os._exit(0)
