import React, { Component } from "react";
import PropTypes from "prop-types";
import {
  FormGroup,
  ControlLabel,
  FormControl,
  HelpBlock,
  Button,
  Row,
  Col
} from "react-bootstrap";

export class TweetOptionsInterval extends Component {
  constructor(props) {
    super(props);
    this.state = {
      // We actually want to show the user's current tweet interval setting here, or default to 30 if not yet set.
      value: this.props.tweetInterval
    };
    this.getValidationState = this.getValidationState.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleClick = this.handleClick.bind(this);
  }

  handleChange(e) {
    e.target.value = e.target.value < 0 ? "" : e.target.value;

    this.setState({
      value: e.target.value
    });
  }

  handleClick(e) {
    e.preventDefault();

    // Prevent user from submitting invalid number of minutes.
    if (this.getValidationState() != null) {
      return null;
    }

    let url = "/api/update-user-settings";
    let payload = JSON.stringify({
      userId: this.props.userId,
      tweetInterval: this.state.value
    });

    console.log(payload);

    fetch(url, {
      credentials: "same-origin",
      method: "POST",
      body: payload,
      headers: new Headers({
        "Content-Type": "application/json"
      })
    })
      .then(res => res.json())
      .catch(error => console.error("Error:", error))
      .then(response => {
        console.log("Success:", response);
      });
  }
  getValidationState() {
    if (this.state.value < 30) {
      return "warning";
    }
    return null;
  }

  render() {
    let minutesText = this.state.value <= 1 ? "Minute" : "Minutes";

    return (
      <div>
        <form>
          <FormGroup
            controlId="tweetSettingsForm"
            validationState={this.getValidationState()}
            bsSize="lg"
          >
            <Row>
              <Col xs={12}>
                <ControlLabel>
                  <h4>Set Tweet interval in minutes.</h4>
                </ControlLabel>
              </Col>
            </Row>
            <Row>
              <Col md={4}>
                <FormControl
                  type="number"
                  value={this.state.value}
                  onChange={this.handleChange}
                />
              </Col>
              <Col md={8}>
                <Button
                  bsSize="large"
                  type="submit"
                  onClick={this.handleClick}
                  value={this.state.value}
                >
                  Set to {this.state.value} {minutesText}
                </Button>
              </Col>
            </Row>
            <HelpBlock
              style={
                this.getValidationState() === null
                  ? { display: "none" }
                  : { display: "block" }
              }
            >
              Don't spam your friends! Value must be greater than 30 minutes.
            </HelpBlock>
          </FormGroup>
        </form>
      </div>
    );
  }
}

TweetOptionsInterval.propTypes = {
  userId: PropTypes.number.isRequired,
  tweetInterval: PropTypes.number.isRequired
};
