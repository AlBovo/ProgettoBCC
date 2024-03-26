/*
    Creates the users table if it does not already exist.
    The table stores user information including their email, password, and admin status.
    The id column is the primary key and is auto-incremented.
    The email column is a unique constraint to ensure each user has a unique email address.
    The password column stores the SHA256 hash of the user's password.
    The is_admin column is a boolean flag indicating whether the user is an admin or not.
*/
CREATE TABLE IF NOT EXISTS users(
    id INT AUTO_INCREMENT PRIMARY KEY ,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL, -- Hash of the real password
    is_admin BOOLEAN NOT NULL DEFAULT false -- TODO : change this with different tables
) AUTO_INCREMENT = 0;
-- SPLIT
/*
    This script creates the events table if it does not already exist.
    The table stores information about events, including the day, start and end time, user ID, and category.
*/
CREATE TABLE IF NOT EXISTS events(
    id INT PRIMARY KEY AUTO_INCREMENT,
    day INT NOT NULL, -- timestamp of the day
    start_hour TIME NOT NULL,
    end_hour TIME NOT NULL,
    user_id INT NOT NULL,
    categories ENUM('prova', 'prova2', 'prova3') NOT NULL -- TODO : change this actual categories
);
-- SPLIT
/*
    This script creates the 'questions' table if it does not already exist.
    The 'questions' table stores information about questions, including the user who asked the question,
    the admin who answered the question, the title of the question, the content of the question,
    and the status of the question (open or closed).
*/
CREATE TABLE IF NOT EXISTS questions(
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_users INT NOT NULL,
    id_admin INT NOT NULL DEFAULT -1, -- TODO : change this with different tables
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    status ENUM('aperta', 'chiusa') NOT NULL DEFAULT 'aperta'
);