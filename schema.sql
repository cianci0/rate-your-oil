CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE regions (
    region_id SERIAL PRIMARY KEY,
    region_name VARCHAR UNIQUE
);

CREATE TABLE producers (
    producer_id SERIAL PRIMARY KEY,
    producer_name VARCHAR(255),
    region_id INT REFERENCES regions(region_id)
);

CREATE TABLE oils (
    oil_id SERIAL PRIMARY KEY,
    oil_name VARCHAR(255) UNIQUE,
    producer_id INT REFERENCES producers(producer_id),
    region_id INT REFERENCES regions(region_id)
);

CREATE TABLE ratings (
    rating_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    oil_id INT REFERENCES oils(oil_id),
    rating FLOAT,
    fruity INT,
    grassy INT,
    salty INT,
    sweet INT,
    floral INT,
    pungent INT,
    citrusy INT
);
