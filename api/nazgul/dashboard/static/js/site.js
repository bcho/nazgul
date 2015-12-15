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
    let dates = [];
    for (let date in actionsByDate) {
      actionsCount.push({
        x: dates.length,
        y: actionsByDate[date].length
      });
      dates.push(date);
    }

    let chartData = {
      data: [{key: SITE_NETLOC, name: SITE_NETLOC, values: actionsCount}],
      tickFormat: (i) => { return dates[i];},
      include: {xy: false, title: true},
      title: {text: 'title'},
    };

    d3.select('#traffic').chart('Compose', lineChart).draw(chartData);
  }
})();
