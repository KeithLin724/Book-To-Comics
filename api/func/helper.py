import socket

from . import api_json


def get_local_ip():
    """The function `get_local_ip` returns the local IP address of the machine by creating a temporary
    socket connection to a remote address and retrieving the local IP address from the socket.

    Returns
    -------
        The function `get_local_ip()` returns the local IP address of the device. If the function is able
    to create a temporary socket connection to a remote address, it will return the local IP address. If
    there is an error in creating the socket or connecting to the remote address, it will return the
    loopback address "127.0.0.1".

    """
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
    """The function saves server IP and port data to a JSON file.

    Parameters
    ----------
    server_ip : str
        The server IP address, which is a string representing the IP address of the server.
    server_port : str
        The server_port parameter is a string that represents the port number of the server.

    Returns
    -------
        Nothing is being returned.

    """
    data = {"ip": server_ip, "port": server_port}
    api_json.json_to_file(data, "server_data.json")
    return
