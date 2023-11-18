# Book-To-Comic-API
## Written By KYLiN , Vincent

--- 
## Description
Using the fastAPI to build it 


### How to use
```sh
# first cd to api
cd api

# second open the docker '-d mean open in background'
docker-compose up --build -d

# or use this command (after build)
docker-compose up -d 

# check the log 
docker-compose logs -f

# check the api_server log ctrl+c exit
docker logs -f api_server_1

# close 
cd api
docker-compose down 
```
### Mention
You need to make a`./api/.env` 
#### Format of `./api/.env`
```sh
SERVER_IP={your_server_ip}
SERVER_PORT=5000
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