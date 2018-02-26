import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ListGroup } from 'react-bootstrap';
import { SentTweet } from './SentTweet';

export class SentTweetsContainer extends Component {

  render() {
    return (
      this.props.tweets.map((tweet, key)=> (
        <ListGroup key={key}>
          <SentTweet
            key={key}
            clipId={tweet.clipId}
            createdAt={tweet.createdAt}
            message={tweet.message}
            permalink={tweet.permalink}
            tweetTwtrId={tweet.tweetTwtrId}
            userId={tweet.userId}
          />
        </ListGroup>
      ))
    )
  }
}

SentTweetsContainer.propTypes = {
  tweets: PropTypes.array.isRequired
}