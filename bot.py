from address_book import Record, AddressBook


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError):
            return "Invalid input. Please try again."

    return inner

contacts = AddressBook()

@input_error
def add_contact(name, surname, phone):
    full_name = f"{name} {surname}"
    rec = Record(full_name)
    rec.add_phone(phone)
    contacts.add_record(rec)
    return f"Contact '{full_name}' with phone '{phone}' added."


@input_error
def change_phone(name, new_phone):
    record = contacts.find(name)
    if record:
        record.edit_phone(record._phones[0].value, new_phone)
        return f"Phone number for '{name}' updated to '{new_phone}'."
    return f"Contact '{name}' not found."

@input_error
def get_phone(name):
    record = contacts.find(name)
    if record:
        return f"The phone number for '{name}' is '{record._phones[0].value}'."
    return f"Contact '{name}' not found."

# @input_error
def show_all_contacts():
    return "\n".join(f"{name}: {', '.join(p.value for p in record._phones) if record._phones else 'No phone number'}" for name, record in contacts.data.items())

@input_error
def search_contacts(query):
    results = contacts.search(query)
    if results:
        return "\n".join(str(record) for record in results)
    return f"No matching records found for '{query}'."

def main():
    while True:
        command = input("Enter a command: ").lower()

        if command == 'hello':
            print("How can I help you?")
        elif command.startswith('add'):
            _, name, surname, phone = command.split()
            print(add_contact(name, surname, phone))
        elif command.startswith('change'):
            _, name, new_phone = command.split()
            print(change_phone(name, new_phone))
        elif command.startswith('phone'):
            _, name = command.split()
            print(get_phone(name))
        elif command == 'show all':
            print(show_all_contacts())
        elif command.startswith('search'):
            _, query = command.split()
            print(search_contacts(query))
        elif command in ['good bye', 'close']:
            print("Good bye!")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
