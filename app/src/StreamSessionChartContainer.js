import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { StreamSessionChartDynamic } from './StreamSessionChartDynamic';
import moment from 'moment';
import { roundTimeToMinute } from '../src/services/log'

export class StreamSessionChartContainer extends Component { 

  constructor(props) {
    super(props);
    this.state = {
      fetched: false
    };
  }

  componentWillMount() {
    // Fetch data here
    console.log(this.props.streamId)

    let url = `/api/streams/data/${this.props.streamId}`;

  
    fetch(url,{
      credentials: 'same-origin'
    })
    .then((response)=> response.json())
    .then((data) => {
      // Rounds timestamps down to the minute for charts
      let roundedData = new Array();

      data.data.forEach(dataPoint => {
        let roundedDataPoint = {}

        roundedDataPoint.timestamp = roundTimeToMinute(dataPoint.timestamp);
        roundedDataPoint.viewers = dataPoint.viewers;
        roundedData.push(roundedDataPoint); 
      });

      this.setState({
        streamData: roundedData,
        fetched: true
      });
    })        
  }

  render() {
    if (this.state.fetched) {
      return (
        <StreamSessionChartDynamic streamData={this.state.streamData} />
      )
    }
    return <div></div>
  }
}


// StreamSessionChartContainer.propTypes = {
//   stream: PropTypes.object.isRequired,
// }