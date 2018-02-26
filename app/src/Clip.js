import React, { Component } from 'react';
import PropTypes from 'prop-types';

export class Clip extends Component {

  componentWillMount() {
    // Fetch to get clip info.
  }

  render() {
    const clip = (
      <iframe
        src="https://clips.twitch.tv/embed?clip=BigTemperedTroutEagleEye&autoplay=false"
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