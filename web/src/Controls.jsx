import React from 'react';
import { Button } from 'react-bootstrap';

class Control extends React.Component {
  action() { this.props.send({ [this.props.var]: !this.props.agv[this.props.var] }); }

  render() {
    return (
        <Button onClick={this.action.bind(this)} disabled={this.props.disabled}
          bsStyle={this.props.default === this.props.agv[this.props.var] ? "success" : "warning"} >
          {this.props.var}
        </Button>
        );
  }
}

class Controls extends React.Component {
  render() {
    if (this.props.agv.x) {
      var disabled = !this.props.connected;
      var send = this.props.send;
      var agv = this.props.agv;
      return (
          <div>
            <Control disabled={disabled} send={send} agv={agv} var="stop" default={false} />
            <Control disabled={disabled} send={send} agv={agv} var="boost" default={false} />
            {/*<Control disabled={disabled} send={send} agv={agv} var="reverse" default={true} />*/}
            {/*<Control disabled={disabled} send={send} agv={agv} var="smoothe" default={false} />*/}
            {/*<Control disabled={disabled} send={send} agv={agv} var="smoothe_speed" default={true} />*/}
          </div>
          );
    } else return <div />;
  }
}

export default Controls;
