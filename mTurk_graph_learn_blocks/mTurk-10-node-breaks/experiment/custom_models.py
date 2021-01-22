# pylint: disable=C0326,C0330
"""
This file defines custom database models.

In particular, it is used to save subject walk information.
"""


import json

from psiturk.db import Base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy import types

from networkx.readwrite import json_graph

# from experiment_config import *

import numpy as np

from utilities import walks, graphs

####################################
# Static Content
####################################


class Quiz(Base):
    """
    Entry for a single quiz question

    Parameters
    ----------
    quiz_no : int
        What quiz this question is part of
    question_no : int
        What question this is, for the given quiz
    question : str
        Question prompt text
    ans1 : str
        Answer 1 text
    ans2 : str
        Answer 2 text
    ans3 : str
        Answer 3 text
    correct_ans : int
        Index of the correct answer

    """

    __tablename__ = "quiz_js"
    id = Column(Integer, primary_key=True, unique=True)
    quiz_no = Column(Integer)
    question_no = Column(Integer)
    question = Column(Text)
    ans1 = Column(Text)
    ans2 = Column(Text)
    ans3 = Column(Text)
    correct_ans = Column(Integer)

    def __init__(self, quiz_no, question_no, question, ans1, ans2, ans3, correct_ans):
        self.quiz_no = quiz_no
        self.question_no = question_no
        self.question = question
        self.ans1 = ans1
        self.ans2 = ans2
        self.ans3 = ans3
        self.correct_ans = correct_ans

####################################
# Experiment
####################################

# The below are definitions of all desired 1- and 2-target combinations.
#
# In the 10-finger case, there are more than necessary, and a few have
# been commented out to end up with 28 possibilities.

#FINGER_COMBINATIONS_5 = np.array([[ True, False, False, False, False],
#                                  [False,  True, False, False, False],
#                                  [False, False,  True, False, False],
#                                  [False, False, False,  True, False],
#                                  [False, False, False, False,  True],
#                                  [ True,  True, False, False, False],
#                                  [ True, False,  True, False, False],
#                                  [ True, False, False,  True, False],
#                                  [ True, False, False, False,  True],
#                                  [False,  True,  True, False, False],
#                                  [False,  True, False,  True, False],
#                                  [False,  True, False, False,  True],
#                                  [False, False,  True,  True, False],
#                                  [False, False,  True, False,  True],
#                                  [False, False, False,  True,  True]])

# 10 fingers, each one individually
FINGER_COMBINATIONS_10 = np.array([[ True, False, False, False, False, False, False, False, False, False],
    [False,  True, False, False, False, False, False, False, False, False],
    [False, False,  True, False, False, False, False, False, False, False],
    [False, False, False,  True, False, False, False, False, False, False],
    [False, False, False, False,  True, False, False, False, False, False],
    [False, False, False, False, False,  True, False, False, False, False],
    [False, False, False, False, False, False,  True, False, False, False],
    [False, False, False, False, False, False, False,  True, False, False], 
    [False, False, False, False, False, False, False,  False, True, False],
    [False, False, False, False, False, False, False,  False, False, True]])

class JSONStr(types.TypeDecorator): # pylint: disable=W0223
    """
    Class to store JSON-serializable data as a string.

    Transparently encodes and decodes the data.
    """

    impl = types.Text

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

class GraphStr(types.TypeDecorator): # pylint: disable=W0223
    """
    Type to store a networkx graph a database string.

    Dumps and loads the data to json to store it.
    """

    impl = types.Text

    def process_result_value(self, value, dialect):
        return json_graph.node_link_graph(json.loads(value))

    def process_bind_param(self, value, dialect):
        return json.dumps(json_graph.node_link_data(value))


class Walkdata(Base):
    """
    Entry for a series of walks.

    Parameters
    ----------
    walk_one : list [0-14] # I think this is actually 1-15...
        List of nodes for walk one
    is_crosscluster : list [0/1]
        Boolean for whether each trial in walk one crosses a cluster boundary
    is_lattice : list [0/1]
        Boolean for whether each trial in walk one is part of a lattice graph or modular graph
    walk_two : list [0-14]
        List of nodes for walk two
    walk_three : list [0-14]
        List of nodes for walk two
    walk_four : list [0-14]
        List of nodes for walk two
    nback_queries : list [0-2]
        List of whether to query the previous trial (1), two trials ago (2), or neither (0)

    """

    __tablename__ = "walkdata_js"
    walk_id = Column(Integer, primary_key=True, unique=True)

    demo = Column(JSONStr)

    walk_one = Column(JSONStr)
    is_crosscluster = Column(JSONStr)
    is_lattice = Column(JSONStr)

    walk_two = Column(JSONStr)
    walk_three = Column(JSONStr)
    walk_four = Column(JSONStr)
    nback_queries = Column(JSONStr)

    def __init__(self, walk_one, is_crosscluster, is_lattice, walk_two, walk_three, walk_four, nback_queries):
        self.demo = walks.hamiltonian_walk(10) # changed this so they see every key
        self.walk_one = walk_one
        self.is_crosscluster = is_crosscluster
        self.is_lattice = is_lattice
        self.walk_three = walk_three
        self.walk_two = walk_two
        self.walk_four = walk_four
        self.nback_queries = nback_queries


class Exp(Base):
    """
    Entry for an experimental subject

    Parameters
    ----------
    uniqueId : str
        Subject identifier
    walk_id : int
        Index of a walk in the Walkdata table

    """
    __tablename__ = "exp_js"
    id = Column(Integer, primary_key=True, unique=True)
    uniqueId = Column(String, unique=True)

    # Mapping of fingers to nodes
    finger_mapping = Column(JSONStr)

    # Walk Index
    walk_id = Column(Integer)

    bonus_info = Column(JSONStr)

    def __init__(self, uniqueId, walk_id):
        self.uniqueId = uniqueId

        mapping = FINGER_COMBINATIONS_10.copy()
        np.random.shuffle(mapping)
        self.finger_mapping = mapping.tolist()

        self.demo = walks.random_walk(graphs.modular, 10)

        self.walk_id = walk_id

        self.bonus_info = None

    def __repr__(self):
        return "uid: %s" % \
             (self.uniqueId)
