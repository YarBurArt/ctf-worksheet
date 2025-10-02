# Contributing to CTF Worksheet

## Цель проекта
Репозиторий для сбора и изучения writeups CTF-challengers.

## Правила контрибуции

### Формат writeup
- Markdown (.md)
- Должен ключать:
  - Название челленджа
  - Категория
  - Источник
  - Автор оригинала

### Процесс вклада
1. Форкнуть репозиторий
```bash
git clone https://github.com/YarBurArt/ctf-worksheet.git
cd ctf-worksheet
git checkout -b add/challenge-writeup
```

2. Добавить writeup
```bash
git add ctf/web/your-challenge/README.md
git commit -m "add/web-exploitation-sqlinjection-writeup"
git push origin add/challenge-writeup
```

3. Создать Pull Request на GitHub
   - Внятное описание кратко
   - Ссылка на источник 

## Правила коммитов
- Осмысленные названия
- Указывать название таска
- Пример: 
  - Хорошо: `add/web-exploit-sqlinjection-writeup`
  - Плохо: `update`

## Этика
- Уважать авторов
- Делиться знаниями
- Помогать изучать кибербезопасность

## Вопросы?
Открывайте issues.
