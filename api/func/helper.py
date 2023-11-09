import socket
import api_json


def get_local_ip():
    try:
        # 创建一个临时的套接字连接到一个远程地址，然后获取本地 IP 地址
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # 这里的远程地址可以是任意已知 IP 地址和端口
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except socket.error:
        return "127.0.0.1"


def save_server_data_to_json(server_ip: str, server_port: str):
    data = {"ip": server_ip, "port": server_port}
    api_json.json_to_file(data, "server_data.json")
    return
