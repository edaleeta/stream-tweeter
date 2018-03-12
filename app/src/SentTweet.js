import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ListGroupItem, Button, ButtonToolbar } from 'react-bootstrap';
import { convertTimeStampToDateTime } from './services/log'
import Autolinker from 'autolinker';
import { ClipContainer } from './ClipContainer'

export class SentTweet extends Component {

  constructor(props) {
    super(props);
    this.state = {
      clipHidden: true,
      clipLoaderShown: false
    }
    this.handleClickToggleClip = this.handleClickToggleClip.bind(this);
    this.handleOnLoadEmbed = this.handleOnLoadEmbed.bind(this);
  }

  handleClickToggleClip(e) {
    this.setState({
      clipHidden: this.state.clipHidden ? false : true,
      clipLoaderShown: true,
    });

    // If the clip is shown, hide the loader when hiding the clip. 
    if (!this.state.clipHidden) {
      this.setState({
        clipLoaderShown: false
      });
    }
  }

  handleOnLoadEmbed() {
    // Hide some spinner element when clip embed loads...
    this.setState({
      clipLoaderShown: false
    })
  }

  render() {
    let messageHTML = Autolinker.link(this.props.message, {
      newWindow : true,
      truncate  : 30
    });

    let clipButtonText = this.state.clipHidden ? "View Clip" : "Hide Clip"
    let clipContainer, viewClipButton;
    if (this.props.clipId) {
      clipContainer = (
        <ClipContainer
          clipId={this.props.clipId}
          clipHidden={this.state.clipHidden}
          clipLoaderShown={this.state.clipLoaderShown}
          onLoadEmbed={this.handleOnLoadEmbed}
        />
      )
      viewClipButton = (
        <Button
          onClick={this.handleClickToggleClip}
          bsStyle="primary"
        >
            {clipButtonText}
        </Button>
      )
    } else {
      clipContainer = <div></div>
      viewClipButton = <span></span>
    }

    return (
      <div className="tweet-container">
        <ListGroupItem
          header={"Tweet Created: " + convertTimeStampToDateTime(this.props.createdAt)}
          target="_blank"
          className="tweet-card"
        >
          <br /><span dangerouslySetInnerHTML={{__html: messageHTML}}></span>
          <br /><br />
        </ListGroupItem>
        <ButtonToolbar>
          <Button 
            href={this.props.permalink}
            target="_blank"
            bsStyle="primary"
          >
            View on Twitter
          </Button>
          {viewClipButton}
        </ButtonToolbar>
        {clipContainer}
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