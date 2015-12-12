'use strict';

let lineChart = (opts) => {
  let scales = {
    x: {type: 'ordinal', data: opts.data, key: 'x', adjacent: true},
    y: {data: opts.data, key: 'y'}
  };

  let charts = [
    d3c.bars('results', {
      data: opts.data,
      xScale: scales.x,
      yScale: scales.y,
    }),
  ];

  let xAxis = d3c.axis('xAxis', {scale: scales.x, ticks: 5});
  let yAxis = d3c.axis('yAxis', {scale: scales.y, ticks: 5});

  return [
    [yAxis, d3c.layered(charts)],
    xAxis,
  ];
};
