import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { TweetOptionsInterval } from './TweetOptionsInterval'
import { TweetOptionsRevoke } from './TweetOptionsRevoke'
import { StartTweetingButton } from './StartTweetingButton'

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
          <h2>Tweet Options</h2>
          <TweetOptionsInterval
            userId={this.props.userId}
            tweetInterval={this.props.tweetInterval}
          />
          <TweetOptionsRevoke
            userId={this.props.userId}
            tweetInterval={this.props.tweetInterval}
            onClick={this.props.onClick}
          />
          <StartTweetingButton userId={this.props.userId} />
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