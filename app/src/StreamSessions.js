import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ListGroup } from 'react-bootstrap';
import { StreamSessionContainer } from './StreamSessionContainer';

export class StreamSessions extends Component {
  
  constructor(props) {
    super(props);
    this.state = {
      streams: "",
      nextPage: ""
    };
  }

  componentWillMount() {
    fetch("/api/streams",
    {credentials: 'same-origin'})
    .then((response)=> response.json())
    .then((data) => {
      console.log("StreamSessions mounted!");
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
          <ListGroup>
            <StreamSessionContainer key={key} stream={stream} />
          </ListGroup>
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