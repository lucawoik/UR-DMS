import React from "react";

const DeviceDetail = () => {
    return (
        <div className="mt-6 mb-6">
            <button className="button is-grey is-light mb-3">
                Zurück
            </button>
            <div className="box">
                <div className="tile is-ancestor">
                    <div className="tile is-vertical">
                        <div className="tile">
                            <div className="tile is-parent is-vertical">
                                <article className="tile is-child box">
                                    <h1 className="title">MacBook Pro 13</h1>
                                    <h2 className="subtitle"><b>Gerätetyp: </b>Laptop</h2>
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
                                                Lorem ipsum dolor sit amet, consetetur sadipscing elitr,
                                                sed diam nonumy eirmod tempor invidunt ut labore et dolore
                                                magna aliquyam erat, sed diam voluptua. At vero eos et accusam
                                                et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea
                                                takimata sanctus est Lorem ipsum dolor sit amet.
                                            </p>
                                        </div>
                                        <div className="field">
                                            <label className="label mb-1">
                                                Zubehör:
                                            </label>
                                            <p>
                                                Lorem, ipsum, dolor
                                            </p>
                                        </div>
                                        <div className="field">
                                            <label className="label mb-1">
                                                Seriennummer:
                                            </label>
                                            <p>
                                                e51c1ff1580d2b730daae20
                                            </p>
                                        </div>
                                        <div className="field">
                                            <label className="label mb-1">
                                                Käufer:
                                            </label>
                                            <p>
                                                wol33712
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
