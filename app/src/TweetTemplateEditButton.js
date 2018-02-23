import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Button } from 'react-bootstrap';

export class TweetTemplateEditButton extends Component {

  render() {
    return (
      <Button
        className="del-edit-button"
        value={this.props.templateId}
        onClick={this.props.onClick}
      >
        Edit Template
      </Button>
    )
  }
}

TweetTemplateEditButton.propTypes = {
  templateId: PropTypes.number.isRequired
}