(function(window) {
  'use strict';

  let $ = window.$;
  let vg = window.vg;

  window.drawChart = (data, el) => {
    if (!data) {
      $(el).html('<p>暂时没有记录</p>');
      return;
    }

    vg.parse.spec(data, (chart) => {
      chart({'el': el, 'renderer': 'svg'}).update();
    });
  };
})(window);
