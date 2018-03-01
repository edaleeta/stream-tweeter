import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { TweetOptionsInterval } from './TweetOptionsInterval'
import { TweetOptionsRevoke } from './TweetOptionsRevoke'
import { StartTweetingButton } from './StartTweetingButton'
import { Row, Col, ButtonToolbar } from 'react-bootstrap';

export class TweetOptions extends Component {
  
  constructor(props) {
    super(props);
    this.state = {
      isUpdated: false
    }
  };

  render() {
    if (this.props.isTwitterAuth) {
      return (
        <Col>
          <Row>
            <h2>Tweet Options</h2>
          </Row>
          <Row>
            <TweetOptionsInterval
              userId={this.props.userId}
              tweetInterval={this.props.tweetInterval}
            />
          </Row>
          <Row>
            <ButtonToolbar>
              <StartTweetingButton userId={this.props.userId} />
              <TweetOptionsRevoke
                userId={this.props.userId}
                tweetInterval={this.props.tweetInterval}
                onClick={this.props.onClick}
              />
            </ButtonToolbar>
          </Row>
        </Col>
      ); 
    } else {
      return <div></div>
    }
  }
}



TweetOptions.propTypes = {
  isTwitterAuth: PropTypes.bool.isRequired,
  userId: PropTypes.number.isRequired,
  tweetInterval: PropTypes.number.isRequired,
  onClick: PropTypes.func.isRequired
}