$(function() {
  var classified_response = null;
  $('#question').material_select();
  $('#categories').hide();
  $('#grade').on('click', gradeResponse);
  $('#grade').leanModal();
  $('#confirm-response').on('click', createNewResponse);
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

function selectQuestion(){
 var question = $('#question option:selected').val();

 $.ajax({
     url: '/grader/getcategories',
     data: {question_id: question},
     type: 'POST',
     success: function(response) {
       console.log(response);
       addCategoryOpts(response);
       classified_response = response;
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
