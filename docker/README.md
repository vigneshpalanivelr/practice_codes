# Why Docker ?
- Compatability of OS with Application Service
- Compatability of Library & Dependencies
- Checking everytime when the application Upgrades
- Setting Up Environment for Developers - Easily

# Container?
**Namespace**: Process and HW
**Control Groups**: Memory, CPU & BW


# Docker Package Checks:

    yum list docker-ce --showduplicates | sort -r

# Docker Details

    docker version
    docker info
    docker help | more

# Container Images:

    docker pull nginx         # Pull the image from docker hub
    docker images             # List all the imager present
  
# Remove Image/ Delete Containers:

    docker rm nginx     # Remove the Stopped/Exited Container not the Image
    docker rmi nginx    # Remove the Image <Stop & Delete all dependent containers> else failed
    docker system prune # Remove the Stopped containers
  
# Create/Start/Stop Container:
# Container Lives as long as the process is running

    docker create image       # Create the container
    docker start image/ID     # Start the container 
    docker start -a image/ID  # Start the container with all output
    docker stop ID/Name       # Stop the container
    Ctrl + C; Ctrl + D; exit; # Stop the container

# Containers list:

    docker ps           # List all the Running Containers
    docker ps -a/--all  # List all the Running/Stopped/Exited Containers

# Run Containers(Pull : Creating + Starting):

    docker run nginx                 # Pull the image and install container
    docker run hello-world           # Pull the image and install container
    docker run busybox echo hi       # Execute a command on container while starting it 
    docker run busybox ls            # Execute a command on container while starting it 
    docker run hello-world ls        # Execute a command on container while starting it 
    docker run nginx sleep 5         # Execute a command on container while starting it 
    docker run redis-server          # Execute a command on running container frpm outside

#  Execute in Container
    docker exec nginx cat /etc/hosts # Execute a command on running container frpm outside
    docker exec -it ID redis-cli     # Connect to Container using Executable 
    docker exec -it ID bash          # Connect to Container using Executable 
    Ctrl + C : No action

# Container Attach/Detach:

    docker run -it nginx # Attached Container
    exit                 # Detach   Container

# Check Logs:

    docker logs ID       # Check the logs of strated container
***STDIN              # Input communication to Container process***
***STDOUT             # Output communication from Container process***
***STDERR             # Output Error communication from Container process***

# Docker Commit

    docker commit -c 'CMD ["redis-server"]' ID

# Commands
    docker commit -c 'CMD ["redis-server"]' ID
    docker run --name test-njs -p 8080:8080 -d vigneshpr/simplenjs
    docker run --name test-pgs -p 5432:5432 -d postgres
    
    docker run --name dbs-app-redis -d redis-ld
    docker run --name web-app-python -p 80:5000 --link dbs-app-redis:redis-lb -d python-app

    docker run --name test-bb               -d busybox ping google.com
