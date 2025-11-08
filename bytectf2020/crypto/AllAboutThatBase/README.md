## All About That Base
Основная идея получения флага это base подсказка.
#### шаг - 1:
После загрузки `allabouthatbase.png`, это дает представление о base.

<img src="https://github.com/rishitsaiya/ByteCTF-Writeups/blob/master/crypto/All%20About%20That%20Base/allabouthatbase.png?raw=true">

Шифротекст в `ciphertext.png`, его содержание:

<img src="https://github.com/rishitsaiya/ByteCTF-Writeups/blob/master/crypto/All%20About%20That%20Base/ciphertext.png?raw=true">

#### шаг - 2:
В файле `allabouthatbase.png` дизайн похож на часы, тогда сопоставим их на 1-13 и получим типа Base13, у нее такая последовательность: `0123456789ABC`

#### шаг - 3:
Если мы декодируем шифротекст мы получим:
`7B 84 76 7C 96 3A 86 8C 3C 8A 78 7A 45 8C 58 39 86 98`

#### Step-4:
Через эту утилиту декодируем обратно в ASCII 
https://onlineasciitools.com/convert-arbitrary-base-to-ascii

<img src="https://github.com/rishitsaiya/ByteCTF-Writeups/blob/master/crypto/All%20About%20That%20Base/Flag.png">

#### Step-5:
Итоговый флаг будет:
`flag{1nt3rce9tI0n}`
