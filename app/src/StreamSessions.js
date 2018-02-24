import React, { Component } from 'react';
import PropTypes from 'prop-types';

export class StreamSessions extends Component {
  
  constructor(props) {
    super(props);
    this.state = {
      isUpdated: false
    };
    this.onClickUpdateStreamSessionsCurrent = this.onClickUpdateStreamSessionsCurrent.bind(this);
  }

  onClickUpdateStreamSessionsCurrent() {
    this.setState({
      isUpdated: true
    });
  }

  render() {
    return (
      <div>
        I'm going to display stream sessions.
      </div>
    ); 
  }
}

StreamSessions.propTypes = {
  userId: PropTypes.number.isRequired
}