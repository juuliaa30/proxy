# HTTP Proxy Server with Blacklist

**Многопоточный HTTP прокси-сервер с системой блокировки доменов**

## Описание проекта
Прокси-сервер, реализующий HTTP проксирование с возможностью блокировки нежелательных доменов через черный список. 

## Технологический стек
- Язык: Python 
- Сетевые модули: `socket`, `_thread`
- Парсинг URL: `urllib.parse`
- Протокол: HTTP/1.1

## Функциональность

### Проксирование запросов
- Пересылка HTTP запросов от клиента к целевому серверу
- Поддержка всех HTTP методов (GET, POST, PUT, DELETE, etc.)
- Обработка очереди параметров и путей
- Прозрачная передача заголовков и тела запроса

### Система блокировки
- Загрузка черного списка доменов из файла
- Блокировка запросов к запрещенным доменам
- Возврат HTTP 403 Forbidden для заблокированных ресурсов
- Динамическая перезагрузка черного списка

### Логирование
- Логирование всех обрабатываемых запросов
- Отображение HTTP статус-кодов ответов
- Информация об ошибках и исключениях

## Фрагменты работы

![](https://github.com/juuliaa30/proxy/blob/master/screens/1.png)
Захват трафика из беспроводной сети:
![](https://github.com/juuliaa30/proxy/blob/master/screens/2.png)
Захват трафика из loopback:
![](https://github.com/juuliaa30/proxy/blob/master/screens/3.png)
Добавим example.com в черный список
![](https://github.com/juuliaa30/proxy/blob/master/screens/4.png)
Захват трафика из беспроводной сети:
![](https://github.com/juuliaa30/proxy/blob/master/screens/5.png)
Захват трафика из loopback:
![](https://github.com/juuliaa30/proxy/blob/master/screens/6.png)
