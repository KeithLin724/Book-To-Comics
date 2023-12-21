# Book-To-Comic-API
## Written By KYLiN , Vincent

--- 
## Description
Using the fastAPI to build it 

---
# Download 

**Zip** : [here](https://github.com/KeithLin724/Book-To-Comics/zipball/main)

**git**:  `git clone https://github.com/KeithLin724/Book-To-Comics.git`


---

### How to use
install [Docker](https://www.docker.com/) and [Docker-compose](https://docs.docker.com/compose/)

```sh
# first cd to api
cd api

# second open the docker '-d mean open in background'
docker-compose up --build -d

# or use this command (after build)
docker-compose up -d 

# check the log 
docker-compose logs -f

# check the api_server log, ctrl+c exit
docker logs -f api_server_1

# close 
cd api
docker-compose down 
```
In `api` folder is a main server for handler other service, such as `chat`, `text_to_image`

In `api_cuda` folder is a text_to_image server, for provide text to image service


### Mention
You need to make a`./api/.env` and `./api_cuda/.env`
#### Format of `./api/.env`
```sh
SERVER_IP={your_server_ip}
SERVER_PORT=5000
```

#### Format of `./api_cuda/.env`
```sh
LAB_SERVER_IP={YOUR_CONNECT_SERVER_IP}
LAB_SERVER_PORT=5000
HOST_IP={YOUR_HOST_IP}
```
---

## Example app 
In `chat` folder, we put a example app for test the server 

### How to use 
```sh
# go to folder
cd chat

# install some need
pip install -r ./requirement.txt

# go to src
cd src

# run app
python ./app.py
```
### Mention
You need to make a`./chat/src/.env` 
#### Format of `./chat/src/.env`
```sh
SERVER_IP={your_server_ip}
SERVER_PORT=5000
```
---
## Firewall
You need to allow 
|port|function|
|-|-|
|5000|main API|
|6379|redis Database|
|8001|redis Database Webpage Monitor|
|4080|Text-to-image API|
