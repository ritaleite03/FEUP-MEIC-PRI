import { useLocation, useNavigate } from "react-router-dom";
import Header from "./components/Header";
import Card from "react-bootstrap/Card";
import {
    FaRegQuestionCircle,
    FaRegListAlt,
    FaStethoscope,
} from "react-icons/fa";

const RenderField = ({
    label,
    value,
    icon,
}: {
    label: string;
    value: any;
    icon?: JSX.Element;
}) => {
    if (!value) {
        return null;
    }

    return (
        <div className="my-4">
            <h4 className="d-flex align-items-center text-primary">
                {icon && <span className="me-2">{icon}</span>} {label}
            </h4>
            <div className="border rounded p-4 bg-light shadow-sm">
                {typeof value === "string" || typeof value === "number" ? (
                    <p>{value}</p>
                ) : Array.isArray(value) ? (
                    <ul className="list-group list-group-flush">
                        {value.map((item, index) => (
                            <li key={index} className="list-group-item">
                                {item}
                            </li>
                        ))}
                    </ul>
                ) : typeof value === "object" ? (
                    Object.entries(value).map(([key, val], index) => (
                        <div key={index}>
                            <h5>{key}</h5>
                            <p>{val as string}</p>
                        </div>
                    ))
                ) : (
                    <p>No information available</p>
                )}
            </div>
        </div>
    );
};

function DiseaseDetail() {
    const location = useLocation();
    const navigate = useNavigate();
    const disease = location.state?.disease;

    if (!disease) {
        navigate("/");
        return null;
    }

    const fields = [
        {
            label: "Overview",
            value: disease["Overview"],
            icon: <FaRegQuestionCircle size={24} />,
        },
        {
            label: "Total Revisions",
            value: disease["Total Revisions"],
            icon: <FaRegQuestionCircle size={24} />,
        },
        {
            label: "Last Revision Date",
            value: disease["Last Revision Date"],
            icon: <FaRegQuestionCircle size={24} />,
        },
        {
            label: "Alias",
            value: disease["Alias"],
            icon: <FaRegListAlt size={24} />,
        },
        {
            label: "Causes",
            value: disease["Causes"],
            icon: <FaStethoscope size={24} />,
        },
        {
            label: "Can Cause",
            value: disease["Can Cause"],
            icon: <FaRegListAlt size={24} />,
        },
        {
            label: "Caused By",
            value: disease["Caused By"],
            icon: <FaRegListAlt size={24} />,
        },
        {
            label: "Complications",
            value: disease["Complications"],
            icon: <FaStethoscope size={24} />,
        },
        {
            label: "Diagnosis",
            value: disease["Diagnosis"],
            icon: <FaStethoscope size={24} />,
        },
        {
            label: "Prevention",
            value: disease["Prevention"],
            icon: <FaStethoscope size={24} />,
        },
        {
            label: "Symptoms",
            value: disease["Symptoms"],
            icon: <FaStethoscope size={24} />,
        },
        {
            label: "List of Symptoms",
            value: disease["Symptoms List"],
            icon: <FaRegListAlt size={24} />,
        },
        {
            label: "Risk Factors",
            value: disease["Risk factors"],
            icon: <FaStethoscope size={24} />,
        },
        {
            label: "List of Risk Factors",
            value: disease["Risk Factors List"],
            icon: <FaRegListAlt size={24} />,
        },
        {
            label: "Treatment",
            value: disease["Treatment"],
            icon: <FaStethoscope size={24} />,
        },
        {
            label: "Treatments List",
            value: disease["Treatments List"],
            icon: <FaRegListAlt size={24} />,
        },
        {
            label: "Specialty",
            value: disease["Specialty"],
            icon: <FaRegListAlt size={24} />,
        },
        {
            label: "Age Onsets",
            value: disease["Age Onsets"],
            icon: <FaRegListAlt size={24} />,
        },
        {
            label: "Anatomical Location",
            value: disease["Anatomical Location"],
            icon: <FaRegListAlt size={24} />,
        },
        {
            label: "Characteristics",
            value: disease["Characteristics"],
            icon: <FaRegListAlt size={24} />,
        },
        {
            label: "Different From",
            value: disease["Different From"],
            icon: <FaRegListAlt size={24} />,
        },
        {
            label: "Opposit Of",
            value: disease["Opposit Of"],
            icon: <FaRegListAlt size={24} />,
        },
        {
            label: "Genetic Associations",
            value: disease["Genetic Associations"],
            icon: <FaRegListAlt size={24} />,
        },
        {
            label: "Medical Exams",
            value: disease["Medical Exams"],
            icon: <FaRegListAlt size={24} />,
        },
        {
            label: "Transmission Processes",
            value: disease["Transmission Processes"],
            icon: <FaRegListAlt size={24} />,
        },
    ];

    return (
        <div>
            <Header />
            <main className="container mt-4">
                <Card className="shadow-lg rounded-lg border-0">
                    <Card.Body>
                        <Card.Title className="text-center mb-4">
                            <h3>{disease.Name}</h3>
                        </Card.Title>
                        <div style={{ textAlign: "left" }}>
                            {fields.map(
                                (field, index) =>
                                    field.value && (
                                        <RenderField
                                            key={index}
                                            label={field.label}
                                            value={field.value}
                                            icon={field.icon}
                                        />
                                    )
                            )}
                        </div>
                    </Card.Body>
                </Card>
            </main>
        </div>
    );
}

export default DiseaseDetail;
