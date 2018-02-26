import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Button } from 'react-bootstrap';
import { Clip } from './Clip'

export class ClipContainer extends Component {

  constructor(props) {
    super(props);
    this.state = {
      clipSlug: null,
    };
  }

  componentWillMount() {
    // Fetch to get clip info.
  }

  render() {
    return (
      <div> 
        <Clip
          clipSlug={this.state.clipSlug}
          hidden={this.props.clipHidden}
        />
      </div>
    )
  }
}

ClipContainer.propTypes = {
  clipId: PropTypes.number,
  clipHidden: PropTypes.bool.isRequired
}