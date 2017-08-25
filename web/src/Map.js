import React, { Component } from 'react';
import Websocket from  'react-websocket';
import { Button, Table } from 'react-bootstrap';
import './Map.css';

/*
var last_seen = new Date();
var roues = [0, -Math.PI / 4, Math.PI / 4, Math.PI];
        $('#agv' + a + ' .v').attr({
          x2: data[a]['v'] * Math.cos(data[a]['t']) * {{ SPEED_MEAN_MAX }} * size_coef,
          y2: data[a]['v'] * Math.sin(data[a]['t']) * {{ SPEED_MEAN_MAX }} * size_coef,
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

class MapSVG extends Component {
  render() {
    if (this.props.consts.bords) {
      return (
          <svg
          height={this.props.consts.height * this.props.consts.px_par_m}
          width={this.props.consts.width * this.props.consts.px_par_m } >
            <g id="g3" transform={"scale(1, -1) translate(0, -" + (this.props.consts.height * this.props.consts.px_par_m) + ")"} >
              <circle className="destination" r={this.props.consts.px_par_m / 2} cx={this.props.agv.destination[0] * this.props.consts.px_par_m} cy={this.props.agv.destination[1] * this.props.consts.px_par_m} />
              <polygon className="c3" points={this.props.consts.bords} />
              <path id="path3" />
              <g id="agv3" transform={ "translate(" + (this.props.agv.x * this.props.consts.px_par_m) + ", " + (this.props.agv.y * this.props.consts.px_par_m) + ") rotate(" + this.props.agv.a + ")" } >
                <polygon points={this.props.consts.octogone} />
                <circle className="centre" cx="0" cy="0" r="2" />
                <circle className="r1" r="2" cx={-this.props.consts.agv_radius * this.props.consts.px_par_m * 1.000} cy="0" />
                <circle className="r2" r="2" cx={+this.props.consts.agv_radius * this.props.consts.px_par_m * 0.707} cy={+this.props.consts.agv_radius * this.props.consts.px_par_m * 0.707} />
                <circle className="r3" r="2" cx={+this.props.consts.agv_radius * this.props.consts.px_par_m * 0.707} cy={-this.props.consts.agv_radius * this.props.consts.px_par_m * 0.707} />
                <line className="v" x1="0" y1="0" />
                <line className="t1" x1={+this.props.consts.agv_radius * this.props.consts.px_par_m * 0.707} y1={-this.props.consts.agv_radius * this.props.consts.px_par_m * 0.707}
                                     x2={+this.props.agv.vm[0] * Math.cos(this.props.agv.tm[0]) * 2 + this.props.consts.agv_radius * this.props.consts.px_par_m * 0.707}
                                     y2={+this.props.agv.vm[0] * Math.sin(this.props.agv.tm[0]) * 2 - this.props.consts.agv_radius * this.props.consts.px_par_m * 0.707}
                />
                <line className="t2" x1={+this.props.consts.agv_radius * this.props.consts.px_par_m * 0.707} y1={+this.props.consts.agv_radius * this.props.consts.px_par_m * 0.707}
                                     x2={+this.props.agv.vm[1] * Math.cos(this.props.agv.tm[1]) * 2 + this.props.consts.agv_radius * this.props.consts.px_par_m * 0.707}
                                     y2={+this.props.agv.vm[1] * Math.sin(this.props.agv.tm[1]) * 2 + this.props.consts.agv_radius * this.props.consts.px_par_m * 0.707}
                />
                <line className="t3" x1={-this.props.consts.agv_radius * this.props.consts.px_par_m * 1.000} y1="0"
                                     x2={+this.props.agv.vm[2] * Math.cos(this.props.agv.tm[2]) * 2 - this.props.consts.agv_radius * this.props.consts.px_par_m * 1.000}
                                     y2={+this.props.agv.vm[2] * Math.sin(this.props.agv.tm[2]) * 2}
                />
              </g>
            </g>
          </svg>
      );
    } else return <div />;
  }
}

class MapTable extends Component {
  boost() { this.props.send("boost"); }
  render() {
    if (this.props.agv.x) {
      return (
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
              <td>{this.props.agv.x.toFixed(2)}</td>
              <td>{this.props.agv.y.toFixed(2)}</td>
              <td>{this.props.agv.a.toFixed(2)}</td>
              <td>{this.props.agv.v.toFixed(2)}</td>
              <td>{this.props.agv.w.toFixed(2)}</td>
              <td>{this.props.agv.t.toFixed(2)}</td>
            </tr>
            <tr>
              <td>{this.props.agv.errors}</td>
              <td><Button onClick={this.boost.bind(this)} bsStyle={this.props.agv.boost ? "warning" : "success"} >Boost</Button></td>
            </tr>
          </tbody>
        </Table>
      );
    } else return <div />;
  }
}

class Map extends Component {
  constructor(props) {
    super(props);
    this.state = {
      consts: '',
      agv: '',
    }
  }
  handleWS(data) {
    let d = JSON.parse(data);
    if (d.agv) this.setState({agv: d.agv});
    if (d.consts) this.setState({consts: d.consts});
  }
  send(cmd) {
    console.log(cmd);
  }

  render() {
    return (
      <div>
        <MapSVG consts={this.state.consts} agv={this.state.agv} />
        <MapTable agv={this.state.agv} send={this.send.bind(this)} />
        <Websocket url="ws://localhost:9000" onMessage={this.handleWS.bind(this)} />
      </div>
    );
  }
}

export default Map;
