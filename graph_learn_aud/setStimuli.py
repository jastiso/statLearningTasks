
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

typing_instruct="""On average, how many hours a day do you spend typing on a computer (not a phone). \
\n\n\
a - less than 1 \n\n\
b - between 1 and 3 \n\n\
c - between 3 and 5 \n\n\
d - greater than 5 \n\n\
"""


instruct1="""In a few minutes, you will see 10 squares shown on the screen.\
Squares will light up in red as the experiment progresses. These squares \
correspond with keys on your keyboard, and your job is to watch \
the squares and press the corresponding keys when the squares lights up as \
quickly as possible to increase your score. \
The experiment will take around 20 minutes.
\n\n\
\n\n\
\n\n\
\n\n\
Press any key when you are ready to proceed to the next instruction screen.\
"""

instruct2="""The 10 squares, from left to right, correspond with the keys \
\n\n\
'q', 'w', 'e', 'r', 'v','b', 'u', 'i', 'o', 'p' \
\n\n\
It is important that only one finger is used to press each key. \
The easiest way to do this is to use the hand set up shown below.
\n\n\
\n\n\
\n\n\
\n\n\
\n\n\
Press any key when you are ready to proceed to the next instruction screen. \
"""

instruct3="""Your goal is to complete the key presses both quickly and \
accurately to get as many points as possible. The faster you press the keys, \
the faster you complete the experiment, and the more points you get!\
\n\n\
The amount of time the experiment takes is not fixed, \
but the number of responses you have to make is. The \
20 minute estimate is based on previous data, and may take shorter \
or longer for you. 
\n\n\
The experiment will take place in 4 blocks. After each block, you \
will be shown your score and accuracy. Remember, \
your score depends on how fast you can press the correct keys!
\n\n\


Press any key when you are ready to proceed to the next instruction screen.\
"""
instruct4="""If you make a mistake, a message will display \
on the screen and the trial will be counted as incorrect, \
but the same square will remain lit until you press the correct key. \
\n\n\
\n\n\
\n\n\
\n\n\
Once you finish the experiment,\
 the proportion of trials that you completed without any mistakes will be calculated. \
An overall accuracy greater than 90% means you are in the top tier \
of participants! \
\n\n\
Press any key when you are ready to proceed to the next instruction screen.\
"""

instruct5="""You're almost ready to begin! To help you with the main task, \
you'll first complete a very brief demonstration in which we will label the keys \
you should press. This will take less than a minute and will not count towards your \
accuracy.\
\n\n\
Press any key when you are ready to begin the task.\
"""

instruct6="""You're almost ready to begin the main task! Remember to \
respond as quickly and accurately as possible, and to keep one finger on each key!
\n\n\
Press any key when you are ready to begin the task.\
"""


readyPrac="""The practice stream will begin now. Remember, for each trial,\
press 'q', 'w', 'e', 'r', 'v' iwith your left hand, and 'b', 'u', 'i', 'o', ans 'p'\
with your left hand.\
 Remember to keep one finger on each key!
\n\n\
Ready? We'll get started as soon as you press a key!\
"""


#Set up instructions to show
fixation = visual.TextStim(win, text="+", height=2, color="#FFFFFF")
Sync_instructScreen = visual.TextStim(win, text=Sync_instruct, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")
typingInstructScreen = visual.TextStim(win, text=typing_instruct, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")
instructScreen1 = visual.TextStim(win, text=instruct1, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")
instructScreen2 = visual.TextStim(win, text=instruct2, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")
instructScreen3 = visual.TextStim(win, text=instruct3, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")
instructScreen4 = visual.TextStim(win, text=instruct4, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")
instructScreen5 = visual.TextStim(win, text=instruct5, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")
instructScreen6 = visual.TextStim(win, text=instruct6, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")

instructPic1 = visual.ImageStim(win, 'img/QWERTY_home_10.PNG', size=(14.76,8.16), pos=(0,-2))
instructPic2 = visual.ImageStim(win, 'img/task-example-10.PNG', size=(21.74,3.08), pos=(0,-2))
instructPic3 = visual.ImageStim(win, 'img/task-example-10-error.PNG', size=(21.74,5.46), pos=(0,1))

#Set up ready screens to show
readyPracScreen = visual.TextStim(win, text=readyPrac, wrapWidth=35, alignHoriz="center", height=1.0, color="#FFFFFF")


################
# Set up preTask stimuli #
################ 

#Set Trial Stimuli
img = visual.ImageStim(win,'img/null.png', size=(42,10))
imgL = visual.ImageStim(win,'img/null.png',pos=(-5,0))
imgR = visual.ImageStim(win,'img/null.png',pos=(5,0))

#resp_prompt0 = visual.TextStim(win, text="Carefully watch the sequence!", wrapWidth=35, pos=(0,9.5),  height=1.4, color="#FFFFFF", bold=True)
#resp_prompt1 = visual.TextStim(win, text="Q", wrapWidth=35, pos=(-8.5,2.5),  height=1, color="#FFFFFF")

photodiode = visual.Rect(win,units = 'norm',fillColor = 'white',size=([.75,1]), pos = (1, 1))
error_screen =  visual.TextStim(win, text="Error", wrapWidth=35, pos=(0,-9.5),  height=1.4, color="#FF0000", bold=True)


################
# Set block end stimuli #
################ 
score_txt = visual.TextStim(win, text="Great job! Your score is:", pos = (0,2), height = 1.5,wrapWidth=35, color="#FFFFFF")
other = visual.TextStim(win, text="Try to respond even faster in the next block to increase your score!", pos = (0,-6),wrapWidth=35, color="#FFFFFF", alignHoriz='center')
cont = visual.TextStim(win, text="Ready? Press any key to continue", pos = (0,-8),wrapWidth=35, color="#FFFFFF")

################
# Import trial lists #
################ 

def set_trials(subj_id,sess):
 
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
        prac_logName = '{}/subj{}_log_prac{}{}.csv'.format(logdir, subj_id, sess, lognum)
        ct += 1
    
    return (prac_logName, motor_pracTrials)

################
# Miscellaneous pieces #
################ 


#Set up instructions to show
fixation = visual.TextStim(win, text="+", height=2, color="#FFFFFF")

