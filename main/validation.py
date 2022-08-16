import re


def validate_number(number):
    return re.match(r'^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$', number) is not None


def validate_email(email):
    return email == "" or re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) is not None


def validate_name(name):
    return re.match(r'^[a-zA-Zа-яА-ЯёЁ]+$', name) is not None
