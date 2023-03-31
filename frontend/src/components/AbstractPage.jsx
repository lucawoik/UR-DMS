import React from 'react'

import Footer from "./Footer";
import Header from "./Header";

const AbstractPage = (props) => {
    return (
        <>
            <Header />
            <div className={'container'}>
                <section className={'section'}>
                    {props.children}
                </section>
            </div>
            <Footer />
        </>
    )
}

export default AbstractPage
