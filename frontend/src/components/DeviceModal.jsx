import React, {useState} from "react";

const DeviceModal = ({active, handleModal, token, id, setErrorMessage}) => {

    const [owner, setOwner] = useState("");
    const [location, setLocation] = useState("");
    const [type, setType] = useState("");
    const [title, setTitle] = useState("");
    const [accessories, setAccessories] = useState("");
    const [serialnumber, setSerialnumber] = useState("");
    const [description, setDescription] = useState("");
    const [imageurl, setImageure] = useState("");
    const [buyer, setBuyer] = useState("");

    const resetFormData = () => {
        setOwner("");
        setLocation("");
        setType("");
        setTitle("");
        setAccessories("");
        setSerialnumber("");
        setDescription("");
        setImageure("");
        setBuyer("");
    }

    const handleCreation = async (e) => {
        e.preventDefault();
        const createDevice = async () => {
            const requestOptions = {
            method: "POST",
            headers: {
                "content-type": "application/json",
                Authorization: "Bearer " + token
            },
            body: JSON.stringify({
                title: title,
                device_type: type,
                description: description,
                accessories: accessories,
                rz_username_buyer: buyer,
                serial_number: serialnumber,
                image_url: imageurl
            })
        }
        const response = await fetch("/api/devices", requestOptions)
        const data = await response.json();

        if (!response.ok) {
            setErrorMessage(data.detail);
        }
        else {
            resetFormData();
            handleModal();
        }
        }
        // TODO: Create transactions and information
        await createDevice();
    }

    return (
        <div className={`modal ${active && "is-active"}`}>
            <div className="modal-background" onClick={handleModal}></div>
            <div className="modal-card">
                <header className="modal-card-head has-background-primary-light">
                    <h1 className="modal-card-title">Gerät anlegen</h1>
                </header>
                <section className="modal-card-body">
                    <form>
                        <div className="field">
                            <label className="label">Besitzer</label>
                            <div className="control">
                                <input
                                    type="text"
                                    placeholder="RZ-Kürzel des Besitzers"
                                    value={owner}
                                    onChange={(e) => setOwner(e.target.value)}
                                    className="input"
                                    required
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Standort</label>
                            <div className="select">
                                <select
                                    value={location}
                                    onChange={(e) => setLocation(e.target.value)}
                                >
                                    <option>Audimax</option>
                                    <option>H6</option>
                                </select>
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Gerätetyp</label>
                            <div className="select">
                                <select
                                    value={type}
                                    onChange={(e) => setType(e.target.value)}
                                >
                                    <option>Laptop</option>
                                    <option>Monitor</option>
                                </select>
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Name des Geräts</label>
                            <div className="control">
                                <input
                                    type="text"
                                    placeholder="Namen eingeben"
                                    value={title}
                                    onChange={(e) => setTitle(e.target.value)}
                                    className="input"
                                    required
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Zubehör</label>
                            <div className="control">
                                <input
                                    placeholder="Zubehör eingeben"
                                    value={accessories}
                                    onChange={(e) => setAccessories(e.target.value)}
                                    className="input"
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Seriennummer</label>
                            <div className="control">
                                <input
                                    type="text"
                                    placeholder="Seriennummer eingeben"
                                    value={serialnumber}
                                    onChange={(e) => setSerialnumber(e.target.value)}
                                    className="input"
                                    required
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Beschreibung</label>
                            <div className="control">
                                <textarea
                                    className="textarea"
                                    placeholder="Gerätebeischreibung hinzufügen"
                                    value={description}
                                    onChange={(e) => setDescription(e.target.value)}
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">URL für Bild</label>
                            <div className="control">
                                <input
                                    type="text"
                                    placeholder="URL zum Bild des Geräts"
                                    value={imageurl}
                                    onChange={(e) => setImageure(e.target.value)}
                                    className="input"
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">RZ-Kürzel des Käufers</label>
                            <div className="control">
                                <input
                                    type="text"
                                    placeholder="RZ-Kürzel eingeben"
                                    value={buyer}
                                    onChange={(e) => setBuyer(e.target.value)}
                                    className="input"
                                />
                            </div>
                        </div>
                    </form>
                </section>
                <footer className="modal-card-foot has-background-primary-light">
                    <button className="button is-primary" onClick={handleCreation}>
                        Hinzufügen
                    </button>
                    <button className="button" onClick={handleModal}>
                        Abbruch
                    </button>
                </footer>
            </div>
        </div>
    )
}

export default DeviceModal