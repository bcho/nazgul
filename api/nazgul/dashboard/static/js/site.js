(function() {
  'use strict';

  let dataApi = document.location.href + '/data';

  $.get(dataApi).done((siteData) => {
    siteData.visitor_actions.forEach(convertDatetime('created_at'));

    drawTraffic(siteData);
  }).fail((e) => {
    console.error(e);
  });

  function drawTraffic(siteData) {
    let actionsByDate = _.groupBy(siteData.visitor_actions, (x) => {
      return datetimeToDate(x['created_at']);
    });
    let actionsCount = [];
    for (let date in actionsByDate) {
      actionsCount.push({
        x: date,
        y: actionsByDate[date].length
      });
    }

    let chartData = {
      data: [{key: SITE_NETLOC, name: SITE_NETLOC, values: actionsCount}],
      include: {xy: false, title: true},
      title: {text: 'title'},
    };

    let chart = d3.select('#traffic').chart('Compose', lineChart);
    chart.draw(chartData);
  }
})();
