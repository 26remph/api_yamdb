# Документация к API проекта YAMDB (v1)

### Описание
Проект YaMDb собирает отзывы пользователей на различные произведения;

### Как запустить проект:

- Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/26remph/api_yamdb.git
cd api_yamdb
``` 

- Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
source env/bin/activate
```

- Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

- Выполнить миграции:
```
python3 manage.py migrate
```

- Запустить проект:
```
python3 manage.py runserver
```
Ознакомиться с документацией по адресу.
[http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)



### Алгоритм получения токена:
#### 1. Получить код подтвержения.
в теле передать JSON
{
  "username": "имя_пользователя",
  "email": "адрес эл. почты"
}
POST-запрос на эндпоинт:
```
http://127.0.0.1:8000/api/v1/auth/signup/
```


в папке sent_emails найти письмо и скопировать полученный код подтверждения.

#### 2. Получить токен.
в теле передать JSON
{
  "username": "имя_пользователя",
  "confirmation_code": "код_подтвержения"
}
POST-запрос на эндпоинт:
```
http://127.0.0.1:8000/api/v1/auth/token/
```
Токен использовать для авторизации

### Некоторые примеры запросов к API.
Доступные энд-поинты:
GET-запросы
```
/api/v1/users/
```
```
/api/v1/titles/
```
```
/api/v1/categories/
```
```
/api/v1/genres/
```
```
/api/v1/titles/{title_id}/reviews/
```
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
### Авторы
_Вадим Барсуков, python-developer_  
_Денис Мурашов, python-developer_
_Денис Мурашов, python-developer_
_Юра Ананьин, python-developer_
