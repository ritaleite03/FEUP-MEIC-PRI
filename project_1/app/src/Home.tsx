import { useState } from "react";
import { Link } from "react-router-dom";
import Card from "react-bootstrap/Card";
import "./App.css";
import "font-awesome/css/font-awesome.min.css";
import Header from "./components/Header";

function Home() {
    const [inputValue, setInputValue] = useState("");
    const [diseases, setDiseases] = useState<Array<Record<string, any>>>([]);

    const handleSubmit = async (event: any) => {
        event.preventDefault();
        const response = await fetch("http://localhost:5223/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ query: inputValue }),
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch diseases: ${response.statusText}`);
        } else {
            const data = await response.json();
            setDiseases(data);
        }
    };

    return (
        <div>
            <Header></Header>
            <main>
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        placeholder="Write here ..."
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                    />
                    <button type="submit">
                        <i className="fa fa-search"></i>
                    </button>
                </form>
                <div>
                    {diseases.length > 0 ? (
                        diseases.map((disease, index) => (
                            <Card
                                key={index}
                                style={{ width: "80%", margin: "1em auto" }}
                            >
                                <Link
                                    to={`/disease/${disease["id"]}`}
                                    state={{ disease }}
                                >
                                    <Card.Body>
                                        <Card.Title>
                                            {disease["Name"]}
                                        </Card.Title>
                                        <Card.Text>
                                            {disease["Overview"] !== undefined
                                                ? disease["Overview"].length >
                                                  100
                                                    ? disease[
                                                          "Overview"
                                                      ].substring(0, 500) +
                                                      "..."
                                                    : disease["Overview"]
                                                : "There is no overview"}
                                        </Card.Text>
                                    </Card.Body>
                                </Link>
                            </Card>
                        ))
                    ) : (
                        <p>No diseases found</p>
                    )}
                </div>
            </main>
        </div>
    );
}

export default Home;
