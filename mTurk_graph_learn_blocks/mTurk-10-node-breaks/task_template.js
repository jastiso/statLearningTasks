/*
 * Requires:
 *     psiturk.js
 *     utils.js
 */

/* global PsiTurk, Q, Promise, pako */
/* global make_ravens_experiment, make_n_back_experiment, make_temp_discount */
/* global jsPsych, addID */
/* global uniqueId, mode, adServerLoc */
/* global $, document, window, event, btoa */

/* eslint no-use-before-define: ["error", { "functions": false }] */
/* eslint no-param-reassign: 0 */
/* eslint no-restricted-globals: 0 */

// Initalize psiturk object
const psiTurk = new PsiTurk(uniqueId, adServerLoc, mode);


// All pages to be loaded
const loading = ['loading.html'];
psiTurk.preloadPages(loading);
psiTurk.showPage('loading.html');

const basePages = [
  'quiz.html',
  'postquestionnaire.html',
  'failed.html',
  'pretask.html',
  'results.html',
  'stage10.html',
  'waiting.html',
  'free_response.html',
  'block_end.html',
  'show_score.html',
];

const readyDemo = [
  'instructions/ready-pretask.html',
];

const readyWalkOne = [
  'instructions/ready-walk-one.html',
];

// const readyWalkTwo = [
//   'instructions/ready-walk-two.html',
// ];

 const readyNBack = [
   'instructions/ready-n-back.html',
 ];

const instructionsOverview = [
  'instructions/instruct-overview-1.html',
  'instructions/instruct-overview-2.html',
];

const instructionsWalkOne = [
  'instructions/instruct-1-1.html',
  'instructions/instruct-1-2.html',
  'instructions/instruct-1-3.html',
  'instructions/instruct-1-4.html',
];

// const instructionsWalkTwo = [
//   'instructions/instruct-2-1.html',
// ];

const retryQuizPages = [
  'instructions/quiz-retry.html',
];

const instructionPages = [
  instructionsWalkOne,
  // instructionsWalkTwo,
];

psiTurk.preloadPages(basePages);
psiTurk.preloadPages(readyDemo);
psiTurk.preloadPages(readyNBack);
psiTurk.preloadPages(readyWalkOne);
// psiTurk.preloadPages(readyWalkTwo);
psiTurk.preloadPages(instructionsWalkOne);
// psiTurk.preloadPages(instructionsWalkTwo);
psiTurk.preloadPages(instructionsOverview);
psiTurk.preloadPages(retryQuizPages);

// const KEY_1 = "65";  // a
// const KEY_2 = "83";  // s
// const KEY_3 = "68";  // d
// const KEY_4 = "70";  // f
// const KEY_5 = "74";  // j
// const KEY_6 = "75";  // k
// const KEY_7 = "76";  // l
// const KEY_8 = "186";  // ;
// const KEY_CODES = [KEY_1, KEY_2, KEY_3, KEY_4, KEY_5, KEY_6, KEY_7, KEY_8];
// const KEY_NAMES = ["<a>","<s>","<d>","<f>","<j>","<k>","<l>","<;>"];

const KEY_1 = '81'; // q
const KEY_2 = '87'; // w
const KEY_3 = '69'; // e
const KEY_4 = '82'; // r
const KEY_5 = '86'; // v
const KEY_6 = '66'; // b
const KEY_7 = '85'; // u
const KEY_8 = '73'; // i
const KEY_9 = '79'; // o
const KEY_10 = '80'; // p
//const KEY_5_ALT = '59'; // ; on other browsers
// See https://unixpapa.com/js/key.html
const KEY_CODES = [KEY_1, KEY_2, KEY_3, KEY_4, KEY_5, KEY_6, KEY_7, KEY_8, KEY_9, KEY_10];
//const KEY_CODES_ALT = [KEY_1, KEY_2, KEY_3, KEY_4, KEY_5_ALT];
const KEY_NAMES = ['<q>', '<w>', '<e>', '<r>', '<v>', '<b>', '<u>', '<i>', '<o>', '<p>'];

const QuizData = [];
const TaskData = [];

function appendTaskData(data) {
  TaskData.push(data);
}

function appendQuizData(data) {
  QuizData.push(data);
}

function compressJSONData(data) {
  const pakoDataEncoded64 = btoa(pako.deflate(JSON.stringify(data), { to: 'string' }));
  return pakoDataEncoded64;
}

function recordQuizData() {
  recordCompressedData(QuizData, 'compressed_quiz_data');
}

function recordTaskData() {
  recordCompressedData(TaskData, 'compressed_task_data');
}

function recordCompressedData(data, field) {
  const compressedData = compressJSONData(data);
  psiTurk.recordUnstructuredData(field, compressedData);
}

class Keymap {
  constructor() {
    this.state = {};
    for (let i = 0; i < KEY_CODES.length; i += 1) {
      this.state[KEY_CODES[i]] = false;
      //this.state[KEY_CODES_ALT[i]] = false;
    }
  }

  get nKeys() {
    return this.chord.reduce((a, b) => a + b);
  }

  get chord() {
    const chord = new Array(KEY_CODES.length).fill(false);
    for (let i = 0; i < KEY_CODES.length; i += 1) {
      chord[i] = this.state[KEY_CODES[i]] //|| this.state[KEY_CODES_ALT[i]];
    }
    return chord;
  }

  get length() {
    return this.state.length;
  }
}

const ISI = 50; // to match ECoG data
const CHORD_TIMEOUT = 100;
const MAX_TRIAL_TIME_MS = 60000;
const SAVE_PER_TRIALS = 250; // Save data to server after every n trials

// from https://stackoverflow.com/questions/11833759/add-stylesheet-to-head-using-javascript-in-body
function toggleStylesheet(href, onoff) {
  let existingNode = 0; // get existing stylesheet node if it already exists:
  for (let i = 0; i < document.styleSheets.length; i += 1) {
    if (document.styleSheets[i].href && document.styleSheets[i].href.indexOf(href) > -1) {
      existingNode = document.styleSheets[i].ownerNode;
    }
  }
  if (onoff === undefined) {
    onoff = !existingNode; // toggle on or off if undefined
  }
  if (onoff) { // TURN ON:
    if (existingNode) return onoff; // already exists so cancel now
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.type = 'text/css';
    link.href = href;
    document.getElementsByTagName('head')[0].appendChild(link);
  } else if (existingNode) { // TURN OFF:
    existingNode.parentNode.removeChild(existingNode);
  }
  return onoff;
}

/*
 ********************
 * MOTOR TASK       *
 ********************
 */
function MotorTask(nodes, queries, fingerCombinations, hints, stage, color, stimPerBlock) {
  const deferred = Q.defer();

  let node = 0;
  let query = 0;
  let nextQuery = 0;
  let targetChord;
  let prevTargetChord;
  let trialStartTime;
  let trial = -1;
  let nTries = 1;
  let listening = false; // Currently listening
  let canListen = false; // Listen once no keys are pressed
  let trialTimer = null;
  let chordTimer = null;
  let correct = false;
  let chord = null;
  let rt = 0;
  let keyCode = null;
  let block = 1;
  let score = 0;
  let prev_score = 0;
  let blockAcc = 0;
  var blockStart = new Date().getTime();
  

  // if we weren't passed queries, set it to zeros
  if (queries === null) {
    queries = new Array(nodes.length).fill(0);
  }

  /**
     * Toggles the target for an individual finger on or off
     * @param {integer} finger - which finger to toggle
     * @param {integer} state - On/Off
     */
  function toggleTarget(finger, state) {
    if (state) {
      $(`#target-${finger}`).addClass(color);
    } else {
      $(`#target-${finger}`).removeClass(color);
    }
  }

  /**
     * Sets the full array of targets
     * @param {array} fingers - Array of booleans, true/false for each finger
     */
  function showTargets(fingers) {
    for (let t = 0; t < fingers.length; t += 1) {
      toggleTarget(t + 1, fingers[t]);
    }
  }

  function hideTargets() {
    for (let t = 0; t < KEY_CODES.length; t += 1) {
      toggleTarget(t + 1, false);
    }
  }

  // Keep a dictionary of key states, true or false
  const keymap = new Keymap();

  function checkListen() {
    // Check if keys are released, and we should be listening.
    if (keymap.nKeys === 0 && canListen) {
      listening = true;
    }
  }

  function showHints(fingers) {
    let used = 0;
    let hintString = 'Press ';
    for (let t = 0; t < fingers.length; t += 1) {
      if (fingers[t]) {
        if (used === 0) {
          hintString += KEY_NAMES[t];
        } else {
          hintString += ' and ';
          hintString += KEY_NAMES[t];
        }
        used += 1;
      }
    }
    $('#notice').text(hintString);
  }

  function showPoints(points) {
    // show points, and display at the bottom
    $('#flag').text("Score: " + points);
  }


  function finish() {
    $('body').unbind('keydown', keydownFn);
    $('body').unbind('keyup', keyupFn);
    psiTurk.showPage('waiting.html');
  }

  function success() {
    finish();
    psiTurk.recordUnstructuredData(`completed_${stage}`, true);
    recordTaskData();
    psiTurk.saveData({ success: deferred.resolve });
  }

  function failure() {
    finish();
    psiTurk.recordUnstructuredData(`failed_${stage}`, true);
    recordTaskData();
    psiTurk.saveData({ success: deferred.reject });
  }

  function next() {
    if (nodes.length === 0 && nextQuery === 0) {
      success();
    } else {
      if (nextQuery > 0) { // Is this trial a query?
        query = nextQuery;
        nextQuery = 0;
        $('#target-wrapper').hide();
        if (query === 1) {
         $('#notice')
            .html('Repeat the key combo from the <span style="color:red">LAST</span> trial!');
        } else if (query === 2) {
          targetChord = prevTargetChord;
          $('#notice')
            .html('Repeat the key combo from <span style="color:red">TWO trials ago</span>!');
        } else {
          console.log(`Invalid query number: ${query}`);
        }
      } else { // Normal trial
        if (query > 0) { // Do we need to clean up from a query?
          $('#target-wrapper').show();
          $('#notice').text('');
          query = 0;
        }
        node = nodes.shift();
        nextQuery = queries.shift();
        prevTargetChord = targetChord;
        targetChord = fingerCombinations[node];
        trial += 1;
        if (trial % SAVE_PER_TRIALS === 0) {
          recordTaskData();
          psiTurk.saveData();
        }
        showTargets(targetChord);
        if (hints) {
          showHints(targetChord);
        } else {
          showPoints(score)
        }
      }
      trialTimer = setTimeout(failure, MAX_TRIAL_TIME_MS);
      $('#error').text('');
      nTries = 1;
      trialStartTime = new Date().getTime()
      canListen = true;
      checkListen();
      //checkSwitch();
    }
  }

  function cleanupTrial() {
    if (query > 0) {
      console.log(correct);
    }
    canListen = false;
    clearTimeout(trialTimer);
    clearTimeout(chordTimer);
    chordTimer = null;      
    if (ISI > 0) {
      hideTargets();
      setTimeout(next, ISI);
    } else {
      next();
    }
  }

  function checkSwitch() {
    // check if it is time to switch blocks
    if ((trial % stimPerBlock === 0) && (trial != 0)) {
      switchBlock();
      blockStart = new Date().getTime();
      block += 1;
      blockAcc = 0;
    }
  }

  function logTrial(event) {
    const trialRecord = {
      phase: 'task',
      stage,
      trial,
      node,
      correct,
      nTries,
      rt,
      response: chord.map(Number),
      target: targetChord.map(Number),
      keyCode,
      event,
      query,
    };
    appendTaskData(trialRecord);
  }

  function trialError() {
    if (query > 0) { // Record our data, right or wrong
      cleanupTrial();
    } else {
      nTries += 1;
      $('#error').text('Error!');
    }
  }

  function checkChord() {
    listening = false; // Force key release
    ({ chord } = keymap);
    correct = _.isEqual(targetChord, chord);
    if (correct) {
      logTrial('correct');
      blockAcc += 1
      cleanupTrial();
    } else {
      logTrial('incorrect');
      trialError();
    }
  }

  function keyupFn(e) {
    e = e || event; // to deal with IE

    ({ keyCode } = e);
    const prevState = keymap.state[keyCode];
    const validKey = prevState !== undefined;
    if (validKey) {
      if (listening) {
        checkChord();
      }
      keymap.state[keyCode] = e.type === 'keydown';
    }
    checkListen();
  }

  function keydownFn(e) {
    e = e || event; // to deal with IE

    ({ keyCode } = e);
    const prevState = keymap.state[keyCode];
    const validKey = prevState !== undefined;
    if (validKey) {
      keymap.state[keyCode] = e.type === 'keydown';
    }
    rt = new Date().getTime() - trialStartTime;
    if (listening && validKey && prevState !== true) {
      clearTimeout(chordTimer);
      if (keymap.nKeys > 1) {
        checkChord();
      } else {
        chordTimer = setTimeout(checkChord, CHORD_TIMEOUT);
      }
    }
  }

  // Load the stage.html snippet into the body of the page
  psiTurk.showPage('stage10.html');
  $('#notice').text('Press any key to begin');

  function startFn() {
    // Register the response handler that is defined above to handle any
    // key down events.
    $('body').unbind('keyup', startFn);

    $('#notice').text('');
    $('body').focus().keydown(keydownFn);
    $('body').focus().keyup(keyupFn);

    // Start the test
    next();
  }

  function switchBlock() {
    // stop 1 minute timer
    clearTimeout(trialTimer);
    
    // block end screen
    psiTurk.showPage('block_end.html');
    $('body').unbind('keyup', keyupFn);
    $('body').unbind('keydown', keydownFn);
    $('#notice').text("You just finished block " + block + " out of 4.");
    $('#notice2').text("Ready to see your score? Press any key to continue")

    // display for switching blocks
    prev_score = score;
    const currentTime = new Date().getTime();
    score = Math.round(score + (100/(currentTime - blockStart)/stimPerBlock)*1000);
    $('body').focus().keypress(moveToScore);
    $('body').blur()
  }


  function animateScore(ID) {
    // for timeout function
    var disp = prev_score;

    ID = setTimeout( function() {
      $('#notice2').text(disp);
      //increase display by one
      if (disp < score) {
        disp += 1;
      } else { 
        //when display equals score, stop animation
        disp = score;
        clearInterval(ID);
      }
    }, 10);
  };

  function moveToScore() {
    // Register the response handler that is defined above to handle any
    // key down events.
    //$('body').unbind('keydown', moveToScore);

    // move to next screen
    psiTurk.showPage('show_score.html');
    $('#notice').text("Great job! Your score is");

    var animation
    //animateScore(animation)
    $('#notice2').text(score);
    $('#notice3').text("and your accuracy is: " + blockAcc);
    $('#notice4').text("Try to respond even faster in the next block to increase your score!");
    $('#notice5').text("Ready? Press any key to continue");
    $('body').focus().keypress(resetBlock);
    $('body').blur()
  }

  function resetBlock() {
    //$('body').unbind('kepup', resetBlock);
    psiTurk.showPage('stage10.html');
    $('#notice').text('Press any key to begin');
    $('body').focus().keypress(function() {
      $('#notice').text('');
      $('body').focus().keydown(keydownFn);
      $('body').focus().keyup(keyupFn);

      // Start the test
      next();
    });
  }

  $('body').focus().keyup(startFn);

  return deferred.promise;
}


function Quiz(qid) {
  const deferred = Q.defer();

  let ansResponses = [];
  let quizData;
  let qNumber;
  let listening = false;
  let timestamp;

  function responseHandler(e) {
    if (!listening) return;

    const { keyCode } = e;
    let response = 0;

    switch (keyCode) {
      case 49: // 1
        response = 1;
        break;
      case 50: // 2
        response = 2;
        break;
      case 51: // 3
        response = 3;
        break;
      default: // everything else
        response = 0;
        break;
    }
    if (response > 0) {
      listening = false;
      ansResponses.push(response);
      const currentTime = new Date().getTime();
      const rt = currentTime - timestamp;
      qNumber += 1;
      const data = {
        phase: 'quiz',
        qid,
        responses: ansResponses,
        rt,
      };
      appendQuizData(data);
      if (qNumber === quizData.questions.length) {
        checkFinish();
      } else {
        nextQuestion();
      }
    }
  }

  function checkFinish() {
    $.ajax({
      // send this user's unique id and get stimuli back
      url: '/check_quiz',
      contentType: 'application/json',
      data: JSON.stringify({
        qid,
        q_order: quizData.q_order,
        a_order: quizData.a_order,
        answers: ansResponses,
      },
      null, '\t'),
      type: 'POST',
      success: (data) => {
        if (data.result) {
          success();
        } else {
          retry();
        }
      },
    });
  }

  function success() {
    recordQuizData();
    $('body').unbind('keydown', responseHandler);
    deferred.resolve();
  }

  function retry() {
    recordQuizData();
    showInstructions(true);
  }

  function loadQuiz() {
    return $.ajax({
      url: '/quiz',
      data: { qid },
      success: (data) => {
        quizData = data;
      },
    });
  }

  function startQuiz() {
    psiTurk.showPage('quiz.html');
    qNumber = 0;
    ansResponses = [];
    nextQuestion();
  }

  function nextQuestion() {
    $('#question').text(quizData.questions[qNumber]);
    $('#answer1').text(quizData.answers[qNumber][0]);
    $('#answer2').text(quizData.answers[qNumber][1]);
    $('#answer3').text(quizData.answers[qNumber][2]);
    timestamp = new Date().getTime();
    listening = true;
  }

  function showInstructions(repeat) {
    const doLoadQuiz = loadQuiz();
    let quizPages = instructionPages[qid - 1];
    if (repeat) { // Tack on instructions that we're repeating the quiz if they failed
      quizPages = retryQuizPages.concat(quizPages);
    }
    psiTurk.doInstructions(
      quizPages,
      () => {
        doLoadQuiz.then(startQuiz);
      },
    );
  }

  $('body').focus().keydown(responseHandler);

  showInstructions(false);

  return deferred.promise;
}

/**
* Questionnaire *
*/
function Questionnaire() {
  const errorMessage = "<h1>Oops!</h1><p>Something went wrong submitting your HIT. This might happen if you lose your internet connection. Press the button to resubmit.</p><button id='resubmit'>Resubmit</button>";

  function recordResponses() {
    psiTurk.recordTrialData({ phase: 'postquestionnaire', status: 'submit' });

    $('textarea').each((i, elem) => {
      psiTurk.recordUnstructuredData($(elem).id, $(elem).value);
    });
    $('select').each((i, elem) => {
      psiTurk.recordUnstructuredData($(elem).id, $(elem).value);
    });
  }

  function resubmit() {
    $('body').html = '<h1>Trying to resubmit...</h1>';
    const reprompt = setTimeout(promptResubmit, 10000);

    psiTurk.saveData({
      success: () => {
        clearInterval(reprompt);
        psiTurk.completeHIT();
        // psiTurk.computeBonus('compute_bonus', () => {
        // psiTurk.completeHIT(); // when finished saving compute bonus, the quit
        // });
      },
      error: promptResubmit,
    });
  }

  function promptResubmit() {
    $('body').html = errorMessage;
    $('#resubmit').click(resubmit);
  }

  // Load the questionnaire snippet
  psiTurk.showPage('postquestionnaire.html');
  psiTurk.recordTrialData({ phase: 'postquestionnaire', status: 'begin' });

  $('#next').click(() => {
    recordResponses();
    psiTurk.saveData({
      success: () => {
        // psiTurk.computeBonus('compute_bonus', () => {
        psiTurk.completeHIT(); // when finished saving compute bonus, the quit
        // });
      },
      error: promptResubmit,
    });
  });
}


function FreeResponse() {
  const deferred = Q.defer();

  psiTurk.showPage('free_response.html');

  $('#next').click(() => {
    const response = $('textarea').val();
    psiTurk.recordUnstructuredData('free_response_question', response);
    psiTurk.saveData({ success: deferred.resolve });
  });

  return deferred.promise;
}


function Results() {
  const deferred = Q.defer();

  function showResults() {
    $.ajax({
      url: '/post_bonus',
      contentType: 'application/json',
      data: JSON.stringify({ uniqueId }, null, '\t'),
      type: 'POST',
      success: (data) => {
        // const totalBonus = parseFloat(Math.round(data.total_bonus * 100) / 100).toFixed(2);

        if (data.walk_one_perf === null) {
          $('#r1').text('Part Two Score: Incomplete');
          $('#p1').text('Part Two Performance Bonus: $0');
        } else {
          const walkOnePerformance = parseFloat(Math.round(data.walk_one_perf * 10000) / 100)
            .toFixed(1);
          const walkOneBonus = parseFloat(Math.round(data.walk_one_bonus * 100) / 100)
            .toFixed(2);
          $('#r1').text(`Part Two Score: ${walkOnePerformance}% Correct`);
          $('#p1').text(`Part Two Performance Bonus: $${walkOneBonus}`);
        }
        // if (data.walk_two_perf === null) {
        //   $('#r2').text('Part Three Score: Incomplete');
        //   $('#p2').text('Performance Bonus: $0');
        // } else {
        //   const walkTwoPerformance = parseFloat(Math.round(data.walk_two_perf * 10000) / 100)
        //     .toFixed(1);
        //   const walkTwoBonus = parseFloat(Math.round(data.walk_two_bonus * 100) / 100)
        //     .toFixed(2);
        //   $('#r2').text(`Part Three Score: ${walkTwoPerformance}% Correct`);
        //   $('#p2').text(`Part Three Performance Bonus: $${walkTwoBonus}`);
        // }
        // $('#total').text(`Overall Total: $${totalBonus}`);
      },
    });
  }

  psiTurk.showPage('results.html');

  $('#next').click(deferred.resolve);

  showResults();

  return deferred.promise;
}

/*
 ******************
 * Run Task
 *****************
 */
const jspsychExperiments = {
  ravens: {
    page: 'jspsych/ravens.html',
    timeline: make_ravens_experiment(mode),
    id: 'ravens',
    stylesheets: [
      '/static/css/jspsych/jspsych.css',
      '/static/css/jspsych/default_style.css',
      '/static/css/ravens/style.css',
    ],
    display_element: 'getDisplayElement',
  },

  'n-back': {
    page: 'jspsych/n-back.html',
    timeline: make_n_back_experiment(mode),
    id: 'n-back',
    stylesheets: [
      '/static/css/jspsych/jspsych.css',
      '/static/css/jspsych/default_style.css',
      '/static/css/n-back/style.css',
    ],
    display_element: 'getDisplayElement',
  },

  'temp-discount': {
    page: 'jspsych/discount.html',
    timeline: make_temp_discount(),
    id: 'temp-discount',
    stylesheets: [
      '/static/css/jspsych/jspsych.css',
      '/static/css/jspsych/default_style.css',
    ],
  },
};

// Preload experiment pages
const jspsychPages = Object.values(jspsychExperiments).map(x => x.page);
psiTurk.preloadPages(jspsychPages);

function runJspsychExp(exp) {
  const deferred = Q.defer();

  psiTurk.showPage(exp.page);

  exp.stylesheets.map(url => toggleStylesheet(url, 1));

  const opts = {
    timeline: exp.timeline,
    fullscreen: false, // changed to be consistent with graph learning part
    on_trial_finish: (data) => { // eslint-disable-line no-unused-vars
      addID(exp.id);
    },

    on_finish: (data) => { // eslint-disable-line no-unused-vars
      exp.stylesheets.map(url => toggleStylesheet(url, 0));

      // Serialize the data
      const promise = new Promise((resolve) => {
        const jsPsychData = jsPsych.data.getData();
        resolve(jsPsychData);
      });

      promise.then((jsPsychData) => {
        recordCompressedData(jsPsychData, exp.id);
      }).then(deferred.resolve);
    },
  };

  if (exp.display_element) {
    opts.display_element = exp.display_element;
  }

  jsPsych.init(opts);

  return deferred.promise;
}

async function experiment() {
  function initSubject() {
    return Q($.ajax({
      url: '/init',
      contentType: 'application/json',
      data: JSON.stringify({ uniqueId }, null, '\t'),
      type: 'POST',
    }));
  }

  function getFingerMapping() {
    return Q($.ajax({ url: '/get_finger_mapping' }));
  }

  function getWalk() {
    return Q($.ajax({ url: '/get_walk', data: { uniqueId } }));
  }

  function doFailure() {
    const deferred = Q.defer();
    psiTurk.showPage('failed.html');
    $('#next').click(deferred.resolve);
    return deferred.promise;
  }

  function InstructionsDeferred(pages) {
    const deferred = Q.defer();
    psiTurk.doInstructions(pages, deferred.resolve);
    return deferred.promise;
  }

  try {
    // ----- Setup
    await initSubject();
    const fingerMappingResponse = await getFingerMapping();
    const fingerMapping = fingerMappingResponse.finger_mapping;
    const walk = await getWalk();
    // -----

    // ----- n-back
     //await InstructionsDeferred(instructionsOverview);
     //await InstructionsDeferred(readyNBack);
     //await runJspsychExp(jspsychExperiments['n-back']);

    // ----- Instructions and Demo
    //await Quiz(1); // commented so testing is faster
    //await psiTurk.finishInstructions();
    //await InstructionsDeferred(readyDemo);
    //await MotorTask(walk.demo, null, fingerMapping, true, 'demo', 'red', 250);
    // -----

    // ----- Experiment
    //await InstructionsDeferred(readyWalkOne);
    await MotorTask(walk.walk_one, null, fingerMapping, false, 'walk_one', 'red', 5);
    // -----

    // // ----- Walk 2
    // await InstructionsDeferred(instructionsWalkTwo);
    // await InstructionsDeferred(readyWalkTwo);
    // await MotorTask(walk.walk_two, walk.nback_queries, fingerMapping, false, 'walk_two', 'red');
    // // -----

    // ----- ERROR HANDLING
  } catch (err) {
    if (mode === 'debug') {
      console.log(err);
    }
    await doFailure();
  }
  // -----

  // ----- Cleanup
  await FreeResponse();
  await Results();
  await Questionnaire();
  // -----
}

$.ajaxSetup({
  dataType: 'json',
  shouldRetry: 5,
  data: { uniqueId },
});

$(window).load(experiment);
