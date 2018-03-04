import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { TweetOptionsInterval } from './TweetOptionsInterval'
import { TweetOptionsRevoke } from './TweetOptionsRevoke'
// import { StartTweetingButton } from './StartTweetingButton'
import { EnableTweeting } from './EnableTweeting'
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
        <Col xs={12}>
          <Row>
            <Col xs={12}>
              <h2>Tweet Options</h2>
            </Col>
          </Row>
          <Row>
            <Col xs={12}>
            <TweetOptionsInterval
              userId={this.props.userId}
              tweetInterval={this.props.tweetInterval}
            />
            </Col>
          </Row>
          <Row>
            <Col xs={12}>
              <ButtonToolbar>
                {/* <StartTweetingButton userId={this.props.userId} /> */}
                <EnableTweeting
                  userId={this.props.userId}
                  isTweeting={this.props.isTweeting}
                />
                <TweetOptionsRevoke
                  userId={this.props.userId}
                  tweetInterval={this.props.tweetInterval}
                  onClick={this.props.onClick}
                />
              </ButtonToolbar>
            </Col>
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
  isTweeting: PropTypes.bool,
  onClick: PropTypes.func.isRequired
}