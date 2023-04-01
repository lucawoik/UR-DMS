import React from "react";

const Footer = () => {
    return (
        <>
            <footer className="footer">
                <div className="content has-text-centered">
                    <p>
                        Abschlussprojekt ASE WS22/23 - <strong>Geräteverwaltung</strong> von Luca Woik.
                        <br/>
                        {/* TODO: Add Licensing */}
                        The source code is
                        licensed <a href="http://opensource.org/licenses/mit-license.php">MIT</a>.
                        <br/>
                        The website content
                        is licensed <a href="http://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY NC SA 4.0</a>.
                    </p>
                </div>
            </footer>
        </>
    )
}

export default Footer
