import React from 'react';
import ReactDOM from 'react-dom';
// import './index.css';
// import './styles.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';
import { BrowserRouter } from 'react-router-dom';
import { Grid } from 'react-bootstrap';

ReactDOM.render((
  <BrowserRouter>
    <Grid fluid={false}>
      <App />
    </Grid>
  </BrowserRouter>
), document.getElementById('root'));
registerServiceWorker();
