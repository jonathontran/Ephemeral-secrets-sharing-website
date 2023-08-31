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