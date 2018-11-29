import React, { Component } from "react";
import PropTypes from "prop-types";
import { Button } from "react-bootstrap";

export class TweetTemplateEditButton extends Component {
  render() {
    let buttonText = this.props.isEditHidden ? "Edit Template" : "Cancel";

    return (
      <Button
        value={this.props.templateId}
        onClick={this.props.onClick}
        bsStyle="primary"
      >
        {buttonText}
      </Button>
    );
  }
}

TweetTemplateEditButton.propTypes = {
  templateId: PropTypes.number.isRequired,
  isEditHidden: PropTypes.bool.isRequired
};
