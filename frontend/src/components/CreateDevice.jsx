import React, {useContext, useState} from "react";
import DeviceModal from "./DeviceModal";
import {UserContext} from "../context/UserContext";

const CreateDevice = () => {
    const [token] = useContext(UserContext);
    const [activeModal, setActiveModal] = useState(false);

    const handleModal = () => {
        setActiveModal(!activeModal);

    }

    return (
        <>
            <DeviceModal active={activeModal} handleModal={handleModal} token={token}></DeviceModal>
            <div className="mt-6 mb-6">
                <div className="tile is-ancestor">
                    <div className="tile is-vertical">
                        <div className="tile">
                            <div className="tile is-parent is-vertical">
                                <article className="tile is-child box">
                                    <h1 className="title">Gerät anlegen</h1>
                                    <h2 className="subtitle">Anlegen eines neuen Geräts in der DMS-Datenbank.</h2>
                                    <div className="column has-text-right">
                                        <button className="button is-primary is-fullwidth" onClick={handleModal}>
                                            Neu anlegen
                                        </button>
                                    </div>
                                </article>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default CreateDevice
