import React, { Component } from 'react';
import PropTypes from 'prop-types';

export class SentTweetsContainer extends Component {

  render() {
    return (
      <div>
        Hi! Tweets will live inside of me.
      </div>
    )
  }
}

SentTweetsContainer.propTypes = {
  tweets: PropTypes.array.isRequired
}