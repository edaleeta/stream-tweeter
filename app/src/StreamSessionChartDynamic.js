import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { convertTimeStampToTime } from './services/log'

export class StreamSessionChartDynamic extends Component { 

  render() {
    return (
      <ResponsiveContainer width="100%" height={250}>
        <LineChart width={730} height={250} data={this.props.streamData}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
          <XAxis type="number"
            scale="time"
            domain={['dataMin', 'dataMax']}
            dataKey="key"
            tickFormatter={convertTimeStampToTime}
            
          />
          <YAxis />
          <Tooltip labelFormatter={convertTimeStampToTime} />
          <Legend />
          <Line 
            name="Viewers"
            type="monotone"
            dataKey="value"
            stroke="#8884d8"
            strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    )
  }
}


// StreamSessionChartDynamic.propTypes = {
//   stream: PropTypes.object.isRequired,
// }