import React from "react";

import Login from './components/Login'
import AbstractPage from './components/AbstractPage'
import Dashboard from "./components/Dashboard";
import DeviceTable from "./components/DeviceTable";

const authorized = false;

const App = () => {
  return (
    <AbstractPage>
        {authorized ? <></>  : <Login />}
        <Dashboard />
        <DeviceTable />
    </AbstractPage>
  );
}

export default App;
