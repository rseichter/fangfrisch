PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE automx2 (
	db_version INTEGER NOT NULL, 
	PRIMARY KEY (db_version)
);
INSERT INTO automx2 VALUES(2);
CREATE TABLE refreshlog (
	url VARCHAR NOT NULL, 
	digest VARCHAR, 
	path VARCHAR NOT NULL, 
	provider VARCHAR, 
	updated DATETIME, 
	PRIMARY KEY (url)
);
COMMIT;
