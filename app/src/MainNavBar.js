import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Navbar, Nav, NavItem } from 'react-bootstrap';
import { HelpModal } from './HelpModal'
// import './MainNavBar.css';

const navLinks = {
  home: "/",
  login: "/login/twitch",
  logout: "/logout",
  log: "/log"
}

// Navigation 
export class MainNavBar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      showHelp: false
    };
  }

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
            <NavItem eventKey={3} onClick={()=>this.setState({showHelp: true})}>
              Help
            </NavItem>
            <NavItem eventKey={4} href={navLinks.logout}>
              Logout
            </NavItem>
          </Nav>
        </Navbar.Collapse>
        <HelpModal
          show={this.state.showHelp}
          onHide={() => this.setState({showHelp: false})}
        />
      </Navbar>
    );
  }

}