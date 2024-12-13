import { useState } from "react";
import "./App.css";
import "font-awesome/css/font-awesome.min.css";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";

function App() {
    const [inputValue, setInputValue] = useState("");
    const [diseases, setDiseases] = useState<Array<Record<string, any>>>([]);

    const handleSubmit = async (event: any) => {
        event.preventDefault();
        const response = await fetch("http://localhost:5001/projects");
        if (!response.ok) {
            throw new Error(`Failed to fetch projects: ${response.statusText}`);
        } else {
            const data = await response.json();
            setDiseases(data);
        }
    };

    return (
        <>
            <header>
                <h1>DISEASES' WIKI</h1>
            </header>
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
                                <a href="">
                                    <Card.Body>
                                        <Card.Title>
                                            {disease["name"]}
                                        </Card.Title>
                                        <Card.Text>
                                            {disease["overview"] !== undefined
                                                ? disease["overview"].length >
                                                  100
                                                    ? disease[
                                                          "overview"
                                                      ].substring(0, 500) +
                                                      "..."
                                                    : disease["overview"]
                                                : "There is no overview"}
                                        </Card.Text>
                                    </Card.Body>
                                </a>
                            </Card>
                        ))
                    ) : (
                        <p>No diseases found</p>
                    )}
                </div>
            </main>
            <footer></footer>
        </>
    );
}

export default App;
