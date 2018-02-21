import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { TweetTemplateContainer } from './TweetTemplateContainer'

export class TweetTemplates extends Component {
    
    constructor(props) {
        super(props);
        this.state = {templates: ""};
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

    render() {
        if (this.props.isTwitterAuth && this.state.templates) {
            
            return (
                <div>
                    <h3>Your Tweet Templates</h3>
                    {this.state.templates.map((template, key) => (
                        <TweetTemplateContainer template={template} key={key} />
                    ))}
                </div>
            );

            // return (
                // <div>
                //     Tweet templates will live here!
                //     <p>
                //         {this.state.templates.map((template) => (
                //             <p>ID: {template.templateId}; Content: {template.contents}</p>
                //         ))}
                //     </p>
                // </div>
            // );
        } else {
            return <div></div>
        }
    }
}

TweetTemplates.propTypes = {
    isTwitterAuth: PropTypes.bool.isRequired
}