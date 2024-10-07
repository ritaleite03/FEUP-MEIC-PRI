CREATE SCHEMA IF EXISTS pri_proj;

CREATE TABLE "disease"
(
    id SERIAL,
    overview TEXT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE "risk_factor"
(
    id SERIAL,
    description TEXT,
    PRIMARY KEY(id),
    id_disease INTEGER REFERENCES "disease" (id)
);

CREATE TABLE "complication"
(
    id SERIAL,
    description TEXT,
    PRIMARY KEY(id),
    id_disease INTEGER REFERENCES "disease" (id)
);

CREATE TABLE "prevention"
(
    id SERIAL,
    description TEXT,
    PRIMARY KEY(id),
    id_disease INTEGER REFERENCES "disease" (id)
);

CREATE TABLE "diagnostic"
(
    id SERIAL,
    description TEXT,
    PRIMARY KEY(id),
    id_disease INTEGER REFERENCES "disease" (id)
);

CREATE TABLE "health_speciality"
(
    id SERIAL,
    description TEXT,
    PRIMARY KEY(id),
    id_disease INTEGER REFERENCES "disease" (id)
);

CREATE TABLE "alias"
(
    id SERIAL,
    name TEXT,
    PRIMARY KEY(id),
    id_disease INTEGER REFERENCES "disease" (id)
);

CREATE TABLE "symptom"
(
    id SERIAL,
    description TEXT,
    PRIMARY KEY(id),
    id_disease INTEGER REFERENCES "disease" (id)
);

CREATE TABLE "cause"
(
    id SERIAL,
    description TEXT,
    PRIMARY KEY(id),
    id_disease INTEGER REFERENCES "disease" (id)
);

CREATE TABLE "treatment"
(
    id SERIAL,
    description TEXT,
    PRIMARY KEY(id),
    id_disease INTEGER REFERENCES "disease" (id)
);

CREATE TABLE "subclass"
(
    id SERIAL,
    name TEXT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE "disease_subclass"
(
    disease_id INTEGER REFERENCES "disease" (id),
    subclass_id INTEGER REFERENCES "subclass" (id),
    PRIMARY KEY(disease_id, subclass_id)
);
