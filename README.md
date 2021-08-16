# Тестовое задание Pets

## Перед запуском

### Переменные окружения

__Для обычного запуска__

* DEBUG - bool, отладочный режим, по умолчанию отключен
* ALLOWED_HOSTS - список доменов, для которых может работать приложение (перечисление через ";")
* SECRET_KEY - серверный секретный ключ (используется, например, для формирования хешей)
* USE_S3_STORAGE - bool, использовать Amazon Simple Storage Service для хранения статических и медиа файлов
* AWS_ACCESS_KEY_ID - ID для доступа к Amazon S3
* AWS_S3_ENDPOINT_URL - URL для доступа к Amazon S3
* API_KEY - эталонный API ключ для доступа к сервису (сравнивается с переданным в заголовке X-API-KEY)
* DATABASE_URL - данные для доступа к базе данных в формате *engine://user:password@host:port/db_name*

__Для запуска через Docker__

* DEBUG - аналогично
* ALLOWED_HOSTS - аналогично
* USE_S3_STORAGE - аналогично
* AWS_ACCESS_KEY_ID - аналогично
* AWS_S3_ENDPOINT_URL - аналогично

*Примечание:* примеры переменных окружения можно найти в файлах **.example.env*, однако сами файлы с переменными окружения не должны содержать инфикса ".example"

### Секреты:

При запуске приложения через docker-compose в папке *secrets* должны лежать файлы, содержащие секретную информацию:

* aws_secret_access_key.secret - секретный ключ доступа к Amazon S3 хранилищу (*если используется хранилище*)
* api_key.secret - эталонный API ключ для доступа к сервису
* db_password.secret - пароль для доступа к базе данных
* secret_key.secret - серверный секретный ключ (используется, например, для формирования хешей)

*Примечание:* примеры файлов содержатся в папке *secrets* и имеют суффикс **.example.secret* 

## Запуск

### Shell

`python manage.py runserver --settings=settings.default HOST:PORT`

Для запуска в папке *environments* должен лежать файл *default.env* с переменными окружения или же можно использовать другие способы передачи переменных окружения в программу (например, переменные окружения текущей сессии)

### Docker Compose

`docker-compose up`

## Описание

REST API для ведения учёта питомцев (собак и кошек).

Для использования необходимо в каждом запросе передавать HTTP заголовок X-API-KEY

### Endpoints:

* POST /pets

request body
```javascript
{
	"name": "Good Boy",
    "age": 3,
    "type": "dog"
}
```
response body
```javascript
{
	"id" "58df3879-d65a-421d-9cb0-3c55e2cac86c",
    "name": "Good Boy",
    "age": 3,
    "type": "dog",
    "photos" [],
    "created_at": "2021-08-15:12:55:46"
}
```

* POST /pets/{id}/photo
form data
*file: binary*

response body

```javascript
{
	"id": "c502603a-2fb7-4b4d-8bde-2eb9e0b7f62a",
    "url": "https://dipcoy.fra1.digitaloceanspaces.com/pets/mediafiles/1_gCSYcFK.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=4CVAOEWXAGFF2U74SM7S%2F20210816%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20210816T081242Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=cda59e0d77612d455e5f6171166ee70f96563589bfbdba4f2c14e1f61837ba60"
}
```

* GET /pets

  query params

  *limit: integer (optional, default=20)*

  *offset: integer (optional, default=0)*

  *has_photos: boolean (optional)*
  
  *has_photos* = __true__ - записи с фотографиями
  
  *has_photos* = __false__ - записи без фотографий
  
  *не указано has_photos* - все записи
  
response body
```javascript
{
	"count": 2,
    "items": [
        {
          "id" "58df3879-d65a-421d-9cb0-3c55e2cac86c",
          "name": "Good Boy",
          "age": 3,
          "type": "dog",
          "photos" [],
          "created_at": "2021-08-15:12:55:46"
      	},
        {
          "id" "76ed4423-c56e-8dae-09ab-4b5a286c36eaa",
          "name": "Mrrr",
          "age": 1,
          "type": "cat",
          "photos" [
          	{
          		"id": "c502603a-2fb7-4b4d-8bde-2eb9e0b7f62a",
                "url": "https://dipcoy.fra1.digitaloceanspaces.com/pets/mediafiles/1_gCSYcFK.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=4CVAOEWXAGFF2U74SM7S%2F20210816%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20210816T081242Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=cda59e0d77612d455e5f6171166ee70f96563589bfbdba4f2c14e1f61837ba60"
          	}
          ],
          "created_at": "2021-08-15:12:59:03"
      	}
    ]
}
```

* DELETE /pets

request body
```javascript
{
    "ids": [
        "3szbdv",
        "c502603a-2fb7-4b4d-8bde-2eb9e0b7f62a",
        "33bce70a-ffd6-4d86-a23c-53bf1211aafb"
    ]
}
```

response body
```javascript
{
    "deleted": 1,
    "errors": [
        {
            "id": "c502603a-2fb7-4b4d-8bde-2eb9e0b7f62a",
            "error": "Pet with the matching ID was not found."
        },
        {
            "id": "3szbdv",
            "error": "The matching ID is not a valid UUID."
        }
    ]
}
```

### CLI

`python manage.py --settings=settings.default listpets`

*params*:

* optional
	`--has_photos=[true, false]`
    
    Если не указан - выводит всех питомцев
    
    Если *true* - только тех, у которых есть фото
    
    Если *false* - только тех, у которых нет фото

*output*
```javascript
{
    "pets": [
        {
            "id": "976f5e96-6dd5-459e-8a9c-a49625b7aec4",
            "name": "Good Boy",
            "age": 1,
            "type": "dog",
            "photos": [
                "https://dipcoy.fra1.digitaloceanspaces.com/pets/mediafiles/1_bSGN29V.jpg?X-Amz-Algorithm=AWS4-H
MAC-SHA256&X-Amz-Credential=4CVAOEWXAGFF2U74SM7S%2F20210816%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20210816T
084137Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=2e738e258c6b9ef1ab37e8fed52ed9d14dc4e3adcc67
667f8539e0d2935215cd"
            ],
            "created_at": "2021-08-16:08:41:09"
        },
        {
            "id": "3ed1e732-74ac-410f-982b-1438c1845d73",
            "name": "FileStorage",
            "age": 3,
            "type": "dog",
            "photos": [
                "https://dipcoy.fra1.digitaloceanspaces.com/pets/mediafiles/1_bGw0j96.jpg?X-Amz-Algorithm=AWS4-H
MAC-SHA256&X-Amz-Credential=4CVAOEWXAGFF2U74SM7S%2F20210816%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20210816T
084138Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=b04edb01684e4bedce3d3fc562e6046ff32018511eb2
edf5960b69c5247a4ea4"
            ],
            "created_at": "2021-08-14:20:13:38"
        }
    ]
}
```