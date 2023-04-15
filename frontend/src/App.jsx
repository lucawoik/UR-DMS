import React, {useContext, useEffect, useState} from "react";

import Login from './components/Login'
import AbstractPage from './components/AbstractPage'
import Dashboard from "./components/Dashboard";
import DeviceTable from "./components/DeviceTable";
import CreateDevice from "./components/CreateDevice";
import DeviceModal from "./components/DeviceModal";
import DeviceDetail from "./components/DeviceDetail";
import History from "./components/History";
import {UserContext} from "./context/UserContext";

const App = () => {

    const [message, setMessage] = useState("");
    const [token] = useContext(UserContext);

    const getWelcomeMessage = async () => {
        const requestOptions = {
            method: "GET",
            headers: {
                "content-type": "application/json",
            },
        };
        const response = await fetch("http://localhost:8000/api", requestOptions);
        const data = await response.json();

        if (!response.ok) {
            console.log("No connection to backend could be established.");
        }
        else {
            setMessage(data.message);
        }
    };

    useEffect(() => {
        getWelcomeMessage()
    }, [])

    return (
        <AbstractPage>
            {!token ?
                <>
                    <Login/>
                    <DeviceTable/>
                </>
                :
                <>
                    <Dashboard/>
                    <CreateDevice/>
                    <DeviceTable/>
                </>
            }
        </AbstractPage>
    );
}

export default App;
