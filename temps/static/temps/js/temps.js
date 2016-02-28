$(document).ready(function() {
  console.log("Hello....JQuery Document Loaded");
  google.charts.load('current', {'packages':['corechart']});
  console.log("Google Charts Loaded");

/*	$('#start_batch').click(function(){
    console.log("Starting batch");
    var batch_id;
    batch_id = $(this).attr("batch-id");
     $.get('/temps/start_batch/', {batch_id: batch_id}, function(data){
               alert("Batch Started");
               $('#start_batch').hide();
           });
	});

	$('#stop_batch').click(function(){
     $.get('/temps/stop_batch/', function(data){
               alert("Batch Stopped");
               $('#stop_batch').hide();
           });
	});*/

  $('#start_stop').click(function(){
    var status = $(this).attr("status");
    if(status == "stopped"){
      var batch_id;
      batch_id = $(this).attr("batch-id");
      $.get('/temps/start_batch/', {batch_id: batch_id}, function(data){
              $('#start_stop').addClass("btn-danger").removeClass("btn-success");
              $('#start_stop').text('Stop Batch');
              $('#start_stop').attr("status", "started");
              alert("Batch Started");
              $('#start_batch').hide();
      });
    }
    else if(status == "started"){
      $.get('/temps/stop_batch/', function(data){
              $('#start_stop').addClass("btn-success").removeClass("btn-danger");
              $('#start_stop').text('Start Batch');
              $('#start_stop').attr("status","stopped");
              alert("Batch Stopped");
              $('#stop_batch').hide();
      });
    }
  });

  $('#load_chart').click(function(){
    var b1 = $('#batch_1').val();
    var b2 = $('#batch_2').val();
     $.ajax({
        url: '/temps/serve_compare_chart/' + b1 + '/' + b2,
        //data: {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
        //data: {csrfmiddlewaretoken: {{csrf_token}}},
        success: function(data){
          console.log("Success - Loading");
            //$('#compare_batch_chart').load('/temps/serve_compare_chart/1/2');
            $('#compare_batch_chart').html(data);
            loadCompareChart();
        }
     });
  });

  function loadSingleChart(){
    if($('#single_batch_chart').length)
    {
        console.log("single batch chart function running");
        google.charts.setOnLoadCallback(drawChart);
        function drawChart() {
          var data = new google.visualization.DataTable();
          data.addColumn('number','Sequence');
          data.addColumn('number','Temp C');
          data.addColumn({type: 'string', role: 'tooltip'});
          data.addColumn({type: 'string', role: 'style'});
          data.addRows(djangodata);
          var options = {title: 'Batch', width:'100%', height:300};
          var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
          chart.draw(data, options);
        }
    }
  }

    /*function loadSingleChart(){
    if($('#single_batch_chart').length)
    {
        console.log("single batch chart function running");
        google.charts.setOnLoadCallback(drawChart);
        function drawChart() {
          var data = new google.visualization.DataTable();
          data.addColumn('number','Sequence');
          data.addColumn('number','Temp C');
          data.addColumn({type: 'string', role: 'tooltip'});
          data.addRows(djangodata);
          var options = {title: 'Batch', width:'100%', height:300};
          var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
          chart.draw(data, options);
        }
    }
  }*/
  

  function loadCompareChart(){
    if($('#compare_batch_chart').length)
    {   
      console.log("compare batch chart function running")
      google.charts.setOnLoadCallback(drawChart);
      function drawChart() {
        var dataA = new google.visualization.DataTable();
        dataA.addColumn('number','Sequence');
        dataA.addColumn('number','Temp C - A');
        dataA.addColumn({type: 'string', role: 'tooltip'});
        dataA.addColumn({type: 'string', role: 'style'});
        dataA.addRows(batchA);
        var dataB = new google.visualization.DataTable();      
        dataB.addColumn('number','Sequence');
        dataB.addColumn('number','Temp C - B');
        dataB.addColumn({type: 'string', role: 'tooltip'});
        dataB.addColumn({type: 'string', role: 'style'});
        dataB.addRows(batchB);
        var compareData = google.visualization.data.join(dataA, dataB, 'full', [[0, 0]], [1,2,3], [1,2,3]);
        var options = {title: 'Comparing Batches', width:'100%', height:300};
        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(compareData, options);
      }
    }  
  }

  loadSingleChart();

  $(window).resize(function(){
    loadSingleChart();
    loadCompareChart();
  });

});