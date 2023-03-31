import React from "react";

import Login from './components/Login'
import AbstractPage from './components/AbstractPage'
import Dashboard from "./components/Dashboard";
import DeviceTable from "./components/DeviceTable";
import CreateDevice from "./components/CreateDevice";
import DeviceModal from "./components/DeviceModal";
import DeviceDetail from "./components/DeviceDetail";

const authorized = false;

const App = () => {
    return (
        <AbstractPage>
            {authorized ? <></> : <Login/>}
            <Dashboard/>
            <CreateDevice/>
            <DeviceTable/>
            {/*<DeviceModal/>*/}
            <DeviceDetail />
        </AbstractPage>
    );
}

export default App;
