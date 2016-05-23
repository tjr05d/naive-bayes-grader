$(function() {
  $('select').material_select();
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
      },
      error: function(error) {
          console.log(error);
      }
  });

}

function appendResponse(response) {
  console.log("I fired!");
  var response_list = $('#ajax-test');
  console.log("+++++++++");
  var suggested_category = response.category;
  console.log(suggested_category);

  var new_response = "<h6>Here's how I would grade this response: "+ suggested_category+"</h6>"
  response_list.append(new_response);

  var probabilities = response.probabilities;
  for(i = 0; i < probabilities.length; i++){
    console.log(probabilities[i]);
    response_list.append("<p><bold>Category: </bold>"+ probabilities[i][0]+"<bold>  probability: </bold>"+ probabilities[i][1]+"</p>");
  };
}
