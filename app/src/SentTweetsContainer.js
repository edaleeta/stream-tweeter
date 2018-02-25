import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { SentTweet } from './SentTweet';

export class SentTweetsContainer extends Component {

  render() {
    return (
      this.props.tweets.map((tweet, key)=> (
        <SentTweet
          clipId={tweet.clipId}
          createdAt={tweet.createdAt}
          message={tweet.message}
          permalink={tweet.permalink}
          tweetTwtrId={tweet.tweetTwtrId}
          userId={tweet.userId}
        />
      ))
    )
  }
}

SentTweetsContainer.propTypes = {
  tweets: PropTypes.array.isRequired
}