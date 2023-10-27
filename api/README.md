# API-server
## Written BY KYLiN

---
## Update list 
- use FastAPI


---

- Text to speech 
- summery function  : https://www.youtube.com/watch?v=TsfLm5iiYb4&t=3s

- free gpu 
- https://www.youtube.com/watch?v=wBCEDCiQh3Q

- install ngrok

python package
```
pip freeze > requirements.txt

# install 

pip install -r requirements.txt
```


```
- RabbitMQ
https://youtu.be/hfUIWe1tK8E?si=mPC4pw0RzpSwO8yW

- Docker
https://youtu.be/Ozb9mZg7MVM?si=I2QS82bs2QUd6sFN

https://youtu.be/bi0cKgmRuiA?si=9089YSxd9amBdGAA

https://ithelp.ithome.com.tw/articles/10246065

- llama
https://huggingface.co/blog/llama2
```

### docker command with gpu
```
docker run --name api_server_image --gpus '"device=0"' nvidia/cuda

docker start myrunoob

docker stop myrunoob

docker restart myrunoob

docker-compose -f ./redis-docker-compose.yml up
rq worker generate-image-queue
```

#### python venv 

- https://zhuanlan.zhihu.com/p/341481537
- ./api_server_venv/Scripts/Activate.ps1
- pip install accelerate