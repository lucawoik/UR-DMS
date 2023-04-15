import React from "react";

/*
Error message that is shown when an error occurs
Source: https://github.com/sixfwa/react-fastapi/blob/main/frontend/src/components/ErrorMessage.jsx
 */

const ErrorMessage = ({message}) => {
    return (
        <p className="has-text-weight-bold has-text-danger">{message}</p>
    )
}

export default ErrorMessage