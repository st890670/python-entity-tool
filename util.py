def convert_to_camel_naming(name):
    while name.find('_') != -1:
        index = name.find('_')
        name = ''.join(
            (name[:index], '', name[index+1].upper(), name[index+2:]))
    return name


def uppercase_first_word(str):
    return str[0:1].upper() + str[1: len(str)+1]
