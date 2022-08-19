import re

from flask import flash, redirect, url_for
from flask_login import current_user

from main.lazy_strings import r_not_found, not_allowed_delete, not_allowed_edit, not_allowed_get
from main.models import Phonebook


def validate_number(number):
    return re.match(r'^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$', number) is not None


def validate_email(email):
    # Also allowing email be empty
    return email == "" or re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) is not None


def validate_name(name):
    return re.match(r'^[a-zA-Zа-яА-ЯёЁ]+$', name) is not None


def valid_ph_or_redirect(id, action):

    flash_message = {
        'get': not_allowed_get,
        'edit': not_allowed_edit,
        'delete': not_allowed_delete
    }

    if not id:
        flash(r_not_found)
        return redirect(url_for('phonebook'))

    phonebook = Phonebook.query.get(id)
    if not phonebook:
        flash(r_not_found)
        return redirect(url_for('phonebook'))

    if phonebook.user_id != current_user.id:
        flash(flash_message[action])
        return redirect(url_for('phonebook'))

    return phonebook
