

from psychopy import visual, core, event, data, gui, logging
#from psychopy.hardware.labjacks import U3
# Import modules
import os
import random
import re
import urllib
import csv
#import u3


from psychopy import prefs
#prefs.general['audioLib'] = ['pyo']
prefs.general['audioLib'] = ['pygame']
from psychopy import sound
#print sound.Sound()
#print prefs

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


def set_WalkData(subj_id):
    
    #########
    # log file
    # Get logfile name
    
    expdir = os.getcwd()
    logdir = '{}/subjData'.format(expdir)
    
    print(logdir)
    
    ct = 0
    while 'logname' not in locals() or os.path.exists(logname):
        if ct > 0:
            lognum = '_%d' % (ct)
        else:
            lognum = ''
        logname = '{}/subj{}_log_motor{}.csv'.format(logdir, subj_id, lognum)
        ct += 1
    
    ######
    # set up trial handler
    motor_trialFile = 'walks/subj{}/exposure_walk.csv'.format(subj_id)
    motor_trial_list = [ item for item in csv.DictReader(open(motor_trialFile,'rU'))]
    
    #Split trials into 5 runs...I would prefer not to do this...so commenting out for now
    motor_trials1 = data.TrialHandler(motor_trial_list,nReps=1,method='sequential')
    
    
    #Add data types to trials
    motor_trials1.data.addDataType('resp')
    motor_trials1.data.addDataType('onset')
    motor_trials1.data.addDataType('rt')
    motor_trials1.data.addDataType('correct')

    # setup logging #
    current_run=0
    log_file = logging.LogFile("logs/subj%s_motor.log" % (subj_id),  level=logging.DATA, filemode="w")
    return (log_file,logname,motor_trials1)

def do_run(subj_id,trials,logname,runID,hand):
    
    log_file = logging.LogFile("logs/subj%s_motor.log" % (subj_id),  level=logging.DATA, filemode="w")
    
    ########################
    # SHOW READY SCREEN #
    ########################

    # set clock
    globalClock = core.Clock()
    logging.setDefaultClock(globalClock)

    logging.log(level=logging.DATA, msg="** START exposure **")
    trials.extraInfo={'START':globalClock.getTime()}

    
    tidx = 0
    acc = 0 # to report accuracy at the end
    
    print('Starting to run trials')
    for tidx, trial in enumerate(trials):
        event.clearEvents()
        
        if hand == ['r']:
            print('In trial {} - walk = {} key = {}'. format(tidx+1, trial['walk'], trial['respR']))
        else:
            print('In trial {} - walk = {} key = {}'. format(tidx+1, trial['walk'], trial['respL']))
            
        print(trial['path'])
        
        # make progress tracker
        print(tidx)
        # to one decimal place
        percent = "{}% Comlpeted".format((((tidx+1)*1000)/(nTrial))/10.0)
        progress = visual.TextStim(win, text=percent, wrapWidth=35, pos=(0,5),  height=1.0, color="#FFFFFF")
        
        logging.log(level=logging.DATA, msg="Trial %i - Stimuli %s" % (tidx+1, trial['path']))
        
        #Set values for trial
        img.setImage(trial['path'])
        key=None
        correct_resp=0
        rt=None
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
            progress.draw()
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
                progress.draw()
                win.flip()
                
            elif (presses==['escape']):
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
                progress.draw()
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
            progress.draw()
            win.flip()
            
            # clear event
            event.clearEvents()
            
            
            # get ISI
            ISI=random.uniform(ISI_st,ISI_en)
            core.wait(ISI)
            
            break
            
        # If no response, now this doesn't do anything but it usde to mark if they waited more than  trialDur
        #if presses==None:
        #    presses='NA'
        #    rt='NA'
        #    correct=0
        
        # record response
        trials.addData('resp',[presses]) 
        trials.addData('onset', onset)
        trials.addData('rt',rt)
        trials.addData('correct',correct_resp)
        trials.addData('ISI', ISI)
        acc = acc + correct_resp
    
    # final fixation
    #timer = core.CountdownTimer(fixDur)
    #while timer.getTime() > 0:
    #    fixation.draw()
    #    win.flip()
    
    
    logging.log(level=logging.DATA, msg="*** END ****")
       
    trials.extraInfo['END']=globalClock.getTime()
    trials.saveAsText(fileName=logname, delim=',', dataOut=('all_raw'), appendFile=False)
    
    # report accuracy
    return acc



if __name__ == '__main__':
    subj_id=999
    log_file,logname,motor_trials1 = set_WalkData(subj_id)
    
    #round 1
    # This is just a place holder for testings
    acc=do_run(subj_id,motor_trials1,logname.replace('.csv','_run1.csv'),1,'l')
        
    core.quit()