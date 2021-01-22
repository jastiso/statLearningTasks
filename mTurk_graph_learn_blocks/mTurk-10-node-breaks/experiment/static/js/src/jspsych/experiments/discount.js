var make_temp_discount = function() { //eslint-disable-line no-unused-vars
    var feedback_instruct_text = 'Welcome to this survey.<br><br> Press <strong>enter</strong> to begin.';
    var getInstructFeedback = function() {
        return '<div class = centerbox><p class = center-block-text>' + feedback_instruct_text + '</p></div>';
    };
    var sumInstructTime = 0; //ms
    var instructTimeThresh = 5;  ///in seconds
    var feedback_instruct_block = {
        type: 'poldrack-text',
        cont_key: [13],
        text: getInstructFeedback,
        timing_post_trial: 0,
        timing_response: 180000,
        data: {
            exp_id: "temp-discount"
        }
    };
    /// This ensures that the subject does not read through the instructions too quickly.  If they do it too quickly, then we will go over the loop again.
    var instructions_block = {
        type: 'poldrack-instructions',
        pages: [
            '<div class = centerbox><p class = block-text>There is no correct answer for the questions in the following task, therefore, they will not count towards your bonus. Still, we encourage you to think carefully and provide honest responses.</p></div>',
        ],
        allow_keys: false,
        show_clickable_nav: true,
        timing_post_trial: 1000,
        data: {
            exp_id: "temp-discount"
        }
    };

    var instruction_node = {
        timeline: [feedback_instruct_block, instructions_block],
        /* This function defines stopping criteria */
        loop_function: function(data) {
            for (i = 0; i < data.length; i++) {
                if ((data[i].trial_type == 'poldrack-instructions') && (data[i].rt != -1)) {
                    let rt = data[i].rt;
                    sumInstructTime = sumInstructTime + rt;
                }
            }
            if (sumInstructTime <= instructTimeThresh * 1000) {
                feedback_instruct_text =
                'Read through instructions too quickly.  Please take your time and make sure you understand the instructions.  Press <strong>enter</strong> to continue.';
                return true;
            } else if (sumInstructTime > instructTimeThresh * 1000) {
                feedback_instruct_text =
                'Done with instructions. Press <strong>enter</strong> to continue.';
                return false;
            }
        }
    };

    var end_block = {
        type: 'text',
        text: '<div class = centerbox><p class = center-block-text>Congratulations for completing this task!</p><p class = center-block-text>Press <strong>enter</strong> to continue.</p></div>',
        cont_key: [13],
        data: {
            exp_id: "temp-discount"
        }
    };

    var page_1_options = ["Now!", "I'll wait."];

    var questions = [
        {prompt: "Would you prefer $11 now, or $25 in 5 days?", options: page_1_options, required:true, horizontal: true,},
        {prompt: "Would you prefer $11 now, or $30 in 11 days?", options: page_1_options, required: true, horizontal: true,},
        {prompt: "Would you prefer $12 now, or $30 in 38 days?", options: page_1_options, required: true, horizontal: true,},
        {prompt: "Would you prefer $12 now, or $35 in 76 days?", options: page_1_options, required: true, horizontal: true,},
        {prompt: "Would you prefer $16 now, or $25 in 113 days?", options: page_1_options, required: true, horizontal: true,},
        {prompt: "Would you prefer $16 now, or $25 in 70 days?", options: page_1_options, required: true, horizontal: true,},
        {prompt: "Would you prefer $18 now, or $30 in 67 days?", options: page_1_options, required: true, horizontal: true,},
        {prompt: "Would you prefer $19 now, or $25 in 20 days?", options: page_1_options, required: true, horizontal: true,},
        {prompt: "Would you prefer $21 now, or $30 in 171 days?", options: page_1_options, required: true, horizontal: true,},
        {prompt: "Would you prefer $25 now, or $35 in 4 days?", options: page_1_options, required: true, horizontal: true,},
        {prompt: "Would you prefer $30 now, or $35 in 3 days?", options: page_1_options, required: true, horizontal: true,},
        {prompt: "Would you prefer $32 now, or $35 in 59 days?", options: page_1_options, required: true, horizontal: true,},
        {prompt: "Would you prefer $30 now, or $35 in 42 days?", options: page_1_options, required: true, horizontal: true,},
        {prompt: "Would you prefer $15 now, or $30 in 158 days?", options: page_1_options, required: true, horizontal: true,},
        {prompt: "Would you prefer $31 now, or $35 in 129 days?", options: page_1_options, required: true, horizontal: true,},
        {prompt: "Would you prefer $13 now, or $35 in 27 days?", options: page_1_options, required: true, horizontal: true,},
        {prompt: "Would you prefer $17 now, or $25 in 9 days?", options: page_1_options, required: true, horizontal: true}];


    var temp_discount=[];
    temp_discount.push(instruction_node);

    var question_order = _.shuffle(_.range(questions.length));
    for (var i in question_order){
        var multi_choice_block = {
            type: 'survey-multi-choice',
            questions: [questions[i]],
            data:{identifier:'c'},
            required:['true']
        };
        temp_discount.push(multi_choice_block);
    }

    temp_discount.push(end_block);
    return temp_discount;
};