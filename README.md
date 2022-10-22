# RubTengeBot

### Описание:

https://t.me/RubTengeBot

Телеграм бот учета расходов в Республике Казахстан. Переводит национальную валюту тенге в русские рубли и ведет учет расходов по категориям и по 
конкретным пользователям записывая информацию в базу данных Postgres. Конвертация валюты происходит по текущему курсу тенге к российскому 
рублю, который так же можно посмотреть отдельно. Имеется возможность вывода статистики расходов за текущий день, неделю, месяц. Плюс несколько
лайфхаков и полезных ссылок по проживанию в Республике Казахстан, эта информация будет пополняться.

### Используемые технологии:

- Python 3.10
- Aiogram
- Aiohttp
- Asyncio
- Pytest
- SQLAlchemy
- Postgres
- Docker

### Запуск бота

**Для запуска необходимо настроить переменные окружения в файле .env**

**DEBUG** - Режим отладки

**TELEGRAM_TOKEN** - Токен телеграм бота

**LOGGING_PATH** - Путь к логам

**DB_URL** - url базы данных

**EXCHANGE_RATE_URL** - url api курса валют



`pip install -r requirements.txt`

`python run.py`
