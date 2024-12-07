import { useState } from "react";
import "./App.css";
import "font-awesome/css/font-awesome.min.css";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";

function App() {
    const [inputValue, setInputValue] = useState("");
    const [diseases, setDiseases] = useState<Array<Record<string, any>>>([]);

    const handleSubmit = (event: any) => {
        event.preventDefault();
        setDiseases([
            {
                name: "Aliquam maximus molestie arcu",
                overview:
                    "Morbi tincidunt vitae arcu rutrum tincidunt. Cras nec ligula odio. Nullam sagittis dolor nec magna luctus posuere. Praesent lectus elit, dignissim sit amet nisl non, fringilla sodales augue. Pellentesque iaculis massa in vestibulum hendrerit. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Nulla facilisi. Praesent rutrum ultrices nisl, at rutrum ex. Duis eleifend malesuada dui iaculis elementum. Morbi sem nibh, pulvinar quis luctus ut, auctor a leo. Vivamus a libero posuere, mollis turpis a, faucibus tortor. Quisque sed lectus id nisl pharetra molestie in id elit. Aliquam at lectus ut nulla lobortis bibendum. Ut purus tortor, interdum eget dui eleifend, tincidunt eleifend purus. Aliquam id est molestie, vehicula ipsum quis, euismod nulla. In dolor urna, consectetur ut sodales eget, malesuada nec est. ",
            },
            {
                name: "Mauris euismod pretium justo non",
                overview:
                    " In eleifend ut diam nec euismod. Morbi lorem orci, blandit nec lectus ac, blandit mollis nisl. Vestibulum lobortis nisl vel sem placerat pretium. Cras vel sapien placerat, sagittis odio eu, lacinia massa. Nulla bibendum urna est, quis pellentesque magna convallis ut. Pellentesque vehicula, turpis eget ultrices mattis, purus enim scelerisque ex, cursus egestas metus est vel nulla. Mauris at tincidunt justo, id malesuada turpis. Mauris ut placerat leo. ",
            },
            {
                name: "Fusce luctus accumsan velit efficitur",
            },
        ]);
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
