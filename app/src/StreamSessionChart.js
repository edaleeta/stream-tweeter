import React, { Component } from "react";
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend
} from "recharts";
import { convertTimeStampToTime } from "./services/log";

export class StreamSessionChart extends Component {
  componentWillMount() {
    this.setState({
      data: [
        { name: 1519348333, viewers: 35 },
        { name: 1519348333 + 60 * 5, viewers: 40 },
        { name: 1519348333 + 2 * (60 * 5), viewers: 56 },
        { name: 1519348333 + 3 * (60 * 5), viewers: 100 },
        { name: 1519348333 + 4 * (60 * 5), viewers: 90 },
        { name: 1519348333 + 5 * (60 * 5), viewers: 110 },
        { name: 1519348333 + 8 * (60 * 5), viewers: 105 }
      ]
    });
  }

  render() {
    return (
      <LineChart
        width={730}
        height={250}
        data={this.state.data}
        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
      >
        <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
        <XAxis
          type="number"
          scale="utc"
          domain={["dataMin", "dataMax"]}
          dataKey="name"
          tickFormatter={convertTimeStampToTime}
        />
        <YAxis />
        <Tooltip labelFormatter={convertTimeStampToTime} />
        <Legend />
        <Line
          type="monotone"
          dataKey="viewers"
          stroke="#000000"
          strokeWidth={2}
        />
      </LineChart>
    );
  }
}
