## Функциональность

Список API, которые должны быть покрыты в этом задании:

- Создать отель поставщика
- Объединить 1 и более отелей поставщиков в один мета-отель
- Получить список мета-отелей и входящих в них отелей
- Перепривязать отель к другому мета-отелю
- Получить историю привязки отеля (к каким мета-отелям в какой момент времени он был привязан)

## Требования и ограничения

- Авторизация/аутентификация не нужна
- Отель может быть привязан только к одному мета-отелю в один момент времени
- В мета-отеле должен быть минимум один отель
- Отель можно отвязать от мета-отеля и привязать к другому

## Пример данных

Мета-отель:

```
id: mercure_pattaya

id: windways
```

Отель:
```
id: 1
name: Mercure Pattaya
supplier_id: AAA

id: 2
name: Mercure Pattaya
supplier_id: BBB

id: 3
name: Windways Hotel
supplier_id: AAA
```

## Оценка

Цель этого тестового задания - увидеть ваш лучший/самый идиоматичный код на Python/Django. 

Мы ожидаем увидеть:

- Документацию API
- README с описанием как запустить проект, запустить тесты и т.д
- Чистую архитектуру, с корректной связанностью кода (decoupling), complexity isolation
- Аккуратный, понятный, поддерживаемый код, с наличием комментариев к коду (если нужны)
- Код на публичной платформе (github/gitlab/bitbucket)
- Отсутствие "мертвого" кода (т.е пустые модули, неиспользуемые функции и параметры и т.д)
- Тесты (доказательство работоспособности кода)
- Реализация на Django + любой REST или RPC фреймворк, с которым вам комфортно
- PostgreSQL в качестве БД (помните про блокировки, транзакции, race conditions)
- Сервис корректно работает, если запущен в нескольких экземплярах (инстансах)
- Проект должен запускаться через docker-compose

### Установка проекта

```code
git clone https://github.com/voidCaloneian/metaHotel.git
cd metaHotel
docker-compose build
docker-compose run django sh -c "python ./src/manage.py makemigrations && python ./src/manage.py migrate"
```

### Запуск проекта
```code
docker-compose up -d
```

### Запуск тестов API
```code
docker-compose exec django sh -c "python ./src/manage.py test api"
```

### Работа с API через запросы
- Создать отель поставщика
  - Отправить **POST** запрос на ```http://127.0.0.1:8000/api/hotel/``` 
    - Пример боди запроса
      ```code
      {
        "name": "имя_отеля",
        "meta_hotel": "имя_уже_существующего_мета_отеля"  
      }
      ```
      - meta_hotel можно оставить пустым, либо вовсе не писать, если вы не хотите привязывать отель
- Объединить 1 и более отелей поставщиков в один мета-отель
  - Отправить **PUT** запрос на ```http://127.0.0.1:8000/api/bind/```
    - Пример боди запроса 
      ```code
      {
        "hotels_pks": "1,4,21,314,15",
        "meta_hotel": "имя_мета_отеля" 
      }
      ```
      - hotels_pks - ID отелей, которые нужно привязать (перечислять через запятую)
      - meta_hotel - Имя отеля, к которому нужно привязать все отели. Если мета отеля не существует, создастся новый с этим именем

- Получить список мета-отелей и входящих в них отелей
  - Отправить **GET** запрос на ```http://127.0.0.1:8000/api/metahotel/```

- Перепривязать отель к другому мета-отелю 
  - Отправить **PATCH** запрос на ```http://127.0.0.1:8000/api/hotel/id_отеля/```
    - Пример боди запроса 
      ```code
      {
          "meta_hotel": "имя_уже_существующего_мета_отеля"
      }
      ```
- Получить историю привязки отеля (к каким мета-отелям в какой момент времени он был привязан)
  - Отправить **GET** запрос на ```http://127.0.0.1:8000/api/hotel/id_отеля/```
