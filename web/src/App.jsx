import React from 'react';
import Websocket from  'react-websocket';
import Map from './Map';
import Controls from './Controls';

class App extends React.Component {
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
        <Map consts={this.state.consts} agv={this.state.agv} size_coef={3} connected={this.state.connected}
                ar={this.state.consts.agv_radius * this.state.consts.px_par_m} ppm={this.state.consts.px_par_m} />
        <Controls agv={this.state.agv} send={this.send.bind(this)} connected={this.state.connected} />
        <Websocket url="ws://localhost:9000" onMessage={this.handleWS.bind(this)} />
      </div>
    );
  }
}

export default App;
