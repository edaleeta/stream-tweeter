import React, { Component } from 'react';
import PropTypes from 'prop-types';

export class StreamSessions extends Component {
  
  constructor(props) {
    super(props);
    this.state = {
      streams: "",
      nextPage: ""
    };
  }

  componentWillMount() {
    fetch("/api/stream-sessions",
    {credentials: 'same-origin'})
    .then((response)=> response.json())
    .then((data) => {
      console.log("StreamSessions mounted!");
      console.log(data.streams);
      console.log(data.next);
      this.setState({
        streams: data.streams,
        nextPage: data.next
      });
    })        
  }

  render() {
    if (this.state.streams) {
      return (
        this.state.streams.map((stream, key) => (
          <div key={key}>{stream.startedAt} {stream.endedAt} {stream.twitchSessionId} {stream.userId}</div>
        ))
      ); 
    } else {
      return <div></div>
    }
  }
}

StreamSessions.propTypes = {
  userId: PropTypes.number.isRequired
}