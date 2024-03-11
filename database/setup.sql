-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS watermanagement;

-- Create the user if it doesn't exist and grant privileges
CREATE USER IF NOT EXISTS 'foo'@'localhost' IDENTIFIED BY 'foo123';

-- Ensure that the user has all privileges on the watermanagement database
GRANT ALL PRIVILEGES ON watermanagement.* TO 'foo'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;
