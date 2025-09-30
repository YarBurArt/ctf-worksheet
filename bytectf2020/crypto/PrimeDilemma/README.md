## Prime Dilemma

Основная идея ипользовать RSA Encryption с известными значениями факторизации.

#### Step-1:
После загрузки `primedilemma.txt`, автор получил это:

```
q > p
(p^3)*(q**2) = 731741085649420699672720315154308733768
e = 6969
encrypted text : 12541396840306196572
```

#### Step-2:
Если вы понимаете алгоритм [RSA](https://ru.wikipedia.org/wiki/RSA) его функциональность, техники и варианты атак через известные переменные.

Следовательно переменные будут:
p<sup>3</sup>.q<sup>2</sup> = 731741085649420699672720315154308733768

`c` это шифротекст с десятичном представлении. 
c = 12541396840306196572

`e` это открытая (публичная) экспонента шифра RSA.
e = 6969

#### Step-3:
Можно попытаться факторизовать число для получения простых `p` & `q` через [FactorDB](http://factordb.com/) .

<img src="https://raw.githubusercontent.com/rishitsaiya/ByteCTF-Writeups/refs/heads/master/crypto/Prime%20Dilemma/Factor.png">

#### Step-4:
Тогда мы получаем `p = 2` & `q = 9563871376496945939`. Тогда `n = p.q`, 
`n = 19127742752993891878`

Автор из pr0ctf написал скрипт [`prime.py`](https://github.com/rishitsaiya/ByteCTF-Writeups/blob/master/crypto/Prime%20Dilemma/prime.py) для получения флага.

```py
from Crypto.Util.number import inverse
import binascii

e = 6969
c = 12541396840306196572
n = 19127742752993891878

# из factordb

p = 2
q = 9563871376496945939

phi = (p-1) * (q-1)

d = inverse(e,phi)
m = pow(c,d,n)

hex_str = hex(m)[2:] # срез по '0x'
print(binascii.unhexlify(hex_str))
```
```math
\begin{align*}
\phi & = (p - 1) \cdot (q - 1) \\
d & = e^{-1} \mod \phi \\
m & = c^d \mod n \\
\end{align*}
```

#### Step-5:
Запуск как `python3 prime.py`, и мы получим:

```bash
b'tuchainz'
```

#### Step-6:
Итоговый флаг будет:
`flag{tuchainz}`
