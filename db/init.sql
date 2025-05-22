CREATE TABLE status (
    id SERIAL PRIMARY KEY,
    status_code INT NOT NULL,
    status_desc TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    stand VARCHAR(50) NOT NULL
);

CREATE TABLE version (
    id SERIAL PRIMARY KEY,
    stand VARCHAR(50) NOT NULL,
    version VARCHAR(10) NOT NULL
);