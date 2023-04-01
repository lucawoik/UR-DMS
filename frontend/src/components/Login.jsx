import React from 'react'

const Login = () => {
    return (
        <div className="mt-6 mb-6">
            <div className="column is-two-thirds m-auto">
            {/* TODO: Taken from https://github.com/sixfwa/react-fastapi/blob/main/frontend/src/components/Login.jsx */}
            <form className="box">
                <h1 className="title has-text-centered">Login</h1>
                <div className="column is-half m-auto">
                    <div className="field">
                    <label className="label">Email Address</label>
                    <div className="control">
                        <input
                            type="email"
                            placeholder="Enter email"
                            className="input"
                            required
                        />
                    </div>
                </div>
                <div className="field">
                    <label className="label">Password</label>
                    <div className="control">
                        <input
                            type="password"
                            placeholder="Enter password"
                            className="input"
                            required
                        />
                    </div>
                </div>
                </div>
                <br />
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