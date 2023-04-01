import React from "react";

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
                            </article>
                        </div>
                        <div className="tile is-parent">
                            <article className="tile is-child box">
                                <h1 className="title">Standorte</h1>
                                <h2 className="subtitle">Verlauf der bisherigen Standorte des Geräts</h2>
                            </article>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default History;