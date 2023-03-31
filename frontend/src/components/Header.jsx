import React from "react";

import logo from "../Logo.png"

const Header = () => {
    return (
        <nav className="navbar is-fixed-top" role="navigation" aria-label="main navigation">
            <div className="navbar-brand">
                <a className="navbar-item" href="#">
                    <img src={logo}
                         alt="UR-DMS: Geräteverwaltung an der Uni Regensburg" width="112"
                         height="28" />
                </a>

                <a role="button" className="navbar-burger" aria-label="menu" aria-expanded="false">
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                </a>
            </div>
        </nav>
    )
}

export default Header
