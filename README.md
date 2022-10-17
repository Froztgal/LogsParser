# LogsParser

## Установка

1. Скопировать репозиторий:
```console
git clone https://github.com/Froztgal/LogsParser.git
```

2. Перейти в папку проекта:
```console
cd LogsParser
```

3. Развернуть приложение в Docker:
```console
docker-compose up -d
```

После выполнения перечисленных выше действий в Doceker будет запущено 3 контейнера, отвечающих за frontend (80 порт), backend (порт 8080) и БД (порт 5432).

![alt text](https://github.com/Froztgal/LogsParser/blob/main/images/DockerContainers.jpg?raw=true)

## Использование

Введя в браузере адрес хоста, в случае запуска на локальной машине: ```localhost:80```, вы попадете на домашнюю страницу сайта

![alt text](https://github.com/Froztgal/LogsParser/blob/main/images/HomePage.png?raw=true)

С инструкцией по использованию сайта можно ознакомиться во вкладке "Интсрукции"

![alt text](https://github.com/Froztgal/LogsParser/blob/main/images/GuidesPage.png?raw=true)

Загрузить новые файлы можно во вкладке "Загрузить"

![alt text](https://github.com/Froztgal/LogsParser/blob/main/images/UploadPageBase.png?raw=true)

После выбора файлов через проводник (открывается при нажатии на значек файла в заштрихованной области) или перенесения файлов в заштрихованную олбасть иконка сменится на слудующую

![alt text](https://github.com/Froztgal/LogsParser/blob/main/images/UploadPageSelected.png?raw=true)

После этого можно нажать кнопку "Выгрузить файлы", после загрузки файлов иконка смениться на следующую

![alt text](https://github.com/Froztgal/LogsParser/blob/main/images/UploadPageUploaded.png?raw=true)

Просмотреть отчеты можно во вкладке "Отчеты", имеется возможность фильтрации при помощи фильтра над таблицей отчетов

![alt text](https://github.com/Froztgal/LogsParser/blob/main/images/ReportsPageUploaded.png?raw=true)

Для обработки загруженных файлов и их дальнейшего просмотра необходимо нажать на кнопки "uploaded", после обработки они поменяют статус на "processed"

![alt text](https://github.com/Froztgal/LogsParser/blob/main/images/ReportsPageProcessed.png?raw=true)

По нажатию на любую из кнопок "processed" за конкретную дату можно перейти к дашборду соотвествующего отчета, в котором представлены две таблицы

![alt text](https://github.com/Froztgal/LogsParser/blob/main/images/DashboardPage.png?raw=true)

Выгрузить файл ошибок можно нажав на кнопку "Скачать errors", появиться модальное окно с выбором времени начала и конца выгрузки в файл, после выбора времени, нажатие кнопки "Скачать errors" в модальном окне скачает файл на компьютер

![alt text](https://github.com/Froztgal/LogsParser/blob/main/images/DashBoardPageErrors.png?raw=true)

Пример файла errors

![alt text](https://github.com/Froztgal/LogsParser/blob/main/images/ErrorsFile.png?raw=true)

Выгрузить график можно нажав на кнопку "Скачать график", появиться модальное окно с известных точек на маршруте (время расчитывается исходя из ближайших координат, можно поменять вручную при несоотвествии действительности), после выбора времени, нажатие кнопки "Построить график" в модальном окне скачает файл на компьютер

![alt text](https://github.com/Froztgal/LogsParser/blob/main/images/DashboardPageGraph.png?raw=true)

Пример графика (+ зум)

![alt text](https://github.com/Froztgal/LogsParser/blob/main/images/Graph.png?raw=true)

![alt text](https://github.com/Froztgal/LogsParser/blob/main/images/ZoomedGraph.png?raw=true)

Выгрузить KML файл можно нажав на кнопку "Скачать KML" после этого файл на скачается на компьютер

Пример KML файла в Google Earth (+ зум)

![alt text](https://github.com/Froztgal/LogsParser/blob/main/images/KML.png?raw=true)

![alt text](https://github.com/Froztgal/LogsParser/blob/main/images/ZoomedKML.png?raw=true)

