## Запуск
### Создаем образ
<code> docker build . --tag=my_django </code>

### Запускаем контейнер
<code>docker run -p 8000:8000 my_django</code>

### Отправляем запросы
Файл с примерами запросов [requests-examples.http](requests-examples.http)</br>
Отправляем запросы с помощью VS Code REST Client или Postman
