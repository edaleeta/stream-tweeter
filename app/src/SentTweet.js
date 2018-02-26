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
      clipHidden: true
    }
    this.handleClickToggleClip = this.handleClickToggleClip.bind(this);
  }

  handleClickToggleClip(e) {
    this.setState({
      clipHidden: this.state.clipHidden ? false : true
    });
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
          <ClipContainer clipId={this.props.clipId}
            clipHidden={this.state.clipHidden}
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