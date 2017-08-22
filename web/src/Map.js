import React, { Component } from 'react';
import Websocket from  'react-websocket';
import { Table } from 'react-bootstrap';

/*
var last_seen = new Date();
var size_coef = 2;
var data;
var roues = [0, -Math.PI / 4, Math.PI / 4, Math.PI];
var tpsq = 3 * Math.PI / 4;  // 3π/4
var x, y, alpha;
{% if replay %}
var sv = ['x', 'y'];
var mv = [];
var uv = [];
{% else %}
var sv = ['x', 'y', 'v', 'w'];
var mv = ['nt'];
var uv = ['stop', 'sens', 'boost', 'arriere', 'reverse', 'rotation', 'smoothe', 'smoothe_speed'];
{% endif %}
var source;
$(document).ready(function() {
  source = new EventSource("/sub");
  source.onmessage = function(e) {
    data = JSON.parse(e.data);
    for (a = 3; a < 4; a++) {
      if (data[a]) {
        x = data[a]['x'];
        y = data[a]['y'];
        alpha = data[a]['a'];
        $('#agv' + a).attr({
          transform: 'translate(' + (x * {{ PX_PAR_M }}) + ' ' + (y * {{ PX_PAR_M }}) + ') rotate(' + (alpha * 180 / Math.PI) +') scale(-1, -1)',
        });
        for (v in sv) $('#a' + a + ' .' + sv[v]).html(data[a][sv[v]].toFixed(1));
        for (v in mv) {
          for (i = 0; i < data[a][mv[v]].length; i++) {
            $('#a' + a + ' .' + mv[v] + [i]).html(data[a][mv[v]][i]);
          }
        }
        for (v in uv) {
          if (data[a][uv[v]]){
            $('#a' + a + ' .' + uv[v] + '-ok').removeClass('hidden');
            $('#a' + a + ' .' + uv[v] + '-ko').addClass('hidden');
          } else {
            $('#a' + a + ' .' + uv[v] + '-ko').removeClass('hidden');
            $('#a' + a + ' .' + uv[v] + '-ok').addClass('hidden');
          }
        }
        {% if not replay %}
        $('#agv' + a + ' .v').attr({
          x2: data[a]['v'] * Math.cos(data[a]['t']) * {{ SPEED_MEAN_MAX }} * size_coef,
          y2: data[a]['v'] * Math.sin(data[a]['t']) * {{ SPEED_MEAN_MAX }} * size_coef,
        });
        $('#agv' + a + ' .t1').attr({
          x2: data[a]['vm'][0] * Math.cos(data[a]['tm'][0]) * size_coef + {{ AGV_RADIUS * PX_PAR_M * 0.707 }},
          y2: data[a]['vm'][0] * Math.sin(data[a]['tm'][0]) * size_coef - {{ AGV_RADIUS * PX_PAR_M * 0.707 }},
        });
        $('#agv' + a + ' .t2').attr({
          x2: data[a]['vm'][1] * Math.cos(data[a]['tm'][1]) * size_coef + {{ AGV_RADIUS * PX_PAR_M * 0.707 }},
          y2: data[a]['vm'][1] * Math.sin(data[a]['tm'][1]) * size_coef + {{ AGV_RADIUS * PX_PAR_M * 0.707 }},
        });
        $('#agv' + a + ' .t3').attr({
          x2: data[a]['vm'][2] * Math.cos(data[a]['tm'][2]) * size_coef - {{ AGV_RADIUS * PX_PAR_M }},
          y2: data[a]['vm'][2] * Math.sin(data[a]['tm'][2]) * size_coef,
        });
        $('#g' + a + ' .destination').attr({
          cx: data[a]['destination'][0] * {{ PX_PAR_M }},
          cy: data[a]['destination'][1] * {{ PX_PAR_M }},
        });
        $('#a' + a + ' .status').html(data[a]['status']);
        {% endif %}
        {% if expert %}
        $('#a' + a + ' .anomaly').html(data[a]['anomaly'] ? '✔' : '✘');
        $('#a' + a + ' .state').html(data[a]['state']);
        $('#a' + a + ' .choosen_path').html(data[a]['choosen_path']);
        $('li .' + a).html(data[a]['erreurs']);
        {% endif %}
        {% if expert or partout %}
        if (x != 0) {
          d = $('#path' + a).attr('d');
          $('#path' + a).attr({d: (d ? d + " L " : "M ") + (x * {{ PX_PAR_M }}) + ' ' + (y * {{ PX_PAR_M }})});
          {% if partout %}
          d = $('#pt' + a + '1').attr('d');
          $('#pt' + a + '1').attr({d: (d ? d + " L " : "M ") + ((x + Math.cos(alpha + tpsq) *
            {{ AGV_RADIUS }}) * {{ PX_PAR_M }}) + ' ' + ((y + Math.sin(alpha + tpsq) * {{
              AGV_RADIUS }}) * {{ PX_PAR_M }})});
          d = $('#pt' + a + '2').attr('d');
          $('#pt' + a + '2').attr({d: (d ? d + " L " : "M ") + ((x + Math.cos(alpha - tpsq) *
            {{ AGV_RADIUS }}) * {{ PX_PAR_M }}) + ' ' + ((y + Math.sin(alpha - tpsq) * {{
              AGV_RADIUS }}) * {{ PX_PAR_M }})});
          d = $('#pt' + a + '3').attr('d');
          $('#pt' + a + '3').attr({d: (d ? d + " L " : "M ") + ((x + Math.cos(alpha) * {{
            AGV_RADIUS }}) * {{ PX_PAR_M }}) + ' ' + ((y + Math.sin(alpha) * {{ AGV_RADIUS }}) * {{ PX_PAR_M }})});
          {% endif %}
        }
        {% endif %}
        {% if replay %}
        $('#timestamp').html(data['timestamp']);
        {% endif %}
        $('#agv' + a).css('fill', data[a]['is_up'] ? data[a]['stop'] ? 'yellow' : 'none' : 'orange');
      }
    }
    last_seen = new Date();
  };
});
{% if not replay %}
setInterval(function(){
  now = new Date();
  diff = now - last_seen;
  diff = new Date(diff);
  if (diff.getSeconds() >= 1) {
    $('svg').css("background-color", "orange");
    $('button').addClass('disabled');
  } else {
    $('svg').css("background-color", "white");
    $('button').removeClass('disabled');
  }
}, 500);
{% endif %}
*/

class Map extends Component {
  constructor(props) {
    super(props);
    this.state = {
      x: 0,
      y: 0,
      a: 0,
      v: 0,
      w: 0,
      t: 0,
    }
  }
  handleWS(data) {
    let d = JSON.parse(data)[3];
    this.setState({x: d.x, y: d.y, a: d.a, v: d.v, w: d.w, t: d.t});
  }

  render() {
    return (
      <div>
        <Table striped >
          <thead>
            <tr>
              <th>x</th>
              <th>y</th>
              <th>a</th>
              <th>v</th>
              <th>w</th>
              <th>t</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{this.state.x.toFixed(2)}</td>
              <td>{this.state.y.toFixed(2)}</td>
              <td>{this.state.a.toFixed(2)}</td>
              <td>{this.state.v.toFixed(2)}</td>
              <td>{this.state.w.toFixed(2)}</td>
              <td>{this.state.t.toFixed(2)}</td>
            </tr>
          </tbody>
        </Table>
        <Websocket url="ws://localhost:9000" onMessage={this.handleWS.bind(this)} />
      </div>
    );
  }
}

export default Map;


/*
      <svg>
      <g transform="translate(0,{{ PX_PAR_M * HEIGHT }})">
      <g transform="scale(1,-1)">
      <g transform="translate({{ PX_PAR_M * LEFT_WIDTH }},0)">
      {% for agv in [3] %}{% for t in [1, 2, 3] %}<path id="pt{{ agv }}{{ t }}" class="c{{ agv }}" />{% endfor %}{% endfor %}
      <g id="g3" class="c3">
      <circle class="destination" r="{{ PX_PAR_M / 2 }}" />
      {% if expert %}<polygon points="{% for p in ALLER_RETOURS_SVG[3] %}{{p|join(',')}} {% endfor %}" />{% endif %}
      <polygon points="{% for p in BORDS_SVG[3] %}{{p|join(',')}} {% endfor %}" />
      <path id="path3" />
      <g id="agv3">
      <polygon points="{% for p in OCTOGONE %}{{p|join(',')}} {% endfor %}" />
      <circle cx="0" cy="0" r="{{ DIST_MIN_AGV * PX_PAR_M / 2}}" />
      <circle class="centre" cx="0" cy="0" r="2" />
      <circle class="r1" r="2" cx="-{{ AGV_RADIUS * PX_PAR_M }}" cy="0" />
      <circle class="r2" r="2" cx="{{ AGV_RADIUS * PX_PAR_M * 0.707 }}" cy="+{{ AGV_RADIUS * PX_PAR_M * 0.707 }}" />
      <circle class="r3" r="2" cx="{{ AGV_RADIUS * PX_PAR_M * 0.707 }}" cy="-{{ AGV_RADIUS * PX_PAR_M * 0.707 }}" />
      <line class="v" x1="0" y1="0" />
      <line class="t1" x1="{{ AGV_RADIUS * PX_PAR_M * 0.707 }}" y1="-{{ AGV_RADIUS * PX_PAR_M * 0.707 }}" />
      <line class="t2" x1="{{ AGV_RADIUS * PX_PAR_M * 0.707 }}" y1="+{{ AGV_RADIUS * PX_PAR_M * 0.707 }}" />
      <line class="t3" x1="-{{ AGV_RADIUS * PX_PAR_M }}" y1="0" />
      </g>
      </g>

      </g>
      </g>
      </g>
      </svg>


*/
