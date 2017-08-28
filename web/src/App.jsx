import React from 'react';
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
      ws: false,
      reconnect: true,
      wsURL: 'ws://localhost:9000',
      attempts: 1000,
    }
    setInterval(this.checkConnection.bind(this), 500);
    this.handleWS = this.handleWS.bind(this);
    this.setupWS = this.setupWS.bind(this);
    this.send = this.send.bind(this);
  }

  componentDidMount() {
    this.setupWS();
  }

  componentWillUnmount() {
    this.setState({reconnect: false});
    this.state.ws.close();
  }

  setupWS() {
    var ws = new WebSocket(this.state.wsURL);
    ws.onmessage = this.handleWS;
    ws.onopen = () => { this.setState({attempts: 1000}); }
    ws.onclose = () => { if (this.state.reconnect) {
      this.setState({attempts: this.state.attempts + 1000});
      setTimeout(this.setupWS, Math.min(60000, this.state.attempts));
    }}
    this.setState({ws: ws});
  }

  checkConnection() {
      var last = new Date(new Date() - this.state.last).getSeconds();
      this.setState({connected: last < 1});
  }

  handleWS(evt) {
    let d = JSON.parse(evt.data);
    if (d.agv) this.setState({agv: d.agv});
    if (d.consts) this.setState({consts: d.consts});
    this.setState({last: new Date(), connected: true});
  }

  send(cmd) {
    this.state.ws.send(JSON.stringify(cmd));
  }

  render() {
    return (
      <div>
        <Map consts={this.state.consts} agv={this.state.agv} size_coef={3} connected={this.state.connected} send={this.send} />
        <Controls agv={this.state.agv} send={this.send} connected={this.state.connected} />
      </div>
    );
  }
}

export default App;
