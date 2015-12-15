'use strict';

let lineChart = (opts) => {
  let scales = {
    x: {data: opts.data, key: 'x', type: 'ordinal', adjancent: true},
    y: {data: opts.data, key: 'y'}
  };

  let charts = [
    d3c.lines('l', {
      data: opts.data,
      xScale: scales.x,
      yScale: scales.y,
    }),
  ];

  let xAxis = d3c.axis('xAxis', {scale: scales.x, ticks: 2, tickFormat: opts.tickFormat});
  
  let yAxis = d3c.axis('yAxis', {scale: scales.y, ticks: 5});

  return [
    [yAxis, d3c.layered(charts)],
    xAxis,
  ];
};
