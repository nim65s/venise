import React from 'react';
import './Map.css';

class Map extends React.Component {
  render() {
    if (this.props.consts.bords && this.props.agv) {
      return (
          <svg style={{backgroundColor: this.props.connected ? 'white': 'orange'}}
               width={this.props.consts.width * this.props.ppm }
               height={this.props.consts.height * this.props.ppm } >
            <g id="g3" transform={"scale(1, -1) translate(0, -" + (this.props.consts.height * this.props.ppm) + ")"} >
              <circle className="destination" r={this.props.ppm / 2} cx={this.props.agv.destination[0] * this.props.ppm} cy={this.props.agv.destination[1] * this.props.ppm} />
              <polygon className="c3" points={this.props.consts.bords} />
              <path id="path3" />
              <g id="agv3" transform={ "translate(" + (this.props.agv.x * this.props.ppm) + ", " + (this.props.agv.y * this.props.ppm) + ") rotate(" + (this.props.agv.a * 180 / Math.PI + 180) + ")" }
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

export default Map;
