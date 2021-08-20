# write your code here
# !/usr/bin/python3

import hashlib
import os
import sys

BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

# https://www.tutorialspoint.com/python3/os_walk.htm


def sorting_option():
    print("Size sorting options:")
    print("1. Descending")
    print("2. Ascending")
    while True:
        try:
            sort_option = int(input("Enter a sorting option:"))
        except (ValueError, TypeError):
            print("Wrong option")
        else:
            if sort_option < 1 or sort_option > 2:
                print("Wrong option")
            else:
                return sort_option


def ask_for(str_to_ask):
    print(str_to_ask)
    while True:
        check_option = input()
        if check_option == 'yes' or check_option == 'no':
            # return check_option
            break
        else:
            print("Wrong option")
    return check_option


def check_for_duplicates(dictionary, sorting_order):
    dict_duplicates = dict()

    list_keys = list(dictionary.keys())
    list_keys.sort()
    for size in list_keys:
        value = dictionary[size]
        # print(f"{key} bytes")

        if len(value) > 1:  # больше одного файла такой длины
            # для таких файлов заполняем значение хеша
            dict_duplicates[size] = dict()

            for i in value:
                with open(i[0], 'rb') as f:
                    md5 = hashlib.md5()
                    while True:  # считаем хеш блоками BUF_SIZE
                        data = f.read(BUF_SIZE)
                        if not data:
                            break
                        md5.update(data)

                    i[1] = md5.hexdigest()
                    if dict_duplicates[size].get(i[1]) is None:
                        dict_duplicates[size][i[1]] = [i[0]]  # key = hash, value = <имя файла>
                    else:
                        # print('Встретился повторно хеш')
                        dict_duplicates[size][i[1]].append(i[0])

                # i[1] = hash_md5(i[0])
                # print(i[0], i[1])

    # пробежаться по новому словарю и показать его содержимое
    # print(dict_duplicates)
    i = 1  # номер строки с файлом

    list_keys = list(dict_duplicates.keys())
    list_keys.sort()
    if sorting_order == 1:
        list_keys = list_keys[::-1]

    # for size, value in dict_duplicates.items():
    to_delete_candidates = [['список кандидатов на удаление', 0]]
    for size in list_keys:
        value = dict_duplicates[size]

        print(f"{size} bytes")
        for hash_d, filenames in value.items():
            # print(f"Hash: {hash_d}, {filenames}")

            if len(filenames) > 1:
                print(f"Hash: {hash_d}")
                for filename in filenames:
                    # print(type(filenames))
                    to_delete_candidates.append([filename, size])  # вместо 0 будет размер файла
                    print(f"{i}. {filename}")
                    i += 1

    return to_delete_candidates  # вернуть список кандидатов на удаление (массив)


def print_dictionary(input_dict, sorting_order):
    list_keys = list(input_dict.keys())
    list_keys.sort()
    if sorting_order == 1:
        list_keys = list_keys[::-1]

    for key in list_keys:
        value = input_dict[key]
        print(f"{key} bytes")
        for i in value:
            print(i[0])


def main():
    if len(sys.argv) != 2:
        print("Directory is not specified")
        return

    file_format = input("Enter file format:").lower()

    sort_option = sorting_option()

    dictionary = dict()
    for root, dirs, files in os.walk(sys.argv[1]):
        for name in files:
            if not name.endswith(file_format):
                continue

            full_name = os.path.join(root, name)
            size = os.path.getsize(full_name)

            if dictionary.get(size) is None:
                dictionary[size] = [[full_name, "hash"]]
            else:
                dictionary[size].append([full_name, "hash"])

    print_dictionary(dictionary, sort_option)
    if ask_for('Check for duplicates?') == 'yes':
        to_delete_candidates = check_for_duplicates(dictionary, sort_option)  # нужно вернуть массив с именами файлов, кандидатов на удаление
        if ask_for('Delete files?') == 'yes':
            print('Enter file numbers to delete:')
            str_to_delete = input()
            # преобразовать в массив индексов файлов для удаления
            # там должны быть только положительные целые числа меньше чем кол-во претендентов на удаление
            if str_to_delete == '':
                print('Wrong format')
            else:
                array_to_delete = str_to_delete.split()
                # print(array_to_delete)
                try:
                    for i in array_to_delete:
                        _ = int(i)
                except (ValueError, TypeError):
                    print('Wrong format')
                    # break
                else:
                    # напечатать (и удалить) список файлов-кандидатов на удаление
                    total_freed_up_space = 0
                    for i in array_to_delete:
                        # print(f'delete: {to_delete_candidates[int(i)][0]}, {to_delete_candidates[int(i)][1]} bytes')
                        try:
                            # pass
                            os.remove(to_delete_candidates[int(i)][0])
                        except Exception:
                            print(f'Не удалось удалить файл: {to_delete_candidates[int(i)][0]}')
                        total_freed_up_space += to_delete_candidates[int(i)][1]
                    print(f'Total freed up space: {total_freed_up_space} bytes')


if __name__ == '__main__':
    main()
