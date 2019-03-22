

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


########################
# Helper function for reading csv strings#
########################
def replaceWord(resp,l1,word):
    if not all(n in resp for n in l1):
        return resp
    else:
        tmp = list(resp)
        for n in tmp:
            if n in l1:
                # we want to delete exaclty 1 occurance of each letter in the target list (space or semi colon)
                resp.remove(n)
                l1.remove(n)
            
        resp.append(word)
        return resp

########################
# FINAL INSTRUCTIONS #
########################
#define a function to show instructions to move from pretask to exposure task
def moveToTask():
    instructScreen4.draw()
    win.flip()
    event.waitKeys(keyList=('1'))
    

########################
# SHOW INSTRUCTIONS #
########################

def instructOnly():
        
    instructScreen1.draw()
    win.flip()
    hand=event.waitKeys(keyList=('l','r'))
    
    instructScreen2.draw()
    win.flip()
    event.waitKeys(keyList=('1'))
    
    instructScreen3.draw()
    win.flip()
    event.waitKeys(keyList=('1'))
    
    instructScreen4.draw()
    win.flip()
    event.waitKeys(keyList=('1'))
    
    instructScreen5.draw()
    win.flip()
    event.waitKeys(keyList=('1'))
    
    return hand
    
    event.clearEvents()

########################
# PRACTICE #
########################
#define a function to run the practice trials
def do_prac(trials,logname,hand):
    
    #start with practice instructions screen
    readyPracScreen.draw()
    win.flip()
    event.waitKeys(keyList=('1'))     

    #add initial fixation to let participant get prepped
    for frame in range(2):
        fixation.draw()
        win.flip()
    
    tidx = 0
    globalClock = core.Clock()
    
    for tidx, trial in enumerate(trials):
        event.clearEvents();
        
        if hand == ['r']:
            print('In trial {} - walk = {} key = {}'. format(tidx+1, trial['walk'], trial['respR']))
        else:
            print('In trial {} - walk = {} key = {}'. format(tidx+1, trial['walk'], trial['respL']))
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
            resp_prompt1.draw()
            if hand == ['r']:
                keys=['space','j', 'k', 'l', 'semicolon', 'escape'] #at the end of each frame, look for a key press
                respType = 'respR'
                resp_promptR1.draw()
                resp_promptR2.draw()
                resp_promptR3.draw()
                resp_promptR4.draw()
                resp_promptR5.draw()
            elif hand == ['l']:
                keys=['a','s', 'd', 'f', 'space', 'escape']
                respType = 'respL'
                resp_promptL1.draw()
                resp_promptL2.draw()
                resp_promptL3.draw()
                resp_promptL4.draw()
                resp_promptL5.draw()
            
            
            # format correct response
            
            # make correct response into a list
            allowable = []
            # add things to spell out space and semi colon
            allowable.extend(keys)
            allowable.extend(['s', 'p', 'a', 'c', 'e', 'm', 'i', 'c', 'o', 'l', 'n'])
            correct=[char for char in trial[respType] if char in allowable]
                
            # read replace characters with words
            correct = replaceWord(correct,['s','p','a','c','e'],'space')
            correct = replaceWord(correct,['s','e','m','i','c', 'o', 'l', 'o', 'n'],'semicolon')
            
            # sort to take care of order issues
            correct.sort()
            
            # finish drawing screen
            photodiode.draw()
            win.flip()
            
            # wait for two key presses
            presses = []
            
            key=event.waitKeys(keys)
            st = globalClock.getTime()
            curr = st
            while curr-st < interkey:
                if len(key)==1:
                    presses.append(key[0])
                elif len(key)>1:
                    presses.extend(key)
                key=event.getKeys(keys) #at the end of each frame, look for additional key press
                curr = globalClock.getTime()
                
            #if key was pressed during that frame, check if response was correct
            if len(presses)>=1:
                rt=globalClock.getTime()-onset
                presses = list(set(presses))
                presses.sort()
                
            if (presses==correct):
                correct_resp=1
                # display squares during ISI
                img.setImage('img/no_target.png')
                img.draw()
                resp_prompt1.draw()
                if hand == ['r']:
                    resp_promptR1.draw()
                    resp_promptR2.draw()
                    resp_promptR3.draw()
                    resp_promptR4.draw()
                    resp_promptR5.draw()
                elif hand == ['l']:
                    resp_promptL1.draw()
                    resp_promptL2.draw()
                    resp_promptL3.draw()
                    resp_promptL4.draw()
                    resp_promptL5.draw()
                win.flip()
                    
            elif (presses==['escape']):
                correct=0
                logging.flush() # if you are using logger
                win.close()
                core.quit()
                break
            else:
                correct_resp=0
                
                # error screen
                error_screen.draw()
                img.draw()
                resp_prompt1.draw()
                if hand == ['r']:
                    resp_promptR1.draw()
                    resp_promptR2.draw()
                    resp_promptR3.draw()
                    resp_promptR4.draw()
                    resp_promptR5.draw()
                elif hand == ['l']:
                    resp_promptL1.draw()
                    resp_promptL2.draw()
                    resp_promptL3.draw()
                    resp_promptL4.draw()
                    resp_promptL5.draw()
                photodiode.draw()
                win.flip()
                    
                # wait for correct response
                tmp=globalClock.getTime()
                while presses != correct:
                    presses = []
                    key=event.waitKeys(keys)
                    st = globalClock.getTime()
                    curr = st
                    while curr-st < interkey:
                        if len(key)==1:
                            presses.append(key[0])
                        elif len(key)>1:
                            presses.extend(key)
                        key=event.getKeys(keys) #at the end of each frame, look for additional key press
                        curr = globalClock.getTime()
                    presses = list(set(presses))
                    presses.sort()
                    
                    
            # display squares during ISI
            img.setImage('img/no_target.png')
            img.draw()
            resp_prompt1.draw()
            if hand == ['r']:
                resp_promptR1.draw()
                resp_promptR2.draw()
                resp_promptR3.draw()
                resp_promptR4.draw()
                resp_promptR5.draw()
            elif hand == ['l']:
                resp_promptL1.draw()
                resp_promptL2.draw()
                resp_promptL3.draw()
                resp_promptL4.draw()
                resp_promptL5.draw()
            win.flip()
            
            # clear event
            event.clearEvents()


            # get ISI
            ISI=random.uniform(ISI_st,ISI_en)
            core.wait(ISI)
            
            break
            
            
        # record response
        trials.addData('resp',[presses]) 
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
    
