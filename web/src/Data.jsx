import React from 'react';
import { Table } from 'react-bootstrap';

class Data extends React.Component {
  render() {
    if (this.props.agv.x) {
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
                  <th colSpan={3} >nt</th>
                  <th colSpan={3} >reverse</th>
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
                  <td>{this.props.agv.nt[0]}</td>
                  <td>{this.props.agv.nt[1]}</td>
                  <td>{this.props.agv.nt[2]}</td>
                  <td>{this.props.agv.reversed[0] ? 1 : 0 }</td>
                  <td>{this.props.agv.reversed[1] ? 1 : 0 }</td>
                  <td>{this.props.agv.reversed[2] ? 1 : 0 }</td>
                </tr>
              </tbody>
            </Table>
            <Table>
              <thead>
                <tr>
                  <th>status</th>
                  <th>errors</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{this.props.agv.status}</td>
                  <td>{this.props.agv.errors}</td>
                </tr>
              </tbody>
            </Table>
          </div>
      );
    } else return <div />;
  }
}

export default Data;
