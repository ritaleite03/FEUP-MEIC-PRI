import { useState } from "react";
import { Link } from "react-router-dom";
import Card from "react-bootstrap/Card";
import "./App.css";
import "font-awesome/css/font-awesome.min.css";
import Header from "./components/Header";
import { useAppContext } from "./context";

function Home() {
    const {
        diseases,
        setDiseases,
        selectedDiseases,
        setSelectedDiseases,
        lastInputValue,
        setLastInputValue,
        inputValue,
        setInputValue,
    } = useAppContext();
    const handleSubmit = async (event: any) => {
        event.preventDefault();
        let response;

        if (lastInputValue !== "" && lastInputValue === inputValue) {
            const relevant_vectors = [];
            const non_relevant_vectors = [];

            diseases.forEach((disease) => {
                if (selectedDiseases.some(d => d === disease["id"])) {
                    relevant_vectors.push(disease["vector"]);
                }
                else {
                    non_relevant_vectors.push(disease["vector"]);
                }
            })

            response = await fetch("http://localhost:5223/relevance_feedback", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    query: inputValue,
                    relevant_vectors: relevant_vectors,
                    non_relevant_vectors: non_relevant_vectors
                })
            });
        }
        else {
            response = await fetch("http://localhost:5223/search", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ query: inputValue }),
            });
        }

        if (!response.ok) {
            throw new Error(`Failed to fetch diseases: ${response.statusText}`);
        } else {
            const data = await response.json();
            setDiseases(data);
            setLastInputValue(inputValue);
        }
    };

    const handleCheckboxChange = (id: string) => {
        setSelectedDiseases((prevSelected) => {
            if (prevSelected.includes(id)) {
                return prevSelected.filter((item) => item !== id);
            } else {
                return [...prevSelected, id];
            }
        });
    };

    return (
        <div>
            <Header />
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
                                style={{
                                    width: "80%",
                                    margin: "1em auto",
                                    display: "flex",
                                    alignItems: "center",
                                    justifyContent: "space-between",
                                }}
                            >
                                <Link
                                    to={`/disease/${disease["id"]}`}
                                    state={{ disease }}
                                    style={{ textDecoration: "none", flex: 1 }}
                                >
                                    <Card.Body>
                                        <Card.Title>
                                            {disease["Name"]}
                                        </Card.Title>
                                        <Card.Text>
                                            {disease["Overview"] !== undefined
                                                ? disease["Overview"].length >
                                                  500
                                                    ? disease[
                                                          "Overview"
                                                      ].substring(0, 500) +
                                                      "..."
                                                    : disease["Overview"]
                                                : "There is no overview"}
                                        </Card.Text>
                                    </Card.Body>
                                </Link>
                                <input
                                    type="checkbox"
                                    checked={selectedDiseases.includes(
                                        disease["id"]
                                    )}
                                    onChange={() =>
                                        handleCheckboxChange(disease["id"])
                                    }
                                    style={{ margin: "10px" }}
                                />
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
