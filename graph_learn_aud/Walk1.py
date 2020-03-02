

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


def show_progress(time,acc,nStim,blockID,score):
    # give feedback on how well subjects are doing
    
    # calculate score
    score_orig = score
    score = round(score + 1/(time/nStim)*100)
    score_str = "{}".format(score)
    
    # display
    block_txt = "You just finished block {} out of 4.\n\nReady to see your score? Press any key to continue".format(blockID)
    block_screen = visual.TextStim(win, text=block_txt, wrapWidth=35, color="#FFFFFF", bold=True)
    block_screen.draw()
    win.flip()
    event.waitKeys()
    
    tmp = score_orig
    while tmp < score:
        show_score = visual.TextStim(win, text="{}".format(tmp), wrapWidth=35, color="#00FF00", bold = True, height =2)
        tmp = tmp+2
        score_txt.draw()
        show_score.draw()
        win.flip()
    
    show_score = visual.TextStim(win, text=score_str, wrapWidth=35, color="#00FF00", bold = True, height =2)
    acc_txt = visual.TextStim(win, text="and your accuracy was: {}%".format((acc*100)/(nStim*blockID)), pos = (0,-2),wrapWidth=35, height = 1.5, color="#FFFFFF", alignHoriz='center')
    score_txt.draw()
    show_score.draw()
    acc_txt.draw()
    other.draw()
    cont.draw()
    win.flip()
    event.waitKeys()
    
    return score


def set_WalkData(subj_id,sess):
    
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
        logname = '{}/subj{}_log_motor_run{}{}.csv'.format(logdir, subj_id, sess, lognum)
        ct += 1
    
    ######
    # set up trial handler
    motor_trialFile = 'walks/subj{}/exposure_walk{}.csv'.format(subj_id,sess)
    motor_trial_list = [ item for item in csv.DictReader(open(motor_trialFile,'rU'))]
    
    #Split trials into 5 runs...I would prefer not to do this...so commenting out for now
    motor_trials1 = data.TrialHandler(motor_trial_list,nReps=1,method='sequential')
    
    
    #Add data types to trials
    motor_trials1.data.addDataType('resp')
    motor_trials1.data.addDataType('onset')
    motor_trials1.data.addDataType('rt')
    motor_trials1.data.addDataType('correct')
    motor_trials1.data.addDataType('typing')

    # setup logging #
    current_run=0
    log_file = logging.LogFile("logs/subj{}_motor{}.log".format(subj_id,sess),  level=logging.DATA, filemode="w")
    return (log_file,logname,motor_trials1)

def do_run(subj_id,trials,logname,runID, type_resp, sess):
    
    log_file = logging.LogFile("logs/subj{}_motor{}.log".format(subj_id,sess),  level=logging.DATA, filemode="w")
    
    ########################
    # SHOW READY SCREEN #
    ########################

    # set clock
    globalClock = core.Clock()
    logging.setDefaultClock(globalClock)

    logging.log(level=logging.DATA, msg="** START exposure **")
    trials.extraInfo={'START':globalClock.getTime()}

    
    acc = 0 # to report accuracy at the end
    block = 0
    score = 0
    # set score visual
    score_screen = visual.TextStim(win, text="Score: {}".format(score), wrapWidth=35, pos=(0,-6),  height=1.0, color="#FFFFFF")
    
    print('Starting to run trials')
    block_st = globalClock.getTime()
    for tidx, trial in enumerate(trials):
        win.mouseVisible = False
        
        event.clearEvents()
        print('In trial {} - walk = {} key = {}'. format(tidx+1, trial['walk'], trial['resp']))
        print(trial['path'])
        
        # make progress tracker
        # to one decimal place
        #percent = "{}% Comlpeted".format((((tidx+1)*1000)/(nTrial))/10.0)
        #progress = visual.TextStim(win, text=percent, wrapWidth=35, pos=(0,5),  height=1.0, color="#FFFFFF")
        
        # show progress is it is the end of a block
        if ((tidx) % stimPerBlock == 0) & (tidx != 0):
            block = block + 1
            score = show_progress((globalClock.getTime() - block_st),acc,stimPerBlock,block,score)
            block_st = globalClock.getTime()
            # set score visual
            score_screen = visual.TextStim(win, text="Score: {}".format(score), wrapWidth=35, pos=(0,-6),  height=1.0, color="#FFFFFF")
        
        
        logging.log(level=logging.DATA, msg="Trial %i - Stimuli %s" % (tidx+1, trial['path']))
        
        #Set values for trial
        img.setImage(trial['path'])
        key=None
        correct_resp=0
        rt=None
        onset = globalClock.getTime()
        
        #set loop to present trial for predetermined time (defined by trialDur) - removed to avoid frustration and prevent skipping trials
        while True:
            img.draw()
            score_screen.draw()
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
                rt=globalClock.getTime()-onset
                correct_resp=1
                # display squares during ISI
                img.setImage('img/no_target.png')
                img.draw()
                score_screen.draw()
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
                score_screen.draw()
                photodiode.draw()
                win.flip()
                
                # wait for correct response
                tmp=globalClock.getTime()
                while key != correct:
                    key=event.waitKeys(keys)
                    
                rt=globalClock.getTime()-onset
            # display squares during ISI
            img.setImage('img/no_target.png')
            img.draw()
            score_screen.draw()
            win.flip()
            
            # clear event
            event.clearEvents()
            
            
            # get ISI
            ISI=random.uniform(ISI_st,ISI_en)
            core.wait(ISI)
            
            #update accuracy
            acc = acc + correct_resp
            
            break
            
        # If no response, now this doesn't do anything but it usde to mark if they waited more than  trialDur
        #if presses==None:
        #    presses='NA'
        #    rt='NA'
        #    correct=0
        
        # record response
        trials.addData('resp',[key]) 
        trials.addData('onset', onset)
        trials.addData('rt',rt)
        trials.addData('correct',correct_resp)
        trials.addData('ISI', ISI)
        trials.addData('typing', type_resp)
    
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