import React, { Component } from 'react';
import { Link } from 'react-router-dom';

const navLinks = {
  home: "/",
  login: "/login/twitch",
  logout: "/logout",
  log: "/log"
}

// Navigation 
export class NavBar extends Component {
  render() {
    return (
      <ul>
      <li><Link to={navLinks.home}>Home</Link></li>
      <li><a href={navLinks.login}>Login</a></li>
      <li><a href={navLinks.logout}>Logout</a></li>
      <li><Link to={navLinks.log}>Log</Link></li>
    </ul>
    );
  }
}