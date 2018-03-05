import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Navbar, Nav, NavItem } from 'react-bootstrap';
import './MainNavBar.css';

const navLinks = {
  home: "/",
  login: "/login/twitch",
  logout: "/logout",
  log: "/log"
}

// Navigation 
export class MainNavBar extends Component {
  render() {
    return (
      <Navbar fluid={true}>
        <Navbar.Header>
          <Navbar.Brand>
            <Link to={navLinks.home}>Stream Tweeter</Link>
          </Navbar.Brand>
          <Navbar.Toggle />
        </Navbar.Header>
        <Navbar.Collapse>
          <Nav>
            <NavItem eventKey={1} href={navLinks.login}>
              Login
            </NavItem>
            <NavItem eventKey={2} href={navLinks.logout}>
              Logout
            </NavItem>
            <NavItem eventKey={3}
              componentClass={Link}
              href="/log"
              to="/log"
            >
              View Log
            </NavItem>
          </Nav>
          <Nav pullRight>
            <NavItem eventKey={1} href="#">
              Help
            </NavItem>
          </Nav>
        </Navbar.Collapse>
    </Navbar>
    );
  }

}