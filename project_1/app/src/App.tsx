import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import "font-awesome/css/font-awesome.min.css";
import Home from "./Home";
import DiseaseDetail from "./DiseaseDetail";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/disease/:diseaseId" element={<DiseaseDetail />} />
            </Routes>
        </Router>
    );
}

export default App;
