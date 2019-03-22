from psychopy import visual, core, event, data, gui, logging
from psychopy.hardware.labjacks import U3
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
#print sound.Sound()
#print prefs


#import custom python modules
from config import *
from setStimuli import *


def setSoc_WalkData(subj_id):

    #########
    # log file
    # Get logfile name

    expdir = os.getcwd()
    logdir = '{}/subjData'.format(expdir)

    print logdir

    ct = 0
    while 'logname' not in locals() or os.path.exists(logname):
        if ct > 0:
            lognum = '_%d' % (ct)
        else:
            lognum = ''
        logname = '{}/subj{}_logSoc{}.csv'.format(logdir, subj_id, lognum)
        ct += 1

    ######
    # set up trial handler
    Soc_trialFile = 'walks/subj{}/exposure_walk2.csv'.format(subj_id)
    Soc_trial_list = [ item for item in csv.DictReader(open(Soc_trialFile,'rU'))]

    #Split trials into 5 runs
    Soc_trials1 = data.TrialHandler(Soc_trial_list[0:len(Soc_trial_list)/5],nReps=1,method='sequential')
    Soc_trials2 = data.TrialHandler(Soc_trial_list[(len(Soc_trial_list)/5):(len(Soc_trial_list)/5*2)],nReps=1,method='sequential')
    Soc_trials3 = data.TrialHandler(Soc_trial_list[(len(Soc_trial_list)/5*2):(len(Soc_trial_list)/5*3)],nReps=1,method='sequential')
    Soc_trials4 = data.TrialHandler(Soc_trial_list[(len(Soc_trial_list)/5*3):(len(Soc_trial_list)/5*4)],nReps=1,method='sequential')
    Soc_trials5 = data.TrialHandler(Soc_trial_list[(len(Soc_trial_list)/5*4):(len(Soc_trial_list)/5*5)],nReps=1,method='sequential')

#    #Just test 10 trials/run
#    Soc_trials1 = data.TrialHandler(Soc_trial_list[0:10],nReps=1,method='sequential')
#    Soc_trials2 = data.TrialHandler(Soc_trial_list[10:20],nReps=1,method='sequential')
#    Soc_trials3 = data.TrialHandler(Soc_trial_list[20:30],nReps=1,method='sequential')
#    Soc_trials4 = data.TrialHandler(Soc_trial_list[30:40],nReps=1,method='sequential')
#    Soc_trials5 = data.TrialHandler(Soc_trial_list[40:50],nReps=1,method='sequential')

    #Add data types to trials
    Soc_trials1.data.addDataType('resp')
    Soc_trials1.data.addDataType('onset')
    Soc_trials1.data.addDataType('rt')
    Soc_trials1.data.addDataType('correct')

    Soc_trials2.data.addDataType('resp')
    Soc_trials2.data.addDataType('onset')
    Soc_trials2.data.addDataType('rt')
    Soc_trials2.data.addDataType('correct')

    Soc_trials3.data.addDataType('resp')
    Soc_trials3.data.addDataType('onset')
    Soc_trials3.data.addDataType('rt')
    Soc_trials3.data.addDataType('correct')

    Soc_trials4.data.addDataType('resp')
    Soc_trials4.data.addDataType('onset')
    Soc_trials4.data.addDataType('rt')
    Soc_trials4.data.addDataType('correct')

    Soc_trials5.data.addDataType('resp')
    Soc_trials5.data.addDataType('onset')
    Soc_trials5.data.addDataType('rt')
    Soc_trials5.data.addDataType('correct')

    # setup logging #
    current_run=0
    log_file = logging.LogFile("logs/subj%s_Soc.log" % (subj_id),  level=logging.DATA, filemode="w")
    return (log_file,logname,Soc_trials1,Soc_trials2,Soc_trials3,Soc_trials4,Soc_trials5)

def do_runSoc(subj_id,trials,logname,runID):
    log_file = logging.LogFile("logs/subj%s_Soc.log" % (subj_id),  level=logging.DATA, filemode="w")

    ########################
    # SHOW READY SCREEN #
    ########################
    import u3
    lj = u3.U3()
    print(lj.configIO(FIOAnalog = 252))

    ready_screen.draw()
    win.flip()
    # send pulses while waiting for trigger from admin
    waitClock = core.Clock()
    while True:
        keys=event.getKeys(keyList=('1','2','3'))
        # React to response
        if waitClock % 1 == 0:
            lj.setFIOState(4, 1)
            lj.getFeedback(u3.WaitShort(time = 39)
            lj.setFIOState(4,0)
        if '1' in keys:
            break
    # wait for trigger from admin (1 press)

    # set clock
    globalClock = core.Clock()
    logging.setDefaultClock(globalClock)

    logging.log(level=logging.DATA, msg="** START Social exposure **")
    trials.extraInfo={'START':globalClock.getTime()}

#    # disdaq fixation
#    logging.log(level=logging.DATA, msg="FIXATION")
#    for frame in range(frames['disdaq']):
#        fixation.draw()
#        win.flip()

    tidx = 0

    for tidx, trial in enumerate(trials):
        print('In trial {} - walk = {} altered = {}'. format(tidx+1, trial['walk'], trial['altered']))
        print trial['path']

        logging.log(level=logging.DATA, msg="Trial %i - Stimuli %s" % (tidx+1, trial['path']))

        #Set values for trial
        img.setImage(trial['path'])
        onset = globalClock.getTime()
        trials.addData('onset', onset)
        correct=None
        responses=None
        key=None
        rt=None

        while globalClock.getTime() < (tidx+1)*trialDur:
            img.draw()
            Soc_resp_prompt1.draw()
            Soc_resp_prompt2.draw()
            Soc_resp_prompt3.draw()
            win.flip()

            key=event.getKeys(keyList=('f','j','escape'), timeStamped=globalClock)
            if len(key)==1:
                rt=globalClock.getTime()-onset
                responses=key[0][0]
                if (key[0][0]=='j' and (trial['altered']=='False' or trial['altered']==0)):
                    high.play()
                    correct=0
                elif (key[0][0]=='f' and (trial['altered']=='True' or trial['altered']==1)):
                    high.play()
                    correct=0
                elif (key[0][0]=='escape'):
                    logging.flush() # if you are using logger
                    win.close()
                    core.quit()
                    break
                else:
                    correct=1
            event.clearEvents()
        # If no response, play low sound
        if responses==None:
            low.play()
            responses='NA'
            rt='NA'
            correct=0
        # record response
        trials.addData('resp',responses)
        trials.addData('rt',rt)
        trials.addData('correct',correct)

    # final fixation
    timer = core.CountdownTimer(fixDur)
    while timer.getTime() > 0:
        fixation.draw()
        win.flip()

    # break
    if runID<5:
        Soc_breakScreen.draw()
        win.flip()
        event.waitKeys(keyList=('1'))

    logging.log(level=logging.DATA, msg="*** END ****")

    trials.extraInfo['END']=globalClock.getTime()
    trials.saveAsText(fileName=logname, delim=',', dataOut=('all_raw'), appendFile=False)



if __name__ == '__main__':
    subj_id=1
    log_file,logname,Soc_trials1,Soc_trials2,Soc_trials3,Soc_trials4,Soc_trials5 = setSoc_WalkData(subj_id)

    #round 1
    do_runSoc(subj_id,Soc_trials1,logname.replace('.csv','_run1.csv'),1)

    core.quit()
