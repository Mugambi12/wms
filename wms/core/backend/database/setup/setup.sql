-- Purpose: This script is used to setup the database and user for the application.
-- It creates the database, user, and grants the user all privileges on the database.

-- Author: Silas Mugambi
-- Date: February 2024

-- Create the database if it doesn't exist
-- DROP DATABASE IF EXISTS watermanagement;
CREATE DATABASE IF NOT EXISTS watermanagement;

-- Create the user if it doesn't exist and grant privileges
CREATE USER IF NOT EXISTS 'foo'@'localhost' IDENTIFIED BY 'foo123';

-- Ensure that the user has all privileges on the watermanagement database
GRANT PROCESS ON *.* TO 'foo'@'localhost';
-- GRANT ALL PRIVILEGES ON watermanagement.* TO 'foo'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;
