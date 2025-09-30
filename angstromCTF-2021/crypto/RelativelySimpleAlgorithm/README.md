## angstromCTF-2021



## Задача 3(Relatively Simple Algorithm)

Подготовлено: `lamchcl`

Автор: `lamchcl`

Уровень сложности: Средний


## Описание

[RSA](./rsa.txt) снова наносит удар! [Источник](./rsa.py)

## Подсказка

[https://ru.wikipedia.org/wiki/RSA_(cryptosystem)]
(https://ru.wikipedia.org/wiki/RSA_(cryptosystem))

## Решение

RSA достаточно хорошо описан в статье в Википедии.

Я использовал этот java-код ( *взят* из [здесь](https://crypto.stackexchange.com/questions/19915/rsa-decryption-given-n-e-and-phin)):


<details>

<summary>Code</summary>

```java
import java.math.BigInteger; //для работы с большими целыми (криптография)
import java.util.ArrayList; //для хранения последовательности байт (значений 0–255)
import java.util.Scanner; //для чтения ввода пользователя

public class RSA {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in); //cканер для чтения строк из консоли
        BigInteger N,phiN,e,d,m,c; //объявление чисел

        // cipertext c, plaintext m

        System.out.println("Insert N"); //ввод модуля

        N = new BigInteger (sc.nextLine()); //чтение

        System.out.println("Input e");//ввод модуля

        e = new BigInteger (sc.nextLine()); //чтение

        System.out.println("Input c"); //ввод модуля

        c = new BigInteger (sc.nextLine()); //чтение

        System.out.println("Input phi"); //ввод модуля

        phiN = new BigInteger (sc.nextLine()); //чтение

        sc.close(); //закрывает сканер

        d = e.modInverse(phiN); //вычисление 
        m = c.modPow(d, N); //дешифрование

        System.out.println("d = "+d);           
        System.out.println("m = "+m);

        System.out.println("m in base 256 = "+base256(m)); //Вывод результата функции base256 
        System.out.println("Convert with ASCII \n"+ Encode256(base256(m))); //Преобразует полученные байты в строку через кодирование в char.

    }
    static ArrayList<BigInteger> base256 (BigInteger M) {
        BigInteger base = new BigInteger("256");
        ArrayList<BigInteger> message256 = new ArrayList<BigInteger>();
        BigInteger sisa=M; //временная переменная для деления
        BigInteger k; //временная перепменная
        double z = Double.parseDouble(M.toString()); //Преобразует M в double чтобы взять логарифм
        double p = Math.floor(Math.log(z)/Math.log(256)); //Вычисляет индекс старшего байта;
        int r = (int) p;
        for (int j=0;j<=r;j++){
            k=sisa.mod(base);
            sisa=sisa.divide(base);
            message256.add(k);
        }
        return message256;
    }

    static String Encode256 (ArrayList<BigInteger> ascii) {
        String ascii256=""; //Накопитель результирующей строки
        int g;
        for (int i=0;i<ascii.size();i++) {
            g = Integer.parseInt(""+ascii.get(i)); //получение int
            ascii256=ascii256+( (char) g ); //Преобразует число 0..255 в символ Java 
        }
        return ascii256;
    }
}
```

</details>

В RSA: 

$$
\phi\ = (p - 1)(q - 1)
$$

Поэтому я использовал [большое число calculator](https://www.calculator.net/big-number-calculator.html?cx=11556895667671057477200219387242513875610589005594481832449286005570409920461121505578566298354611080750154513073654150580136639937876904687126793459819368&cy=9789731420840260962289569924638041579833494812169162102854947552459243338614590024836083625245719375467053459789947717068410632082598060778090631475194566&cp=20&co=multiple) для вычисления значения phi. Затем я запустил приведенный выше код, и он выдал результат: `}gnitupmoc_mutnauq_litnu_tsael_ta_llew_doog_llits_tub_dlo{ftca`

Я изменил в Python

```python
print("}gnitupmoc_mutnauq_litnu_tsael_ta_llew_doog_llits_tub_dlo{ftca"[::-1])
```
После чего получил флаг

## Flag

actf{old_but_still_good_well_at_least_until_quantum_computing}