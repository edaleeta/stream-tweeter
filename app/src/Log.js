import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { StreamSessions } from './StreamSessions'

export class Log extends Component {

  render() {
    return (
      <div>
        <h3>Your Stream History</h3>
        <StreamSessions userId={this.props.userId} />
      </div>
    )
  
  }
}

Log.propTypes = {
  userId: PropTypes.number.isRequired,
}


