import React from "react";

const DeviceTable = () => {
    return (
        <div className="mt-6 mb-6 box">
            <h1 className="title">Liste aller Geräte</h1>
            <h2 className="subtitle">Auflistung aller registrierten Geräte der Uni Regensburg.</h2>
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
                        <tr>
                            <td>MacBook Pro 13</td>
                            <td>Laptop</td>
                            <td>
                                <button className="button is-primary is-light mr-2 mb-2">
                                    Details
                                </button>
                                <button className="button is-danger is-light">
                                    Löschen
                                </button>
                            </td>
                        </tr>
                        <tr>
                            <td>Dell U2520D</td>
                            <td>Monitor</td>
                            <td>
                                <button className="button is-primary is-light mr-2 mb-2">
                                    Details
                                </button>
                                <button className="button is-danger is-light">
                                    Löschen
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    )
}

export default DeviceTable
