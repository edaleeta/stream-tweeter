import React, { Component } from 'react';
import PropTypes from 'prop-types';
// import './ConnectTwitter.css';
import { Well } from 'react-bootstrap'

export class ConnectTwitter extends Component {

  render() {
      if (this.props.isTwitterAuth) {
          return (
              <Well bsSize="small">
                  Your Twitter is account is connected! Let's make some Tweets!
              </Well>
          );
      }
      return (
          <Well bsSize="small">
              To get started, please connect your Twitter account:<br />
              <a href="/auth-twitter">Connect Twitter</a>
          </Well>
      )
  }
}

ConnectTwitter.propTypes = {
  isTwitterAuth: PropTypes.bool.isRequired,
}