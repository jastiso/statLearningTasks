#Config file

from psychopy import visual, core, event, data, gui, logging
#from psychopy.hardware.labjacks import U3
# Import modules
import os
import random
import re
import urllib
import csv

from psychopy import prefs
#prefs.general['audioLib'] = ['pyo']
prefs.general['audioLib'] = ['pygame']
from psychopy import sound


expdir = os.getcwd()



################
# Set up window #
################

# this was initially set to true
useFullScreen=True
win = visual.Window([1440,900], monitor="testMonitor", units="deg", fullscr=useFullScreen, allowGUI=False, color = 'black')


##############
# Parameters #
##############

fixDur=10 #seconds
trainDur=2 #seconds
trialDur=2 #seconds
interkey = 0.2 #seconds
nTrial = 1000
ISI_st = .05 #shortest intertrial interval
ISI_en = .05 # longest intertrial interval
