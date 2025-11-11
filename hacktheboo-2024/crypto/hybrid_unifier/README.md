# Hybrid unifier

Подготовлено: `rasti`

Автор задания: `rasti`

Уровень сложности: Легко

## Описание 

- В глубинах древней библиотеки старинная рукопись хранила ключ к невиданной силе. Учёные, осмелившиеся раскрыть её тайны, сначала обменивались *рядом* зашифрованных символов, образуя узы, которые никто не мог разорвать. Когда они *закрепляли* свою *связь*, вокруг них словно невидимые цепи обворачивали *слои защиты*. Но когда был установлен последний шифр, их поразило леденящее осознание - связь, которую они создали, теперь была привязана к чему-то куда более тёмному, к чему-то, что наблюдало из тени.

В таске дано несколько файлов

```bash
$ tree .

.
├── Dockerfile
├── build-docker.sh
├── challenge
│   ├── README.pdf
│   └── application
│       ├── app.py
│       ├── crypto
│       │   └── session.py
│       ├── requirements.txt
│       └── views.py
└── flag.txt
```

Для решения интересно в основном содержимое `challenge/application`.
Также есть Dockerfile и `build-docker.sh` для автоматизации развертывания локально. 

## Анализ исходного кода

Код в `views.py` обрабатывает запросы к/от API ручек. Над каждым методом есть комментарии, подсказывающие правильный порядок обращения к эндпоинтам.

С криптографической точки зрения, взаимодействие происходит так:
- Клиент отправляет серверу свой публичный ключ Диффи-Хеллмана.
- Сервер вычисляет сессионный ключ.
- Сервер отправляет свой публичный ключ клиенту, чтобы клиент согласовал тот же сессионный ключ.
- Этот сессионный ключ хэшируется с помощью SHA-256 и будет использован как симметричный AES-ключ для шифрования остального общения.

Эта информация также приведена в `README.pdf`.

Чтобы получить флаг, нам нужно зашифровать пакет поверх HTTP с полем action, установленным в `flag`, отправить его на эндпоинт `/api/dashboard` и, если расшифровка пройдёт успешно, мы получим флаг.

```python
@bp.route('/api/dashboard', methods=['POST'])
def access_secret():
    # обработчики ошибок вырезаны для краткости
    data = request.json
    encrypted_packet = data['packet_data']
    packet = session.decrypt_packet(encrypted_packet)
    action = packet['packet_data']
    if action == 'flag':
        return jsonify(session.encrypt_packet(open('/flag.txt').read()))
    elif action == 'about':
        return jsonify(session.encrypt_packet('<REDACTED>'))
    else:
        return jsonify(session.encrypt_packet('[!] Unknown action.'))
```

В верху исходного кода `views.py` можно увидеть инициализацию объекта `SecureSession` , который обрабатывает криптографическую часть приложения. 

```python
from Crypto.Util.number import getPrime
import os
from secrets import randbelow

class SecureSession:
    def __init__(self, bits):
        self.bits = bits
        self.g = 2
        self.p = getPrime(self.bits)
        self.compute_server_public_key()
        self.reset_challenge()
        self.initialized = False
		
    def compute_server_public_key(self):
        self.a = randbelow(self.p)
        self.server_public_key = pow(self.g, self.a, self.p)

    def reset_challenge(self):
    	self.challenge = os.urandom(24)
        
    # остальное читайте в session.py
```
Приложение использует в качестве механизма аутентификации 24-байтовую строку и протокол Диффи-Хеллмана с случайным 384-битным простым числом.

## Решение

Сначала нужно запросить параметры Диффи—Хеллмана 
```python
# Step 1. Request the Diffie Hellman parameters
@bp.route('/api/request-session-parameters', methods=['POST'])
def get_session_parameters():
    return jsonify({'g': hex(session.g), 'p': hex(session.p)})
```

Этот эндпоинт возвращает генератор $g$ и простое $p$ , которые также влияют на параметры нашего публичного ключа.

Чтобы автоматизировать это напишем функцию `retrieve_dh_parameters`
```python
import json, requests

URL = 'http://localhost:1337/api'

def retrieve_dh_parameters():
		params = json.loads(requests.post(f'{URL}/request-session-parameters').content)
  	g = eval(params['g'])
		p = eval(params['p'])
    return g, p
```

Инициализация безопасного соеденения происходит здесь 
```python
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
```

Есть проверки не было ли уже инициализовано, запрос в формате JSON должен содержать поле `client_public_key` , значение которого передается в этот метод:

```python
def establish_session_key(self, client_public_key):
    key = pow(client_public_key, self.a, self.p)
    self.session_key = sha256(str(key).encode()).digest()
```

Здесь создается общий секретный ключ уже для симметричного шифрования.Затем публичный ключ `server_public_key` возвращается в ответе.

Тогда автоматизируем клиентскую часть генерации ключей Диффи-Хеллмана
```python
from hashlib import sha256
import random

def establish_secure_session(g, p):
  	a = random.randint(2, p-2)
    A = pow(g, a, p)
    server_public_key = eval(
        json.loads(
            requests.post(
                f'{URL}/init-session',
                json={'client_public_key': A}
            ).content
        )['server_public_key'])
    shared_key = pow(server_public_key, a, p)
    session_key = sha256(str(shared_key).encode()).digest()
    return session_key
```

Теперь обе стороны согласовали единый ключ сессии. Пакеты будут зашифрованны до сервера в виде E2E шифрования.

Следующая ручка подтверждает ключ по дешифрованию сообщения проверки, сервер возвращает его в чистом виде.

```python
# Step 3. Request an encrypted challenge.
@bp.route('/api/request-challenge', methods=['POST'])
def request_challenge():
    if not session.initialized:
        return jsonify({'status_code': 400, 'error': 'A secure server-client session has to be established first.'})

    return jsonify({'encrypted_challenge': session.get_encrypted_challenge().decode()})
```

Для дальнейшего доступа к другим ручкам клиенту нужно тоже дешифровать сообщение проверки и вернуть серверу.

```python
from base64 import b64encode as be

def get_encrypted_challenge(self):
    iv = os.urandom(16)
    cipher = AES.new(self.session_key, AES.MODE_CBC, iv)
    encrypted_challenge = iv + cipher.encrypt(pad(self.challenge, 16))
    return be(encrypted_challenge)
```

Нам остается написать функцию, которая обращается к этой ручке и расшифровывает сообщение проверки после корректного парсинга зашифрованного пакета. Процесс парсинга сводится к следующему:

- Декодировать из Base64.
- Использовать первые 16 байт как параметр IV для AES-CBC, остальное это зашифрованные данные.
- Расшифровать зашифрованные данные и убрать паддинг.

Обработчик ручки для получения флага:
```python
# Step 4. Authenticate by responding to the challenge and send an encrypted packet with 'flag' as action to get the flag. 
@bp.route('/api/dashboard', methods=['POST'])
def access_secret():
    data = request.json
    challenge_hash = data['challenge']
    if not session.validate_challenge(challenge_hash):
        return jsonify({'status_code': 401, 'error': 'visit /request-challenge to get a new challenge!'})
    encrypted_packet = data['packet_data']

    packet = session.decrypt_packet(encrypted_packet)
    if not 'packet_data' in packet:
        return jsonify({'status_code': 400, 'error': packet['error']})
    
    action = packet['packet_data']
    if action == 'flag':
        return jsonify(session.encrypt_packet(open('/flag.txt').read()))
    # ... полный код читайте в views.py
```

Код валидации сообщения-проверки:
```python
def validate_challenge(self, challenge_hash):
    validated = challenge_hash == sha256(self.challenge).hexdigest()
    if validated:
        self.reset_challenge()
    return validated
```

Сообщения сравниваются по их хешам SHA256, если валиден - идет дальше и отправляет флаг, иначе сбрасывает сообщение проверки.

Чтобы получить флаг, мы должны отправить хэш сообщения проверки, зашифровать строку `flag`, используя сессионный ключ, и отправить её на сервер в виде base64. Сервер ответит также зашифрованным флагом, который нужно еще расшифровать через общий ключ. Автоматизируем это
```python
from base64 import b64encode as be

def get_flag(challenge, session_key):
    iv = b'\x00'*16
    cipher = AES.new(session_key, AES.MODE_CBC, iv)
    encrypted_packet = iv + cipher.encrypt(pad(b'flag', 16))
    data = bd(json.loads(
        requests.post(
            f'{URL}/dashboard',
            json = {
                'challenge': sha256(challenge).hexdigest(),
                'packet_data': be(encrypted_packet).decode()
            }
        ).content)['packet_data'])
    iv = data[:16]
    encrypted_flag = data[16:]
    cipher = AES.new(session_key, AES.MODE_CBC, iv)
    flag = unpad(cipher.decrypt(encrypted_flag), 16)
    return flag
```

Итоговая функция получения флага 
```python
def pwn():
    g, p = retrieve_dh_parameters()
    session_key = establish_secure_session(g, p)
    challenge = decrypt_challenge(session_key)
    flag = get_flag(challenge, session_key)
    print(flag.decode())

if __name__ == '__main__':
    pwn()
```