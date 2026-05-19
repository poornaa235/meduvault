-- MeduVault Database Setup
-- Run this file with: mysql -u root -p < meduvault.sql

CREATE DATABASE IF NOT EXISTS meduvault;
USE meduvault;

-- Users table (hospital login)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL
);

-- Personal details table
CREATE TABLE IF NOT EXISTS personal_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aadhar_number VARCHAR(20) NOT NULL,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(20),
    blood_group VARCHAR(10)
);

-- Medical history table
CREATE TABLE IF NOT EXISTS medical_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aadhar_number VARCHAR(20) NOT NULL,
    diagnosis VARCHAR(200),
    treatment VARCHAR(200),
    date DATE
);

-- Allergies table
CREATE TABLE IF NOT EXISTS allergies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aadhar_number VARCHAR(20) NOT NULL,
    allergen VARCHAR(100),
    reaction VARCHAR(100)
);

-- Insurance table
CREATE TABLE IF NOT EXISTS insurance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aadhar_number VARCHAR(20) NOT NULL,
    provider VARCHAR(100),
    policy_number VARCHAR(100),
    coverage VARCHAR(100)
);

-- Sample hospital user (username: admin, password: admin123)
INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'hospital');
