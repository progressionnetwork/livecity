[![build & deploy](https://github.com/gg-goodgenius/livecity/actions/workflows/deploy.yml/badge.svg)](https://github.com/gg-goodgenius/livecity/actions/workflows/deploy.yml)

# Проект «Живой город»

## ЛИДЕРЫ ЦИФРОВОЙ ТРАНСФОРМАЦИИ 2022
## Задача: Создать сервис формирования задач для москвичей по контролю работ подрядчиков в сфере городского благоустройства 
### Команда Good Genius \ 2022.

### Суть проекта:
Платформа «Живой город» решает проблемы оптимизации работы со сметами, проверки правильности заполненной сметы, проверку
стоимости работ в смете, категоризацию разделов в смете, что делает наш продукт уникальным а рынке удобной работы со
сметами и оптимизации расчётов, который не имеет аналогов.
С платформой «Живой город», составление сметы будет занимать в два раза меньше времени, благодаря простоте платформы

### Описание алгоритма получения результата:
Получив загруженный пользователем файл(ы) сметы, парсер первым делом проверяет формат сметы, выделяется шапка сметы из нее выделяются названия и положение колонок. После этого колонки проверяются на соответствие СН или ТСН структур. 
Далее определяются границы разделов, подразделов, и каждой отдельной записи. После этого каждая отдельная позиция преобразовывается в словарь в соответствии с именами колонок. 
Все словари складываются по разделам и подразделам. После этого обрабатывается итоговая сумма сметы и выделяются сущности из текста над шапкой. Алгоритм адаптивен и подстраивается под извлечение необходимых полей и их групп, формируя
структуру обработанной сметы.

### Сложности при обработке данных:
- Мультистраничные файлы XLSX (определение наличия сметы на странице)
- Шапка как и другие объекты сметы не имеют точного расположения
- Присутствие объединенных колонок в таблице
- Наличие формул с ссылками на ячейки из других вкладок
- Разнородное название для вкладок с ведомостями в сметах
- Отсутствие вкладок для расчета стоимости ресурсов в некоторых сметах
- Множество единиц измерений
- Наличие позиций с дробным номером (необходимо объединить к родительской позиции)
- В некоторых листах смет присутствуют несколько локальных смет

## Dashboard:
Кабинет пользователя.
![alt text](https://github.com/gg-goodgenius/livecity/blob/main/screen.png?raw=true)

## Возможности сервиса:
- Использование микросервисной архитектуры
- Подготовлен API для последующего внедрения ЕАИСТ
- Использование доп. классификаторов
- Выделения адреса и сопостовление с ФИАС
- Использование языковых и статистических моделей для вывления ключевых позиций
- Многопоточная, быстрая обработка смет
- Устойчивость к изменениям формата сметы

## Описание алгоритма получения результата:
Получив загруженный пользователем файл(ы) сметы, парсер первым делом проверяет
формат сметы, выделяется шапка сметы из нее выделяются названия и положение
колонок. После этого колонки проверяются на соответствие СН или ТСН структур. 
Далее определяются границы разделов, подразделов, и каждой отдельной записи. 
После этого каждая отдельная позиция преобразовывается в словарь в соответствии 
с именами колонок. Все словари складываются по разделам и подразделам. 
После этого обрабатывается итоговая сумма сметы и выделяются сущности из текста над шапкой.
Алгоритм подстраивается под извлечение необходимых полей и их групп, формируя
структуру обработанной сметы.

## API сервис:
Для работы с API сервисом можно использовать логины указанные выше. 
Вся документация по работе с сервисом указана в swagger по адресу:
https://api.livecity.goodgenius.ru/docs/

Авторизация в сервисе используется с заголовком Authorization: Token <ваш токен>.
Установка на собственных ресурсах
Для этого необходимо иметь устновленый docker и/или docker-compose выполнить
следующие команды:

- git clone https://github.com/gg-goodgenius/livecity
- cd livecity
- docker compose –f docker-compose.local.yml build —no-cache —pull
- docker compose –f docker-compose.local.yml up –d

Также для разворачивания только API сервиса можно использовать файл docker-compose.back.yml

## Логины и пароли
Для работы с сервисом созданы демо пользователи (для полноценной демонстрации
лучше использовать пользователя superadmin@livecity.gg):
- Логин: superadmin@livecity.gg
- Пароль: password
- Логин: admin@livecity.gg
- Пароль: password
- Логин: user@livecity.gg
- Пароль: password

## Полезные ссылки
- Веб сервис: https://livecity.goodgenius.ru/
- Административная панель: https://api.livecity.goodgenius.ru/admin/
- API сервис: https://api.livecity.goodgenius.ru/
- Документация API сервиса: https://api.livecity.goodgenius.ru/docs/
- Github: https://github.com/gg-goodgenius/livecity

## Стек используемых технологий и библиотек:
- Python/Pandas/regex
- Levenshtein/TfidfVectorizer/NLTK
- FastText/Pymorphy
- Sbercloud IaaS/PaaS Infrastructure
- Docker
- React js
- Django/python
- Nginx
- Postgresql
- Rabbitmq
