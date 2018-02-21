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
                    <TweetTemplateDeleteButton templateId={this.props.template.templateId} />
                    <TweetTemplateEditButton templateId={this.props.template.templateId} />
                </ButtonToolbar>
            </div>
        )
    }
}

TweetTemplateContainer.propTypes = {
    template: PropTypes.object.isRequired
}