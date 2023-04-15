import React, {useEffect, useState} from "react";

const DeviceDetail = ({handleDetail, token, setErrorMessage, deviceid}) => {
    const [device, setDevice] = useState("");

    const getDeviceDetail = async () => {
        const requestOptions = {
            method: "GET",
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
        else {
            setDevice(data)
        }
    }

    useEffect(() => {
        getDeviceDetail();
    }, [])

    return (
        <div className="mt-6 mb-6">
            <button className="button is-grey is-light mb-3" onClick={handleDetail}>
                Zurück
            </button>
            <div className="box">
                <div className="tile is-ancestor">
                    <div className="tile is-vertical">
                        <div className="tile">
                            <div className="tile is-parent is-vertical">
                                <article className="tile is-child box">
                                    <h1 className="title">{device.title}</h1>
                                    <h2 className="subtitle"><b>Gerätetyp: </b>{device.device_type}</h2>
                                    <figure className="image is-5by4">
                                        <img src="https://bulma.io/images/placeholders/600x480.png"/>
                                    </figure>
                                </article>
                            </div>
                            <div className="tile is-parent">
                                <article className="tile is-child is-flex is-align-items-flex-start is-flex-wrap-wrap">
                                    <div className="content">
                                        <div className="field">
                                            <label className="label mb-1">
                                                Beschreibung:
                                            </label>
                                            <p>
                                                {device.description}
                                            </p>
                                        </div>
                                        <div className="field">
                                            <label className="label mb-1">
                                                Zubehör:
                                            </label>
                                            <p>
                                                {device.accessories}
                                            </p>
                                        </div>
                                        <div className="field">
                                            <label className="label mb-1">
                                                Seriennummer:
                                            </label>
                                            <p>
                                                {device.serial_number}
                                            </p>
                                        </div>
                                        <div className="field">
                                            <label className="label mb-1">
                                                Käufer:
                                            </label>
                                            <p>
                                                {device.rz_username_buyer}
                                            </p>
                                        </div>
                                        <br/>
                                        <div className="field">
                                            <label className="label mb-1">
                                                Besitzer:
                                            </label>
                                            <p>
                                                wol33712
                                            </p>
                                        </div>
                                        <div className="field">
                                            <label className="label mb-1">
                                                Standort:
                                            </label>
                                            <p>
                                                Audimax
                                            </p>
                                        </div>
                                    </div>
                                    <div className="is-flex is-align-self-flex-end ml-auto">
                                        <div className="">
                                        <button className="button is-primary is-light mr-2 mb-2">
                                            Bearbeiten
                                        </button>
                                        <button className="button is-danger is-light">
                                            Löschen
                                        </button>
                                    </div>
                                    </div>
                                </article>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default DeviceDetail
