import React, { Component } from "react";
import PropTypes from "prop-types";
import { Row, Col } from "react-bootstrap";
import { TweetTemplatesCurrent } from "./TweetTemplatesCurrent";
import { TweetTemplateCreateNew } from "./TweetTemplateCreateNew";

export class TweetTemplates extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isUpdated: false
    };
    this.onClickUpdateTweetTemplatesCurrent = this.onClickUpdateTweetTemplatesCurrent.bind(
      this
    );
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
          <Row>
            <Col xs={12}>
              <h2>Create a new Tweet Template</h2>
            </Col>
          </Row>
          <Row>
            <Col xs={12}>
              <TweetTemplateCreateNew
                onClick={this.onClickUpdateTweetTemplatesCurrent}
                twitchDisplayName={this.props.twitchDisplayName}
              />
            </Col>
          </Row>
          <Row>
            <Col xs={12}>
              <h2>Your Tweet Templates</h2>
            </Col>
          </Row>
          <Row>
            <Col xs={12}>
              <TweetTemplatesCurrent
                onClick={this.onClickUpdateTweetTemplatesCurrent}
                isUpdated={this.state.isUpdated}
              />
            </Col>
          </Row>
        </div>
      );
    } else {
      return <div />;
    }
  }
}

TweetTemplates.propTypes = {
  isTwitterAuth: PropTypes.bool.isRequired,
  userId: PropTypes.number.isRequired,
  twitchDisplayName: PropTypes.string
};
