# Bitrix24_Currency_Updater
Выполняет обновление курса валют на портале Битрикс24 в соответствии с курсом ЦБ РФ;
в данном виде обновляет только курсы Доллара США, Евро и Тенге.

Для корректной работы, на портале должен быть создан вебхук, url-адрес которого надо поместить в переменную WEBHOOK в файле .env (в корне);
Список валют, курсы которых необходимо обновить также должен быть задан на портале, так как данный скрипт не предусматривает создание валют;

## Принцип работы скрипта

Обмен данными с порталом Битрикс24 осуществляется с помощью библиотеки `fast_bitrix24` через вебхук;

### Функция `get_rates()` 
с помощью библиотеки requests, запрашивает данные курса валют на сайте ЦБ РФ, сохраняет их в xml файл по адресу "./exrates", парсит эти данные посредством модуля `xml.etree.ElementTree` и помещает их в возвращаемый список;

### Функция `do_update()` 
используя переданный от `get_rates()` список с данными о курсах валют, отправляет вызов на портал Битрикс24 для обновления курсов.

### Функция `main()`
запускает скрипты, проверяя наличие необходмой папки exrates, в которой хранятся xml файлы;
По умолчанию:

требуемая дата запроса к ЦБ РФ - на последнюю зарегистрированную дату (date_req='');

дата выполнения нами запроса курсов - сегодня (rates_date = date.today()) - исползуется для присвоения имени файлу xml;

## До
![До выполнения скрипта](/images/before.jpg)

## После
![После выполнения скрипта](/images/after.jpg)


## Зависимости
fast_bitrix24

requests

dotenv