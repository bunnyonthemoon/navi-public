import random
import re


def normalize_phone(phone):
    phone = re.sub('\D', '', phone)

    if phone[0] == '8':
        phone = '7' + phone[1:]
    if len(phone) < 11:
        raise Exception('Неверный формат телефона')

    return '+' + phone


def generate_code(length=4):
    numbers = list('0123456789')
    numbers = numbers + numbers + numbers + numbers
    random.shuffle(numbers)
    code = ''.join([random.choice(numbers) for x in range(length)])

    return code
