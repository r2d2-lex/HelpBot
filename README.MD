# HelpBot

```
Install:
cd /scripts/
git clone https://github.com/r2d2-lex/HelpBot.git
cd /scripts/HelpBot/
cp service/helpbot.service /etc/systemd/system/
apt-get install python3-venv
python3 -m venv venv
source ./venv/bin/activate
python -m pip install --upgrade pip
pip install -r reqirements.txt

create database help_bot;
CREATE USER help_bot WITH PASSWORD 'help_bot';
GRANT ALL PRIVILEGES ON DATABASE "help_bot" to help_bot;

apt-get install redis
```

Docker:
```
Создание, запуск:
# docker build -t help_bot .
# docker run help_bot
```

Создание через docker-compose:
```
# docker-compose build bot
# docker-compose run bot
# docker-compose up --build bot
```

Запуск Celery:
```
celery -A tasks worker -B --loglevel=info
```
