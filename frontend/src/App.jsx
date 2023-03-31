import React from "react";

import Login from './components/Login'
import AbstractPage from './components/AbstractPage'
import Dashboard from "./components/Dashboard";

const authorized = false;

const App = () => {
  return (
    <AbstractPage>
        {authorized ? <></>  : <Login />}
        <Dashboard />
    </AbstractPage>
  );
}

export default App;
