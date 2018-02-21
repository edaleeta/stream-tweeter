import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { TweetTemplateContainer } from './TweetTemplateContainer'

export class TweetTemplatesCurrent extends Component {
    constructor(props) {
        super(props);
        this.state = {
            templates: "",
            isUpdated: props.isUpdated
        }
        this.onClickUpdateTweetTemplatesCurrent = this.onClickUpdateTweetTemplatesCurrent.bind(this);
    }

    componentDidMount() {
        fetch("/api/current-user-templates.json",
        {credentials: 'same-origin'})
        .then((response)=> response.json())
        .then((data) => {
            this.setState({
                templates: data
            });
        })        
    }

    componentWillUpdate() {
        fetch("/api/current-user-templates.json",
        {credentials: 'same-origin'})
        .then((response)=> response.json())
        .then((data) => {
            this.setState({
                templates: data
            });
        })        
    }


    onClickUpdateTweetTemplatesCurrent() {
        this.setState({
            isUpdated: true
        })
    }


    render() {
        if (this.state.templates) {
            return (this.state.templates.map((template, key) => (
                <TweetTemplateContainer template={template} key={key} onClick={this.onClickUpdateTweetTemplatesCurrent} />
            )))
        } else {
            return <div></div>
        }


    }
}

TweetTemplatesCurrent.propTypes = {
    isUpdated: PropTypes.bool.isRequired,
}