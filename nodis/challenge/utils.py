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
    return result