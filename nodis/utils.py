from boa.builtins import concat

def concat_bytes(args):
    result = b''
    for i in args:
        result = concat(result, i)
    return result


def concat_strings(args):
    result = ''
    for i in args:
        result = concat(result, i)
    return result

def concat_arrays(arrays):
    result = []
    for array in arrays:
        for item in array:
            result.append(item)

def remove_list_duplicates(array):
    d = {}
    result = []
    for item in array:
        if not has_key(d, item):
            result.append(item)
            d[item] = 1
    return result

def sort(array):
    less = list(length=m)
    equal = list(length=m)
    greater = list(length=m)

    if len(array) > 1:
        pivot = array[0]
        for x in array:
            print(x)
            if x < pivot:
                less.append(x)
            if x == pivot:
                equal.append(x)
            if x > pivot:
                greater.append(x)
        sorted_less = sort(less)
        sorted_greater = sort(greater)
        arrays = [sorted_less, equal, sorted_greater]
        s = concat_arrays(arrays)
        return concat_strings(s)
    else:
        return array[0]

def get_keys(d, value):
    result = []
    for key in d:
        if d[key] == value:
            result.append(key)
    return result

def sorted_dict_keys(d):
    keys = []
    value_list = sort(values(d))
    for value in value_list:
        temp_keys = get_keys(d, value)
        keys = concat_arrays([keys, temp_keys])
    return concat_strings(keys)

def Main(operation, args):

    if operation == 'sort':
        return sort(args)

    if operation == 'sort_dict':
        d = {'nathan':args[0], 'sean':args[1]}
        return sorted_dict_keys(d)
    return False