from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit
import socket
from uuid import uuid4
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-very-secret-key-here'
socketio = SocketIO(app)

# Kết nối TCP đến server nội bộ
try:
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.connect(('127.0.0.1', 12345))
    print("✅ Đã kết nối TCP đến server.py")
except Exception as e:
    print("❌ Lỗi TCP:", e)
    tcp_client = None

# Lưu trữ người dùng đang hoạt động
active_users = {}  # {session_id: {'username': str, 'keycode': str, 'socket_id': str}}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('login_attempt')
def handle_login(data):
    username = data.get('username', '').strip()
    keycode = data.get('keycode', '').strip()
    
    if not username or not keycode:
        emit('login_error', 'Vui lòng nhập đầy đủ thông tin!')
        return
    
    # Kiểm tra nếu username đã tồn tại
    for user in active_users.values():
        if user['username'] == username:
            if user['keycode'] != keycode:
                emit('login_error', 'Tên người dùng đã được sử dụng với mã bí mật khác!')
                return
            else:
                # Đăng nhập lại với cùng thông tin
                break
    
    session_id = str(uuid4())
    active_users[session_id] = {
        'username': username,
        'keycode': keycode,
        'socket_id': request.sid
    }
    
    emit('login_success', {'username': username, 'keycode': keycode})
    
    # Thông báo có người dùng mới tham gia
    emit('receive_message', {
        'username': 'Hệ thống',
        'message': f'{username} đã tham gia cuộc trò chuyện'
    }, broadcast=True)

@socketio.on('logout')
def handle_logout(user_data):
    session_id = None
    for sid, user in active_users.items():
        if user['username'] == user_data['username'] and user['keycode'] == user_data['keycode']:
            session_id = sid
            break
    
    if session_id:
        username = active_users[session_id]['username']
        del active_users[session_id]
        
        # Thông báo người dùng đã rời đi
        emit('user_disconnected', username, broadcast=True)

@socketio.on('send_message')
def handle_message(data):
    if 'username' not in data or 'keycode' not in data or 'message' not in data:
        return
    
    # Kiểm tra người dùng có tồn tại không
    valid_user = False
    for user in active_users.values():
        if user['username'] == data['username'] and user['keycode'] == data['keycode']:
            valid_user = True
            break
    
    if not valid_user:
        return
    
    timestamp = datetime.now().strftime('%H:%M:%S')
    formatted_message = f"[{timestamp}] {data['username']}: {data['message']}"
    
    # Gửi tới TCP Server nếu kết nối thành công
    if tcp_client:
        try:
            tcp_client.send(formatted_message.encode())
        except Exception as e:
            print("❌ Lỗi khi gửi đến TCP server:", e)
    
    # Gửi lại cho các client web khác
    emit('receive_message', {
        'username': data['username'],
        'message': data['message']
    }, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    # Xóa người dùng khi disconnect
    session_id = None
    for sid, user in active_users.items():
        if user['socket_id'] == request.sid:
            session_id = sid
            break
    
    if session_id:
        username = active_users[session_id]['username']
        del active_users[session_id]
        
        # Thông báo người dùng đã rời đi
        emit('user_disconnected', username, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')