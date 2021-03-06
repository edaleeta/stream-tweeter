import React, { Component } from "react";
import PropTypes from "prop-types";

export class WelcomeUser extends Component {
  render() {
    if (this.props.twitchDisplayName) {
      return <h2>Welcome, {this.props.twitchDisplayName}!</h2>;
    } else {
      return (
        <h2>
          Welcome!{" "}
          <a href="/login/twitch" className="primary">
            Log in with Twitch
          </a>{" "}
          to get started!
        </h2>
      );
    }
  }
}

WelcomeUser.propTypes = {
  twitchDisplayName: PropTypes.string
};
