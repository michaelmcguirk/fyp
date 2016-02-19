$(document).ready(function() {
  

	$('#start_batch').click(function(){
    console.log("hello");
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

  if($('#single_batch_chart').length)
  {
    function viewSingleBatchChart(){
      alert("View");
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);
      function drawChart() {
        var djangodata = {{djangodict|safe}};
        //var djangodata = dataset;
        var data = google.visualization.arrayToDataTable(djangodata);
        var options = {title: 'My Daily Activities'};
        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    } 
  }
});