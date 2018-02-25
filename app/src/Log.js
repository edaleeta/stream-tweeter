import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { StreamSessions } from './StreamSessions';
import { Grid } from 'react-bootstrap';

export class Log extends Component {

  render() {
    return (
      <Grid fluid={true}>
        <h3>Your Stream Tweeter History</h3>
        <StreamSessions userId={this.props.userId} />
      </Grid>
    )
  
  }
}

Log.propTypes = {
  userId: PropTypes.number.isRequired,
}


