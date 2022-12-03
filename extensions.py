import requests


class APIException(Exception):
    pass


class Currency:
    def __init__(self, url):
        self.rates = requests.get(url).json()
        self.rates['Valute']['RUB'] = dict(CharCode='RUB', Nominal=1.0, Name='Российский рубль', Value=1.0)

    def get_price(self, base, quote, amount):
        if base == quote:
            raise APIException('Введены одинаковые валюты\n')
        try:
            val1 = self.rates['Valute'][base]
        except KeyError:
            raise APIException(f'Валюты {base} нет в справочнике\n')
        try:
            val2 = self.rates['Valute'][quote]
        except KeyError:
            raise APIException(f'Валюты {quote} нет в справочнике\n')
        return (val1['Value'] / val1['Nominal']) / (val2['Value'] / val2['Nominal']) * amount

    def get_valute(self):
        res = ''
        for key, val in self.rates['Valute'].items():
            res += f"{key}\t{val['Name']}\n"
        return res



