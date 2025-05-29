import socket
from datetime import datetime

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 12345))
server_socket.listen(1)

print("🚀 Server TCP đang lắng nghe tại 127.0.0.1:12345...")
client_socket, addr = server_socket.accept()
print("✅ Kết nối từ:", addr)

try:
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        
        message = data.decode()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] Nhận được từ Flask:", message)
        
except Exception as e:
    print("❌ Lỗi:", e)
finally:
    client_socket.close()
    server_socket.close()