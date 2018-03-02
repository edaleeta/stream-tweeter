import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { convertTimeStampToTime } from './services/log'
import { convertTimeStampToTimeAndTZ } from './services/log'
import { convertToCommaSeparated } from './services/log'

export class StreamSessionChartDynamic extends Component { 

  render() {
    return (
      <ResponsiveContainer width="100%" height={250}>
        <LineChart width={730} height={250} data={this.props.streamData}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid
            stroke="#ccc"
            strokeDasharray="5 5"
            horizontal={false}
          />
          <XAxis
            type="number"
            scale="time"
            domain={['dataMin', 'dataMax']}
            dataKey="key"
            tickFormatter={convertTimeStampToTime}
            tickMargin={5}
          />
          <YAxis
            domain={['dataMin', 'dataMax']}
            tickFormatter={convertToCommaSeparated}
            padding={{ top: 20, bottom: 20 }}
            tickMargin={5}
          />
          <Tooltip
            labelFormatter={convertTimeStampToTimeAndTZ}
            formatter={convertToCommaSeparated}
          />
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


StreamSessionChartDynamic.propTypes = {
  streamData: PropTypes.array.isRequired,
}