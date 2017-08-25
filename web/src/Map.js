import React, { Component } from 'react';
import Websocket from  'react-websocket';
import { Button, Table } from 'react-bootstrap';
import './Map.css';

class MapSVG extends Component {
  render() {
    if (this.props.consts.bords) {
      return (
          <svg style={{backgroundColor: this.props.connected ? 'white': 'orange'}}
               width={this.props.consts.width * this.props.ppm }
               height={this.props.consts.height * this.props.ppm } >
            <g id="g3" transform={"scale(1, -1) translate(0, -" + (this.props.consts.height * this.props.ppm) + ")"} >
              <circle className="destination" r={this.props.ppm / 2} cx={this.props.agv.destination[0] * this.props.ppm} cy={this.props.agv.destination[1] * this.props.ppm} />
              <polygon className="c3" points={this.props.consts.bords} />
              <path id="path3" />
              <g id="agv3" transform={ "translate(" + (this.props.agv.x * this.props.ppm) + ", " + (this.props.agv.y * this.props.ppm) + ") rotate(" + this.props.agv.a + ")" }
                 style={{fill: (this.props.agv.is_up ? this.props.agv.stop ? 'yellow' : 'none' : 'orange')}} >
                <polygon points={this.props.consts.octogone} />
                <circle className="centre" cx="0" cy="0" r="2" />
                <circle className="r1" r="2" cx={-this.props.ar * 1.000} cy="0" />
                <circle className="r2" r="2" cx={+this.props.ar * 0.707} cy={+this.props.ar * 0.707} />
                <circle className="r3" r="2" cx={+this.props.ar * 0.707} cy={-this.props.ar * 0.707} />
                <line className="v" x1="0" y1="0" x2={ this.props.agv.v * Math.cos(this.props.agv.t) * this.props.consts.speed_mean_max * this.props.size_coef }
                                                  y2={ this.props.agv.v * Math.sin(this.props.agv.t) * this.props.consts.speed_mean_max * this.props.size_coef } />
                <line className="t1" x1={ + this.props.ar * 0.707 }
                                     y1={ - this.props.ar * 0.707 }
                                     x2={ + this.props.ar * 0.707 + this.props.agv.vm[0] * Math.cos(this.props.agv.tm[0]) * this.props.size_coef }
                                     y2={ - this.props.ar * 0.707 + this.props.agv.vm[0] * Math.sin(this.props.agv.tm[0]) * this.props.size_coef } />
                <line className="t2" x1={ + this.props.ar * 0.707 }
                                     y1={ + this.props.ar * 0.707 }
                                     x2={ + this.props.ar * 0.707 + this.props.agv.vm[1] * Math.cos(this.props.agv.tm[1]) * this.props.size_coef }
                                     y2={ + this.props.ar * 0.707 + this.props.agv.vm[1] * Math.sin(this.props.agv.tm[1]) * this.props.size_coef } />
                <line className="t3" y1="0"
                                     x1={ - this.props.ar * 1.000} y2={this.props.agv.vm[2] * Math.sin(this.props.agv.tm[2]) * this.props.size_coef }
                                     x2={ - this.props.ar * 1.000    + this.props.agv.vm[2] * Math.cos(this.props.agv.tm[2]) * this.props.size_coef } />
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
              <td><Button onClick={this.boost.bind(this)} disabled={!this.props.connected}
                          bsStyle={this.props.agv.boost ? "warning" : "success"} >
                          {this.props.agv.boost ? 'Stop' : 'Start'} Boost </Button></td>
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
      connected: false,
      last: new Date(),
    }
    setInterval(this.checkConnection.bind(this), 500);
  }
  checkConnection() {
      var last = new Date(new Date() - this.state.last).getSeconds();
      this.setState({connected: last < 1});
  }
  handleWS(data) {
    let d = JSON.parse(data);
    if (d.agv) this.setState({agv: d.agv});
    if (d.consts) this.setState({consts: d.consts});
    this.setState({last: new Date(), connected: true});
  }
  send(cmd) {
    console.log(cmd);
  }

  render() {
    return (
      <div>
        <MapSVG consts={this.state.consts} agv={this.state.agv} size_coef={3} connected={this.state.connected}
                ar={this.state.consts.agv_radius * this.state.consts.px_par_m} ppm={this.state.consts.px_par_m} />
        <MapTable agv={this.state.agv} send={this.send.bind(this)} connected={this.state.connected} />
        <Websocket url="ws://localhost:9000" onMessage={this.handleWS.bind(this)} />
      </div>
    );
  }
}

export default Map;
