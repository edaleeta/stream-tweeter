import React, { Component } from "react";
import PropTypes from "prop-types";
import { ConnectTwitter } from "./ConnectTwitter";
import { TweetTemplates } from "./TweetTemplates";
import { TweetOptions } from "./TwitterOptions";
import { WelcomeUser } from "./WelcomeUser";
import { Row, Col } from "react-bootstrap";

export class Home extends Component {
  render() {
    return (
      <div>
        <Row>
          <Col xs={12} md={7}>
            <WelcomeUser twitchDisplayName={this.props.twitchDisplayName} />
            <ConnectTwitter isTwitterAuth={this.props.isTwitterAuth} />
            <TweetTemplates
              isTwitterAuth={this.props.isTwitterAuth}
              userId={this.props.userId}
              twitchDisplayName={this.props.twitchDisplayName}
            />
          </Col>
          <Col xs={12} md={5}>
            <TweetOptions
              isTwitterAuth={this.props.isTwitterAuth}
              userId={this.props.userId}
              tweetInterval={this.props.tweetInterval}
              isTweeting={this.props.isTweeting}
              onClick={this.props.onClick}
            />
          </Col>
        </Row>
      </div>
    );
  }
}

Home.propTypes = {
  isTwitterAuth: PropTypes.bool.isRequired,
  userId: PropTypes.number.isRequired,
  tweetInterval: PropTypes.number.isRequired,
  isTweeting: PropTypes.bool,
  onClick: PropTypes.func.isRequired,
  twitchDisplayName: PropTypes.string
};
