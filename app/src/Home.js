import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ConnectTwitter } from './ConnectTwitter'
import { TweetTemplates } from './TweetTemplates'
import { TweetOptions } from './TwitterOptions'
import { Row, Col } from 'react-bootstrap';

export class Home extends Component {

  render() {
    return (
      <Row>
          <Row>
            <Col xs={12} md={8}>
              <ConnectTwitter isTwitterAuth={this.props.isTwitterAuth} />
            </Col>
          </Row>
          <Row>
            <Col xs={12} md={8}>
              <TweetTemplates isTwitterAuth={this.props.isTwitterAuth}
                userId={this.props.userId}
              />
            </Col>
            <Col xs={12} md={4}>
              <TweetOptions
                isTwitterAuth={this.props.isTwitterAuth}
                userId={this.props.userId}
                tweetInterval={this.props.tweetInterval}
                onClick={this.props.onClick}
              />
            </Col>
          </Row>
      </Row>
    )
  
  }
}

Home.propTypes = {
  isTwitterAuth: PropTypes.bool.isRequired,
  userId: PropTypes.number.isRequired,
  tweetInterval: PropTypes.number.isRequired,
  onClick:PropTypes.func.isRequired
}


