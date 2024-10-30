from collections import UserList
from datetime import datetime
from typing import Optional


class ValidationError(Exception):
    pass


class Field:
    def __init__(self, value: str):
        self.validate(value)
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value: str):
        self.validate(new_value)
        self._value = new_value

    def validate(self, value: str):
        pass

    def __str__(self) -> str:
        return str(self._value)


class Name(Field):
    def validate(self, value: str):
        if not value or not value.strip():
            raise ValidationError("Name cannot be empty")
        if not all(char.isalnum() or char.isspace() for char in value):
            raise ValidationError("Name can only contain letters, numbers, and spaces")


class PhoneList(UserList):
    def __str__(self) -> str:
        return f"{'; '.join(p.value for p in self.data)}"

class Phone(Field):
    def validate(self, value: str):
        digits = "".join(filter(str.isdigit, value))
        if len(digits) != 10:
            raise ValidationError("Phone number must contain exactly 10 digits")
        self._value = digits

    @staticmethod
    def normalize_phone(phone: str) -> str:
        return "".join(filter(str.isdigit, phone))


class Birthday(Field):
    def __init__(self, value: str):
        self.validate(value)
        self._value = datetime.strptime(value, "%d.%m.%Y").date()

    def validate(self, value: str):
        try:
            date = datetime.strptime(value, "%d.%m.%Y").date()
            if date > datetime.now().date():
                raise ValidationError("Birthday cannot be in the future")
            self._value = date
        except ValueError:
            raise ValidationError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self) -> str:
        return self._value.strftime("%d.%m.%Y")
