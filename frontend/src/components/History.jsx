import React, {useEffect, useState} from "react";
import HistoryRow from "./HistoryRow";
import ErrorMessage from "./ErrorMessage";

const History = ({token, deviceid, setErrorMessage}) => {

    const [ownerTransactions, setOwnerTransactions] = useState(null);
    const [ownerLoaded, setOwnerLoaded] = useState(false);

    const getOwnerTransactions = async () => {
        console.log(deviceid)
        const requestOptions = {
            method: "GET",
            headers: {
                "content-type": "application/json",
                Authorization: "Bearer " + token
            },
        }
        const response = await fetch(`http://localhost:8000/api/devices/${deviceid}/owner-transactions`, requestOptions)
        const data = await response.json();

        if (!response.ok) {
            setErrorMessage(data.detail)
        }
        else {
            setOwnerTransactions(data)
            setOwnerLoaded(true)
        }
    }

    useEffect(() => {
        getOwnerTransactions();
    }, [])
    
    const [locationTransactions, setLocationTransactions] = useState(null);
    const [locationLoaded, setLocationLoaded] = useState(false);

    const getLocationTransactions = async () => {
        console.log(deviceid)
        const requestOptions = {
            method: "GET",
            headers: {
                "content-type": "application/json",
                Authorization: "Bearer " + token
            },
        }
        const response = await fetch(`http://localhost:8000/api/devices/${deviceid}/location-transactions`, requestOptions)
        const data = await response.json();

        if (!response.ok) {
            setErrorMessage(data.detail)
        }
        else {
            setLocationTransactions(data)
            setLocationLoaded(true)
        }
    }

    useEffect(() => {
        getLocationTransactions();
    }, [])

    return (
        <div className="tile is-ancestor">
            <div className="tile is-vertical">
                <div className="tile">
                    <div className="tile is-parent is-vertical">
                        <article className="tile is-child box">
                            <h1 className="title">Besitzer</h1>
                            <h2 className="subtitle">Verlauf der bisherigen Besitzer des Geräts.</h2>
                            <div className="notification is-primary is-light is-flex is-flex-wrap-nowrap mb-1">
                                <p className="mr-auto"><b>RZ-Kürzel</b></p>
                                <p><b>Datum</b></p>
                            </div>
                            {ownerTransactions && ownerLoaded ? ownerTransactions.map((ownerTransaction) => (
                                <HistoryRow
                                    column1={ownerTransaction.rz_username}
                                    column2={ownerTransaction.timestamp_owner_since}>
                                </HistoryRow>
                                    ))
                            :
                                (<ErrorMessage message={"No owner transactions..."}></ErrorMessage>)
                            }
                        </article>
                    </div>
                    <div className="tile is-parent">
                        <article className="tile is-child box">
                            <h1 className="title">Standorte</h1>
                            <h2 className="subtitle">Verlauf der bisherigen Standorte des Geräts</h2>
                            <div className="notification is-primary is-light is-flex is-flex-wrap-nowrap mb-1">
                                <p className="mr-auto"><b>Raumnummer</b></p>
                                <p><b>Datum</b></p>
                            </div>
                            {locationTransactions && locationLoaded ? locationTransactions.map((locationTransaction) => (
                                <HistoryRow
                                    column1={locationTransaction.room_code}
                                    column2={locationTransaction.timestamp_located_since}>
                                </HistoryRow>
                                    ))
                            :
                                (<ErrorMessage message={"No location transactions..."}></ErrorMessage>)
                            }
                        </article>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default History;