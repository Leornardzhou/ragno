import sys
from math import log


def convert(s):
    '''Convert to an integer'''
    try:
        x = int(s)
        return x
    except (ValueError, TypeError) as e:
        print('Conversion error: {}'.format(str(e)), file=sys.stderr)
        raise

def string_log(s):
    v = log(convert(s))
    return v


# print(convert("Ex"))
# print(string_log("2"))
# print(string_log("Ex"))
print(string_log([1,3,3]))
