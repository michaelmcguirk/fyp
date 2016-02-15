$(document).ready(function() {

	$('#start_batch').click(function(){
    var batch_id;
    batch_id = $(this).attr("batch-id");
     $.get('/temps/start_batch/', {batch_id: batch_id}, function(data){
               alert("Batch Started");
               $('#start_batch').hide();
           });
	});

	$('#stop_batch').click(function(){
    var batch_id;
    batch_id = $(this).attr("batch-id");
     $.get('/temps/stop_batch/', {batch_id: batch_id}, function(data){
               alert("Batch Stopped");
               $('#start_batch').hide();
           });
	});

});