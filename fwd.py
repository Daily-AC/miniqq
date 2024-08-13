import socket  # 导入socket模块，用于网络通信
import threading  # 导入threading模块，用于多线程处理

# 存储已连接的客户端，键为客户端IP，值为客户端socket对象
clients = {}

# 处理客户端连接的函数
def handle_client(client_socket, addr):
    while True:
        try:
            # 接收客户端消息，最多接收1024字节
            message = client_socket.recv(1024).decode()
            if message:
                # 假设消息格式为 "目标IP:消息内容"
                target_ip, msg_content = message.split(":")
                
                # 如果目标IP在已连接客户端列表中
                if target_ip in clients:
                    target_socket = clients[target_ip]
                    # 将消息转发给目标主机
                    target_socket.send(f"来自{addr[0]}的消息: {msg_content}".encode())
                else:
                    # 如果目标主机不在线或IP错误，返回错误信息
                    client_socket.send("目标主机不在线或IP错误".encode())
            else:
                break
        except:
            break
    
    # 关闭客户端连接，并从列表中移除该客户端
    client_socket.close()
    del clients[addr[0]]

# 启动服务器函数
def start_server(server_ip, server_port):
    # 创建服务器socket对象
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定服务器IP和端口
    server.bind((server_ip, server_port))
    # 开始监听，最大连接数为5
    server.listen(5)
    print(f"服务器启动，监听 {server_ip}:{server_port}")

    while True:
        # 接受新的客户端连接
        client_socket, addr = server.accept()
        # 将客户端IP和socket对象存入字典
        clients[addr[0]] = client_socket
        print(f"新连接: {addr}")
        # 为每个客户端创建一个线程处理通信
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

# 启动服务器
start_server('192.168.0.107', 5000)  # 替换 '服务器IP' 为实际的服务器IP地址
