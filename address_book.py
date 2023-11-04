from datetime import datetime
import json
from collections import UserDict

class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

class Name(Field):
    pass

class Phone(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not isinstance(value, str):
            raise ValueError("Phone number must be a string")
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format")
        self._value = value

class Birthday(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid date format, please use YYYY-MM-DD")
        self._value = value


class Record:
    def __init__(self, name, birthday=None):
        self._name = Name(name)
        self._phones = []
        self._birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        phone = Phone(phone)
        self._phones.append(phone)

    def remove_phone(self, phone):
        self._phones = [p for p in self._phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        if not any(old_phone == p.value for p in self._phones):
            raise ValueError(f"Phone number '{old_phone}' does not exist.")
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self._phones:
            if p.value == phone:
                return p

    def days_to_birthday(self):
        if not self._birthday:
            return None
        today = datetime.today()
        next_birthday = datetime(today.year, int(self._birthday.value.split('-')[1]), int(self._birthday.value.split('-')[2]))
        if next_birthday < today:
            next_birthday = datetime(today.year + 1, int(self._birthday.value.split('-')[1]), int(self._birthday.value.split('-')[2]))
        return (next_birthday - today).days

    def __str__(self):
        phones = '; '.join(p.value for p in self._phones)
        return f"Contact name: {self._name.value}, phones: {phones}, birthday: {self._birthday.value if self._birthday else 'N/A'}"
    
    def to_dict(self):
        return {
            "name": self._name.value,
            "phones": [phone.value for phone in self._phones],
            "birthday": self._birthday.value if self._birthday else None
        }

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record._name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            print(f"Contact '{name}' does not exist in the address book.")

    def iterator(self, N):
        records = list(self.data.values())
        for i in range(0, len(records), N):
            yield records[i:i + N]

    def save_to_file(self, filename):
            with open(filename, "w") as file:
                json.dump([record.to_dict() for record in self.data.values()], file)
    
    def load_from_file(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)
            for entry in data:
                record = Record(entry["name"], entry["birthday"])
                for phone in entry["phones"]:
                    record.add_phone(phone)
                self.add_record(record)

    def search(self, query):
        results = []
        for record in self.data.values():
            if query.lower() in record._name.value.lower() or any(query.lower() in p.value.lower() for p in record._phones):
                results.append(record)
        return results




