import requests

url = "http://140.113.238.35:5000/uploadfile/"
files = {
    "file": ("cat.jpg", open("./cat.jpg", "rb"), "image/jpeg"),
}
response = requests.post(url, files=files)
print(response.json())
