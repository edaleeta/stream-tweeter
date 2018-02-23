import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { TweetOptionsInterval } from './TweetOptionsInterval'
import { TweetOptionsRevoke } from './TweetOptionsRevoke'

export class TweetOptions extends Component {
  
  constructor(props) {
    super(props);
    this.state = {
      isUpdated: false
    }
  };

  render() {
    if (this.props.isTwitterAuth) {
      return (
        <div>
          <h2>Twitter Options</h2>
          <TweetOptionsInterval
            userId={this.props.userId}
            tweetInterval={this.props.tweetInterval}
          />
          <TweetOptionsRevoke
            userId={this.props.userId}
            tweetInterval={this.props.tweetInterval}
            onClick={this.props.onClick}
          />
        </div>
      ); 
    } else {
      return <div></div>
    }
  }
}

TweetOptions.propTypes = {
  isTwitterAuth: PropTypes.bool.isRequired,
  userId: PropTypes.number.isRequired,
  tweetInterval: PropTypes.number.isRequired,
  onClick: PropTypes.func.isRequired
}