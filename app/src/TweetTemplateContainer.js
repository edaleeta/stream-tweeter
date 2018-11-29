import React, { Component } from "react";
import PropTypes from "prop-types";
import { ButtonToolbar } from "react-bootstrap";
import { TweetTemplateText } from "./TweetTemplateText";
import { TweetTemplateDeleteButton } from "./TweetTemplateDeleteButton";
import { TweetTemplateEditButton } from "./TweetTemplateEditButton";
import { TweetTemplateEditForm } from "./TweetTemplateEditForm";

export class TweetTemplateContainer extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isEditHidden: true
    };
    this.handleClickEdit = this.handleClickEdit.bind(this);
    this.handleClickSave = this.handleClickSave.bind(this);
  }

  // Passed to EditButton to toggle Edit Form.
  handleClickEdit() {
    let isEditHidden = this.state.isEditHidden ? false : true;
    this.setState({
      isEditHidden: isEditHidden
    });
  }

  // Passed to EditForm to close form after saving edits.
  // And tells TweetTemplates an update happened.
  handleClickSave() {
    this.props.onClick();
    this.setState({
      isEditHidden: true
    });
  }

  render() {
    return (
      <div>
        <TweetTemplateText contents={this.props.template.contents} />
        <ButtonToolbar>
          <TweetTemplateDeleteButton
            onClick={this.props.onClick}
            templateId={this.props.template.templateId}
          />
          <TweetTemplateEditButton
            onClick={this.handleClickEdit}
            templateId={this.props.template.templateId}
            isEditHidden={this.state.isEditHidden}
          />
        </ButtonToolbar>
        <TweetTemplateEditForm
          onClick={this.handleClickSave}
          hidden={this.state.isEditHidden}
          templateId={this.props.template.templateId}
          contents={this.props.template.contents}
        />
      </div>
    );
  }
}

TweetTemplateContainer.propTypes = {
  template: PropTypes.object.isRequired,
  onClick: PropTypes.func.isRequired
};
