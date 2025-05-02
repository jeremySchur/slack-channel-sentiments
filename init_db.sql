CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(100),
  email VARCHAR(100)
);

INSERT INTO users (username, email) VALUES ('john_doe', 'john@example.com');