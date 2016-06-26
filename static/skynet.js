$(function() {
  //variables
  classified_response = null;
  responseCards = [];
  cardCounter = 1;
//hide elements on pageload
  $('#cat_form').hide();
  $('#categories').hide();
  $('#response-menu').hide();

//add materialize elememts
  $('#question').material_select();
  $('#training_question').material_select();
  $('#test_cat').material_select();
  $('#grade').leanModal();

  //event listeners
  $('#grade').on('click', gradeResponse);
  $('#confirm-response').on('click', createNewResponse);
  $('#training_question').on('change', trainingQuestion);
  $('body').on('click', '#next_card',  nextCard);
  $('body').on('click', '#new_cat', newCat);
  $('#cat_form_submit').on('click', submitCatForm);


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

}

function appendResponse(response) {
  var response_list = $('#ajax-test');
  var suggested_category = response.category;
  var new_response = "<h6>Here's how I would grade this response: "+ suggested_category+"</h6>"
  response_list.append(new_response);

  var probabilities = response.probabilities;
  for(i = 0; i < probabilities.length; i++){
    response_list.append("<p><bold>Category: </bold>"+ probabilities[i][0]+"<bold>  probability: </bold>"+ probabilities[i][1]+"</p>");
  };
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

  options += '<option value= "" disabled selected>Select a Category</option>'

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
      var material_card = ['<div class="row">',
                       '<div class="col s12 m6">',
                       '<div class="card">',
                       '<div class="card-content">',
                       '<span class="card-title">',
                       key,
                       '</span>',
                       '<p>',
                       responses[key],
                       '</p>',
                       '<select id="add_cat" name=category></select>',
                       '</div>',
                       '<div class="card-action">',
                       '</div>',
                       '</div>',
                       '</div>',
                       '</div>',
                       '<a id="next_card" class="waves-effect waves-light btn">Next</a>']
     responseCards.push(material_card.join(""));
   };
   if(responseCards[0]){
     $('#placeholder-screen').remove();
     card.empty();
     card.append(responseCards[0]);
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
    var questionSelector = $('#training_question option:selected').val();;
    card.empty();
    appendCard.empty();
    $('#response-menu').show();
    if(responseCards[cardCounter]){
    card.append(responseCards[cardCounter]);
    cardCounter += 1;
  } else {
    responseCards = [];
    cardCounter = 1;
    card.append("Yay select another question!");
  }
    selectQuestion(questionSelector, appendCard);
  }

//Functions to create new categpries in the training area
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

  //first be able to return all of the responses that are not classified already
  //give the user a way to select or create a category for that response
