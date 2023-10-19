import os
from monsterapi import client

#Set the Monster API key as an environment variable
os.environ['MONSTER_API_KEY'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImNkMzgyZGUyYzkxM2ZlZWExZDM0NDNjOTQzMmUzOTE2IiwiY3JlYXRlZF9hdCI6IjIwMjMtMTAtMTlUMDk6NDY6MTUuNzM3OTAwIn0.g7RfJ4e3wfMgmLUqQJULprEt_79b1zDE39xqd-w7EvQ'

#Initialize the Monster API client
monster_client = client()

#Fetch a response from the Monster API
response = monster_client.generate(model='txt2img', data={
    "prompt": "An image of the ancient village where Xiao Ming lived."})

print(response)