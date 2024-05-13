from datetime import datetime, timedelta
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

class Name(Field):
    
		pass

class Phone(Field):
    def __init__(self, value):
        self.value = self.validate(value)

    def validate(self, value):
        if len(value) != 10:
              raise ValueError('value should be 10 digits')
        if not value.isdigit():
              raise ValueError('value should be only digits')
        return value
    
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
	

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, new_phone):
        phone = Phone(new_phone)
        self.phones.append(phone)

    def remove_phone(self, old_phone):
        phone_object = self.find_phone(old_phone)
        if phone_object:
            self.phones.remove(phone_object)
            return True 
        return False

    def edit_phone(self, old_phone, new_phone):
        if self.remove_phone(old_phone):
            self.add_phone(new_phone)

    def find_phone(self, target_phone):
        for phone_object in self.phones:
            if phone_object.value == target_phone:
                return phone_object
            
    def add_birthday(self, user_birthday):
        self.birthday = Birthday(user_birthday)
             
    def __repr__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        result = self.data.get(name)
        return result
    
    def delete(self, name):
        if self.find(name):
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for name, record in self.data.items():
            if record.birthday is None: 
                continue
            birthday_this_year = record.birthday.value.date()
            birthday_this_year = birthday_this_year.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            timedelta_birthday = (birthday_this_year - today).days

            if 0 <= timedelta_birthday <= 7:

                if birthday_this_year.weekday() >= 5:
                    extra_days = 7 - birthday_this_year.weekday()

                    next_week_day = birthday_this_year + timedelta(days=extra_days)
                    upcoming_birthdays.append({'name': name, 'congratulation_date': next_week_day.strftime("%Y.%m.%d")})

                else: 
                    upcoming_birthdays.append({"name": name,
                                            'congratulation_date': birthday_this_year.strftime("%Y.%m.%d")})
        return upcoming_birthdays

    
		


if __name__ == '__main__':
# Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday('16.05.2000')

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    #book.delete("Jane")
    print(book.get_upcoming_birthdays())