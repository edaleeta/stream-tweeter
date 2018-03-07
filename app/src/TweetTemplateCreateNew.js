import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { FormGroup, ControlLabel, FormControl, Button } from 'react-bootstrap';
import { TweetPlaceholder } from './TweetPlaceholder'

export class TweetTemplateCreateNew extends Component {
  constructor(props) {
    super(props);
    this.state = {
      contents: "Enter your tweet here! Use placeholders, such as ${game}, to include your streamed game's title!",
      defaultContents: "Enter your tweet here! Use placeholders, such as ${game}, to include your streamed game's title!"
    };
    this.handleClick = this.handleClick.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleFocus = this.handleFocus.bind(this);
    this.createPlaceholders = this.createPlaceholders.bind(this);
  }

  handleClick(e) {
    e.preventDefault();
    console.log(this.state.contents);
    console.log(JSON.stringify(this.state));
    let url = "/api/add-tweet-template";
    let payload = JSON.stringify({
      contents: this.state.contents.trim()
    });

    fetch(url, {
        credentials: 'same-origin',
        method: 'POST',
        body: payload, 
        headers: new Headers({
        'Content-Type': 'application/json'
        })
    })
    .then(res => res.json())
    .catch(error => console.error('Error:', error))
    .then(response => {
        this.props.onClick();
        // Clear contents of textbox after submitting.
        this.setState({
          contents: "Your new template has been saved!"
        });
    })
  }

  handleChange(e) {
    this.setState({
      contents: e.target.value
    });
  }

  handleFocus(e) {
    // Clear default text when user clicks into textarea.
    if (this.state.contents === this.state.defaultContents) {
      this.setState({
        contents: ""
      });
    }
  }

  createPlaceholders() {
    const lowerTwitchDisplayName = this.props.twitchDisplayName.toLowerCase()
    const urlHelp = (
      <p>
        Input {"${url}"} to include the link to your live stream in your tweet.
        <br />
        Ex: https://twitch.tv/{lowerTwitchDisplayName}
      </p>
    )
    const gameHelp = (
      <p>
        Input {"${game}"} to include the name of the game you're streaming in your tweet.
      </p>
    )
    const titleHelp = (
      <p>
        Input {"${stream_title}"} to include the title of your stream in your tweet.
      </p>
    )
    const viewersHelp = (
      <p>
        Input {"${viewers}"} to include the viewer count of your stream.
      </p>
    )

    const placeholders = (
      <span className="placeholders">
        <TweetPlaceholder
          name="${url}"
          helpText={urlHelp}
        />

        <TweetPlaceholder
        name="${game}"
        helpText={gameHelp}
        />

        <TweetPlaceholder
          name="${stream_title}"
          helpText={titleHelp}
        />

        <TweetPlaceholder
          name="${viewers}"
          helpText={viewersHelp}
        />
      </span>
    )

    return placeholders;
  }


  render() {
    return (
      <form className="create-new">
        <FormGroup>
          <ControlLabel><h4 style={{display: "inline"}}>Available placeholders:</h4>{this.createPlaceholders()}</ControlLabel>
          <FormControl
            onFocus={this.handleFocus}
            onChange={this.handleChange}
            componentClass="textarea"
            value={this.state.contents}
          >
          </FormControl>
          <Button
            type="submit"
            bsStyle="success"
            onClick={this.handleClick}
          >
            Save Tweet Template
          </Button>
        </FormGroup>
      </form>
    );
  }
}

TweetTemplateCreateNew.propTypes = {
  onClick: PropTypes.func.isRequired,
  twitchDisplayName: PropTypes.string.isRequired
}