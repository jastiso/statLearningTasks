Author: Ari Kahn
Date: August 1, 2018
# psiturk
## Key files:

1. `custom.py`

Contains the server logic

2. `custom_models.py`

Interfaces with the database, contains data models

3. `experiment/static/js/src/task.js`

Actual task file. Use gulp to compile it to:
`experiment/static/js/src/task.js`

## Installation
### NPM (Node Package Manager)
Node is javascript ecosystem, and its package manager, NPM, lets us install a few useful tools. See section on [NPM](#NPM)

There are also scripts defined in `package.json` to compile parts of the project.

```bash
# nvm is a version manager for node,
# and is probably the easiest way to get a quick node environment up and running

# Get nvm installed
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
# Install node
nvm install node
# Install local dependencies
npm install
# Run remaining setup
npm run build
# Start gulp task in the background
npm run gulp watch
```

### Python and Psiturk
Psiturk is a python library, and so we can install it through python. We're going to create a *virtual environment*, meaning the packages we install are only installed for our custom environment, rather than on the whole system. (see https://realpython.com/python-virtual-environments-a-primer/)

***Make sure you follow instructions on activating pyenv in your profile.***

1. Install pyenv: https://github.com/pyenv/pyenv

Optionally also pyenv-virtualenv
```bash
# This works for OSX
brew install pyenv
brew install pyenv-virtualenv
```
2. Create an environment for psiturk
```bash
pyenv install 2.7.15
pyenv virualenv 2.7.15 psiturk
# Both of these don't seem to help, still having framework issues
# PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 2.7.15
# PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv virtualenv 2.7.15 psiturk
```
3. Activate the virtualenv
```bash
pyenv activate psiturk
```
4. Install psiturk
```bash
pip install psiturk
```
5. And a few other useful things
```bash
pip install pandas networkx ipython bctpy
```

# Running Psiturk
Psiturk expects to find an experiment in the directory that you're running it in.
See the documentation at http://www.psiturk.org

# The Code
## backbone
PsiTurk internally uses Backbone (http://backbonejs.org) to keep data synchronized.

Backbone is a basic MVC framework. We're really only using the model definition and syncing though.
In `psiturk.js`, a Backbone model is defined as a number of json serializable properties. Calling `PsiTurk.save` syncs this to the server.

Method to load data:
```
experiment.py: @app.route('/sync/<uid>', methods=['GET'])
```
Load `Participant.datastring` as javascript object

Method to save data:
```
@experiment.py: app.route('/sync/<uid>', methods=['PUT'])
```
This writes the model to `Participant.datastring` after converting it to a string.

See `addTrialData` and `addUnstructuredData`
The only principle difference is that `addTrialData` records the date and trial number alongside the data to save.

## NPM
Necessary dev packages are defined in `package.json`

Run `npm install`

nvm is recommended:
- https://github.com/creationix/nvm

`curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh | bash`
`nvm install node`
## gulp
See `gulpfile.js`

Gulp is a task automator for Node, and lets us do a few useful things:

We can write in modern javascript and translate it back to es2015, which has wider browser support. Lets us use whatever recent features we want, some of which are just syntax improvements and some of which are more functional.
When run, it takes `experiment/static/js/src/task.js`, translates it, and writes it to `experiment/static/js/dist/task.js`

This also requires that we include `babel-polyfill` to support any newer runtime features. Run `cp node_modules/babel-polyfill/dist/polyfill.min.js experiment/static/lib/`.

Second, it allows us to 'minify' and combine our javascript libraries into a smaller combined file, which decreases the amount of data we have to send (and the number of libraries we have to keep track of in our html files).

Commands:
* `npm run gulp`: Convert task.js and jspsych.
* `npm run gulp watch`: Watch for changes to task.js and jspsych, and run whenever a file is updated.

During development, would recommend leaving a terminal open with `npm run gulp watch`

Example of a gulp workflow:

```javascript
// Define a taslk called 'jspsych'
gulp.task('jspsych', () => {
    // List the source files.
    // We want this rule to apply to both the jspsych core library,
    // as well as to the jspsych experiments.
    return gulp.src(['./experiment/static/js/src/jspsych/jspsych/*.js',
                     './experiment/static/js/src/jspsych/experiments/*js'])
        // sourcemaps creates a .map.js file, which is used by the web browser in case
        // we want to debug the new file.
        //
        // It serves as a map between the original files, and the minified source, but
        // isn't required to just run the code.
        .pipe(sourcemaps.init())
        // Combine all our input files into a single library called 'jspsych-combined.js'
        .pipe(concat('jspsych-combined.js'))
        // Now run it through babel, which converts it to older-style JS if needed.
        .pipe(babel({
            presets: ['env']
        }))
        // OObfuscate the source to make it less likely for someone to game it.
        // This also minifies it, reducing the total file size.
        .pipe(uglify())
        // Rename to 'jspsych-combined.min.js'
        .pipe(rename(function (path) {
          path.extname = '.min.js';
        }))
        // Create 'jspsych-combined.min.map.js'
        .pipe(sourcemaps.write('.'))
        // Write it out to the 'dist' directory, which we serve from
        .pipe(gulp.dest('experiment/static/js/dist'));
});
```

# Experiment Checklist

Stuff that's easy to forget to update before running

1. Instructions
2. Ad text
3. Bonus calculation
4. Config file
5. Quiz

Stuff besides code to do:
1. Make sure the new quiz is in the database
2. 

# Combining jspsych and psiturk
Basic example:
- https://psiturk.org/ee/W4v3TPAsiD6FUVY8PDyajH

Getting it running:
1) In standalone experiments, experiment.js contains code to generate a trial sequence. I took the entirety of experiment.js, and encapsulated it in a function, such as `nback()` which when called returns the trial sequence.

Also note that the default n-back experiment throws a bunch of console errors, because `jspsych-poldrack-single-stim` declares `jsPsych.pluginAPI.registerPreload('poldrack-single-stim', 'stimulus', 'image');` when in fact the stimuli are all html, and it attempts to fetch the html as a url. Since this is only due to prefetch, can be safely ignored. In an ideal world, can fix this at some point. Want to keep the prefetching for trial types like Raven's Matrices though.

I've also copied the javascript to load each experiment into task.js, and instead of saving to a custum route or to a local file, just using `psiTurk.recordUnstructuredData`.

## Multiple Library Versions
Depending on the experiments I'm trying to combine, might need separate versions of jspsych.

One option is something akin to this:
https://stackoverflow.com/questions/16156445/multiple-versions-of-a-script-on-the-same-page-d3-js

So far this hasn't been an issue, though, but may come up in the future.

# Exporting data

Here's an example of exporting data from the database into a python-readable format.

First, make sure we have a writable subdirectory within the experiment directory.

```bash
cd experiment
mkdir -p export && chmod 777 export
```

Next, we want to start an ipython session that has loaded `sqlalchemy` as well as our custom DB models.

```bash
ipython -i custom.py
# or pt-ipython
```

We want to read in the participants table, which is where psiturk stores core data on each participant. This includes their condition, bonus, browser, recorded trial data, etc.

```python
# Change these!
codeversion = '18.0'
exp_name = 'sierpinski'

con = db_session.connection()
statement = Participant.query.filter(Participant.codeversion == codeversion).statement
df = pd.read_sql_query(statement, con=con)
df.to_csv('export/participants_%s.csv.gz' % exp_name, compression='gzip')
```

Finally, export our custom model data, which contains info on graphs, walks, node to target maps, and any other info we stored before the experiment started.
We already have a list of the participants, use that.

```python
statement = Exp.query.filter(Exp.uniqueId.in_(df.uniqueid)).statement
exp_df = pd.read_sql_query(statement, con=con)
exp_df.to_csv('export/exp_%s.csv.gz' % exp_name, compression='gzip')
```

# Analyzing the data

The Experiment table data is pretty straightforward.

```python
In [28]: exp_df.iloc[-1]
Out[28]:
id                                                              953
uniqueId               AAF1SJ9FCBF75:3M23Y66PO38TTZ1Q12RBFBXRU856SN
finger_mapping    [[False, False, False, False, True, False, Tru...
walk              [20, 18, 11, 18, 19, 20, 22, 23, 22, 20, 22, 2...
demo                       [25, 26, 25, 23, 25, 24, 26, 25, 26, 25]
bonus_info        {u'walk_total_bonus': 2.0, u'walk_complete': T...
Name: 0, dtype: object
```

The Participant table is a little less obvious.

```python
In [27]: df.iloc[-1]
Out[27]:
uniqueid              A1VIP6S8H2XXH7:33TIN5LC05BD74FXYFMCH7CU1TAY93
assignmentid                         33TIN5LC05BD74FXYFMCH7CU1TAY93
workerid                                             A1VIP6S8H2XXH7
hitid                                3BVS8WK9Q1W8IDHV2F93Y5I8QDVBII
ipaddress                                           184.182.189.212
browser                                                      chrome
platform                                                      macos
language                                                    UNKNOWN
cond                                                              0
counterbalance                                                    0
codeversion                                                    18.0
beginhit                                 2018-08-17 18:22:59.484062
beginexp                                 2018-08-17 23:08:30.412016
endhit                                   2018-08-17 23:16:53.211305
bonus                                                             2
status                                                            7
mode                                                           live
datastring        {"condition":0,"counterbalance":0,"assignmentI...
Name: 111, dtype: object
```

Let's look at the datastring in more detail:

```python
import json

# Pull out a participant
p = df.iloc[-1]
datastring = json.loads(p.datastring)
In [37]: datastring.keys()
Out[37]:
[u'status',
 u'assignmentId',
 u'workerId',
 u'questiondata',
 u'bonus',
 u'hitId',
 u'counterbalance',
 u'useragent',
 u'eventdata',
 u'data',
 u'currenttrial',
 u'condition',
 u'mode']
```

Most of this is pretty boring. But a couple bits here are important.

## questiondata

First, 'questiondata' holds the results from all the psych battery tests, as well as any response the participant provided.

```python
In [44]: datastring['questiondata'].keys()
Out[44]:
[u'n-back',
 u'completed_walk',
 u'engagement',
 u'difficulty',
 u'free_response_question',
 u'completed_demo',
 u'ravens']
```

The psych battery data is all saved as follows:

```python
In [47]: json.loads(datastring['questiondata']['n-back'])[0]
Out[47]:
{u'block_duration': 1806,
 u'exp_id': u'n-back',
 u'focus_shifts': 9,
 u'full_screen': True,
 u'internal_node_id': u'0.0-0.0-0.0',
 u'key_press': 13,
 u'rt': 1806,
 u'text': u'<div class = centerbox><p class = center-block-text>Welcome to the experiment. Press <strong>enter</strong> to begin.</p></div>',
 u'time_elapsed': 1807,
 u'timing_post_trial': 0,
 u'trial_id': u'instruction',
 u'trial_index': 0,
 u'trial_type': u'poldrack-text'}
```

In python, the easiest way to extract this is going to be along the lines of:

```python
pd.read_json(datastring['questiondata']['ravens'])
```

## data

```python
taskdata = datastring['data']

# Pull out instruction and quiz trials
misc_trials = [x['trialdata'] for x in taskdata if 'phase' in x['trialdata']]

task_trials = [x['trialdata'] for x in taskdata if 'ph' in x['trialdata']]

pd.DataFrame(task_trials)
```