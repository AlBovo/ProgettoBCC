/*
    Creates the UTENTI table if it does not already exist.
    The table stores user information including their email, password, and admin status.
    The id column is the primary key and is auto-incremented.
    The email column is a unique constraint to ensure each user has a unique email address.
    The password column stores the SHA256 hash of the user's password.
    The is_admin column is a boolean flag indicating whether the user is an admin or not.
*/
CREATE TABLE IF NOT EXISTS UTENTI(
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(64) NOT NULL, -- SHA256 hash of the real password
    is_admin BOOLEAN NOT NULL DEFAULT FALSE, --TODO : change this with different tables
);


/*
    This script creates the GIORNI table if it doesn't already exist.
    The GIORNI table stores information about different days, including their start and end hours.
    It also includes a placeholder for storing already booked hours.
*/
CREATE TABLE IF NOT EXISTS GIORNI(
    id INT PRIMARY KEY AUTO_INCREMENT,
    start_hour TIME NOT NULL,
    end_hour TIME NOT NULL,
    -- TODO : find a way to store already booked hours
);


/*
    This script creates the 'DOMANDE' table if it does not already exist.
    The 'DOMANDE' table stores information about questions, including the user who asked the question,
    the admin who answered the question, the title of the question, the content of the question,
    and the status of the question (open or closed).
*/
CREATE TABLE IF NOT EXISTS DOMANDE(
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_utente INT NOT NULL,
    id_admin INT NOT NULL DEFAULT -1, -- TODO : change this with different tables
    titolo VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    stato ENUM('aperta', 'chiusa') NOT NULL DEFAULT 'aperta'
);