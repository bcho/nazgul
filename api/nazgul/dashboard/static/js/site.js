(function() {
  'use strict';

  let dataApi = document.location.href + '/data';

  $.get(dataApi).done((siteData) => {
    drawTraffic(siteData);
    drawRefers(siteData);
  }).fail((e) => {
    console.error(e);
  });

  function drawTraffic(siteData) {
    drawChart(siteData.traffic_chart, '#traffic');
  }

  function drawRefers(siteData) {
    drawChart(siteData.refers.to_chart, '#refers-to');
    drawChart(siteData.refers.from_chart, '#refers-from');
  }
})();
