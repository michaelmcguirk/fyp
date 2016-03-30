$(document).ready(function() {
  console.log("Hello....JQuery Document Loaded");
  google.charts.load('current', {'packages':['corechart']});
  console.log("Google Charts Loaded");

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
        success: function(data){
          console.log("Success - Loading");
            $('#compare_batch_chart').html(data);
            loadCompareChart();
            loadComparePieChart();
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

function loadPieChart(){
  if($('#pie_chart_div').length)
    {   
      console.log("Pie chart function running")
      google.charts.setOnLoadCallback(drawChart);
      function drawChart() {
        var pieData = new google.visualization.DataTable();
        pieData.addColumn('string','Classification');
        pieData.addColumn('number','Value');
        pieData.addRows(pie_chart_array);

        var options = {
          title: 'Brewing Activity Chart', 
          width:'100%', 
          height:300,
          colors: ['#ff4d4d', '#1aa3ff', '#008000']
        };

        var pieChart = new google.visualization.PieChart(document.getElementById('pie_chart_div'));

        pieChart.draw(pieData, options);

      }
    }  
}

function loadComparePieChart(){
  if($('#compare_pie_charts').length)
    {   
      console.log("Compare Pie chart function running")
      google.charts.setOnLoadCallback(drawChart);
      function drawChart() {
        var pieDataA = new google.visualization.DataTable();
        pieDataA.addColumn('string','Classification');
        pieDataA.addColumn('number','Value');
        pieDataA.addRows(pie_chart_array_a);

        var pieDataB = new google.visualization.DataTable();
        pieDataB.addColumn('string','Classification');
        pieDataB.addColumn('number','Value');
        pieDataB.addRows(pie_chart_array_b);

        var options = {
          title: 'Brewing Activity Chart', 
          width:'100%', 
          height:300,
          colors: ['#ff4d4d', '#1aa3ff', '#008000']
        };

        var pieChartA = new google.visualization.PieChart(document.getElementById('pie_chart_div_a'));
        var pieChartB = new google.visualization.PieChart(document.getElementById('pie_chart_div_b'));

        pieChartA.draw(pieDataA, options);
        pieChartB.draw(pieDataB, options);

      }
    }  
}

  loadSingleChart();
  loadPieChart();

  $(window).resize(function(){
    loadSingleChart();
    loadCompareChart();
    loadPieChart();
    loadComparePieChart();
  });

});