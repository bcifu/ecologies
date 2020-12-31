import './App.css';
import React from "react";
import {
  BrowserRouter,
  Switch,
  Route,
  Redirect,
} from "react-router-dom";
import Home from "./Home.js"
import Game from "./Game.js"
import { Navbar, NavbarBrand } from 'react-bootstrap';

function App() {
  return (
    <BrowserRouter>
      <Navbar>
        <NavbarBrand>Ecologies</NavbarBrand>
      </Navbar>
      <Switch>    
        <Route exact path="/"> 
          <Home/>
        </Route>   
        <Route path="/game/:id">
          <Game/>
        </Route>
        <Route><Redirect to="/"/></Route>
      </Switch>
    </BrowserRouter>
  );
}

export default App;
