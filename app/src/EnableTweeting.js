import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Switch from "react-switch";

export class EnableTweeting extends Component {
  constructor(props) {
    super(props);
    this.state = {
      enabled: this.props.isTweeting
    }
    this.handleChange = this.handleChange.bind(this);

    console.log(this.state.enabled);
  }

  handleChange(e) {
    console.log(this.props.userId)

    this.setState({
      enabled: this.state.enabled ? false : true
    });
  }

  componentWillUpdate(nextProps, nextState) {
    let url = "/api/current-user.json"
    let payload = JSON.stringify({
      userId: this.props.userId,
      isTweeting: nextState.enabled
    });

    console.log(payload);
    fetch(url, {
      credentials: 'same-origin',
      method: 'PUT',
      body: payload, 
      headers: new Headers({
      'Content-Type': 'application/json'
      })
    })
    .then(res => res.json())
    .catch(error => console.error('Error:', error))
    .then(response => {
      console.log('Success:', response);
    })
  }

  render() {
    return (
      <label htmlFor="enable-tweeting-switch">
        <span>Enable or Disable automated Tweet sending while you're streaming.</span>
        <Switch
          onChange={this.handleChange}
          checked={this.state.enabled}
          id="enable-tweeting-switch"
        />
      </label>
    );
  }
}

EnableTweeting.propTypes = {
  userId: PropTypes.number.isRequired,
  isTweeting: PropTypes.bool
}