# Запуск
## Устанавливаем зависимости
<code>pip install -r requirements.txt</code>

## Запускаем redis через docker-compose
<code>docker-compose up</code>

## Запускаем celery
<code>celery -A app.celery worker</code>

## Запускаем приложение
<code>python app.py</code>

## Отправляем запросы - пример запросов [request_example.py](request_example.py)