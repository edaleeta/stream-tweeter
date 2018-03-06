import React, { Component } from 'react';
import {Row, Col, Panel } from 'react-bootstrap';

export class Landing extends Component {

  render() {
    return(
      <div className="aligner landing">
        <div class="aligner-item aligner-item--top"></div>
        <div className="aligner-item">
          <Panel>
            <h1>Stream Tweeter<br />
              <small>A social media automation tool for Twitch streamers.</small>
            </h1>
            <h2>
              <a href="/login/twitch" className="login">
              Log in with Twitch
              </a> to get started.
          </h2>
          </Panel>
         </div>
        <div class="aligner-item aligner-item--bottom"></div>
      </div>
    )
  }
}