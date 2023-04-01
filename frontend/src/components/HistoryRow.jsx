import React from "react";

const HistoryRow = ({column1, column2}) => {
    return (
        <div className="notification is-flex is-flex-wrap-nowrap is-align-items-center mb-1">
            <p className="mr-auto"><b>{column1}</b></p>
            <p><b>{column2}</b></p>
        </div>
    )
}

export default HistoryRow