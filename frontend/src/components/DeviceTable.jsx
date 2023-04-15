import React, {useContext, useEffect, useState} from "react";

import ErrorMessage from "./ErrorMessage";
import {UserContext} from "../context/UserContext";
import DeviceDetail from "./DeviceDetail";

/*
Component which provides the table of all devices in the database.
Source for most of the logic: https://www.youtube.com/watch?v=Mxh67Vbibqk&list=PLhH3UpV2flrwfJ2aSwn8MkCKz9VzO-1P4&index=7
 */

const DeviceTable = () => {
    const [token] = useContext(UserContext);
    const [devices, setDevices] = useState(null);
    const [errorMessage, setErrorMessage] = useState("");
    const [loaded, setLoaded] = useState(false)
    const [id, setId] = useState(null);

    const [details, setDetails] = useState("");

    const getDevices = async () => {
        const requestOptions = {
            method: "GET",
            headers: {
                "content-type": "application/json",
                Authorization: "Bearer " + token
            },
        }
        const response = await fetch("http://localhost:8000/api/devices", requestOptions)
        const data = await response.json();

        if (!response.ok) {
            setErrorMessage(data.detail)
        }
        else {
            setDevices(data);
            setLoaded(true);
        }
    }

    useEffect(() => {
        getDevices();
    }, [])

    const handleDelete = async (deviceid) => {
        const requestOptions = {
            method: "DELETE",
            headers: {
                "content-type": "application/json",
                Authorization: "Bearer " + token
            },
        }
        const response = await fetch(`http://localhost:8000/api/devices/${deviceid}`, requestOptions)
        const data = await response.json();

        if (!response.ok) {
            setErrorMessage(data.detail)
        }
        getDevices();
    }

    const handleDetail = async (deviceid) => {
        setDetails(deviceid)
    }

    const handleDetailClose = () => {
        setDetails("");
    }

    return (
        <>
            {details ? <>
                <DeviceDetail handleDetail={handleDetailClose} token={token} setErrorMessage={setErrorMessage} deviceid={details}></DeviceDetail>
            </> : <>
                <div className="mt-6 mb-6 box">
                    <h1 className="title">Liste aller Geräte</h1>
                    <h2 className="subtitle">Auflistung aller registrierten Geräte der Uni Regensburg.</h2>
                    <ErrorMessage message={errorMessage}></ErrorMessage>
                    {loaded && devices ? (
                        <>
                            <div className="table-container">
                                <table className="table is-hoverable is-fullwidth">
                                    <thead>
                                    <tr>
                                        <th>Gerät</th>
                                        <th>Typ</th>
                                        <th>Aktionen</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {devices.map((device) => (
                                        <tr key={device.device_id}>
                                            <td>{device.title}</td>
                                            <td>{device.device_type}</td>
                                            <td>
                                                <button className="button is-primary is-light mr-2 mb-2"
                                                        onClick={() => handleDetail(device.device_id)}>
                                                    Details
                                                </button>
                                                <button className="button is-danger is-light"
                                                        onClick={() => handleDelete(device.device_id)}>
                                                    Löschen
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                    </tbody>
                                </table>
                            </div>
                        </>
                    ) : (<progress className="progress is-primary" max="100">15%</progress>)
                    }
                </div>
            </>}
        </>
    )
}

export default DeviceTable;
