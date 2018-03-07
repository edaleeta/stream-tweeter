import React, { Component } from 'react';
import PropTypes from 'prop-types';


export class Clip extends Component {

  componentWillMount() {
    // Fetch to get clip info.
  }

  render() {
    const clip = (
      <div class="embed-responsive embed-responsive-16by9 clip-container">
        <iframe
          src={"https://clips.twitch.tv/embed?clip="+this.props.clipSlug+"&autoplay=false"}
          title={this.props.clipSlug}
          frameBorder={0}
          scrolling="no"
          allowFullScreen={false}
          preload="none"
          className="embed-responsive-item"
          onLoad={this.props.onLoad}
        >
        </iframe>
      </div>
    );
    return this.props.hidden ? <div></div> : clip
  }
}

Clip.propTypes = {
  clipSlug: PropTypes.string,
  hidden: PropTypes.bool.isRequired,
  onLoad: PropTypes.func.isRequired
}