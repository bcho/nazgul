(function(window) {
  'use strict';

  let $ = window.$;
  let vg = window.vg;

  window.drawChart = (data, el) => {
    vg.parse.spec(data, (chart) => {
      chart({'el': el, 'renderer': 'svg'}).update();
    });
  };
})(window);
