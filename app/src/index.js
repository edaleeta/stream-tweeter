import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';
import { BrowserRouter } from 'react-router-dom';
import { Grid } from 'react-bootstrap';

ReactDOM.render((
  <BrowserRouter>
    <Grid>
      <App />
    </Grid>
  </BrowserRouter>
), document.getElementById('root'));
registerServiceWorker();
