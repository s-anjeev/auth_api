-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS auth_api;

-- Use the created database
USE auth_api;

-- Create the Users table
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(10) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create session table if not exists
CREATE TABLE IF NOT EXISTS session (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token VARCHAR(512) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expire_time TIMESTAMP DEFAULT (NOW() + INTERVAL 60 MINUTE),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
-- Create Users_personal_details table if not exists
CREATE TABLE IF NOT EXISTS Users_personal_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(80) NOT NULL,
    last_name VARCHAR(80) NOT NULL,
    country VARCHAR(30) NOT NULL,
    phone_number VARCHAR(15),
    date_of_birth DATE,
    age INT,
    gender VARCHAR(10),
    avatar_url VARCHAR(255),
    user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Create the new view
CREATE VIEW UserDetailsView AS
SELECT upd.user_id AS user_id,
       upd.first_name,
       upd.last_name,
       upd.country,
       upd.phone_number,
       upd.date_of_birth,
       upd.age,
       upd.gender,
       upd.avatar_url,
       u.email,
       u.username,
       u.role
FROM Users_personal_details upd
JOIN Users u ON upd.user_id = u.user_id;


-- create table admin 
CREATE TABLE IF NOT EXISTS Admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updating_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    role VARCHAR(50) DEFAULT 'admin',
    session_token VARCHAR(255),
    UNIQUE (email)
);
