# Calculator
Class project for CS321

## Prerequisites

### Docker
Installing Docker on your system:

For macOS: https://docs.docker.com/docker-for-mac/

For Windows: https://docs.docker.com/docker-for-windows/

For Linux: https://docs.docker.com/engine/installation/#server

### Docker Compose
Installed by default on Windows and macOS. For Linux, run:
```
pip install docker-compose
```

## Installing

While in the same directory as `docker-compose.yml`, run the following:

1) Upon first installation, or if any dependencies are updated:

```
docker-compose build
```

2) To start the services up:

```
docker-compose up
```

3) If the above didn't work, try:
```
sudo docker-compose up
```






