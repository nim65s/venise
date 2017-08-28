import React from 'react';
import './Map.css';

class Map extends React.Component {
  handleClick(evt) {
    var ppm = this.props.consts.px_per_m;
    this.props.send({destination: [evt.pageX / ppm, this.props.consts.height - evt.pageY / ppm]});
  }

  render() {
    if (this.props.consts.bords && this.props.agv) {
      var consts = this.props.consts;
      var agv = this.props.agv;
      var ppm = consts.px_per_m;
      var ar = consts.agv_radius * ppm;
      return (
          <svg style={{backgroundColor: this.props.connected ? agv.inside ? 'white' : 'orange'  : 'red'}}
               width={consts.width * ppm }
               height={consts.height * ppm }
               onClick={this.handleClick.bind(this)}
               >
            <g id="g3" transform={"scale(1, -1) translate(0, -" + (consts.height * ppm) + ")"} >
              <circle className="destination" r={ppm / 2} cx={agv.destination[0] * ppm} cy={agv.destination[1] * ppm} />
              <polygon className="c3" points={consts.bords} />
              <path id="path3" />
              <g id="agv3" transform={ "translate(" + (agv.x * ppm) + ", " + (agv.y * ppm) + ") rotate(" + (agv.a * 180 / Math.PI + 180) + ")" }
                 style={{fill: (agv.is_up ? agv.stop ? 'yellow' : 'none' : 'orange')}} >
                <polygon points={consts.octogone} />
                <circle className="centre" cx="0" cy="0" r="2" />
                <circle className="r1" r="2" cx={ - ar * 1.000 } cy="0" />
                <circle className="r2" r="2" cx={ + ar * 0.707 } cy={ + ar * 0.707 } />
                <circle className="r3" r="2" cx={ + ar * 0.707 } cy={ - ar * 0.707 } />
                <line className="v" x1="0" y1="0" x2={ agv.v * Math.cos(agv.t) * consts.speed_mean_max * this.props.size_coef }
                                                  y2={ agv.v * Math.sin(agv.t) * consts.speed_mean_max * this.props.size_coef } />
                <line className="t1" x1={ + ar * 0.707 }
                                     y1={ - ar * 0.707 }
                                     x2={ + ar * 0.707 + agv.vm[0] * Math.cos(agv.tm[0]) * this.props.size_coef }
                                     y2={ - ar * 0.707 + agv.vm[0] * Math.sin(agv.tm[0]) * this.props.size_coef } />
                <line className="t2" x1={ + ar * 0.707 }
                                     y1={ + ar * 0.707 }
                                     x2={ + ar * 0.707 + agv.vm[1] * Math.cos(agv.tm[1]) * this.props.size_coef }
                                     y2={ + ar * 0.707 + agv.vm[1] * Math.sin(agv.tm[1]) * this.props.size_coef } />
                <line className="t3" y1="0"
                                     x1={ - ar * 1.000} y2={agv.vm[2] * Math.sin(agv.tm[2]) * this.props.size_coef }
                                     x2={ - ar * 1.000    + agv.vm[2] * Math.cos(agv.tm[2]) * this.props.size_coef } />
              </g>
            </g>
          </svg>
      );
    } else return <div />;
  }
}

export default Map;
