import React, { Component } from 'react';
import PropTypes from 'prop-types';

export class Clip extends Component {

  componentWillMount() {
    // Fetch to get clip info.
  }

  render() {
    const clip = (
      <iframe
        src={"https://clips.twitch.tv/embed?clip="+this.props.clipSlug+"&autoplay=false"}
        title={this.props.clipSlug}
        height={300}
        width={550}
        frameborder={0}
        scrolling="no"
        allowFullScreen={false}
        preload="none"
        className="center-block"
        onLoad={this.props.onLoad}
      >
      </iframe>
    );
    return this.props.hidden ? <div></div> : clip
  }
}

Clip.propTypes = {
  clipSlug: PropTypes.string,
  hidden: PropTypes.bool.isRequired,
  onLoad: PropTypes.func.isRequired
}