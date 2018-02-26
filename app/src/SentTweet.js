import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ListGroupItem, Button, Col, Row } from 'react-bootstrap';
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

    return (
      <Row>
        <Col xs={12} md={4}>
          <ListGroupItem
          header={"Tweet Created: " + convertTimeStampToDateTime(this.props.createdAt)}
          target="_blank"
          >
            <span>Message: </span><span dangerouslySetInnerHTML={{__html: messageHTML}}></span>
            <br /><br />
            <Button 
              href={this.props.permalink}
              target="_blank"
            >
              View on Twitter
            </Button>
            <Button
              onClick={this.handleClickToggleClip}>
                {clipButtonText}
            </Button>
          </ListGroupItem>
        </Col>
        <Col xs={12} md={8}>
          <ClipContainer
            clipId={this.props.clipId}
            clipHidden={this.state.clipHidden}
            clipLoaderShown={this.state.clipLoaderShown}
            onLoadEmbed={this.handleOnLoadEmbed}
          />
        </Col>
      </Row>
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