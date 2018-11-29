import React, { Component } from "react";
import FontAwesomeIcon from "@fortawesome/react-fontawesome";
import faHeart from "@fortawesome/fontawesome-free-solid/faHeart";

const heart = <FontAwesomeIcon icon={faHeart} color="#b22222" />;
export class MadeWithLove extends Component {
  render() {
    return (
      <small className="made-with-love">
        made with {heart} by{" "}
        <a href="http://edaleeta.com" target="_blank" rel="noopener noreferrer">
          edaleeta
        </a>
        . &copy; 2018
      </small>
    );
  }
}
