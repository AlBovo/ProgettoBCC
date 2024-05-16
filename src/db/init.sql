/*
    Creates the users table if it does not already exist.
    The table stores user information including their email, password, and admin status.
    The id column is the primary key and is auto-incremented.
    The email column is a unique constraint to ensure each user has a unique email address.
    The password column stores the SHA256 hash of the user's password.
    The is_admin column is a boolean flag indicating whether the user is an admin or not.
*/
CREATE TABLE IF NOT EXISTS users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL, -- Hash of the real password
    is_admin BOOLEAN NOT NULL DEFAULT false
) AUTO_INCREMENT = 0;


/*
    This script creates the events table if it does not already exist.
    The table stores information about events, including the day, start and end time, user ID, and category.
*/
CREATE TABLE IF NOT EXISTS events(
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL, -- timestamp of the day
    start_hour INT NOT NULL, -- military time ex. 830 == 8:30
    end_hour INT NOT NULL,   -- military time
    category TEXT NOT NULL,    -- unique code for each category
    user_id INT NOT NULL,
    operator_id INT NOT NULL
);

/*
    This script initializes the 'operators' table in the database.
    The 'operators' table stores information about operators, including their name, surname, and categories.
*/
CREATE TABLE IF NOT EXISTS operators(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    surname VARCHAR(30) NOT NULL,
    category TEXT NOT NULL -- unique code for each category
) AUTO_INCREMENT = 0;  -- unique id for each operator and auto-incremented

/*
    This script creates the 'questions' table if it does not already exist.
    The 'questions' table stores information about questions, including the user who asked the question,
    the admin who answered the question, the title of the question, the content of the question,
    and the status of the question (open [0] or closed [1]).
*/
CREATE TABLE IF NOT EXISTS questions(
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_users INT NOT NULL,
    id_admin INT NOT NULL DEFAULT 1,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    status BIT NOT NULL DEFAULT 0
);
