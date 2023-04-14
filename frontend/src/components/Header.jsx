import React, {useContext} from "react";
import {UserContext} from "../context/UserContext";

import logo from "../Logo.png"

const Header = () => {
    const [token, setToken] = useContext(UserContext);

    const handleLogout = () => {
        setToken(null);
    }
    return (
        <nav className="navbar is-primary is-spaced" role="navigation" aria-label="main navigation">
            <div className="navbar-brand">
                <div className="navbar-item">
                    <img src={logo}
                         alt="UR-DMS: Geräteverwaltung an der Uni Regensburg" width="112"
                         height="28" />
                </div>
            </div>
            <div className="navbar-menu is-block">
                <div className="navbar-end">
                    <div className="navbar-item">
                    {
                        token && (
                            <button className="button" onClick={handleLogout}>
                                Logout
                            </button>
                        )
                    }
                    </div>
                </div>
            </div>
        </nav>
    )
}

export default Header
