import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Navbar, Nav, NavItem } from 'react-bootstrap';
// import './MainNavBar.css';

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
          <NavItem eventKey={1}
              componentClass={Link}
              href="/"
              to="/"
            >
              Home
            </NavItem>
            <NavItem eventKey={2}
              componentClass={Link}
              href="/log"
              to="/log"
            >
              View Log
            </NavItem>
          </Nav>
          <Nav pullRight>
            <NavItem eventKey={3} href="#">
              Help
            </NavItem>
            <NavItem eventKey={4} href={navLinks.logout}>
              Logout
            </NavItem>
          </Nav>
        </Navbar.Collapse>
    </Navbar>
    );
  }

}