from flask import Flask, render_template, request, jsonify, session, redirect
from crypto_utils import generate_rsa_keys, save_rsa_keys, load_rsa_keys
from cryptography.hazmat.primitives import serialization
from player_logic import Player
from transactions import Transaction
import os
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Khởi tạo game
def setup_game():
    keys_dir = "bank_security_game/keys"
    os.makedirs(keys_dir, exist_ok=True)
    private_path = os.path.join(keys_dir, "rsa_private.pem")
    public_path = os.path.join(keys_dir, "rsa_public.pem")

    if not os.path.exists(private_path) or not os.path.exists(public_path):
        private_key, public_key = generate_rsa_keys()
        save_rsa_keys(private_key, public_key, private_path, public_path)

    return load_rsa_keys(private_path, public_path)

@app.before_request
def before_request():
    if 'player' not in session:
        session['player'] = Player().__dict__
    if 'private_key' not in session or 'public_key' not in session:
        private_key, public_key = setup_game()
        session['private_key'] = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')
        session['public_key'] = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html', player=session['player'])

@app.route('/victory')
def victory():
    return render_template('victory.html', player=session['player'])

@app.route('/next-game')
def next_game():
    player = session.get('player', {'level': 1, 'score': 0})
    if player['level'] < 10:
        player['level'] += 1
    session['player'] = player
    session['transactions'] = generate_transactions(player['level'])
    session['current_transaction'] = 0
    return redirect('/game')

@app.route('/next-level')
def next_level():
    player = session['player']
    player['level'] += 1
    session['transactions'] = generate_transactions(player['level'])
    session['current_transaction'] = 0
    return redirect('/game')

@app.route('/end-game')
def end_game():
    player = session.get('player', {'score': 0})
    score = player.get('score', 0)
    session.clear()
    session['player'] = {'score': score, 'level': 10}  # giả lập level cao nhất
    return redirect('/victory')


@app.route('/start-game', methods=['POST'])
def start_game():
    level = int(request.form.get('level', 1))
    session['player']['level'] = level
    session['transactions'] = generate_transactions(level)
    session['current_transaction'] = 0
    return jsonify({'status': 'success', 'redirect': '/game'})

@app.route('/game')
def game():
    return render_template('game.html', 
                         player=session['player'],
                         level_info=get_level_info(session['player']['level']),
                         transaction_count=len(session['transactions']))

@app.route('/current-transaction')
def current_transaction():
    tx_idx = session['current_transaction']
    tx = session['transactions'][tx_idx]
    return render_template('transaction.html', 
                         player=session['player'],
                         transaction=tx,
                         tx_number=tx_idx+1,
                         tx_total=len(session['transactions']))

@app.route('/process-step', methods=['POST'])
def process_step():
    step = request.form.get('step')
    tx_idx = session['current_transaction']
    tx = session['transactions'][tx_idx]
    player = session['player']

    if step == 'encrypt':
        user_input = request.form.get('input')
        correct = f"{tx['sender']}|{tx['receiver']}|{tx['amount']}"
        if user_input == correct:
            player['score'] += 10
            session.modified = True
            return jsonify({'success': True, 'message': 'Mã hóa đúng!', 'score': player['score']})
        else:
            return jsonify({'success': False, 'message': 'Sai thông tin giao dịch!'})

    elif step == 'sign':
        user_input = request.form.get('input')
        correct_signature = f"sig_{tx['sender']}_{tx['receiver']}_{tx['amount']}"
        if user_input == correct_signature:
            player['score'] += 10
            session.modified = True
            return jsonify({
                'success': True, 
                'message': 'Xác thực thành công!', 
                'score': player['score'],
                'correct_signature': correct_signature
            })
        else:
            return jsonify({'success': False, 'message': 'Chữ ký không hợp lệ!'})

    elif step == 'hash':
        user_input = request.form.get('input')
        correct_hash = f"hash_{tx['sender']}_{tx['receiver']}_{tx['amount']}"

        if user_input == correct_hash:
            player['score'] += 10
            session.modified = True

            if tx_idx + 1 < len(session['transactions']):
                session['current_transaction'] += 1
                return jsonify({
                    'success': True,
                    'message': 'Kiểm tra toàn vẹn thành công!',
                    'score': player['score'],
                    'next': True,
                    'correct_hash': correct_hash
                })
            else:
                max_level = 3
                if player['level'] < max_level:
                 return jsonify({
                    'success': True,
                    'message': 'Hoàn thành level!',
                    'score': player['score'],
                    'ready_for_next': True
                })
                else:
                    return jsonify({
                        'success': True,
                        'message': 'Hoàn thành toàn bộ trò chơi!',
                        'score': player['score'],
                        'victory': True
                    })
        else:
            return jsonify({'success': False, 'message': 'Hash không khớp!'})

    else:
        return jsonify({'success': False, 'message': 'Bước xử lý không hợp lệ!'})

def generate_transactions(level):
    name_pool = [
        "Alice", "Bob", "Carol", "Dave", "Eve", "Frank",
        "Grace", "Heidi", "Ivan", "Judy", "Mallory", "Niaj",
        "Oscar", "Peggy", "Sybil", "Trent", "Victor", "Walter",
        "Yvonne", "Zara"
    ]
    max_level = 3
    if level > max_level:
        level = max_level

    num_tx = {1: 2, 2: 3, 3: 4}.get(level, 2)
    used_names = set()
    tx_list = []

    for _ in range(num_tx):
        sender, receiver = random.sample(name_pool, 2)
        while (sender, receiver) in used_names or sender == receiver:
            sender, receiver = random.sample(name_pool, 2)
        amount = random.randint(50 * level, 300 * level)
        tx_list.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        used_names.add((sender, receiver))

    return tx_list

def get_level_info(level):
    if level == 1:
        return "Cấp độ 1: Giao dịch đơn giản, số tiền nhỏ, thông tin dễ dàng."
    elif level == 2:
        return "Cấp độ 2: Số lượng giao dịch tăng, số tiền lớn hơn, dùng khóa AES mạnh hơn."
    else:
        return "Cấp độ 3: Giao dịch phức tạp, xác thực và kiểm tra toàn vẹn chặt chẽ hơn."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
