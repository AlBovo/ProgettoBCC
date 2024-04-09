#!/bin/sh
# READ THIS BEFORE RUNNING THIS SCRIPT
docker image rm backend -f
docker image rm mysql -f
docker volume prune -af
docker container rm progettobcc-backend-backend-1 -f
docker container rm progettobcc-backend-db-1 -f 
