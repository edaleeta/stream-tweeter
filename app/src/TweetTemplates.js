import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { TweetTemplatesCurrent } from './TweetTemplatesCurrent'
import { TweetTemplateCreateNew } from './TweetTemplateCreateNew'
import { StartTweetingButton } from './StartTweetingButton'

export class TweetTemplates extends Component {
  
  constructor(props) {
    super(props);
    this.state = {
      isUpdated: false
    };
    this.onClickUpdateTweetTemplatesCurrent = this.onClickUpdateTweetTemplatesCurrent.bind(this);
  }

  onClickUpdateTweetTemplatesCurrent() {
    this.setState({
      isUpdated: true
    });
  }

  render() {
    if (this.props.isTwitterAuth) {
      return (
        <div>
          <StartTweetingButton userId={this.props.userId} />
          <h3>Your Tweet Templates</h3>
          <TweetTemplatesCurrent onClick={this.onClickUpdateTweetTemplatesCurrent} isUpdated={this.state.isUpdated}/>
          <TweetTemplateCreateNew onClick={this.onClickUpdateTweetTemplatesCurrent} />
        </div>
      ); 
    } else {
      return <div></div>
    }
  }
}

TweetTemplates.propTypes = {
  isTwitterAuth: PropTypes.bool.isRequired,
  userId: PropTypes.number.isRequired
}