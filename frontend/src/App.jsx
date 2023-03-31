import React from "react";

import Login from './components/Login'
import AbstractPage from './components/AbstractPage'
import Dashboard from "./components/Dashboard";
import DeviceTable from "./components/DeviceTable";
import CreateDevice from "./components/CreateDevice";

const authorized = false;

const App = () => {
  return (
    <AbstractPage>
        {authorized ? <></>  : <Login />}
        <Dashboard />
        <CreateDevice />
        <DeviceTable />
    </AbstractPage>
  );
}

export default App;
