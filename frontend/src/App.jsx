import React from "react";

import Login from './components/Login'
import AbstractPage from './components/AbstractPage'
import Dashboard from "./components/Dashboard";
import DeviceTable from "./components/DeviceTable";
import CreateDevice from "./components/CreateDevice";
import DeviceModal from "./components/DeviceModal";

const authorized = false;

const App = () => {
    return (
        <AbstractPage>
            {authorized ? <></> : <Login/>}
            <Dashboard/>
            <CreateDevice/>
            <DeviceTable/>
            <DeviceModal/>
        </AbstractPage>
    );
}

export default App;
