# Получение заявки с сайта и создание/обновление на в Битрикс24

Написать скрипт, который будет получать заявку с сайта в формате JSON и либо создавать ее либо обновлять.

## Возможные варианты:

* Контакта нет в Bitrix24 (далее b24) → создаем и контакт и сделку и связываем их между собой
* Контакт есть в b24 → Проверяем есть ли уже такая заявка по delivery_code
* Заявки нет в b24 → Создаем заявку и связываем ее с контактом
* Заявка есть в b24 → Сравниваем заявку из b24 с ключевыми полями (delivery_adress, delivery_date, products) из пришедшей заявки
* Поля совпадают → Ничего не делаем
* Поля отличаются → Обновляем заявку
* Если в алгоритме что-то не учтено и вы это обнаружите - это +1 к вам в карму.
 
## Входной JSON:
```json
1{
2    "title": "title",
3    "description": "Some description",
4    "client": {
5        "name": "Jon",
6        "surname": "Karter",
7        "phone": "+77777777777",
8        "adress": "st. Mira, 287, Moscow"
9    },
10    "products": ["Candy", "Carrot", "Potato"],
11    "delivery_adress": "st. Mira, 211, Ekaterinburg",
12    "delivery_date": "2021-01-01:16:00",
13    "delivery_code": "#232nkF3fAdn"
14}
15
```

## Выходные данные:

* crm.deal - Сделка Bitrix24
* crm.contact - Контакт Bitrix24

## Условия:
1. не должно быть дубликатов контакта и сделки
2. контакт должен быть привязан к сделке
3. заявки с одинаковым delivery_code должны объединяться, если это требуется
4. В приоритете те данные, которые пришли позже, т.е. если в первом запросе delivery_adress был “ул. Мира 222“, а в следующем идентичном запросе “ул. Мира 212“ - то в сделку попадает второй адрес (ул. Мира 212)
5. Информация о клиенте - не изменяется, может измениться только- delivery_adress, delivery_date, products
6. Контакт ищем по номеру телефона.


## Использование Docker

### Установка Docker.
Установите Docker, используя инструкции с официального сайта:
* для [Windows и MacOS](https://www.docker.com/products/docker-desktop)
* для [Linux](https://docs.docker.com/engine/install/ubuntu/). Отдельно потребуется установть [Docker Compose](https://docs.docker.com/compose/install/)

* скачайте проект к себе на компьютер 
```bash
    git clone https://github.com/ivbbest/create_task_bitrix24.git
```
* Установите Docker 
```bash
    https://www.docker.com/get-started
```

## Настройка виртуального окружения 

* установите виртуальное окружение
```bash
    python -m venv .venv
```
* Активируйте виртуальное окружение:

### Windows
```bash
    source .venv/Scripts/activate
```

### Linux
```bash
    source .venv/bin/activate
```


* Создайте Docker образ
```bash
    docker build -t test .
```

* Запустите контейнер из образа
```bash
    docker run --name test -it test
```

* В новом терминале выполните команду:
```bash
    docker exec -it test bash
```
* это запустит терминал внутри контейнера

* Запустите  скрипт
```bash
    python create_app_bitrix24.py
```