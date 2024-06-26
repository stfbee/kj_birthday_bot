import datetime
import os.path
import uuid

from datetime import date
from dateutil.parser import parse
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from message_formatter import format_message

SPREADSHEET_ID = os.environ['SPREADSHEET_ID']
RANGE_NAME = os.environ['RANGE_NAME']
SERVICE_TOKEN = os.environ['GOOGLE_TOKEN_JSON']

today = datetime.date.today()


class Kotan:
    def __init__(self, name, born, age, days_until, chat_link):
        self.name = name
        self.born = born
        self.age = age
        self.next_age = age + 1
        self.days_until = days_until
        self.chat_link = chat_link


class RawRow:
    def __init__(self, name, born, chat_link):
        self.name = name
        self.born = born
        self.chat_link = chat_link


def prepare_token_file():
    text_file = open('service.json', 'w')
    text_file.write(SERVICE_TOKEN)
    text_file.close()


def retrieve_data_from_sheets():
    prepare_token_file()
    creds = service_account.Credentials.from_service_account_file('service.json')

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Получаем данные из листа
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        values = result.get('values', [])

        # Если пусто, ничего не делаем
        if not values:
            print('No data found.')

        return values

    except HttpError as err:
        print(err)


def main():
    values = retrieve_data_from_sheets()

    # Фильтруем строки, чтобы у нас были только непустые значения
    raw_rows = []
    for row in values:
        if len(row) == 9 and (row[0] or row[2]):
            raw_rows.append(RawRow(name=row[0], born=row[2], chat_link=row[8]))

    # Считаем дни и даты
    persons = []
    for raw_row in raw_rows:
        born = parse(raw_row.born, dayfirst=True).date()
        days_until = count_days_to_next_birthday(born)
        age = calculate_age(born)
        persons.append(Kotan(
            raw_row.name, born, age, days_until, raw_row.chat_link
        ))

    # Сортируем по остатку дней
    sorted_list = sorted(persons, key=lambda x: x.days_until)

    # Скрипт запускается каждый день, но список будущих др над выводить только по понедельникам
    if date.today().weekday() == 0:
        # Отсекаем челов, у которых др через 60+ дней
        filtered_list = list(filter(lambda x: x.days_until <= 60, sorted_list))
    else:
        # По всем остальным дням недели пишем только о сегодняшних др
        filtered_list = list(filter(lambda x: x.days_until == 0, sorted_list))

    if len(filtered_list) == 0:
        set_multiline_output("has_answer", False)
        return

    # Формируем сообщение
    message = format_message(filtered_list)

    # Отдаем на следующий шаг
    set_multiline_output("has_answer", "true")
    set_multiline_output("tg_message", message)


def set_multiline_output(name, value):
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        delimiter = uuid.uuid1()
        print(f'{name}<<{delimiter}', file=fh)
        print(value, file=fh)
        print(delimiter, file=fh)


def count_days_to_next_birthday(born):
    delta1 = datetime.date(today.year, born.month, born.day)
    delta2 = datetime.date(today.year + 1, born.month, born.day)
    return ((delta1 if delta1 >= today else delta2) - today).days


def calculate_age(born):
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


if __name__ == '__main__':
    main()
