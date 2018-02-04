# Calculator

## Prerequisites

### Docker
Installing Docker on your system:

For macOS: https://docs.docker.com/docker-for-mac/

For Windows: https://docs.docker.com/docker-for-windows/

For Linux: https://docs.docker.com/engine/installation/#server

### Docker Compose
Installed by default on Windows and macOS. For Linux, run:
```
sudo apt-get install python-setuptools python-dev build-essential
sudo easy_install pip
sudo pip install --upgrade virtualenv
sudo pip install docker-compose
```

## Installing

While in the same directory as `docker-compose.yml`, run the following:

1) Upon first installation, or if any dependencies are updated:

```
sudo apt install docker.io
sudo docker-compose build
```

2) To start the services up:

```
sudo docker-compose up
```

## Requirements
```
matplotlib==2.0.2
numpy==1.13.1
plotly==2.2.1
PyYAML==3.12
sanic==0.6.0
pytesseract==0.1.7
Pillow==4.3.0
```




