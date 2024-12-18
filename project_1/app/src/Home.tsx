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

    // Function to handle the initial search
    const handleSearch = async (event: React.FormEvent) => {
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
            setLastInputValue(inputValue);
            setSelectedDiseases([]);
        }
    };

    // Function to handle relevance feedback
    const handleRelevanceFeedback = async () => {
        const relevantVectors: any[] = [];
        const nonRelevantVectors: any[] = [];

        diseases.forEach((disease) => {
            if (selectedDiseases.includes(disease.id)) {
                relevantVectors.push(disease.vector);
            } else {
                nonRelevantVectors.push(disease.vector);
            }
        });

        const response = await fetch("http://localhost:5223/relevance_feedback", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                query: lastInputValue,
                relevant_vectors: relevantVectors,
                non_relevant_vectors: nonRelevantVectors,
            }),
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch diseases: ${response.statusText}`);
        } else {
            const data = await response.json();
            setDiseases(data);
        }
    };

    // Function to handle checkbox selection
    const handleCheckboxChange = (id: string) => {
        setSelectedDiseases((prevSelected) =>
            prevSelected.includes(id)
                ? prevSelected.filter((item) => item !== id)
                : [...prevSelected, id]
        );
    };

    return (
        <div>
            <Header />
            <main>
                {/* Search Form */}
                <form onSubmit={handleSearch}>
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

                {/* Relevance Feedback Button */}
                {selectedDiseases.length > 0 && (
                    <button
                        onClick={handleRelevanceFeedback}
                    >
                        Relevance Feedback
                    </button>
                )}

                {/* Diseases List */}
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
                                    to={`/disease/${disease.id}`}
                                    state={{ disease }}
                                    style={{ textDecoration: "none", flex: 1 }}
                                >
                                    <Card.Body>
                                        <Card.Title>{disease.Name}</Card.Title>
                                        <Card.Text>
                                            {disease.Overview
                                                ? disease.Overview.length > 500
                                                    ? `${disease.Overview.substring(0, 500)}...`
                                                    : disease.Overview
                                                : "There is no overview"}
                                        </Card.Text>
                                    </Card.Body>
                                </Link>
                                <input
                                    type="checkbox"
                                    checked={selectedDiseases.includes(
                                        disease.id
                                    )}
                                    onChange={() =>
                                        handleCheckboxChange(disease.id)
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
