## LIBRARY MANAGEMENT APPLICATION

#### TERMINAL 1 (FRONTEND API)
- start docker container with the specified
- sudo docker start
- sudo docker-compose build
- sudo docker-compose up frontend

- To run the Unitest for the frontend, cd into it and run
- sudo docker-compose exec frontend pytest

#### TERMINAL 2 (BACKEND API)
- start docker container with the specified
- sudo docker start
- sudo docker-compose build
- sudo docker-compose up backend

- To run the Unitest for the backend, cd into it and run
- sudo docker-compose exec backend pytest

n/b both terminal need to be running as some routes requires the webhook to interact