import React, { Component } from "react";
import PropTypes from "prop-types";

export class Clip extends Component {
  render() {
    const clip = (
      <div className="embed-responsive embed-responsive-16by9 clip-container">
        <iframe
          src={
            "https://clips.twitch.tv/embed?clip=" +
            this.props.clipSlug +
            "&autoplay=false"
          }
          title={this.props.clipSlug}
          frameBorder={0}
          scrolling="no"
          allowFullScreen={false}
          preload="none"
          className="embed-responsive-item"
          onLoad={this.props.onLoad}
        />
      </div>
    );
    return this.props.hidden ? <div /> : clip;
  }
}

Clip.propTypes = {
  clipSlug: PropTypes.string,
  hidden: PropTypes.bool.isRequired,
  onLoad: PropTypes.func.isRequired
};
