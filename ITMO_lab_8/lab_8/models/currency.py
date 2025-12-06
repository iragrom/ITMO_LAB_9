import requests
import sys


class CurrencyID:
    def __init__(self, id: str):
        # конструктор
        self.__id = id

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: str):
        if len(id) >= 1:
            self.__id = id.upper()
        else:
            raise ValueError('длина валюты не может быть меньше 1 символа')


def get_currencies(currency_codes: list, url: str = "https://www.cbr-xml-daily.ru/daily_json.js",
                   handle=sys.stdout) -> dict:
    """
    Получает курсы валют из API Банка России.

Аргументы:
    currency_codes (список): Коды валют (например, ['USD', 'EUR'])
    url (строка): Адрес API Банка России
    handle: Поток для ошибок (по умолчанию sys.stdout)

Возвращает:
    словарь: Ключ - код валюты, значение - словарь с курсом, названием и номиналом:
             {'value': курс, 'name': название, 'nominal': номинал}
             или строку с ошибкой, если валюта не найдена

Выбрасывает:
    requests.exceptions.RequestException: При сбоях HTTP-запроса
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        currencies = {}

        if "Valute" in data:
            for code in currency_codes:
                code_upper = code.upper()
                if code_upper in data["Valute"]:
                    currencies[code_upper] = {
                        'value': data["Valute"][code_upper]["Value"],
                        'name': data["Valute"][code_upper]["Name"],
                        'nominal': data["Valute"][code_upper]["Nominal"]
                    }
                else:
                    currencies[code_upper] = f"Код валюты '{code}' не найден."
        return currencies

    except requests.exceptions.RequestException as e:
        handle.write(f"Ошибка при запросе к API: {e}")
        raise requests.exceptions.RequestException('Ошибка при запросе к API')

# currency_list = ['USD', 'EUR', 'GBP', 'NNZ']
#
# currency_data = get_currencies(currency_list)
# if currency_data:
#      print(currency_data)
# main_id = CurrencyID("EU")
# print(main_id.id)
