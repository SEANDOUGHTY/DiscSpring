$('#submit').click(function(){
    data = $('#dataForm').serializeArray();
    
    $.ajax({
    url: '/force.png',
    type: 'POST',
    data: data,
    success: function(response) {
      $("#force_image").attr('src', response);
   },
   error: function(xhr) {
     //Do Something to handle error
  }
  }).done(function(){

  $.ajax({
    url: '/stress.png',
    type: 'POST',
    data: data,
    success: function(response) {
      $("#stress_image").attr('src', response);
  },
  error: function(xhr) {
    //Do Something to handle error
  }
  });
  })

});
