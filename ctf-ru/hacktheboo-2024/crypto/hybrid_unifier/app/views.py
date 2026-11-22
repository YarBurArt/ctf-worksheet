"""
source https://github.com/AttilaTheDog/hybridunifier_changed
"""
from app import app
from flask import Blueprint, render_template, request, session, make_response, redirect, url_for, flash, jsonify
#from crypto.session import SecureSession
from session import SecureSession

bp = Blueprint('views', __name__)
session = SecureSession(384)

# Step 1. Request the Diffie Hellman parameters
@bp.route('/api/request-session-parameters', methods=['POST'])
def get_session_parameters():
    return jsonify({'g': hex(session.g), 'p': hex(session.p)})

# Step 2. Initialize a secure session with the server by sending your Diffie Hellman public key
@bp.route('/api/init-session', methods=['POST'])
def init_session():
    if session.initialized:
        return jsonify({'status_code': 400, 'error': 'A secure session has already been established.'})

    data = request.json
    if 'client_public_key' not in data:
        return jsonify({'status_code': 400, 'error': 'You need to send the client public key.'})
    
    client_public_key = data['client_public_key']
    session.establish_session_key(client_public_key)
    session.initialized = True
    return jsonify({'status_code': 200, 'success': 'A secure session was successfully established. There will be E2E encryption for the rest of the communication.', 'server_public_key': hex(session.server_public_key)})

# Step 3. Request an encrypted challenge.
@bp.route('/api/request-challenge', methods=['POST'])
def request_challenge():
    if not session.initialized:
        return jsonify({'status_code': 400, 'error': 'A secure server-client session has to be established first.'})

    return jsonify({'encrypted_challenge': session.get_encrypted_challenge().decode()})

# Step 4. Authenticate by responding to the challenge and send an encrypted packet with 'flag' as action to get the flag. 
@bp.route('/api/dashboard', methods=['POST'])
def access_secret():
    if not session.initialized:
        return jsonify({'status_code': 400, 'error': 'A secure server-client session has to be established first.'})

    data = request.json

    if 'challenge' not in data:
        return jsonify({'status_code': 400, 'error': 'You need to send the hash of the challenge.'})

    if 'packet_data' not in data:
        return jsonify({'status_code': 400, 'error': 'Empty packet.'})
        
    challenge_hash = data['challenge']
    if not session.validate_challenge(challenge_hash):
        return jsonify({'status_code': 401, 'error': 'Invalid challenge! Something wrong? You can visit /request-challenge to get a new challenge!'})

    encrypted_packet = data['packet_data']

    packet = session.decrypt_packet(encrypted_packet)
    if not 'packet_data' in packet:
        return jsonify({'status_code': 400, 'error': packet['error']})
    
    action = packet['packet_data']
    if action == 'flag':
        return jsonify(session.encrypt_packet(open('/flag.txt').read()))
    elif action == 'about':
        return jsonify(session.encrypt_packet('[+] Welcome to my custom API! You are currently Alpha testing my new E2E protocol.\nTo get the flag, all you have to do is to follow the protocol as intended. For any bugs, feel free to contact us :-] !'))
    else:
        return jsonify(session.encrypt_packet('[!] Unknown action.'))