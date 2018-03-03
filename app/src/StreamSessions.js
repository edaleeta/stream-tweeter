import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ListGroup } from 'react-bootstrap';
import { StreamSessionContainer } from './StreamSessionContainer';

export class StreamSessions extends Component {

  render() {
    if (this.props.streams) {
      return (
        this.props.streams.map((stream, key) => (
          <ListGroup key={key}>
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
  userId: PropTypes.number.isRequired,
  streams: PropTypes.array.isRequired
}