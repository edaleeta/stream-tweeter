import React, { Component } from 'react';
import PropTypes from 'prop-types';

export class StreamSessionContainer extends Component {

  render() {
    return (
      <div>
        {this.props.stream.startedAt} <br />
        {this.props.stream.endedAt} <br />
        {this.props.stream.twitchSessionId} <br />
        {this.props.stream.userId}<br />
      </div>
    )
  }
}

StreamSessionContainer.propTypes = {
  stream: PropTypes.object.isRequired,
  key: PropTypes.number.isRequired
}