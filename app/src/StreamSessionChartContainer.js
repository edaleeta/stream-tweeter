import React, { Component } from "react";
import PropTypes from "prop-types";
import { StreamSessionChartDynamic } from "./StreamSessionChartDynamic";
import { nest } from "d3-collection";
import { max } from "d3-array";
import { roundTimeToMinute } from "../src/services/log";

export class StreamSessionChartContainer extends Component {
  constructor(props) {
    super(props);
    this.state = {
      fetched: false
    };
  }

  componentWillMount() {
    // Fetch data here

    let url = `/api/streams/data/${this.props.streamId}`;

    fetch(url, {
      credentials: "same-origin"
    })
      .then(response => response.json())
      .then(data => {
        // Rounds timestamps down to the minute for charts.
        let roundedData = [];

        data.data.forEach(dataPoint => {
          let roundedDataPoint = {};

          roundedDataPoint.timestamp = roundTimeToMinute(dataPoint.timestamp);
          roundedDataPoint.viewers = dataPoint.viewers;
          roundedData.push(roundedDataPoint);
        });
        // Once rounded, take the max value if more than one data point exists.
        let dataByTimestamp = nest()
          .key(d => d.timestamp)
          .rollup(v => {
            return max(v, d => d.viewers);
          })
          .entries(roundedData);

        dataByTimestamp.forEach(dataPoint => {
          dataPoint.key = parseInt(dataPoint.key, 10);
        });

        this.setState({
          streamData: dataByTimestamp,
          fetched: true
        });
      });
  }

  render() {
    if (this.state.fetched) {
      return <StreamSessionChartDynamic streamData={this.state.streamData} />;
    }
    return <div />;
  }
}

StreamSessionChartContainer.propTypes = {
  streamId: PropTypes.number.isRequired
};
