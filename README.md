 # Ephemeral Secrets Sharing Website

Ephemeral Secrets is a simple, intuitive, and secure method of sharing secrets with people across the internet. It has been developed with Docker to be simple and easy to deploy within any network.

![Screenshot](https://user-images.githubusercontent.com/12218728/264850653-58e39baa-e61f-4b99-8b85-826bae958775.png)

## Features
- The sender is able to set the date which the secret will expire.
- The secret requires a password before it can be viewed.
- Secrets can only be unlocked and viewed once.
- HTTPS connections are supported.

## Built With
- Docker
- Flask
- Bootstrap

# Getting Started
## Prerequisites
To install and run Ephemeral Secrets, [Docker](https://docs.docker.com/engine/install/) must be installed.


## Installation and Usage
1. Clone the repo
   
   `git clone https://github.com/jonathontran/Ephemeral-secrets-sharing-website.git`
2. Change Directory
   
    `cd Ephemeral-secrets-sharing-website`
3. Run Docker

   Installation
    `docker-compose pull`
    `docker-compose up --build -d`
   
   General use:
    `docker-compose rm -f`
    `docker-compose pull`
    `docker-compose up --build -d`

5. Once Docker finishes provision the app, you can open a web browser and navigate to [localhost](https://localhost)

6. Stop The Application/Docker

    `docker-compose stop -t 1`

# Contributers
 - [Jonathon T](https://github.com/jonathontran)
 - [Harry S](https://github.com/Podzee)
 - [Jesse L](https://github.com/ProfessorNudelz)
 - [Damien K](https://github.com/damienkleinn)
 - [Mitch P](https://github.com/mphelan1)
 - [Emily T](https://github.com/emm1010)

## Acknowledgments
The development team would like to acknowledge the project's client, Bad Security Inc, as well as the project's supervisor, Irene M.
