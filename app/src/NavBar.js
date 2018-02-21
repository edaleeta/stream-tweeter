import React, { Component } from 'react';

const navLinks = {
    home: "/",
    login: "http://localhost:7000/login/twitch",
    logout: "http://localhost:7000/logout"
}

// Navigation 
export class NavBar extends Component {
    render() {
        return (
            <ul>
            <li><a href={navLinks.home}>Home</a></li>
            <li><a href={navLinks.login}>Login</a></li>
            <li><a href={navLinks.logout}>Logout</a></li>
        </ul>
        )
    }
}