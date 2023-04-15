import React, {createContext, useEffect, useState} from "react";

/*
Context to check if User is still logged in.
Source: https://www.youtube.com/watch?v=O61aRPSuemE&list=PLhH3UpV2flrwfJ2aSwn8MkCKz9VzO-1P4&index=6
 */

export const UserContext = createContext(undefined);

export const UserProvider = (props) => {
    const [token, setToken] = useState(localStorage.getItem('token'));

    useEffect(() => {
        const fetchUser = async () => {
            const requestOptions = {
            method: "GET",
            headers: {
                "content-type": "application/json",
                Authorization: "Bearer " + token
            },
        };
        const response = await fetch("http://localhost:8000/api/users/me", requestOptions);

        if (!response.ok) {
            setToken(null);

        }
        localStorage.setItem("token", token)
        }
        fetchUser();
    }, [token]);
    return (
        <UserContext.Provider value={[token, setToken]}>
            {props.children}
        </UserContext.Provider>
    )
}


