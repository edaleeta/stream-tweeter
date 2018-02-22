import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ButtonToolbar } from 'react-bootstrap';
import { TweetTemplateText } from './TweetTemplateText';
import { TweetTemplateDeleteButton } from './TweetTemplateDeleteButton';
import { TweetTemplateEditButton } from './TweetTemplateEditButton';
import { TweetTemplateEditForm } from './TweetTemplateEditForm';

export class TweetTemplateContainer extends Component {

    constructor(props) {
        super(props);
        this.state = {
            isEditHidden: true
        }
        this.handleClickEdit = this.handleClickEdit.bind(this);
    }

    handleClickEdit() {
        let isEditHidden = this.state.isEditHidden ? false : true
        console.log("Changing isEditHidden to ", isEditHidden);
        this.setState({
            isEditHidden: isEditHidden
        })
    }

    render() {
        return (
            <div>
                <TweetTemplateText contents={this.props.template.contents} />
                <ButtonToolbar>
                    <TweetTemplateDeleteButton onClick={this.props.onClick} templateId={this.props.template.templateId} />
                    <TweetTemplateEditButton onClick={this.handleClickEdit} templateId={this.props.template.templateId} />
                </ButtonToolbar>
                <TweetTemplateEditForm onClick={this.props.onClick} hidden={this.state.isEditHidden} contents={this.props.template.contents} />
            </div>
        )
    }
}

TweetTemplateContainer.propTypes = {
    template: PropTypes.object.isRequired,
    onClick: PropTypes.func.isRequired
}