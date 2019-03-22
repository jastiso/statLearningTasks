
#
#i. you might need to add the working directory to your sys path so
#
#import sys
#sys.append('.')
#
#or you can be specific
#
#sys.append('/Users/Matt/path/to/folder/mytask')
#
#ii. then any .py file in that folder can be imported, e.g. functions.py
#
#import functions as fn
#then call with
#fn.function1()
#iii. or if you want to put things in folders you can and include an empty __init__.py file in the folder so say
#task_folder
#     | 
#     == utils
#               |
#               === __init__.py
#               === functions.py
#
#then
#import utils.functions as fn

import sys
sys.path.append('.')

from psychopy import visual, core, event, data, gui, logging
#from psychopy.hardware.labjacks import u3
#import u3

# Import modules
import os
import random
from random import randint
import re
import urllib
import csv
import datetime
import pandas as pd

from psychopy import prefs
#prefs.general['audioLib'] = ['pyo']
prefs.general['audioLib'] = ['pygame']
from psychopy import sound
#print sound.Sound()
#print prefs

##### SET UP #######

# get subjID
subjDlg = gui.Dlg(title="Image Viewing Study")
subjDlg.addField('Enter Subject ID:')
#subjDlg.addField('Enter Condition #:')
subjDlg.show()

if gui.OK:
    subj_id=subjDlg.data[0]
#    cond=float(subjDlg.data[1])
    print('Subject ID is',subj_id)
#    print('Condition is',cond)
else:
    sys.exit()


expdir = os.getcwd()
logdir = '{}/subjData/subj{}'.format(expdir,subj_id)

print(logdir)

################
# Set up window #
################

# this was initially true
useFullScreen=True
win = visual.Window([1440,900], monitor="testMonitor", units="deg", fullscr=useFullScreen, allowGUI=False)

##### IMPORT PYTHON SCRIPTS #######
print('Importing relevant scripts')
from config import *
from setStimuli import *
import PreTask as motor1
print('Done importing preTask stuff')
import Walk1 as motor2
print('Done importing walk stuff')

################
# Task #
################
print('Defining functions')
def fullTask():

    #set values and parameters for tasks
    print('Set Vals for Task')
    prac_logname,motor_pracTrials=set_trials(subj_id)

    #instructions and quiz
    print('Loop through instructions and quiz')
    hand=motor1.instructOnly()
    
    #practice
    print('Practice for PreTask')
    motor1.do_prac(motor_pracTrials, prac_logname,hand)
    
    #move to exposure task
    print('Instruction Screen for Exposure Task')
    motor1.moveToTask()
    
    #Load Walk Data (trials etc.)
    log_file,logname,motor_trials1 = motor2.set_WalkData(subj_id)
    
    #Walk round 1
    acc=motor2.do_run(subj_id,motor_trials1,logname.replace('.csv','_run1.csv'),1,hand)

# display accuracy
    acc_txt = "Great job! Your accuracy was:\n\n{}% \n\nThank you for participating! Press any key to exit".format((((acc)*1000)/(nTrial))/10.0)
    acc_screen = visual.TextStim(win, text=acc_txt, wrapWidth=35, pos=(0,5),  height=1.0, color="#FFFFFF")
    acc_screen.draw()
    win.flip()
    event.waitKeys()

def Task_NoTrain():

    #set values and parameters for tasks
    print('Set Vals for Task')
    motor_trainTrials, motor_pracTrials=set_trials(subj_id)

    #move to exposure task
    print('Instruction Screen for Exposure Task')
    motor1.moveToTask()
    
    #Load Social Walk Data (trials etc.)
    log_file,logname,motor_trials1= motor2.set_WalkData(subj_id)
    
    #Walk round 1
    acc = motor2.do_run(subj_id,motor_trials1,logname.replace('.csv','_run1.csv'),1,hand)
    
    


if __name__ == '__main__':
    print('RUNNING TASK')
    fullTask()
    #Task_NoTrain()    
    
core.quit()