from fast_bitrix24 import Bitrix

import requests
import time
import os
import xml.etree.ElementTree as ET
import dotenv
from datetime import date


def get_rates(date_req, rates_date):
    """
    Запрашивает курс валют с сайта ЦБ РФ в фомате .xml;
    Парсит полученный .xml, добавляя нужную информацию ее в список;
    
    :return: список, содержащий данные о валютах [{A: {B: C}}, ...];
    :rtype: list;
    """
    url = "http://www.cbr.ru/scripts/XML_daily.asp"
    params = {
        'date_req': date_req,
    }

    # Запрашиваем и парсим данные
    response = requests.get(url, params); time.sleep(2)
    # Запись в файл использована для обеспечения правильной кодировки (UTF-8)
    if not os.path.exists(f"./exrates/exrates_{rates_date}.xml"):
        with open(f"./exrates/exrates_{rates_date}.xml", "w", encoding="utf-8") as file:
            file.write(response.text)
    with open(f"./exrates/exrates_{rates_date}.xml", "r", encoding="utf-8") as file:
        xml_parser = ET.XMLParser(encoding="utf-8")
        parsed = ET.parse(file, parser=xml_parser)

    # Достаем нужную информацию о валютах и добавляем ее в список
    all_valutes = []
    for element in parsed.findall("./Valute"):
        all_valutes.append({
            element.find("CharCode").text: {
                "ID": element.get("ID"),
                "Numcode": element.find("NumCode").text,
                "Charcode": element.find("CharCode").text,
                "Nominal": element.find("Nominal").text,
                "Name": element.find("Name").text,
                "Value": float(element.find("Value").text.replace(",", ".")),
                }
            }
        )

    return all_valutes


def do_update(all_valutes, rates_date):
    """
    Выполняет обновление данных курсов валют на портале Битрикс24;
    url вебхука надо создать на портале заранее и поместить его в 
    переменную WEBHOOK в файл .env в корне; 

    :return: None
    :rtype: None
    """
    dotenv.load_dotenv()


    data = {}
    for valute in all_valutes:
        data.update(valute)
    
    # Вебхук для работы с данными портала Битрикс24
    webhook = os.getenv("WEBHOOK")
    # Запрашиваем список всех валют с портала
    get = Bitrix(webhook)
    currency_get = get.get_all("crm.currency.list")
    # Отправляем запрос на обновление курса валют
    update = Bitrix(webhook)
    update_data = [
        {
            "ID": item["CURRENCY"],
            "fields":
            {
                "AMOUNT": data[item["CURRENCY"]]["Value"]
            }
        }
        for item in currency_get[1:]
    ]
    update.call("crm.currency.update", items=update_data)


def main():
    """Запускает скрипт"""
    # Используемые переменные:
    rates_date = date.today().strftime("%d-%m-%Y") # Дата выполненного нами запроса курсов
    date_req='' # Дата, на которую запрошен курс валют от Центробанка: "dd/mm/yyyy"
                # Если пустая строка, то запрашивает курсы на последнюю дату
    
    if not os.path.exists("./exrates"):
        os.mkdir("./exrates")
    all_valutes = get_rates(date_req, rates_date)
    do_update(all_valutes, rates_date)

if __name__ == "__main__":
    main()