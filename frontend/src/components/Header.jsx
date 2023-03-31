import React from "react";

import logo from "../Logo.png"

const Header = () => {
    return (
        <nav className="navbar is-fixed-top" role="navigation" aria-label="main navigation">
            <div className="navbar-brand">
                <div className="navbar-item">
                    <img src={logo}
                         alt="UR-DMS: Geräteverwaltung an der Uni Regensburg" width="112"
                         height="28" />
                </div>
            </div>
        </nav>
    )
}

export default Header
