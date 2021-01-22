# pylint: disable=W0703
"""
this file imports custom routes into the experiment server
"""

import random
from random import shuffle
import re
import zlib
import base64
from json import loads

import pandas as pd
from flask import Blueprint, request, jsonify, current_app, render_template_string
from sqlalchemy.orm.exc import NoResultFound

from psiturk.psiturk_config import PsiturkConfig
from psiturk.experiment_errors import ExperimentError
from psiturk.user_utils import nocache

# # Database setup
from psiturk.db import db_session
from psiturk.models import Participant

# from experiment_config import *
from custom_models import Quiz, Exp, Walkdata

# load the configuration options
CONFIG = PsiturkConfig()
CONFIG.load_config()

CURRENT_VERSION = CONFIG.get('Task Parameters', 'experiment_code_version')

# explore the Blueprint
custom_code = Blueprint('custom_code',
                        __name__,
                        template_folder='templates',
                        static_folder='static')

random.seed()

def get_cond(uniqueId):
    """
    Returns the subject experimental condition

    This is a number between 1 and (# conditions)

    Parameters
    ----------
    uniqueId : string
        Subject identifier

    Returns
    -------
    int
        Condition
    """

    user = Participant.query.\
        filter(Participant.uniqueid == uniqueId).one()
    return user.cond


def get_counterbalance(uniqueId):
    """
    Returns the subject experimental counterbalance

    This is a number between 1 and (# counterbalances)

    Parameters
    ----------
    uniqueId : string
        Subject identifier

    Returns
    -------
    int
        Counterbalance
    """
    user = Participant.query.\
        filter(Participant.uniqueid == uniqueId).one()
    return user.counterbalance


####################################
# Consent Route
####################################


def insert_mode(page_html, mode):
    """
    Insert "mode" into pages so it's carried from page to page done server-side
    to avoid breaking backwards compatibility with old templates.

    Raises
    ------
    ExperimentError
        If matching the mode location fails

    Returns
    -------
    string
        Modified HTML
    """

    page_html = page_html.decode("utf-8")
    match_found = False
    matches = re.finditer('workerId={{ workerid }}', page_html)
    match = None
    for match in matches:
        match_found = True
    if match_found:
        new_html = page_html[:match.end()] + "&mode=" + mode +\
            page_html[match.end():]
        return new_html
    else:
        raise ExperimentError("insert_mode_failed")


@custom_code.route('/consentaccept', methods=['GET'])
@nocache
def consentaccept():
    """
    Serves up the consent in the popup window.
    """
    if not ('hitId' in request.args and 'assignmentId' in request.args and
            'workerId' in request.args):
        raise ExperimentError('hit_assign_worker_id_not_set_in_consent')
    hit_id = request.args['hitId']
    assignment_id = request.args['assignmentId']
    worker_id = request.args['workerId']
    mode = request.args['mode']
    with open('templates/consentaccept.html', 'r') as temp_file:
        consent_string = temp_file.read()
    consent_string = insert_mode(consent_string, mode)
    return render_template_string(
        consent_string,
        hitid=hit_id,
        assignmentid=assignment_id,
        workerid=worker_id
    )

####################################
# Pre-experiment functions
####################################


@custom_code.route('/init', methods=['POST'])
@nocache
def do_init_subject():
    """
    Check if a subject has been initialized.

    If so, return.
    If not, initialize the subject.
    """

    req_json = request.get_json()
    if 'uniqueId' not in req_json:
        raise ExperimentError('improper_inputs')
    uniqueId = req_json['uniqueId']
    try:
        get_subject(uniqueId)
        return jsonify(success=True)
    except NoResultFound:
        init_subject(uniqueId)
        return jsonify(success=True)
    except Exception as ex:
        current_app.logger.error(request)
        return current_app.handle_exception(ex)

@custom_code.route('/check_eligibility', methods=['POST'])
@nocache
def check_eligibility():
    """
    Report whether a subject has taken part in the experiment before.

    Returns a response {valid=True} or {valid=False}
    """
    req_json = request.get_json()
    try:
        times_participated = Participant.query.\
            filter(Participant.workerid == req_json['workerid']).\
            filter(Participant.status >= 3).\
            count()
        if times_participated > 0:
            p = Participant.query.\
                filter(Participant.workerid == req_json['workerid']).\
                filter(Participant.status >= 3).first()
            return jsonify(valid=False, hitid=p.hitid)
        else:
            return jsonify(valid=True, hitid=None)
    except Exception as ex:
        current_app.logger.error(request)
        return current_app.handle_exception(ex)
        
def init_subject(uniqueId):
    """
    Initialize a new subject

    Parameters
    ----------
    uniqueId : str
        Subject identifier

    Returns
    -------
    custom_models.Exp
        Subject model
    """

    walk_id = Exp.query.count() % Walkdata.query.count() + 1
    subject = Exp(uniqueId, walk_id)

    db_session.add(subject)
    db_session.commit()

    return subject

def get_worker(workerId):
    """
    Get a participant based on their workerid

    This is mostly a convenience function for manually
    looking into subjects reporting experiment issues.

    Parameters
    ----------
    workerId : str
        Worker identifier

    Returns
    -------
    psiturk.Participant
        Subject model
    """
    participant = Participant.query.filter(Participant.workerid == workerId).one()
    return participant

def get_subject(uniqueId):
    """
    Get an existing subject

    Parameters
    ----------
    uniqueId : str
        Subject identifier

    Returns
    -------
    custom_models.Exp
        Subject model
    """

    subject = Exp.query.filter(Exp.uniqueId == uniqueId).one()
    return subject

def get_subject_walk(uniqueId):
    """
    Given a uniqueId, returns the walk data associated with a subject
    """
    subject = get_subject(uniqueId)
    walk = Walkdata.query.\
        filter(Walkdata.walk_id == subject.walk_id).\
        one()
    return walk

def decompress_pako(datastring):
    """
    Decompress json data that we compressed in the browser with paco.

    Assumes data was then base64-encoded:

    btoa(pako.deflate(JSON.stringify(data), { to: 'string' }));

    Parameters
    ----------
    datastring : string
        base64-encoded json data to decompress

    Returns
    -------
    dict
        JSON-decoded and decompressed data

    """
    data = loads(zlib.decompress(base64.decodestring(datastring)))
    return data

def get_task_data(uniqueId):
    """
    Return the decompressed subject taskdata.

    Parameters
    ----------
    uniqueId : string

    Returns
    -------
    dict
        taskdata

    """
    return get_compressed_data(uniqueId, 'compressed_task_data')

def get_compressed_data(uniqueId, field):
    """
    Return decompressed unstructured data.

    get_compressed_data(uniqueId, 'n-back')

    Parameters
    ----------
    uniqueId : string
        Subject identifier

    field : string
        Name of the data field

    Returns
    -------
    dict
        data
    """
    participant = Participant.query.filter(Participant.uniqueid == uniqueId).one()
    data = loads(participant.datastring)
    field_data = decompress_pako(data['questiondata'][field])
    return field_data

@custom_code.route('/get_finger_mapping', methods=['GET'])
def get_finger_mapping():
    """
    Get the list of finger combinations for the walk
    """
    if 'uniqueId' not in request.args:
        raise ExperimentError('improper_inputs')
    uniqueId = request.args['uniqueId']
    try:
        subject = get_subject(uniqueId)
        finger_mapping = subject.finger_mapping
        return jsonify(finger_mapping=finger_mapping)
    except Exception as ex:
        current_app.logger.error(request)
        return current_app.handle_exception(ex)


####################################
# Quiz and Pre-training
####################################

Quiz = pd.read_csv('stims/quiz.csv')

@custom_code.route('/quiz', methods=['GET'])
def get_quiz():
    """
    Fetch a quiz.

    request.args must contain
    qid : int
        Index of the quiz
    """

    if 'qid' not in request.args:
        raise ExperimentError('improper_inputs')
    qid = request.args['qid']
    try:
        quiz = Quiz[Quiz['quiz'] == int(qid)]
        questions = quiz['question'].tolist()
        answers = quiz[['answer_1', 'answer_2', 'answer_3']].values.tolist()
        correct_answers = quiz['correct_ans'].tolist()
        return jsonify(questions=questions,
                       answers=answers,
                       correct_answers=correct_answers)
    except Exception as ex:
        current_app.logger.error(request)
        return current_app.handle_exception(ex)

####################################
# Experiment 1:
# get_walk: get the walk for the exposure phase
# get_targ: get list of rotated images
# rec_p1: save subjet's answers for the first section
# stat_p1: keep track of how many trials have been completed
##########


@custom_code.route('/get_walk', methods=['GET'])
def get_walk():
    """
    Get the list of finger combinations for the walk
    """
    if 'uniqueId' not in request.args:
        raise ExperimentError('improper_inputs')
    uniqueId = request.args['uniqueId']
    try:
        walk = get_subject_walk(uniqueId)
        return jsonify(
            walk_one=walk.walk_one,
            is_crosscluster=walk.is_crosscluster,
            is_lattice=walk.is_lattice,
            walk_two=walk.walk_two,
            walk_three=walk.walk_three,
            walk_four=walk.walk_four,
            # nback_queries=walk.nback_queries,
            demo=walk.demo
        )
    except Exception as ex:
        current_app.logger.error(request)
        return current_app.handle_exception(ex)

####################################
# Cleanup
####################################

def get_stage_bonus(trials, full_length, base_value, perf_value):
    """
    Convenience function if we have multiple stages and want
    to compute the bonus separately on them.

    Parameters
    ----------
    trials : pd.DataFrame
        DataFrame of trials
    full_length : int
        Total number of trials possible
    base_value : float
        Bonus for completing the stage
    perf_value : float
        Bonus for accuracy above a threshold

    Returns
    -------
    total_bonus : float
        Total dollar amount of bonus
    performance_bonus : float
        Dollar amount of performance bonus
    performance : float
        Fraction of trials correct
    is_complete : bool
        Did they complete the stage?
    """

    if not trials.empty:
        n_complete = int(trials['trial'].max()) + 1
    else:
        n_complete = 0

    # Calculate the fraction of trials completed
    base_bonus = n_complete * base_value / full_length
    performance_bonus = 0.0 # Bonus based on accuracy
    performance = None # Accuracy value to report
    is_complete = False
    if n_complete >= full_length:
        is_complete = True
        performance = (trials[trials.correct].nTries == 1).mean()
        # Threshold for the percentage of trials that need to be correct
        if performance >= 0.9:
            performance_bonus = perf_value

    total_bonus = round(base_bonus + performance_bonus, 2)
    performance_bonus = round(performance_bonus, 2)

    return (total_bonus, performance_bonus, performance, is_complete)

def compute_bonus(uniqueId):
    """
    Computes bonus values for a subject with saved trial data

    Returns a dict of individual stage bonuses and performance

    Parameters
    ----------
    uniqueId : str
        subject identifier

    Returns
    -------
    dict
        Performance and bonuses
    """

    trials = pd.DataFrame(get_task_data(uniqueId))
    # We pass in a label for each stage: demo/walk/test etc
    walk_one_trials = trials.loc[trials['stage'] == 'walk_one']
    walk_two_trials = trials.loc[trials['stage'] == 'walk_two']
    walk_three_trials = trials.loc[trials['stage'] == 'walk_three']
    walk_four_trials = trials.loc[trials['stage'] == 'walk_four']
    #     loc[trials['stage'] == 'walk_two'].\
    #     loc[trials['query'] == 0]

    walkdata = get_subject_walk(uniqueId)

    _, walk_one_bonus, walk_one_performance, _ = get_stage_bonus(
        walk_one_trials, len(walkdata.walk_one), 0.0, 1.5)
    _, walk_two_bonus, walk_two_performance, _ = get_stage_bonus(
         walk_two_trials, len(walkdata.walk_two), 0.0, 1.5)
    _, walk_three_bonus, walk_three_performance, _ = get_stage_bonus(
         walk_three_trials, len(walkdata.walk_three), 0.0, 1.5)
    _, walk_four_bonus, walk_four_performance, _ = get_stage_bonus(
         walk_four_trials, len(walkdata.walk_four), 0.0, 1.5)

    # Below, make sure we have the maximum and minimum bonus values correct
    #total_bonus = walk_one_bonus + walk_two_bonus + walk_three_bonus + walk_four_bonus
    # don't want a performance incentive for this task
    total_bonus = 0
    total_performance = None
    #total_bonus = walk_one_bonus
    total_bonus = max(0.0, total_bonus)
    total_bonus = min(1.5, total_bonus)
    total_bonus = round(total_bonus, 2)

    # get total perf
    if (walk_four_performance is not None) and (walk_three_performance is not None) and (walk_two_performance is not None) and (walk_one_performance is not None):
        total_performance = (walk_one_performance + walk_two_performance + walk_three_performance + walk_four_performance)/4

    return {
        'walk_one_perf': walk_one_performance,
        'walk_one_bonus': walk_one_bonus,
        'walk_two_perf': walk_two_performance,
        'walk_two_bonus': walk_two_bonus,
        'walk_three_perf': walk_three_performance,
        'walk_three_bonus': walk_three_bonus,
        'walk_four_perf': walk_four_performance,
        'walk_four_bonus': walk_four_bonus,
        'total_bonus': total_bonus,
        'total_perf': total_performance
    }


@custom_code.route('/post_bonus', methods=['POST'])
def post_bonus():
    """
    POST request to compute and return the subject bonus information.
    """

    req_json = request.get_json()
    if not 'uniqueId' in req_json:
        raise ExperimentError('improper_inputs')
    uniqueId = req_json['uniqueId']

    try:
        # lookup user in database
        user = Participant.query.\
            filter(Participant.uniqueid == uniqueId).one()
        exp_data = get_subject(uniqueId)

        bonus_results = compute_bonus(uniqueId)
        exp_data.bonus_info = bonus_results
        user.bonus = bonus_results['total_bonus']

        db_session.add(exp_data)
        db_session.add(user)
        db_session.commit()

        return jsonify(bonus_results)
    except Exception as ex:
        current_app.logger.error(request)
        return current_app.handle_exception(ex)
