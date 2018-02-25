import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { convertTimeStamp } from './services/log'
import AutoLinker from 'autolinker';

export class SentTweet extends Component {

  render() {
    return (
      <div>
        <h4>Tweet {this.props.tweetTwtrId}</h4>
        <span>Created: </span><span>{convertTimeStamp(this.props.createdAt)}</span>
        <br />
        <span>Message: </span><span>{this.props.message}</span>
        <br />
        <a href={this.props.permalink} target="_blank">View on Twitter</a>
        
      </div>
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