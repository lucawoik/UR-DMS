import React from "react";
import HistoryRow from "./HistoryRow";

const History = () => {
    return (
        <div className="mt-6 mb-6 box">
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
                                <HistoryRow column1={"wol33712"} column2={"2023-01-29"} />
                                <HistoryRow column1={"wol33712"} column2={"2023-01-29"} />
                                <HistoryRow column1={"wol33712"} column2={"2023-01-29"} />
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
                                <HistoryRow column1={"Audimax"} column2={"2023-02-27"} />
                            </article>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default History;