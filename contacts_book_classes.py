from collections import UserDict
from datetime import datetime
from difflib import SequenceMatcher
import pickle
import re


def error_handler(func):
    def wrapper(*args):
        try:
            return func(*args)
        except IndexError:
            return "You didn't provide contact name or phone number"
        except ValueError as exception:
            return exception.args[0]
        except KeyError:
            return "User is not in contact list"
        except TypeError:
            return "You didn't provide enough parameters"

    return wrapper


class Field:
    """Parent class for all fields"""

    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    """Required field with username"""
    pass


class Phone(Field):
    """Optional field with phone numbers"""

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) != 12:
            raise ValueError("Phone must contains 12 symbols.")
        if not value.startswith('380'):
            raise ValueError("Phone must starts from '380'.")
        if not value.isnumeric():
            raise ValueError("Phone number must include digits only.")
        self.__value = value


class Birthday(Field):
    """Creating 'birthday' fields"""

    def __str__(self):
        return self.value.strftime("%d-%m-%Y")

    def __repr__(self):
        return str(self)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        today = datetime.now().date()
        try:
            value = datetime.strptime(value, "%d-%m-%Y").date()
        except:
            raise ValueError("Birthday must be in a format 'DD-MM-YYYY'")
        if value > today:
            raise ValueError("Birthday can't be bigger than current date.")
        self.__value = value


class Email(Field):
    """Creating 'email fields'"""

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not re.findall(r"\b[A-Za-z][\w+.]+@\w+[.][a-z]{2,3}", value):
            raise ValueError('Wrong format. Example: "mymail@gmail.com"')
        self.__value = value


class Record:
    """Class for add, remove, change fields"""

    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None, email: Email = None):

        self.birthday = birthday
        self.email = email
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)

    def __str__(self) -> str:
        return f'Name: {self.name} Phone: {", ".join([str(p) for p in self.phones])} {"Birthday: " + str(self.birthday) if self.birthday else ""} Email: {str(self.email) if self.email else ""}'

    def __repr__(self) -> str:
        return str(self)

    def add_phone(self, phone):
        self.phones.append(phone)
        return f"Phone {phone} was added successfully"

    def change(self, old_phone: Phone, new_phone: Phone):
        for phone in self.phones:
            if phone.value == old_phone.value:
                self.phones.remove(phone)
                self.phones.append(new_phone)
                return f"Phone {old_phone} was successfully changed to {new_phone}"
            return f"Phone number '{old_phone}' was not found in the record"

    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def add_email(self, email: Email):
        self.email = email

    def days_to_birthday(self):

        cur_date = datetime.now().date()
        cur_year = cur_date.year

        if self.birthday:
            bd = self.birthday.value
            this_year_bd = bd.replace(year=cur_year)
            delta = (this_year_bd - cur_date).days
            if delta > 0:
                return f"{self.name}'s birthday will be in {delta} days"
            else:
                next_year_bd = this_year_bd.replace(year=cur_year + 1)
                delta = (next_year_bd - cur_date).days
                return f"{self.name}'s birthday will be in {delta} days"
        else:
            return f"{self.name}'s birthday is unknown"

    def show_contact_info(self):
        phones = ", ".join([str(ph) for ph in self.phones])
        return {
            "name": str(self.name.value),
            "phone": phones,
            "birthday": self.birthday,
            "email": self.email,
        }

    def remove_phone(self, phone):
        phone = Phone(phone)
        for ph in self.phones:
            if ph.value == phone.value:
                self.phones.remove(ph)
                return f"Phone {ph} was successfully removed from {self.name}"
        return f"Number {phone} not found"


class AddressBook(UserDict):
    """Class for creating address book"""

    def open_file(self):
        with open('AddressBook.txt', 'rb') as open_file:
            self.data = pickle.load(open_file)
        return self.data

    def write_file(self):
        with open('AddressBook.txt', 'wb') as write_file:
            pickle.dump(self.data, write_file)

    def search_in_file(self, data):
        result = ""
        for record in self.data.values():
            if str(data).lower() in str(record.name).lower():
                result += f"Name: {record.name} Birthday: {record.birthday} Phone: {','.join([ph.value for ph in record.phones])}\n"
            else:
                for phone in record.phones:
                    if str(data).lower() in str(phone):
                        result += f"Name: {record.name} Birthday: {record.birthday} Phone: {','.join([ph.value for ph in record.phones])}\n"
        return result

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def remove_record(self, record):
        self.data.pop(record.name.value, None)

    def show_one_record(self, name):
        return f"Name: {name}; Birthday: {self.data[name].birthday}; Phone: {', '.join([str(phone.value) for phone in self.data[name].phones])}; Email: {self.data[name].email}"

    def show_all_records(self):
        return "\n".join(
            f"Name: {rec.name} Birthday: {rec.birthday}; Phone: {', '.join([ph.value for ph in rec.phones])} Email: {rec.email}"
            for rec
            in self.data.values())

    def change_record(self, username, old_n, new_n):
        record = self.data.get(username)
        if record:
            record.change(old_n, new_n)

    def iterator(self, n):
        records = list(self.data.keys())
        records_num = len(records)
        count = 0
        result = ""
        if n > records_num:
            n = records_num
        for rec in self.data.values():
            if count < n:
                result += f'{rec.name} (B-day: {rec.birthday}): {", ".join([p.value for p in rec.phones])}\n'
                count += 1
        yield result


ADDRESSBOOK = AddressBook()


HELP_INSTRUCTIONS = """This contact bot save your contacts 
    Global commands:
      'add contact' - add new contact. Input user name and phone
    Example: add User_name 095-xxx-xx-xx
      'add birthday' - add birthday of some User. Input user name and birthday in format dd-mm-yyyy
    Example: add User_name 1971-01-01
      'add email' - add email of some User.
    Example: add email User_name example@mail.com
      'change' - change users old phone to new phone. Input user name, old phone and new phone
    Example: change User_name 095-xxx-xx-xx 050-xxx-xx-xx
      'delete contact' - delete contact (name and phones). Input user name
    Example: delete contact User_name
      'delete phone' - delete phone of some User. Input user name and phone
    Example: delete phone User_name 099-xxx-xx-xx
      'show' - show contacts of input user. Input user name
    Example: show User_name
      'show all' - show all contacts
    Example: show all
      'show list' - show list of contacts which contains N-users
    Example: show list 5 
      'when birthday' - show days to birthday of User/ Input user name
    Example: when celebrate User_name
      'exit/'.'/'bye'/'good bye'/'close' - exit bot
    Example: good bye"""


@error_handler
def add_phone(*args):
    """Adds new contact, requires name and phone"""
    name = Name(args[0])
    phone = Phone(args[1])
    rec = ADDRESSBOOK.get(name.value)

    if name.value in ADDRESSBOOK:
        while True:
            user_input = input(
                f"Contact with this name already exist, do you want to rewrite it (1), create new record (2) or add this number to '{name.value}' (3)?\n")
            if user_input == "2":
                name.value += "(1)"
                rec = ADDRESSBOOK.get(name.value)
                break
            elif user_input == "1":
                ADDRESSBOOK.remove_record(rec)
                rec = ADDRESSBOOK.get(name.value)
                break
            elif user_input == "3":
                break
            else:
                print("Please type '1' or '2' or '3' to continue")

    if not phone.value.isnumeric():
        raise ValueError
    if rec:
        rec.add_phone(phone)
    else:
        rec = Record(name, phone)
        ADDRESSBOOK.add_record(rec)
    return f'You just added contact "{name}" with phone "{phone}" to your list of contacts'


@error_handler
def hello(*args):
    """Greets user"""
    return "How can I help you?"


@error_handler
def change(*args):
    """Replace phone number for an existing contact"""
    name = Name(args[0])
    old_ph = Phone(args[1])
    new_ph = Phone(args[2])

    if not new_ph.value.isnumeric():
        raise ValueError

    ADDRESSBOOK.change_record(name.value, old_ph, new_ph)
    return f"You just changed number for contact '{name}'. New number is '{new_ph}'"


@error_handler
def phone(*args):
    """Shows a phone number for a chosen contact"""
    return ADDRESSBOOK.show_one_record(args[0])


@error_handler
def helper(*args):
    return HELP_INSTRUCTIONS


@error_handler
def delete_contact(*args):
    name = Name(args[0])
    rec = Record(name)
    if name.value:
        ADDRESSBOOK.remove_record(rec)
        return f"{name} was deleted from your contact list"
    else:
        raise IndexError


@error_handler
def add_email(*args):
    name = Name(args[0])
    email = Email(args[1])
    rec = ADDRESSBOOK.get(name.value)

    if rec:
        rec.add_email(email)
        return f"Email for {name.value} was added"
    return f"{name.value} is not in your contact list"


@error_handler
def add_birthday(*args):
    name = Name(args[0])
    birthday = Birthday(args[1])
    rec = ADDRESSBOOK.get(name.value)

    if rec:
        rec.add_birthday(birthday)
        return f"The birthday for {name.value} was added"
    return f"{name.value} is not in your contact list"


@error_handler
def days_to_birthday(*args):
    name = Name(args[0])
    if name.value in ADDRESSBOOK:
        if ADDRESSBOOK[name.value].birthday:
            days = ADDRESSBOOK[name.value].days_to_birthday()
            return days
        return f"{name.value}'s birthday is not set"
    else:
        return f"{name.value} is not in your contacts"


@error_handler
def delete_phone(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    if name.value in ADDRESSBOOK:
        ADDRESSBOOK[name.value].remove_phone(phone.value)
        return f"Phone {phone} was deleted from {name.value} "
    return f"Contact {name.value} does not exist"


@error_handler
def show_all(*args):
    """Show a list of all contacts that were added before"""
    if len(ADDRESSBOOK) > 0:
        return ADDRESSBOOK.show_all_records()
    return "Your addressbook is empty"


@error_handler
def show_list(*args):
    if len(ADDRESSBOOK):
        return "".join(ADDRESSBOOK.iterator(int(args[0])))
    return "Your address book is empty"


def search(*args):
    return ADDRESSBOOK.search_in_file(str(args[0]))


COMMANDS = {
    show_list: "show list",
    delete_phone: "delete phone",
    days_to_birthday: "when birthday",
    add_birthday: "add birthday",
    add_phone: "add contact",
    hello: "hello",
    show_all: "show all",
    change: "change",
    phone: "show",
    helper: "help",
    delete_contact: "delete contact",
    search: "search",
    add_email: "add email",
}


def command_parser(user_input):
    ratio = 0
    possible_command = ""
    for command, key_word in COMMANDS.items():
        if user_input.startswith(key_word):
            return command, user_input.replace(key_word, "").strip().split(" ")
        else:
            a = SequenceMatcher(None, user_input, key_word).ratio()
            if a > ratio:
                ratio = a
                possible_command = key_word
    print(f"Maybe you meant '{possible_command}' ?")
    return None, None


def main():
    print(
        "Here's a list of available commands: 'Hello', 'Add contact', 'Add birthday', 'Add email', 'When birthday', "
        "'Delete contact', 'Change', 'Phone', 'Show all', 'Delete phone', 'Search', 'Help', 'Exit'")
    try:
        ADDRESSBOOK.open_file()
    except FileNotFoundError:
        ADDRESSBOOK.write_file()
        ADDRESSBOOK.open_file()

    while True:
        user_input = input(">>>")
        end_words = [".", "close", "bye", "exit"]

        if user_input.lower() in end_words:
            save_file = input("Do you want to save changes? 'y/n'")
            if save_file == "y":
                ADDRESSBOOK.write_file()
                print("Your data was saved")
            elif save_file == "n":
                pass
            else:
                print("Incorrect input! Try again please.")
                continue
            print("Goodbye and good luck")
            break

        command, data = command_parser(user_input.lower())

        if command:
            print(command(*data))


if __name__ == '__main__':

    main()