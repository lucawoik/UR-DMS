import React from "react";

const Dashboard = () => {
    return (
        <div className="mt-6 mb-6">
            <div className="tile is-ancestor">
                <div className="tile is-vertical">
                    <div className="tile">
                        <div className="tile is-parent is-vertical">
                            <article className="tile is-child box has-background-success-light">
                                <h1 className="title">Import</h1>
                                <h2 className="subtitle">JSON-Datei importieren</h2>
                                <div className="column has-text-right">
                                    <button className="button is-success">
                                        Datei wählen
                                    </button>
                                </div>
                            </article>
                        </div>
                        <div className="tile is-parent">
                            <article className="tile is-child box has-background-link-light">
                                <h1 className="title">Export</h1>
                                <h2 className="subtitle">Datenbank als JSON-Datei exportieren</h2>
                                <div className="column has-text-right">
                                    <button className="button is-link">
                                        Download
                                    </button>
                                </div>
                            </article>
                        </div>
                    </div>
                </div>
            </div>
            <div className="tile is-ancestor">
                <div className="tile is-vertical">
                    <div className="tile">
                        <div className="tile is-parent is-vertical">
                            <article className="tile is-child box has-background-danger-light">
                                <h1 className="title">Bereinigen</h1>
                                <h2 className="subtitle">Datenbank entleeren! Daten sollten vorher per Export gesichert werden.</h2>
                                <div className="column has-text-right">
                                    <button className="button is-danger">
                                        Löschen
                                    </button>
                                </div>
                            </article>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Dashboard
