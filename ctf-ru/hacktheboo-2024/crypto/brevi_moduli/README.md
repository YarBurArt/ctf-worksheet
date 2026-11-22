# brevi moduli

Подготовлено: `rasti`

Автор задания: `0x50r4`

Уровень сложности: Очень легко

## Описание

В холодную хеллоуинскую ночь пятеро искателей приключений собрались у входа в древний склеп. Хранитель склепа вышел из тени, его голос прошёлся дрожащим шёпотом: «Пять замков охраняют сокровище внутри. Взломайте их, и склеп станет вашим». Один за другим они открывали тайны склепа, но когда скрипнула последняя дверь, в воздухе раздался зловещий смех Хранителя. «Будьте осторожны: не все, кто входит, выходят прежними».

В таске дано только один файл:
- `server.py` : питоновский скрипт, который работает когда мы подключаемся к инстансу по ip:port, просто STDIN/STDOUT по сети

## Анализ исходного кода

```python
rounds = 5
e = 65537

for i in range(rounds):
    print('*'*10, f'Round {i+1}/{rounds}', '*'*10)

    p = getPrime(110)
    q = getPrime(110)
    n = p * q
    pubkey = RSA.construct((n, e)).exportKey()
    print(f'\nCan you crack this RSA public key?\n{pubkey.decode()}\n')

    assert isPrime(_p := int(input('enter p = '))), exit()
    assert isPrime(_q := int(input('enter q = '))), exit()

    if n != _p * _q:
        print('wrong! bye...')
        exit()

    print()

print(open('flag.txt').read())
```

Чтобы получить флаг, нам нужно успешно пройти 5 раундов. На каждом раунде нам даётся открытый ключ RSA, и задача это предоставить простые множители $p, q$ модуля $N$. Значение открытой экспоненты $e$ фиксировано и равно стандартному $65537$.

## Решение

Безопасность криптосистемы RSA полностью основана на сложности задачи факторизации целых чисел. Cуть задачи в следующем:

*Даны  $p = 10412581$ и $q = 15559549$, тогда можно легко и очень быстро вычислить  $10412581 \cdot 15559549 = 162015064285969 = N$. Хотя зная только $N = 162015064285969$, гораздо сложнее определить, какие два числа p и q были перемножены.*

Для значительно больших чисел современным компьютерам это становится невыполнимой задачей.

В этом задании размер каждой из простых $110$ бит, поэтому их произведение содержит $110 + 110 = 220$ бит. Модуль RSA размером $220$ бит небезопасен для криптографии, современные компьютеры могут очень быстро его факторизовать. Существует множество библиотек и инструментов для факторизации целых чисел, но в CTF чаще всего используют SageMath, поэтому будем его применять. Пример на вымышленных числах:

```python
sage: p = random_prime(2^110)
sage: q = random_prime(2^110)
sage: n = p * q
sage: %time factor(n)
CPU times: user 6.46 s, sys: 7.96 ms, total: 6.47 s
Wall time: 6.5 s
356113038545854871808945806883821 * 1270756668530534635604669619715399
sage: p
356113038545854871808945806883821
sage: q
1270756668530534635604669619715399
```

Это заняло только 6.5 секунд для SageMath на факторизацию $n$. Суть таска:
Подключиться к серверу, получить модули каждого раунда, факторизовать их и вернуть простые обратно серверу.
Хотя публичный ключ RSA в формате PEM

```python
pem_pubkey = RSA.construct((n, e)).exportKey()
print(f'\nCan you crack this RSA public key?\n{pubkey.decode()}\n')
```

То есть в виде
```
-----BEGIN PUBLIC KEY-----
MDcwDQYJKoZIhvcNAQEBBQADJgAwIwIcBEwL/SBkcv+AmVwzDWtY80vQ4ALwjtUt
RgeXuwIDAQAB
-----END PUBLIC KEY-----
```

Может показаться странным, почему для передачи открытых ключей RSA используется такой формат. RSA широко применяется в протоколах типа TLS, поэтому формат ключа должен быть согласован, чтобы при парсинге параметров не возникало ошибок. Как правило, приложения используют формат PEM. Если бы формат не был стандартизован, можно было бы спорить, какой из следующих вариантов использовать:
- `(n = value_of_n, e = value_of_e)`
- `(n=value_of_n,e=value_of_e)`
- `[n=value_of_n, e=value_of_e]`
и так далее.

Чтобы прочитать параметры RSA из ключа PEM можно найти и использовать обратную `exportKey` , то есть `importKey`.
```python
>>> from Crypto.PublicKey import RSA
>>> n = 452533018482816403250499886919603981486991592917670642633077659579
>>> e = 65537
>>> pem_pubkey = RSA.construct((n, e)).exportKey()
>>> pem_pubkey
b'-----BEGIN PUBLIC KEY-----\nMDcwDQYJKoZIhvcNAQEBBQADJgAwIwIcBEwL/SBkcv+AmVwzDWtY80vQ4ALwjtUt\nRgeXuwIDAQAB\n-----END PUBLIC KEY-----'
>>> key = RSA.importKey(pem_pubkey)
>>> key
RsaKey(n=452533018482816403250499886919603981486991592917670642633077659579, e=65537)
```

Теперь мы можем написать функцию, которая получает и факторизует пять модулей.
```python
from pwn import *
from Crypto.PublicKey import RSA
from sage.all import *

def get_flag():
    e = 65537
    for _ in range(5):
        io.recvuntil(b'key?\n')
        key = RSA.importKey(io.recvuntil(b'-----END PUBLIC KEY-----\n'))
        n, e = key.n, key.e
        p, q = list(factor(n))
        io.sendlineafter(b'p = ', str(p[0]).encode())
        io.sendlineafter(b'q = ', str(q[0]).encode())
        io.recvline()
    flag = io.recvline().strip().decode()
    return flag
```

Получение флага:
```python
def pwn():
  	flag = get_flag()
    print(flag)

if __name__ == '__main__':
    if args.REMOTE:
        host_port = sys.argv[1].split(':')
        HOST = host_port[0]
        PORT = host_port[1]
        io = remote(HOST, PORT, level='error')
    else:
        import os
        os.chdir('../challenge')
        io = process(['python3', 'server.py'], level='error')

    pwn()
```