from task1 import AddressBook, Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Give me name."
        except KeyError:
            return "Contact not found."

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message



@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        return "contact not found"
    else:
        record.edit_phone(old_phone, new_phone)
        return "contact has been changed"


@input_error   
def get_phone(args, book: AddressBook):
    name = args[0]  
    record = book.find(name)
    if record is None:
        return 'contact not found'
    else:
        return record.phones
    
@input_error
def birthdays(book: AddressBook):
    return book.get_upcoming_birthdays()
 
    
def find_all(book: AddressBook):
    if len(book) == 0:
        return "contact's book is empty"
    else:
        info = "contact book:"
        for record in book.values():
            info += f"\n{record}"
        return info

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record is None:
        return "contact not found"
    else:
        record.add_birthday(birthday)
        return "birthday has been saved"
    
@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        return "contact not found"
    elif record.birthday is None: 
        return "birthday for contact not found"
    else:
        return record.birthday.value.date()
    

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(get_phone(args, book))
        elif command == "all":
            print(find_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()