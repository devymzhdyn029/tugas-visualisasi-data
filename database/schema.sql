-- DDL Skema DBMS 1 (Relational Database - SQLite/PostgreSQL)

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price REAL
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    quantity INTEGER,
    transaction_date TEXT,
    FOREIGN KEY (product_id) REFERENCES products (product_id)
);