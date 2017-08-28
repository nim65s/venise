import React from 'react';
import { Button, Table } from 'react-bootstrap';

class Controls extends React.Component {

  boost() { this.props.send({boost: !this.props.agv.boost}); }

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

export default Controls;
