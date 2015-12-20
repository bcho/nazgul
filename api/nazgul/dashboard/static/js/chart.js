(function(window) {
  'use strict';

  let $ = window.$;
  let vg = window.vg;

  function drawChart(data, el) {
    vg.parse.spec(data, (chart) => {
      chart({'el': el, 'renderer': 'svg'}).update();
    });
  }

  window.trafficChart = (data) => {
    let $el = $('#traffic'),
      el = $el[0];

    let chartData = {
      'width': $el.width() - 20,
      'padding': {'top': 20, 'left': 30, 'bottom': 20, 'right': 10},
      'data': [
        {
          'name': 'traffic',
          'values': data
        }
      ],
      'signals': [
        {
          'name': 'tooltip',
          'init': {},
          'streams': [
            {'type': 'rect:mouseover', 'expr': 'datum'},
            {'type': 'rect:mouseout', 'expr': '{}'},
          ]
        }
      ],
      'predicates': [
        {
          'name': 'tooltip', 'type': '==',
          'operands': [{'signal': 'tooltip._id'}, {'arg': 'id'}]
        }
      ],
      'scales': [
        {'name': 'xscale', 'type': 'ordinal', 'range': 'width',
         'domain': {'data': 'traffic', 'field': 'date'}},
        {'name': 'yscale', 'range': 'height', 'nice': true,
         'domain': {'data': 'traffic', 'field': 'amount'}}
      ],
      'axes': [
        {'type': 'x', 'scale': 'xscale'},
        {'type': 'y', 'scale': 'yscale'},
      ],
      'marks': [
        {
          'type': 'rect',
          'from': {'data': 'traffic'},
          'properties': {
            'enter': {
              'x': {'scale': 'xscale', 'field': 'date'},
              'width': {'scale': 'xscale', 'band': true, 'offset': -1},
              'y': {'scale': 'yscale', 'field': 'amount'},
              'y2': {'scale': 'yscale', 'value': 0}
            },
            'update': {'fill': {'value': 'steelblue'}},
            'hover': {'fill': {'value': 'red'}}
          }
        },
        {
          'type': 'text',
          'properties': {
            'enter': {
              'align': {'value': 'center'},
              'fill': {'value': '#333'}
            },
            'update': {
              'x': {'scale': 'xscale', 'signal': 'tooltip.date'},
              'dx': {'scale': 'xscale', 'band': true, 'mult': 0.5},
              'y': {'scale': 'yscale', 'signal': 'tooltip.amount', 'offset': -5},
              'text': {'signal': 'tooltip.amount'},
              'fillOpacity': {
                'rule': [
                  {
                    'predicate': {'name': 'tooltip', 'id': {'value': null}},
                    'value': 0
                  },
                  {'value': 1}
                ]
              }
            }
          }
        }
      ]
    };

    drawChart(chartData, el);
  };
})(window);
