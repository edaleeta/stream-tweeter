import React, { Component } from 'react';
import PropTypes from 'prop-types';

export class SentTweet extends Component {

  render() {
    return (
      <p>A tweet will live here soon.</p>
    )
  }
}

SentTweet.propTypes = {
  clipId: PropTypes.number,
  createdAt: PropTypes.number.isRequired,
  message: PropTypes.string.isRequired,
  permalink: PropTypes.string.isRequired,
  tweetTwtrId: PropTypes.string.isRequired,
  userId: PropTypes.number.isRequired
}