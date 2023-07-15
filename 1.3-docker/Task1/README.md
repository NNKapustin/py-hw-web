## Запуск
### Создаем образ
<code> docker build -t my-nginx . </code>

### Запускаем контейнер
<code>docker run -p 8080:80 my-nginx</code>

### Переходим по url 
<a href="http://localhost:8080"> localhost:8080 </a>