create database ephemeralSecrets;
use ephemeralSecrets;

CREATE TABLE `user_secret` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `url` varchar(6) NOT NULL,
 `expiry` datetime NOT NULL,
 `password` varchar(256) NOT NULL,
 `SALT` varchar(256) NOT NULL,
 `secret` varchar(10240) NOT NULL,
 `active` tinyint(1) NOT NULL,
 PRIMARY KEY (`id`)
);

/*
Create a new user 'ephemeralappuser' and grant it CRUD permissions on the 'ephemeralSecrets' database

Note SQL files don't have the capability to directly read environment variables. As such keep this file secure. 
*/
CREATE USER 'ephemeralappuser'@'%' IDENTIFIED WITH 'mysql_native_password' BY 'password';
GRANT select, update, insert, delete ON ephemeralSecrets.* TO 'ephemeralappuser'@'%';

CREATE EVENT myevent
    ON SCHEDULE EVERY 1 MINUTE
    DO
      UPDATE ephemeralSecrets.user_secret SET active = 'false' WHERE expiry_date > NOW();