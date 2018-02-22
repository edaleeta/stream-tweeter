import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ButtonToolbar } from 'react-bootstrap';
import { TweetTemplateText } from './TweetTemplateText';
import { TweetTemplateDeleteButton } from './TweetTemplateDeleteButton';
import { TweetTemplateEditButton } from './TweetTemplateEditButton';

export class TweetTemplateContainer extends Component {

    render() {
        return (
            <div>
                <TweetTemplateText contents={this.props.template.contents} />
                <ButtonToolbar>
                    <TweetTemplateDeleteButton onClick={this.props.onClick} templateId={this.props.template.templateId} />
                    <TweetTemplateEditButton onClick={this.props.onClick} templateId={this.props.template.templateId} />
                </ButtonToolbar>
            </div>
        )
    }
}

TweetTemplateContainer.propTypes = {
    template: PropTypes.object.isRequired,
    onClick: PropTypes.func.isRequired
}