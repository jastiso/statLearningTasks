# coding=utf8

import csv
import pandas as pd
from psiturk.db import db_session, init_db
from psiturk.models import Participant
from custom_models import Quiz, Walkdata

init_db()  # initialze the data base, creating tables for the custom_models.py if necessary

if Quiz.query.count() > 0:
    raise Exception('Database is not empty!')

with open('./stims/quiz.csv', 'r') as f:
    def strip(line):
        line = line.replace(u'“', '"').replace(u'”', '"')
        line = line.replace(u"’", "'").replace(u'‘', "'")
        return line
    # db_session.execute("TRUNCATE TABLE quiz RESTART IDENTITY;")
    amt_quiz = csv.reader(f)
    headers = amt_quiz.next()
    for r in amt_quiz:
        quiz_no = int(r[0])
        question_no = int(r[1])
        question = strip(r[2])
        ans1 = strip(r[3])
        ans2 = strip(r[4])
        ans3 = strip(r[5])
        correct_ans = int(r[6])
        q = Quiz(quiz_no=quiz_no,
                 question_no=question_no,
                 question=question,
                 ans1=ans1,
                 ans2=ans2,
                 ans3=ans3,
                 correct_ans=correct_ans)
        db_session.add(q)
    db_session.commit()

nodes_random = pd.read_csv('stims/nodes_random.csv', header=None) - 1
is_lattice = pd.read_csv('stims/is_lattice.csv', header=None) 

for i in range(500):
    nodes = nodes_random.iloc[i]
    clusters = (nodes > 4) * 1
    clusters += (nodes > 9) * 1
    crosscluster = clusters.shift(1) != clusters
    crosscluster[0] = False
    # last element of pythonindexing is not included
    nodes1 = nodes[0:250]
    nodes2 = nodes[250:500]
    nodes3 = nodes[500:750]
    nodes4 = nodes[750:1000]
    w = Walkdata(list(nodes1),
                 list(crosscluster),
                 list(is_lattice.iloc[i]),
                 list(nodes2),
                 list(nodes3),
                 list(nodes4),
                 None, # n-back queries
    )
    db_session.add(w)
db_session.commit()

subjects = pd.read_csv('data/subjects.csv.gz')
subjects = subjects.loc[~subjects.workerid.isnull()]
for s in subjects.itertuples():
    p = Participant(
        workerid = s.workerid,
        hitid = s.hitid,
        assignmentid = s.assignmentid
        )
    p.status = 3
    p.codeversion = 'dummy'
    db_session.add(p)
db_session.commit()
