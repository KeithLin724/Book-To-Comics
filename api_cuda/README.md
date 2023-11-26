# API Text-to-Image
## Written By KYLiN

---

## Setup
Make sure you add a `.env` file under `api` folder, path like `./api_cuda/.env`


```
LAB_SERVER_IP={YOUR_CONNECT_SERVER_IP}
LAB_SERVER_PORT=5000
HOST_IP={YOUR_HOST_IP}
```

## API-information
> You can check in `http://{YOUR_HOST_IP}:5000/docs`

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
