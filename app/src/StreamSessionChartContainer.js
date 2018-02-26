import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { StreamSessionChartDynamic } from './StreamSessionChartDynamic'

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
      console.log(data);
      this.setState({
        streamData: data.data,
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