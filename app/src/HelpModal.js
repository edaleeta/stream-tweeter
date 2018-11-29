import React, { Component } from "react";
import PropTypes from "prop-types";
import { Button, Modal, ListGroup, ListGroupItem } from "react-bootstrap";

export class HelpModal extends Component {
  render() {
    return (
      <Modal {...this.props} aria-labelledby="contained-modal-title-lg">
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-lg">
            Stream Tweeter Help
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <h3>What does Stream Tweeter do?</h3>
          <ListGroup>
            <ListGroupItem>
              <p>
                While you're live on Twitch, a tweet will be sent out at your
                defined interval. Use them to let your Twitter audienece know
                you're online and invite them to watch!
              </p>
              <p>
                The tweet text will be randomly selected from your configured
                "Tweet Templates" and will include a Twitch Clip of your stream
                at publishing time.
              </p>
              {/* eslint-disable no-template-curly-in-string */}
              <p>
                Use placeholders, such as {"${url}"} or {"${game}"} in your
                Tweet Template and they'll be filled in automatically when your
                tweet is published.
              </p>
              {/* eslint-enable no-template-curly-in-string */}
              <p>
                Hit 'View Log' in the menu to see your live stream stats,
                published tweets, and generated Twitch Clips from your stream
                sessions.
              </p>
            </ListGroupItem>
          </ListGroup>
          <small>
            Stream Tweeter is very much in beta! This site may experience
            downtime and strange behavior may occur.
            <br />
            Feel free to drop me a note{" "}
            <a
              href="https://twitter.com/edaleeta"
              target="_blank"
              rel="noopener noreferrer"
            >
              @edaleeta
            </a>
            .
          </small>
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={this.props.onHide}>Close</Button>
        </Modal.Footer>
      </Modal>
    );
  }
}

HelpModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onHide: PropTypes.func.isRequired
};
