import React from 'react';
import MenuElement from './components/MenuElement.js';

const Homepage = (props) => {
  return (
    <React.Fragment>
      <MenuElement href='/stations' name='Stations'/>
      <MenuElement href='/data' name='Data'/>
      <MenuElement href='/edu' name='Education'/>
      <MenuElement href='/about' name='About the Project'/>
    </React.Fragment>
  );
};

export default Homepage;