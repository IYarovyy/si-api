-- Roles -------------------------------------------------------
DROP TYPE IF EXISTS user_role CASCADE;
CREATE TYPE user_role AS ENUM ('admin', 'common');

-- Users -------------------------------------------------------
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    urole user_role not null,
    first_name varchar(255),
	  second_name varchar(255),
	  email varchar(255) not null,
	  password varchar(255)
);

CREATE UNIQUE INDEX idx_user_email ON users(email);
