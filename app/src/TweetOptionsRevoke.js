import React, { Component } from "react";
import PropTypes from "prop-types";
import { Button } from "react-bootstrap";

export class TweetOptionsRevoke extends Component {
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(e) {
    console.log(e.target.value);

    let url = "/api/revoke-twitter";
    let payload = JSON.stringify({ userId: this.props.userId });

    fetch(url, {
      credentials: "same-origin",
      method: "POST",
      body: payload,
      headers: new Headers({
        "Content-Type": "application/json"
      })
    })
      .then(res => res.json())
      .catch(error => console.error("Error:", error))
      .then(response => {
        console.log("Success:", response);
        if ("success" in response) {
          // Tells App that Twitter is no longer authenticated
          this.props.onClick();
        }
      });
  }

  render() {
    return (
      <div>
        <h4>Connect a new Twitter account.</h4>
        <Button
          bsSize="small"
          bsStyle="danger"
          value={this.props.userId}
          onClick={this.handleClick}
        >
          Disconnect Twitter Account
        </Button>
      </div>
    );
  }
}

TweetOptionsRevoke.propTypes = {
  userId: PropTypes.number.isRequired,
  onClick: PropTypes.func.isRequired
};
