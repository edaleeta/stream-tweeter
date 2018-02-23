import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Button } from 'react-bootstrap';

export class TweetTemplateDeleteButton extends Component {

  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(e) {
    console.log(e.target.value);
    this.props.onClick();

    let url = "/api/delete-tweet-template";
    let payload = JSON.stringify({"templateId": this.props.templateId});

    fetch(url, {
      credentials: 'same-origin',
      method: 'POST',
      body: payload, 
      headers: new Headers({
      'Content-Type': 'application/json'
      })
    })
    .then(res => {
      console.log(res)
      res.json();
    })
    .catch(error => console.error('Error:', error))
    .then(response => {
        console.log('Success:', response);
        // Tells Tweet Templates that we deleted a Template!
        this.props.onClick();
    })        
  }

  render() {
    return (
      <Button bsStyle="danger" className="del-tweet-button" value={this.props.templateId} onClick={this.handleClick}>
        Delete Template
      </Button>
    );
  }
}

TweetTemplateDeleteButton.propTypes = {
  templateId: PropTypes.number.isRequired,
  onClick: PropTypes.func.isRequired
}