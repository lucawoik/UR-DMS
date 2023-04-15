import React, {useContext, useState} from 'react'

import ErrorMessage from "./ErrorMessage";
import {UserContext} from "../context/UserContext";

/*
Component which shows a login form and handles the necessary login procedure.
Heavily influenced by: https://www.youtube.com/watch?v=CsnBbaOfmY8&list=PLhH3UpV2flrwfJ2aSwn8MkCKz9VzO-1P4&index=6
 */

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [, setToken] = useContext(UserContext);

    const submitLogin = async () => {
        const requestOptions = {
            method: "POST",
            headers: {
                "content-type": "application/x-www-form-urlencoded",
            },
            body: JSON.stringify(`grant_type=&username=${username}&password=${password}&scope=&client_id=&client_secret=`)
        };
        const response = await fetch("http://localhost:8000/api/login", requestOptions);
        const data = await response.json();

        if (!response.ok) {
            setErrorMessage(data.detail);
        }
        else {
            console.log(data.access_token);
            setToken(data.access_token);
        }
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        submitLogin();
    }

    return (
        <div className="mt-6 mb-6">
            <div className="column is-two-thirds m-auto">
                <form className="box" onSubmit={handleSubmit}>
                    <h1 className="title has-text-centered">Login</h1>
                    <div className="column is-half m-auto">
                        <div className="field">
                            <label className="label">RZ-Nutzername</label>
                            <div className="control">
                                <input
                                    type="text"
                                    placeholder="Nutzername eingeben"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    className="input"
                                    required
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Passwort</label>
                            <div className="control">
                                <input
                                    type="password"
                                    placeholder="Passwort eingeben"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="input"
                                    required
                                />
                            </div>
                        </div>
                    </div>
                    <ErrorMessage message={errorMessage}></ErrorMessage>
                    <br/>
                    <div className="column has-text-right">
                        <button className="button is-primary" type="submit">
                            Login
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default Login;