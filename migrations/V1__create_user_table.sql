create table Users (
    id SERIAL NOT NULL PRIMARY KEY,
    email varchar(255) NOT NULL,
    password varchar(255) NOT NULL
)