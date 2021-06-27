$(document).ready(function() {
    $.datetimepicker.setLocale('pt-BR');
    $('#id_start_date').datetimepicker({
     format:'Y-m-d H:i',
    });
});

$(document).ready(function() {
    $.datetimepicker.setLocale('pt-BR');
    $('#id_end_date').datetimepicker({
         format:'Y-m-d H:i',
    });
});



/*
  delete EVENT
*/

$( "#DeleteEventModalClose" ).click(function() {
  $("#DeleteEventModal").css("display","none");
});


