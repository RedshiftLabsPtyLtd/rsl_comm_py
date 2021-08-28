# Docker Pipelines how-to:


Create docker image from a Dockerfile:
```
docker build -t um7py_image .
```

Create a docker container from the image (this will output the container 
hash value):

```
docker create -t -i um7py_image bash
```

Using the hash value from the previous step, one can login to bash inside
the container:
```
docker start -a -i 123_changethistomyhash_456
```

Alternatively, run a bash inside a docker container (without previous step):
```
docker start -a -i `docker create -t -i um7py_image bash`
```

## Pushing image to the docker hub:

Login to the docker hub from the PC:
```
docker login --username=yourhubusername
```

Look up the required image ID by running:
```
docker images
```

Tag the image
```
docker tag bb38976d03cf yourhubusername/image_name:v0.2
```

In particularly, for our case:
```
docker tag 6efd62ee0490 kselyunin/um7py_image:v0.1
```

Push the image to the dockerhub:
```
docker push kselyunin/um7py_image
```