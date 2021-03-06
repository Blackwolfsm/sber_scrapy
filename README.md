# sber_scrapy
Тестовое задание для Сбер реализованное на библиотеке Scrapy

### Паук собирает следующую информацию по каждой новостройке:

- Адрес
- Статус
- Количество квартир
- Застройщик
- ID Новостройки на сайте наш.дом.рф
### Если статус здания - "строится", то так же дополнительные поля:
- Распроданность квартир
- Средняя цена за 1м2
- Кадастровый номер земельного участка

Если обнаружены пустые поля, то их значения будут 'NULL'. 
В записях где статус 'Сдан' или 'Проблемный' у дополнительных полей значения будут 'NULL'.

## Описание
После выполнения парсера в файле 'buildings.csv' будут все новостройки на текущий момент.

## Логирование
Сообщения об ошибке логируются в файл 'errors.log'.

## Требования
Python v3.8+. Для запуска создайте виртуальное окружение и установаить зависимости с помощью команд ниже:
```
$ python -m venv 'название окружения'
$ pip install -r requirements.txt
```
## Запуск
Находясь в директории с файлом выполнить команду:
```
$ scrapy crawl NewBuildings
```

## Дополнительная информация
В случае недоступности страниц, парсер настроен на 5 повторных попыток подключения.
