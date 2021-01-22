/**
 * jspsych6-call-function
 * plugin for calling an arbitrary function during a jspsych6 experiment
 * Josh de Leeuw
 *
 * documentation: docs.jspsych6.org
 *
 **/

jsPsych6.plugins['call-function-6'] = (function() {

  var plugin = {};

  plugin.info = {
    name: 'call-function',
    description: '',
    parameters: {
      func: {
        type: jsPsych6.plugins.parameterType.FUNCTION,
        pretty_name: 'Function',
        default: undefined,
        description: 'Function to call'
      },
      input_1: {
        type: jsPsych6.plugins.parameterType.INT,
        pretty_name: 'input1',
        default: null,
        description: 'input1'
      },
      input_2: {
        type: jsPsych6.plugins.parameterType.INT,
        pretty_name: 'input2',
        default: null,
        description: 'input2'
      },
      input_3: {
        type: jsPsych6.plugins.parameterType.INT,
        pretty_name: 'input3',
        default: null,
        description: 'input3'
      }
    }
  }

  plugin.trial = function(display_element, trial) {
    trial.post_trial_gap = 0;
    var return_val = trial.func(trial.input_1, trial.input_2, trial.input_3);

    var trial_data = {
      value1: return_val[0],
      value2: return_val[1],
      value3: return_val[2],
      value4: return_val[3],
      value5: return_val[4]
    };

    jsPsych6.finishTrial(trial_data);
  };

  return plugin;
})();
