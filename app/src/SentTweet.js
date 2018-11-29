import React, { Component } from "react";
import PropTypes from "prop-types";
import { ListGroupItem, Button, ButtonToolbar } from "react-bootstrap";
import { convertTimeStampToDateTime } from "./services/log";
import Autolinker from "autolinker";
import { ClipContainer } from "./ClipContainer";

export class SentTweet extends Component {
  state = {
    clipHidden: true,
    clipLoaderShown: false
  };

  handleClickToggleClip = e => {
    this.setState({
      clipHidden: this.state.clipHidden ? false : true,
      clipLoaderShown: true
    });

    // If the clip is shown, hide the loader when hiding the clip.
    if (!this.state.clipHidden) {
      this.setState({
        clipLoaderShown: false
      });
    }
  };

  handleOnLoadEmbed = () => {
    // Hide some spinner element when clip embed loads...
    this.setState({
      clipLoaderShown: false
    });
  };

  renderClipContainer = () => {
    const { clipId } = this.props;
    const { clipHidden, clipLoaderShown } = this.state;
    return clipId ? (
      <ClipContainer
        clipId={clipId}
        clipHidden={clipHidden}
        clipLoaderShown={clipLoaderShown}
        onLoadEmbed={this.handleOnLoadEmbed}
      />
    ) : (
      <div />
    );
  };

  renderViewClipButton = () => {
    const clipButtonText = this.state.clipHidden ? "View Clip" : "Hide Clip";
    return this.props.clipId ? (
      <Button onClick={this.handleClickToggleClip} bsStyle="primary">
        {clipButtonText}
      </Button>
    ) : (
      <span />
    );
  };

  render() {
    const { createdAt, message, permalink } = this.props;
    const messageHTML = Autolinker.link(message, {
      newWindow: true,
      truncate: 30
    });

    return (
      <div className="tweet-container">
        <ListGroupItem
          header={"Tweet Created: " + convertTimeStampToDateTime(createdAt)}
          target="_blank"
          className="tweet-card"
        >
          <br />
          <span dangerouslySetInnerHTML={{ __html: messageHTML }} />
          <p />
        </ListGroupItem>
        <ButtonToolbar>
          <Button href={permalink} target="_blank" bsStyle="primary">
            View on Twitter
          </Button>
          {this.renderViewClipButton()}
        </ButtonToolbar>
        {this.renderClipContainer()}
      </div>
    );
  }
}

SentTweet.propTypes = {
  clipId: PropTypes.number,
  createdAt: PropTypes.number.isRequired,
  message: PropTypes.string.isRequired,
  permalink: PropTypes.string.isRequired,
  tweetTwtrId: PropTypes.string.isRequired,
  userId: PropTypes.number.isRequired
};
