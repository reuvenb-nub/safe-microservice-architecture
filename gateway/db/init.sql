GRANT ALL PRIVILEGES ON gateway.* TO 'auth_user'@'localhost';
FLUSH PRIVILEGES;

-- CREATE DATABASE gateway;

USE gateway;

CREATE TABLE opaque (
    id INT AUTO_INCREMENT PRIMARY KEY,
    auth_key VARCHAR(255) NOT NULL,
    opaque_key VARCHAR(255) NOT NULL
);
