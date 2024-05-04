#!/bin/sh
# READ THIS BEFORE RUNNING THIS SCRIPT
docker container rm progettobcc-backend-1 -f
docker container rm progettobcc-db-1 -f 
docker image rm backend -f
docker image rm mysql -f
docker volume prune -af