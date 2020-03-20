CREATE TABLE refreshlog (
url VARCHAR(255) PRIMARY KEY,
digest VARCHAR(255),
path VARCHAR(255) NOT NULL,
provider VARCHAR(255),
updated TIME
);
