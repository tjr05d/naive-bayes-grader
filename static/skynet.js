$(function() {
  $('#question').material_select();
  $('#categories').hide();
  $('#grade').on('click', gradeResponse);


});

function gradeResponse(event){
  event.preventDefault();
  var answer = $('#response_text').val()
  var category = $('#category').val()
  var question_id = $('#question').val()
  $.ajax({
      url: '/grader/classify',
      data: {answer: answer, category: category, question_id: question_id},
      type: 'POST',
      success: function(response) {
        console.log(response);
        appendResponse(response);
        templateAppend(response);
        selectQuestion();
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


function templateAppend(response) {
  var option_html = "";

  for(i = 0; i < response.probabilities.length; i++){
    option_html.concat("<option>"+response.probabilities[i][0]+"</option>");
  }
  var template = "<div><select id='category'name='category'>"+ option_html+ "</select></div>"
    $('#template-test').append(template);
}

function selectQuestion() {
 var question = $('#question option:selected').val();
 console.log(question);
 $.ajax({
     url: '/grader/getcategories',
     data: {question_id: question},
     type: 'POST',
     success: function(response) {
       console.log(response);
       addCategoryOpts(response);
     },
     error: function(error) {
         console.log(error);
     }
 });
}

function addCategoryOpts(categories){
  var options = "";
  var select= $('#categories');

  for(cat in categories){
   options+=("<option value=\"" +cat +"\">"+ categories[cat] + "</option>");
 };

 select.append(options).material_select().show();
}
