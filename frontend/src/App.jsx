import React from "react";

import Login from './components/Login'
import AbstractPage from './components/AbstractPage'
import Dashboard from "./components/Dashboard";
import DeviceTable from "./components/DeviceTable";
import CreateDevice from "./components/CreateDevice";
import DeviceModal from "./components/DeviceModal";
import DeviceDetail from "./components/DeviceDetail";
import History from "./components/History";

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
            <History />
        </AbstractPage>
    );
}

export default App;
