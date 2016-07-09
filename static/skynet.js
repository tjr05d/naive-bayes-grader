$(function() {
  //variables
  classified_response = null;
  responseCards = [];
  cardCounter = 1;
//hide elements on pageload

  $('#categories').hide();
  $('#response-menu').hide();
  $('#next_card').hide();
  $('#user-reaction-buttons').hide();

//add materialize elememts
  $('#question').material_select();
  $('#training_question').material_select();
  $('#test_cat').material_select();
  $('#new-cat-button').leanModal();

  //event listeners
  $('#grade').on('click', gradeResponse);
  $('#confirm-response').on('click', createNewResponse);
  $('#training_question').on('change', trainingQuestion);
  $('body').on('click', '#next_card',  nextCard);
  $('body').on('click', '#new-cat-button', newCat);
  $('#cat_form_submit').on('click', submitCatForm);
  $('#cat_form_cancel').on('click', closeModal);
  $('#training-submit').on('click', submitTrainingResponse);
  $('#correct-response').on('click', clearResponse);
});

function gradeResponse(event){
  event.preventDefault();
  var answer = $('#response_text').val()
  var question_id = $('#question').val()
  var appendSelector = $('#categories');
  var questionSelector = $('#question option:selected').val();
  $.ajax({
      url: '/grader/classify',
      data: {answer: answer, question_id: question_id},
      type: 'POST',
      success: function(response) {
        console.log(response);
        appendResponse(response);
        selectQuestion(questionSelector, appendSelector);
      },
      error: function(error) {
          console.log(error);
      }
  });
  renderMarkdown(answer);
}

function appendResponse(response) {
  var feedbackDiv = $('#grading-response');
  var suggestedFeedback = ['<div id="feedback-card">',
                            '<div id="feedback-header">',
                            '<h6>',
                            response.category,
                            '</h6>',
                            '</div>',
                            '<div id="feedback-content>"',
                            '<p>',
                            marked(response.feedback),
                            '</p>',
                            '</div>',
                            '</div>'
                           ]
  feedbackDiv.append(suggestedFeedback.join(""));

  var probabilities = response.probabilities;

  var chartArray = []
  for(i = 0; i < probabilities.length; i++){
    chartArray.push([probabilities[i][0], probabilities[i][1]])
  }
  $('#user-reaction-buttons').show();
  $('#graph').highcharts({
          chart: {
              plotBackgroundColor: null,
              plotBorderWidth: null,
              plotShadow: false,
              type: 'pie'
          },
          title: {
              text: 'Category Probabilities'
          },
          tooltip: {
              pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
          },
          plotOptions: {
              pie: {
                  allowPointSelect: true,
                  cursor: 'pointer',
                  dataLabels: {
                      enabled: true,
                      format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                      style: {
                          color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                      }
                  }
              }
          },
          series: [{
              name: 'Category Probabilities',
              colorByPoint: true,
              data: chartArray
          }]
      });
}

function selectQuestion(questionSelector, appendSelector){
 var question = questionSelector;

 $.ajax({
     url: '/grader/getcategories',
     data: {question_id: question},
     type: 'POST',
     success: function(response) {
       console.log(response);
       addCategoryOpts(response, appendSelector);
       classified_response = response;
     },
     error: function(error) {
         console.log(error);
     }
 });
}

function addCategoryOpts(categories, appendSelector, placeholderText){
  var options = "";
  var select= appendSelector;

  options += '<option value= "" disabled selected>Categorize</option>'

  for(cat in categories){
   options+=("<option value=\"" +cat +"\">"+ categories[cat] + "</option>");
 };
 console.log(options);
 select.append(options).material_select();
}

function createNewResponse(){
  var answer = $('#response_text').val()
  var question_id = $('#question').val()
  var category = $('#categories').val()

  $.ajax({
      url: '/grader/create_response',
      data: {answer: answer, category: category, question_id: question_id},
      type: 'POST',
      success: function(response) {
        console.log(response);
      },
      error: function(error) {
          console.log(error);
      }
  });

}
//Functions for the training area
function trainingQuestion(){
  var training_question_id = $('#training_question').val();
  console.log(training_question_id);

  $.ajax({
    url: '/grader/training_question_responses',
    data: {question_id: training_question_id},
    type: 'POST',
    success: function(response) {
      console.log(response);
      createCards(response);
    },
    error: function(error) {
        console.log(error);
    }
  });
}
  function createCards(responses){
    var card = $('#card')
    var i = 0;
    for( key in responses){
      var material_card = ['<div id="response-id-div">',
                          '<span id="response-id-title">',
                          'Response ID: ',
                          '</span>',
                          '<span id="response-id">',
                          key,
                          '</span>',
                          '</div>',
                          '<div id="response-text">',
                          responses[key],
                          '</div>'
                      ]
     responseCards.push(material_card.join(""));
   };
   if(responseCards[0]){
     $('#placeholder-screen').remove();
     card.empty();
     card.append(responseCards[0]);
     $('#next_card').show();
     $('#response-menu').show();
     populateCatSelect();
   } else {
     card.empty();
     card.append("There are no responses to this question yet")
   }
  }

function nextCard(){
  var card = $('#card')
  //changed the append because the select will not populate on the materailize card, going to have to customize this
  // var appendCard = $('#add_cat');
  var appendCard = $('#test_cat');
  // var questionSelector = $('#training_question option:selected').val();
  card.empty();
  appendCard.empty();
  if(responseCards[cardCounter]){
    card.append(marked(responseCards[cardCounter]));
    cardCounter += 1;
  } else {
    responseCards = [];
    cardCounter = 1;
    card.append("Yay select another question!");
  }
  // selectQuestion(questionSelector, appendCard);
  populateCatSelect();
}

function populateCatSelect(){
  var appendCard = $('#test_cat');
  var questionSelector = $('#training_question option:selected').val();
  selectQuestion(questionSelector, appendCard);
}

//Functions to create new categories in the training area
function newCat(){
  $('#cat_form').show();
}

function cancelNewCat(){
  $("#title").empty();
  $("#feedback").empty();
  $('#cat_form').hide();
}

function submitCatForm(){
  var title = $("#title").val();
  var feedback = $("#feedback").val();
  var question_id = $('#training_question').val();

  $.ajax({
      url: '/grader/categories',
      data: {title: title, feedback: feedback, question_id: question_id},
      type: 'POST',
      success: function(response) {
        console.log(response);
      },
      error: function(error) {
          console.log(error);
      }
  });
}

function closeModal(){
  $('.modal').closeModal();
}

function submitTrainingResponse(){
  var role = $('input:checked').val();
  var responseId = $('span#response-id').text();
  var categoryId = $('#test_cat option:selected').val();
  console.log(categoryId);

  $.ajax({
      url: '/grader/response_role',
      data: {response_id: responseId, role: role, category_id: categoryId},
      type: 'PUT',
      success: function(response) {
        console.log(response);
      },
      error: function(error) {
          console.log(error);
      }
  });
  nextCard();
}

function renderMarkdown(input){
  var markdownResponse = ['<div id="markdown-reponse" style= "background-color:white; color: blue; padding: 18px;">',
                          marked(input),
                          '</div>'
                          ]

  $('#response_text').replaceWith(markdownResponse.join(""));
  $('#grade, #markdown-remove').hide();
}

function clearResponse(){
  $('#response-input').load(document.URL +  ' #response-input');
  $('#graph, #grading-response, #categories').empty();
  $('#user-reaction-buttons').hide();
  $('#grade').show();
}
  //first be able to return all of the responses that are not classified already
  //give the user a way to select or create a category for that response
