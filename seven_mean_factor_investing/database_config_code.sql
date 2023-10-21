CREATE DATABASE financial_applications;

USE financial_applications;

CREATE TABLE prices (
	id INTEGER PRIMARY KEY auto_increment,
    date DATE NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    open DECIMAL(10,2),
    high DECIMAL(10,2),
    low DECIMAL(10,2),
    close DECIMAL(10,2)
);

SHOW TABLES;

DESCRIBE prices;