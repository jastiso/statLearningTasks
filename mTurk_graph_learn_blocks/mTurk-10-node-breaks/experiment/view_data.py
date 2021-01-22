####################################
# Data Viewing
####################################


@custom_code.route('/view_participants')
@myauth.requires_auth
def view_participants():
    # to_csv = 'to_csv' in request.args
    version = None
    if 'v' in request.args:
        version = request.args['v']
    try:
        id_list = get_finished_id_list(version)
        show_id_list = get_all_id_list(version)
        if len(show_id_list) > 0:
            users = Participant.query.filter(Participant.uniqueid.in_(show_id_list)).all()
        else:
            users = []
        for u in users:
            uniqueId = u.uniqueid
            u.completed = uniqueId in id_list
            exp = Exposure.query.filter(Exposure.uniqueId == uniqueId).all()
            if len(exp) > 0:
                u.n_complete = exp[0].n_complete
                u.walk_name = exp[0].walk_name
                u.walk_date = exp[0].walk_date
            else:
                u.n_complete = 0
                u.walk_name = np.nan
                u.walk_date = np.nan
        return render_template('show_record.html', participants=users)
    except Exception as ex:
        current_app.logger.error(request)
        return current_app.handle_exception(ex)


def get_all_id_list(filter_version=None):
    if filter_version == 'all':
        return [x.uniqueid for x in Participant.query.all()]
    if not filter_version:
        return get_version(CURRENT_VERSION)
    else:
        return get_version(filter_version)


def get_finished_id_list(filter_version=None):
    # ids = [x.uniqueid for x in Participant.query.all() if x.endhit is not None]
    ids = [x.uniqueId for x in OfflineTest.query.all() if x.response is not None]
    if not filter_version:
        v = get_version(CURRENT_VERSION)
        ids = [x for x in ids if x in v]
    elif filter_version != 'all':
        v = get_version(filter_version)
        ids = [x for x in ids if x in v]
    ids = [x for x in ids if not x.startswith('debug')]
    return ids


def get_version(v):
    return [x.uniqueid for x in Participant.query.all() if x.codeversion == v]


def format_offline_test(id_list):
    offline_test = OfflineTest.query.filter(OfflineTest.uniqueId.in_(id_list)).all()
    data = pd.DataFrame()

    for t in offline_test:
        df = pd.read_json(t.sequence).sort_index()
        df['Subject'] = t.uniqueId
        if t.response is not None:
            df['Response'] = loads(t.response)
            df['ReactionTime'] = loads(t.rt)
            df['Correct'] = (df['Response'] == df['Key'])
        data = data.append(df)
    data = data.reset_index(drop=True)
    return data


@custom_code.route('/view_offline_test', methods=['GET'])
@myauth.requires_auth
def view_offline_test():
    version = None
    if 'v' in request.args:
        version = str([request.args['v']])
    to_csv = 'to_csv' in request.args
    if 'uniqueId' in request.args:
        id_list = [request.args['uniqueId']]
    else:
        if 'all' in request.args:
            id_list = get_all_id_list(version)
        else:
            id_list = get_finished_id_list(version)
    try:
        data = format_offline_test(id_list)
        if to_csv:
            return Response(data.to_csv(), mimetype='text/csv')
        else:
            return render_template('list_offline_test.html', data=data.to_html(), id_list=id_list)
    except Exception as ex:
        current_app.logger.error(request)
        return current_app.handle_exception(ex)


def format_online_test(id_list):
    subject_index = pd.MultiIndex(levels=[[], []],
                                  labels=[[], []],
                                  names=[u'subject', u'data'])
    data = pd.DataFrame(columns=subject_index, index=range(600))
    online_test = OnlineTest.query.filter(OnlineTest.uniqueId.in_(id_list)).all()
    for t in online_test:
        uniqueId = t.uniqueId
        data.loc[:, (uniqueId, 'walk')] = loads(t.walk)
        data.loc[:, (uniqueId, 'random')] = loads(t.is_random)
        data.loc[:, (uniqueId, 'transition')] = get_boundaries(data.loc[:, (uniqueId, 'walk')])
        if t.response is not None:
            data.loc[:, (uniqueId, 'response')] = loads(t.response)
            data.loc[:, (uniqueId, 'ReactionTime')] = loads(t.rt)
            noResponse = (data.loc[:, (uniqueId, 'response')] == 0)
            data.loc[noResponse, (uniqueId, 'ReactionTime')] = np.nan
        else:
            data.loc[:, (uniqueId, 'response')] = np.nan
            data.loc[:, (uniqueId, 'ReactionTime')] = np.nan
    return data


@custom_code.route('/view_online_test', methods=['GET'])
@myauth.requires_auth
def view_online_test():
    version = None
    if 'v' in request.args:
        version = str([request.args['v']])
    to_csv = 'to_csv' in request.args
    if 'uniqueId' in request.args:
        id_list = [request.args['uniqueId']]
    else:
        if 'all' in request.args:
            id_list = get_all_id_list(version)
        else:
            id_list = get_finished_id_list(version)
    try:
        data = format_online_test(id_list)
        if to_csv:
            return Response(data.to_csv(), mimetype='text/csv')
        else:
            return render_template('list_online_test.html', data=data.to_html(), id_list=id_list)
    except Exception as ex:
        current_app.logger.error(request)
        return current_app.handle_exception(ex)


def format_exposure(id_list):
    subject_index = pd.MultiIndex(levels=[[], []],
                                  labels=[[], []],
                                  names=['subject', 'data'])    
    exposure = Exposure.query.filter(Exposure.uniqueId.in_(id_list)).all()
    max_walk_length = np.max([len(loads(t.walk)) for t in exposure])
    data = pd.DataFrame(np.nan, columns=subject_index, index=range(max_walk_length))
    for t in exposure:
        uniqueId = t.uniqueId
        subj_len = len(loads(t.walk))
        data.loc[:subj_len, (uniqueId, 'walk')] = loads(t.walk)
        data.loc[:subj_len, (uniqueId, 'rotated')] = loads(t.targets)
        data.loc[:subj_len, (uniqueId, 'transition')] = get_boundaries(data.loc[:subj_len, (uniqueId, 'walk')])
        if t.response is not None:
            data.loc[:subj_len, (uniqueId, 'response')] = loads(t.response)
            data.loc[:subj_len, (uniqueId, 'ReactionTime')] = loads(t.rt)
            noResponse = (data.loc[:, (uniqueId, 'response')] == 2)
            data.loc[noResponse, (uniqueId, 'ReactionTime')] = np.nan
        else:
            data.loc[:subj_len, (uniqueId, 'response')] = np.nan
            data.loc[:subj_len, (uniqueId, 'ReactionTime')] = np.nan
    return data


@custom_code.route('/view_exposure', methods=['GET'])
@myauth.requires_auth
def view_exposure():
    version = None
    if 'v' in request.args:
        version = str([request.args['v']])
    to_csv = 'to_csv' in request.args
    if 'uniqueId' in request.args:
        id_list = [request.args['uniqueId']]
    else:
        if 'all' in request.args:
            id_list = get_all_id_list(version)
        else:
            id_list = get_finished_id_list(version)
    try:
        data = format_exposure(id_list)
        if to_csv:
            return Response(data.to_csv(), mimetype='text/csv')
        else:
            return render_template('list_exposure.html', data=data.to_html(), id_list=id_list)
    except Exception as ex:
        current_app.logger.error(request)
        return current_app.handle_exception(ex)