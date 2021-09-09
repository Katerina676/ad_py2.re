import re
import csv

DATA = "phonebook_raw.csv"
PHONE_PATTERN = r'(\+7|8)*[\s\(]*(\d{3})[\)\s-]*(\d{3})[-]*(\d{2})[-]*(\d{2})[\s\(]*(доб\.)*[\s]*(\d+)*[\)]*'
PHONE_SUB = r'+7(\2)-\3-\4-\5 \6\7'


def read_data(data):
    with open(data, encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def create_contact_list(contacts_list):
    new_contacts_list = list()
    for contact in contacts_list:
        contacts = list()
        full_name = ",".join(contact[:3])
        result = re.findall(r'(\w+)', full_name)
        if len(result) < 3:
            result.append('')
        phone_pattern = re.compile(PHONE_PATTERN)
        changed_phone = phone_pattern.sub(PHONE_SUB, contact[5])
        contacts += result
        contacts.append(contact[3])
        contacts.append(contact[4])
        contacts.append(changed_phone)
        contacts.append(contact[6])
        new_contacts_list.append(contacts)
    return new_contacts_list


def drop_duplicates(new_contacts_list):
    phones = dict()
    for contact in new_contacts_list:
        if contact[0] in phones:
            contact_value = phones[contact[0]]
            for i in range(len(contact_value)):
                if contact[i]:
                    contact_value[i] = contact[i]
        else:
            phones[contact[0]] = contact
    return list(phones.values())


def write_data(data_name, contacts_list):
    with open(data_name, "w", newline='', encoding='utf-8') as f:
        data_writer = csv.writer(f, delimiter=',')
        data_writer.writerows(contacts_list)


if __name__ == '__main__':
    contacts = read_data(DATA)
    new_list = create_contact_list(contacts)
    without_duplicates = drop_duplicates(new_list)
    write_data("phonebook.csv", without_duplicates)
