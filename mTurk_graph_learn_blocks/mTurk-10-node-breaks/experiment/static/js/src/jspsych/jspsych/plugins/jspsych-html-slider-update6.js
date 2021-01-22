/**
 * jsPsych6-html-slider-response
 * a jsPsych6 plugin for free response survey questions
 *
 * Josh de Leeuw
 *
 * documentation: docs.jsPsych6.org
 *
 */


jsPsych6.plugins['html-slider-update'] = (function() {

  var plugin = {};

  plugin.info = { //this setup is only used in jsPsych 6, unnecessary in previous versions
    name: 'html-slider-update',
    description: '',
    parameters: {   
      dist_center: {
        type: jsPsych6.plugins.parameterType.HTML_INT,
        pretty_name: 'Dist_Center',
        default: undefined,
        description: 'Center of the Current Distribution'
      },
      placement: {
        type: jsPsych6.plugins.parameterType.HTML_INT,
        pretty_name: 'Placement',
        default: undefined,
        description: 'Placement of the square'
      },	
      pay_lb: {
        type: jsPsych6.plugins.parameterType.HTML_INT,
        pretty_name: 'Lower Payment Bound',
        default: undefined,
        description: 'Lower bound of payment structure'
      },
      pay_hb: {
        type: jsPsych6.plugins.parameterType.HTML_INT,
        pretty_name: 'Higher Payment Bound',
        default: undefined,
        description: 'Higher bound of payment structure'
      },
      percentage: {
        type: jsPsych6.plugins.parameterType.HTML_INT,
        pretty_name: 'Percentage',
        default: undefined,
        description: 'Defines the Location of the Stimulus'
      },
      min: {
        type: jsPsych6.plugins.parameterType.INT,
        pretty_name: 'Min slider',
        default: 0,
        description: 'Sets the minimum value of the slider.'
      },
      max: {
        type: jsPsych6.plugins.parameterType.INT,
        pretty_name: 'Max slider',
        default: 100,
        description: 'Sets the maximum value of the slider',
      },
      start: {
        type: jsPsych6.plugins.parameterType.INT,
        pretty_name: 'Slider starting value',
        default: undefined,
        description: 'Sets the starting value of the slider',
      },
      step: {
        type: jsPsych6.plugins.parameterType.INT,
        pretty_name: 'Step',
        default: 1,
        description: 'Sets the step of the slider'
      },
      labels: {
        type: jsPsych6.plugins.parameterType.KEYCODE,
        pretty_name:'Labels',
        default: [],
        array: true,
        description: 'Labels of the slider.',
      },
      button_label: {
        type: jsPsych6.plugins.parameterType.STRING,
        pretty_name: 'Button label',
        default:  'Continue',
        array: false,
        description: 'Label of the button to advance.'
      },
      prompt: {
        type: jsPsych6.plugins.parameterType.STRING,
        pretty_name: 'Prompt',
        default: null,
        description: 'Any content here will be displayed below the slider.'
      },
      stimulus_duration: {
        type: jsPsych6.plugins.parameterType.INT,
        pretty_name: 'Stimulus duration',
        default: null,
        description: 'How long to hide the stimulus.'
      },
      trial_duration: {
        type: jsPsych6.plugins.parameterType.INT,
        pretty_name: 'Trial duration',
        default: null,
        description: 'How long to show the trial.'
      },
      response_ends_trial: {
        type: jsPsych6.plugins.parameterType.BOOL,
        pretty_name: 'Response ends trial',
        default: true,
        description: 'If true, trial will end when user makes a response.'
      },
    }
  }
  
    plugin.trial = function(display_element, trial) {

    var html = '<div id="jsPsych6-html-slider-response-wrapper">'; //this method of updating html (creating var, then assigning to innerHTML) is specific to jsPsych 6, and will cause errors if used in the earlier jsPsych 
    html += '<div id="jsPsych6-html-slider-response-stimulus">';
    html += '<span style="display:block; width:225px; margin: 0 auto;">Most Recent Evidence: '+trial.placement+'</span></div>'; // what does the evidence say?
    html += '<div style="width: 100%">';
    html += '<div style="margin-left: auto; margin-right: auto; margin-top: 50px; width: 80%; height: 5px; position: relative; background-color: rgb(0, 0, 0);"><div style="margin-left: '+trial.percentage+'%; width: 5px; height: 50px; position: relative; background-color: rgb(255, 165, 0);"></div></div>';
    html += '<p>&nbsp;</p>'
    html += '<p>&nbsp;</p>'
    html += '<input type="range" value="'+trial.start+'" min="'+trial.min+'" max="'+trial.max+'" step="'+trial.step+'" style="margin-left:9.5%; margin-right: auto; width: 81%;" id="jsPsych6-html-slider-response-response"></input>';
    html += '<div>'
    
    //the following section creates the labels UNDER the slider, including the minimum, maximum and the continuously updating location of the slider
    
    var width = 80/(3-1);
    
    var left_offset_1 = 10+(0 * (80 /(3 - 1))) - (width/2);
    html += '<div style="display: inline-block; position: absolute; left:'+left_offset_1+'%; text-align: center; width: '+width+'%;">';
    html += '<span style="text-align: center; font-size: 80%;">'+trial.labels[0]+'</span>';
    html += '</div>'

    var left_offset_2 = 10+(1 * (80 /(3 - 1))) - (width/2);
    html += '<div style="display: inline-block; position: absolute; left:'+left_offset_2+'%; text-align: center; width: '+width+'%;">';
    html += '<span style="text-align: center; font-size: 80%;"><p>Prediction: <span id="pred"></span></p></span>';
    html += '</div>'

    var left_offset_3 = 10+(2 * (80 /(3 - 1))) - (width/2);
    html += '<div style="display: inline-block; position: absolute; left:'+left_offset_3+'%; text-align: center; width: '+width+'%;">';
    html += '<span style="text-align: center; font-size: 80%;">'+trial.labels[1]+'</span>';
    html += '</div>'

    html += '</div>';
    html += '</div>';
    html += '</div>';
	html += '<p>&nbsp;</p>'
    if (trial.prompt !== null){
      html += '<span style="display:table; margin:0 auto; font-size: 80%;">'+trial.prompt+'</span>';
    }
    // add submit button
    html += '<button id="jsPsych6-html-slider-response-next" style="margin:0 auto; display:block;" class="jsPsych6-btn">'+trial.button_label+'</button>';

    display_element.innerHTML = html;

 var slider = document.getElementById("jsPsych6-html-slider-response-response");
 var output = document.getElementById("pred"); //updating the number shown
 output.innerHTML = slider.value;

slider.oninput = function() { //updating the slider location after it's dragged
  output.innerHTML = this.value;
}

    var response = {
      rt: null,
      response: null
    };

    display_element.querySelector('#jsPsych6-html-slider-response-next').addEventListener('click', function() {
      // measure response time
      var endTime = (new Date()).getTime();
      response.rt = endTime - startTime; //currently don't use the response time in any analysis
      response.response = display_element.querySelector('#jsPsych6-html-slider-response-response').value;

      if(trial.response_ends_trial){
        end_trial();
      } else {
        display_element.querySelector('#jsPsych6-html-slider-response-next').disabled = true;
      }

    });

// 	if(trial.start==response.response){
// 		var still = 'TRUE';
// 		} else {
// 			var still = 'FALSe';
// 			}
	
	

    function end_trial(){

      jsPsych6.pluginAPI.clearAllTimeouts();

      // save data
      var trialdata = {
        "rt": response.rt,
        "start": trial.start,
        "response": response.response,
        "placement": trial.placement,
        "center": trial.dist_center,
        "LB": trial.pay_lb, //theoretically this is an updating variable that would be used to calculate the reward
        "HB": trial.pay_hb, //theoretically this is an updating variable that would be used to calculate the reward
        "current_prediction_error": Math.abs(trial.placement - trial.start),
        "update": Math.abs(trial.start - response.response),
        "learning_rate": Math.abs(trial.start - response.response)/Math.abs(trial.placement - trial.start),     
      };

      display_element.innerHTML = '';

      // next trial
      jsPsych6.finishTrial(trialdata);
    }

    if (trial.stimulus_duration !== null) {
      jsPsych6.pluginAPI.setTimeout(function() {
        display_element.querySelector('#jsPsych6-html-slider-response-stimulus').style.visibility = 'hidden';
      }, trial.stimulus_duration);
    }

    // end trial if trial_duration is set
    if (trial.trial_duration !== null) {
      jsPsych6.pluginAPI.setTimeout(function() {
        end_trial();
      }, trial.trial_duration);
    }

    var startTime = (new Date()).getTime();
  };

  return plugin;
})();
