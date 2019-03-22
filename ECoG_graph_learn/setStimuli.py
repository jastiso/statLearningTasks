
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

from config import *


################
# Set up instruction stimuli #
################ 

#instruction text
Sync_instruct="""Please wait for administrator to begin. \
(Press 1)"""

instruct1="""Before we begin, are you right or left handed?\
\n\n\
Press L for left and R for right"""

instruct2="""In a few minutes, you will see five squares shown on the screen.\
Pairs of squares will light up as the experiment progresses. These squares \
correspond with keys on your keyboard, and your job is to watch \
the squares and press the corresponding keys when the squares lights up. \
The experiment will take around 30 minutes.
\n\n\
The five squares, from left to right, correspond with the keys \
'space', 'j', 'k', 'l', and ';'. If you are right handed, and 'a', 's', 'd', 'f', \
'space' if you are left handed. \
Please leave your thumb on space and one finger on each of the \
subsequent letters. \
\n\n\
Press 1 when you are ready to proceed to the next instruction screen.\
"""

instruct3="""Your goal is to complete the sequence both quickly and \
accurately. The faster you press the keys, the faster you complete the experiment!\\
If you make a mistake, a message will display \
on the screen and the trial will be counted as incorrect, \
but the same square will remain lit until you press the correct key. \\
 Once you finish the experiment,\
 the proportion of trials that you completed without any mistakes will be calculated. \
An overall accuracy greater than 90% means you are in the top tier \
of participants! \
\n\n\
Press 1 when you are ready to proceed to the next instruction screen.\
"""

instruct4="""The amount of time the experiment takes is not fixed, \
but the number of responses you have to make is. Therefore, \
you should make your responses both quickly and accurately. The \
30 minute estimate is based on previous data, and may take shorter \
or longer for you. 
\n\n\

Press 1 when you are ready to proceed to the next instruction screen.\
"""


instruct5="""You're almost ready to begin! To help you with the main task, \
you'll first complete a very brief demonstration in which we will label the keys \
you should press. This will take less than a minute and will not count towards your \
accuracy.\
\n\n\
Press 1 when you are ready to begin the task.\
"""


readyPrac="""The practice stream will begin now. Remember, for each trial,\
press 'space', 'j', 'k', 'l', or ';' if you are right handed, and 'a', 's', 'd', 'f', or space if\
 you are left handed.\\
 Remember to keep one finger on each key!
\n\n\
Ready? We'll get started as soon as you press 1!\
"""


#Set up instructions to show
fixation = visual.TextStim(win, text="+", height=2, color="#FFFFFF")
Sync_instructScreen = visual.TextStim(win, text=Sync_instruct, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")
instructScreen1 = visual.TextStim(win, text=instruct1, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")
instructScreen2 = visual.TextStim(win, text=instruct2, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")
instructScreen3 = visual.TextStim(win, text=instruct3, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")
instructScreen4 = visual.TextStim(win, text=instruct4, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")
instructScreen5 = visual.TextStim(win, text=instruct5, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")

#Set up ready screens to show
readyPracScreen = visual.TextStim(win, text=readyPrac, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")


################
# Set up preTask stimuli #
################ 

#Set Trial Stimuli
img = visual.ImageStim(win,'img/null.png', size=(21,5))
imgL = visual.ImageStim(win,'img/null.png',pos=(-5,0))
imgR = visual.ImageStim(win,'img/null.png',pos=(5,0))

resp_prompt1 = visual.TextStim(win, text="Carefully watch the sequence!", wrapWidth=35, pos=(0,9.5),  height=1.4, color="#FFFFFF", bold=True)
resp_promptR1 = visual.TextStim(win, text="Space", wrapWidth=35, pos=(-8.5,2.5),  height=1, color="#FFFFFF")
resp_promptR2 = visual.TextStim(win, text="J", wrapWidth=35, pos=(-4.5,2.5),  height=1.0, color="#FFFFFF")
resp_promptR3 = visual.TextStim(win, text="K", wrapWidth=35, pos=(-.5,2.5),  height=1.0, color="#FFFFFF")
resp_promptR4 = visual.TextStim(win, text="L", wrapWidth=35, pos=(4,2.5),  height=1.0, color="#FFFFFF")
resp_promptR5 = visual.TextStim(win, text=";", wrapWidth=35, pos=(8,2.5),  height=1.0, color="#FFFFFF")

resp_promptL1 = visual.TextStim(win, text="A", wrapWidth=35, pos=(-8.5,2.5),  height=1, color="#FFFFFF")
resp_promptL2 = visual.TextStim(win, text="S", wrapWidth=35, pos=(-4.5,2.5),  height=1.0, color="#FFFFFF")
resp_promptL3 = visual.TextStim(win, text="D", wrapWidth=35, pos=(-.5,2.5),  height=1.0, color="#FFFFFF")
resp_promptL4 = visual.TextStim(win, text="F", wrapWidth=35, pos=(4,2.5),  height=1.0, color="#FFFFFF")
resp_promptL5 = visual.TextStim(win, text="Space", wrapWidth=35, pos=(8,2.5),  height=1.0, color="#FFFFFF")

photodiode = visual.Rect(win,units = 'norm',fillColor = 'white',size=([.75,1]), pos = (1, -1))
error_screen =  visual.TextStim(win, text="Error", wrapWidth=35, pos=(0,-9.5),  height=1.4, color="#FF0000", bold=True)

################
# Import trial lists #
################ 

def set_trials(subj_id):
 
    # import practice trial list and info and set up practice trial handler
    motor_prac_trialFile = 'walks/subj{}/prac_walk.csv'.format(subj_id)
    motor_prac_trial_list = [ item for item in csv.DictReader(open(motor_prac_trialFile,'rU'))]
    motor_pracTrials = data.TrialHandler(motor_prac_trial_list,nReps=1,method='sequential')
    
    motor_pracTrials.data.addDataType('resp')
    motor_pracTrials.data.addDataType('correct')
    motor_pracTrials.data.addDataType('onset')
    motor_pracTrials.data.addDataType('rt')
    #motor_pracTrials.data.addDataType('pulseTime')
    
    expdir = os.getcwd()
    logdir = '{}/subjData'.format(expdir)
    
    print(logdir)
    
    ct = 0
    while 'prac_logName' not in locals() or os.path.exists(prac_logName):
        if ct > 0:
            lognum = '_%d' % (ct)
        else:
            lognum = ''
        prac_logName = '{}/subj{}_log_prac{}.csv'.format(logdir, subj_id, lognum)
        ct += 1
    
    return (prac_logName, motor_pracTrials)

################
# Miscellaneous pieces #
################ 


#Set up instructions to show
fixation = visual.TextStim(win, text="+", height=2, color="#FFFFFF")

