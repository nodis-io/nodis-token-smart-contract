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

def contains(array, element):
    i = 0
    while i < len(array):
        if array[i] == element:
            result = { 
                element: i 
            }
            return result
        i += 1
    return False

#V8
def valid_address(address):
    return len(address) == 20