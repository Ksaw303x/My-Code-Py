
def read_list_from_file():
    file_name = 'file.txt'

    with open(file_name, "rb") as fp:
        result_list = list(fp.read())

    print(type(result_list), result_list)


if __name__ == '__main__':
    read_list_from_file()
