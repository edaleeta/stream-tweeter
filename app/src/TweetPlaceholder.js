import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Tooltip, OverlayTrigger } from 'react-bootstrap';

export class TweetPlaceholder extends Component {

  render() {

    let tooltip = (
      <Tooltip id={this.props.name}>
        {this.props.helpText}
      </Tooltip>
    )

    return (
      <OverlayTrigger placement="top" overlay={tooltip}>
        <span className="placeholder">{this.props.name}</span>
      </OverlayTrigger>
    );
  }
}

TweetPlaceholder.propTypes = {
  name: PropTypes.string.isRequired,
  helpText: PropTypes.object.isRequired
}