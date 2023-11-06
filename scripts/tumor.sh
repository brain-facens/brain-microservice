sudo docker rm tumor-detector
docker run --name tumor-detector -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix 4ddf390f38c6