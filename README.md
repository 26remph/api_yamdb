![](./api_yamdb/static/header.png)
#Документация к API проекта YAMDB (v1)
Проект YaMDb собирает отзывы пользователей на различные произведения;
___
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/26remph/api_final_yatube)
![GitHub repo size](https://img.shields.io/github/repo-size/26remph/api_yamdb)
![GitHub](https://img.shields.io/github/license/26remph/api_yamdb)
![pythonversion](https://img.shields.io/badge/python-%3E%3D3.7-blue)


## Оглавление
0. [Как запустить проект](#как-запустить-проект)
1. [...](#cоздание-пользователей)
2. [...](#документация-по-api)
3. [...](#поиск-в-базе-данных)
4. [...](#Демонстрационная-версия-API)
5. [Об авторе](#об-авторе)


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
#
_Вадим Барсуков, python-developer_  
_Денис Мурашов, python-developer_
_Юра Ананьин, python-developer_
#

___
<p>
    <span>© 2022, Contributors on git: 26Remph, viplod, okazivaetsya. ツ </span>
</p>