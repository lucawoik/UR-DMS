import React from "react";

const active = true;

const DeviceModal = () => {
    return (
        <div className={`modal ${active && "is-active"}`}>
            <div className="modal-background"></div>
            <div className="modal-card">
                <header className="modal-card-head has-background-primary-light">
                    <h1 className="modal-card-title">Gerät anlegen</h1>
                </header>
                <section className="modal-card-body">
                    <form>
                        <div className="field">
                            <label className="label">Besitzer</label>
                            <div className="control">
                                <input
                                    type="text"
                                    placeholder="RZ-Kürzel des Besitzers"
                                    className="input"
                                    required
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Standort</label>
                            <div className="select">
                                <select>
                                    <option>Audimax</option>
                                    <option>H6</option>
                                </select>
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Gerätetyp</label>
                            <div className="select">
                                <select>
                                    <option>Laptop</option>
                                    <option>Monitor</option>
                                </select>
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Name des Geräts</label>
                            <div className="control">
                                <input
                                    type="text"
                                    placeholder="Namen eingeben"
                                    className="input"
                                    required
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Zubehör</label>
                            <div className="control">
                                <input
                                    placeholder="Zubehör eingeben"
                                    className="input"
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Seriennummer</label>
                            <div className="control">
                                <input
                                    type="text"
                                    placeholder="Seriennummer eingeben"
                                    className="input"
                                    required
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Beschreibung</label>
                            <div className="control">
                                <textarea className="textarea" placeholder="Gerätebeischreibung hinzufügen"></textarea>
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">URL für Bild</label>
                            <div className="control">
                                <input
                                    type="text"
                                    placeholder="URL zum Bild des Geräts"
                                    className="input"
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">RZ-Kürzel des Käufers</label>
                            <div className="control">
                                <input
                                    type="text"
                                    placeholder="RZ-Kürzel eingeben"
                                    className="input"
                                />
                            </div>
                        </div>
                    </form>
                </section>
                <footer className="modal-card-foot has-background-primary-light">
                    <button className="button is-primary">
                        Hinzufügen
                    </button>
                    <button className="button">
                        Abbruch
                    </button>
                </footer>
            </div>
        </div>
    )
}

export default DeviceModal