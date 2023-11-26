# API-server

## Written BY KYLiN



This server is fastAPI to build it 

## Update list

- put to test to generate

- use FastAPI :  https://fastapi.tiangolo.com/

---
## Setup
Make sure you add a `.env` file under `api` folder, path like `./api/.env`

File format
```sh
SERVER_IP={YOUR_HOST_IP}
SERVER_PORT=5000
```
## API-information
> You can check in `http://{YOUR_HOST_IP}:5000/

## Command 
### run server
```sh
# run server (in background)
sudo docker-compose up --build -d 

# get the logs 
sudo docker-compose logs -f

# shutdown
sudo docker-compose down 

# remove the <none> images
sudo docker image prune 
```

### save python package
```
pip freeze > requirements.txt

# install

pip install -r requirements.txt
```
---

### Note 
#### Docker 
- Docker-Compose : https://www.youtube.com/watch?v=gGkUu_T9848
- Docker-Compose in project(development): https://www.youtube.com/watch?v=CzAyaSolZjY
- Docker-Compose in project(product): https://www.youtube.com/watch?v=8kOubC4sYNk
- Docker-Compose in project(push to hub): https://www.youtube.com/watch?v=bcYmfHOrOPM

- Docker-Compose init easy : https://www.youtube.com/watch?v=iqrS7Q174Ac

---

#### Text to speech
- summery function : https://www.youtube.com/watch?v=TsfLm5iiYb4&t=3s

- free gpu: https://www.youtube.com/watch?v=wBCEDCiQh3Q


#### RabbitMQ
-  https://youtu.be/hfUIWe1tK8E?si=mPC4pw0RzpSwO8yW


#### llama
- https://huggingface.co/blog/llama2

---
### Docker command with gpu

```
docker run --name api_server_image --gpus '"device=0"' nvidia/cuda

docker start myrunoob

docker stop myrunoob

docker restart myrunoob

docker-compose -f ./redis-docker-compose.yml up
rq worker generate-image-queue
```
---
## python venv

- ref link : https://zhuanlan.zhihu.com/p/341481537
- project link : `./api_server_venv/Scripts/Activate.ps1`
```command 
pip install accelerate
```
