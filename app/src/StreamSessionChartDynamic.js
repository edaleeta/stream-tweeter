import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, Legend } from 'recharts';
import { convertTimeStampToTime } from './services/log'

export class StreamSessionChartDynamic extends Component { 

  // componentWillMount() {
  //   this.setState({
  //     data: [
  //       {name: 1519348333, viewers: 35},
  //       {name: 1519348333+(60*5), viewers: 40},
  //       {name: 1519348333+2*(60*5), viewers: 56},
  //       {name: 1519348333+3*(60*5), viewers: 100},
  //       {name: 1519348333+4*(60*5), viewers: 90},
  //       {name: 1519348333+5*(60*5), viewers: 110},
  //       {name: 1519348333+8*(60*5), viewers: 105},
  //     ]
  //   });
  // }

  render() {
    return (
      <LineChart width={730} height={250} data={this.props.streamData}
        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
        <XAxis type="number"
          scale="time"
          domain={['dataMin', 'dataMax']}
          dataKey="timestamp"
          tickFormatter={convertTimeStampToTime}
          
        />
        <YAxis />
        <Tooltip labelFormatter={convertTimeStampToTime} />
        <Legend />
        <Line type="monotone" dataKey="viewers" stroke="#8884d8" strokeWidth={2} />
      </LineChart>
    )
  }
}


// StreamSessionChartDynamic.propTypes = {
//   stream: PropTypes.object.isRequired,
// }