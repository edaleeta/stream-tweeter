import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ConnectTwitter } from './ConnectTwitter'
import { TweetTemplates } from './TweetTemplates'
import { TweetOptions } from './TwitterOptions'

export class Main extends Component {

  render() {
    return (
      <div>
        <ConnectTwitter isTwitterAuth={this.props.isTwitterAuth} />
        <TweetOptions
          isTwitterAuth={this.props.isTwitterAuth}
          userId={this.props.userId}
          tweetInterval={this.props.tweetInterval}
          onClick={this.props.onClick}
        />
        <TweetTemplates isTwitterAuth={this.props.isTwitterAuth}
          userId={this.props.userId}
        />
      </div>
    )
  
  }
}

Main.propTypes = {
  isTwitterAuth: PropTypes.bool.isRequired,
  userId: PropTypes.number.isRequired,
  tweetInterval: PropTypes.number.isRequired,
  onClick:PropTypes.func.isRequired
}


