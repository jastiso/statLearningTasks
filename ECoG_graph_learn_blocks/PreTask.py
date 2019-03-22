

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

#import custom python modules
from config import *
from setStimuli import *
win.mouseVisible = False

########################
# FINAL INSTRUCTIONS #
########################
#define a function to show instructions to move from pretask to exposure task
def moveToTask():
    instructScreen6.draw()
    win.flip()
    event.waitKeys()
    

########################
# SHOW INSTRUCTIONS #
########################

def instructOnly():
    
    typingInstructScreen.draw()
    
    win.flip()
    type_resp = event.waitKeys(keyList = ('a','b','c','d'))
    
    instructScreen1.draw()
    instructPic2.draw()
    win.flip()
    event.waitKeys()
    
    instructScreen2.draw()
    instructPic1.draw()
    win.flip()
    event.waitKeys()
    
    instructScreen3.draw()
    win.flip()
    event.waitKeys()
    
    instructScreen4.draw()
    instructPic3.draw()
    win.flip()
    event.waitKeys()
    
    instructScreen5.draw()
    win.flip()
    event.waitKeys()
    
    return type_resp
    
    event.clearEvents()

########################
# PRACTICE #
########################
#define a function to run the practice trials
def do_prac(trials,logname):
    
    #start with practice instructions screen
    readyPracScreen.draw()
    win.flip()
    event.waitKeys()     

    #add initial fixation to let participant get prepped
    for frame in range(2):
        fixation.draw()
        win.flip()
    
    tidx = 0
    globalClock = core.Clock()
    
    for tidx, trial in enumerate(trials):
        event.clearEvents();
        
        print('In trial {} - walk = {} key = {}'. format(tidx+1, trial['walk'], trial['resp']))
        print(trial['path'])
        
        
        #Set values for trial
        img.setImage(trial['path'])
        key=None
        correct_resp=None
        rt=None
        ISI = None
        onset = globalClock.getTime()

        #set loop to present trial for predetermined time (defined by trialDur)
        while True:
            img.draw()
            #resp_prompt0.draw()
            keys=['q','w', 'e', 'r', 'v', 'b', 'u','i','o','p', 'escape'] #at the end of each frame, look for a key press
            
            # format correct response
            correct=[char for char in trial['resp'] if char in keys]
            
            # sort to take care of order issues
            correct.sort()
            
            # finish drawing screen
            photodiode.draw()
            win.flip()
            
            # wait for key press
            key=event.waitKeys(keys)
            
            # check if response was correct
            if (key==correct):
                correct_resp=1
                # display squares during ISI
                img.setImage('img/no_target_prac.png')
                img.draw()
                #resp_prompt0.draw()
                win.flip()
                
            elif (key==['escape']):
                correct=0
                logging.flush() # if you are using logger
                trials.saveAsText(fileName=logname, delim=',', dataOut=('all_raw'), appendFile=False) # still save data if you quit early
                win.close()
                core.quit()
                break
            else:
                correct_resp=0
                
                # error screen
                error_screen.draw()
                img.draw()
                #resp_prompt0.draw()
                photodiode.draw()
                win.flip()
                
                # wait for correct response
                tmp=globalClock.getTime()
                while key != correct:
                    key=event.waitKeys(keys)
                    
                    
            # display squares during ISI
            img.setImage('img/no_target_prac.png')
            img.draw()
            #resp_prompt0.draw()
            win.flip()
            
            # clear event
            event.clearEvents()
            
            
            # get ISI
            ISI=random.uniform(ISI_st,ISI_en)
            core.wait(ISI)
            
            break
            
            
        # record response
        trials.addData('resp',[key]) 
        trials.addData('onset', onset)
        trials.addData('rt',rt)
        trials.addData('correct',correct_resp)
        trials.addData('ISI', ISI)
        
    trials.saveAsText(fileName=logname, delim=',', dataOut=('all_raw'), appendFile=False)


if __name__ == '__main__':
    subj_id=999
    #set values and parameters for tasks
    print('Set Vals for Motor Task')
    prac_logName, motor_pracTrials=set_trials(subj_id)
    
    #instructions
    instructOnly()
    
    #practice
    do_prac(motor_pracTrials,prac_logName)
    
    #move to exposure task
    moveToTask()
    
