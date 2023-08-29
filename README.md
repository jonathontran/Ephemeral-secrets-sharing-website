 # Ephemeral-secrets-sharing-website HOW TO DOCKER???

# INSTALL
1. Install Docker Desktop on PC, make sure it's running

# RUNNING
1. In a terminal (CMD etc) change your directory to the same directory that the *docker-compose.yml* is in 
2. Run the command: docker compose up -d
3. This will now show up in the docker application and you should be able to acces the application
4. To stop it you can either stop it in Docker desktop or type: dokcer compose down

# To make changes and update:
1. Make your changes
2. Stop the container (See above)
3. Run the command: docker images
4. Find the image that you want to delete and run: docker rmi 'image_id' 
5. Then rerun docker compose and bobs your uncle 

