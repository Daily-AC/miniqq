import socket  # 导入socket模块，用于网络通信
import threading  # 导入threading模块，用于多线程处理

# 启动客户端函数
def start_client(server_ip, server_port):
    # 创建客户端socket对象
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 连接到服务器
    client.connect((server_ip, server_port))

    # 发送消息的函数
    def send_message():
        while True:
            # 输入目标主机IP
            target_ip = input("请输入目标主机IP: ")
            # 输入要发送的消息内容
            message = input("请输入要发送的消息: ")
            # 发送消息到服务器，格式为 "目标IP:消息内容"
            client.send(f"{target_ip}:{message}".encode())

    # 接收消息的函数
    def receive_message():
        while True:
            try:
                # 接收从服务器转发过来的消息
                message = client.recv(1024).decode()
                if message:
                    # 打印收到的消息
                    print(message)
                else:
                    break
            except:
                break
        # 关闭客户端连接
        client.close()

    # 创建发送消息线程
    send_thread = threading.Thread(target=send_message)
    # 创建接收消息线程
    receive_thread = threading.Thread(target=receive_message)

    # 启动发送和接收消息的线程
    send_thread.start()
    receive_thread.start()

# 启动客户端
start_client('1.1.1.1', 5555)  # 替换 '主机A或B的IP' 和 '服务器IP' 为实际IP地址
