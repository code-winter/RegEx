from pprint import pprint
import csv
import re


def fix_names(contacts):
    """
    Fixes all names and sorts them to corresponding place
    :param contacts: nested list with contacts
    """
    for person in contacts:
        # Для ФИО
        person[0] = re.sub(r'([А-Я]\w+)\s([А-Я]\w+)\s([А-Я][а-я]+)', r'\1,\2,\3', person[0])
        # Для Ф,ИО и ФИ
        person[0] = re.sub(r'([А-Я]\w+)\s([А-Я]\w+)', r'\1,\2', person[0])
        person[1] = re.sub(r'([А-Я]\w+)\s([А-Я]\w+)', r'\1,\2', person[1])
        names_split = person[0].split(',')
        # Для первой записи (lastname)
        if len(names_split) == 1:
            person[0] = names_split[0]
        # Для ФИ
        elif len(names_split) == 2:
            person[0] = names_split[0]
            person[1] = names_split[1]
        # Для ФИО
        elif len(names_split) == 3:
            person[0] = names_split[0]
            person[1] = names_split[1]
            person[2] = names_split[2]

        names_split = person[1].split(',')
        # Для первой записи (lastname)
        if len(names_split) == 1:
            person[1] = names_split[0]
        # Для Ф, ИО
        elif len(names_split) == 2:
            person[1] = names_split[0]
            person[2] = names_split[1]


def fix_numbers(contacts):
    """
    Changes all phone numbers to a single format +7(XXX)XXX-XX-XX
    :param contacts: nested list with contacts
    :return:
    """
    for person in contacts:
        # Для номеров
        person[5] = re.sub(r'(8|\+7)?\s?\(?(\d{3})?\)?\s?-?(\d{3})-?(\d{2})-?(\d{2})', r'+7(\2)\3-\4-\5', person[5])
        # Для добавочных
        person[5] = re.sub(r'\(?(доб.)\s(\d+)\)?', r'\1\2', person[5])


def fix_doubles(contacts):
    """
    Searches phonebook for any duplicate entries, merges any extra data to one entry and writes a new list without
    duplicates
    :param contacts: nested list with contacts
    :return: list without duplicate entries
    """
    contacts_dirty = contacts
    for pos, person in enumerate(contacts):
        lastname = person[0]
        name = person[1]
        for entry, search in enumerate(contacts_dirty[pos + 1:]):
            if lastname == search[0] and name == search[1]:
                for point, data in enumerate(search):
                    if person[point] == '':
                        person[point] = data
    clean_dict = {}
    indexes = []
    for pos, person in enumerate(contacts):
        clean_dict.setdefault((person[0], person[1]), pos)
    for val in clean_dict.values():
        indexes.append(val)
    contacts_clean = [[] for _ in range(len(indexes))]
    for count in range(len(indexes)):
        contacts_clean[count] = contacts[indexes[count]]
    return contacts_clean


def main():
    with open("phonebook_raw.csv", encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    fix_names(contacts_list)
    fix_numbers(contacts_list)
    contacts_list = fix_doubles(contacts_list)

    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)


if __name__ == '__main__':
    main()
