import React, { Component } from 'react';
import PropTypes from 'prop-types';
export class ConnectTwitter extends Component {

  render() {
      if (this.props.isTwitterAuth) {
          return (
              <p>
                  Your Twitter is account is connected! <br />
                  Let's make some Tweets!
              </p>
          );
      }
      return (
          <p>
              To get started, please connect your Twitter account:<br />
              <a href="/auth-twitter">Connect Twitter</a>
          </p>
      )
  }
}

ConnectTwitter.propTypes = {
  isTwitterAuth: PropTypes.bool.isRequired,
}