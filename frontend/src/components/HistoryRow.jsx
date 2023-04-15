import React from "react";
import moment from "moment";

const HistoryRow = ({column1, column2}) => {
    return (
        <div className="notification is-flex is-flex-wrap-nowrap is-align-items-center mb-1">
            <p className="mr-auto"><b>{column1}</b></p>
            <p><b>{moment(column2).format("DD MM YYYY")}</b></p>
        </div>
    )
}

export default HistoryRow