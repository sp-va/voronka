# Воронка-вебинар

Юзербот для отправки сообщений пользователям

## Описание

https://docs.google.com/spreadsheets/d/1PevrBGZTGi0glnXj-iGJr3MlZVOExT8oiNmk3Cvd3ac/edit#gid=0

## Установка

1. Клонировать репозиторий:

```bash
git clone https://github.com/ваш_логин/ваш_репозиторий.git
```

2. Перейти в директорию проекта:
```bash
cd voronka
```
3. Установить зависимости:
```bash
pip install -r requirements.txt
```

## Использование:
1. Сначала нужно создать файл .env (по примеру example.env), в который нужно внести данные для подключения к базе данных postgresql и к TelegramAPI
2. Запуск юзербота:
```bash
python bot/bot_funcs.py
```
