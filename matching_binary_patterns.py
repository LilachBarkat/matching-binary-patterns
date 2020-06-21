from multiprocessing import Pool, cpu_count
from itertools import islice
import functools
import binascii
import re
import json
import time


def regex(data, dictionary):
    """
    Get a binary file data and a dictionary of patterns, return patterns locations details
    :param data: bytes, binary file data
    :param dictionary: dictionary, the keys are hexadecimal strings and regex-like patterns
    :return: dictionary, patterns locations details
    """
    results = []
    for key, value in dictionary.items():
        regexp = re.compile(key) if not value else binascii.a2b_hex(key)
        for match in regexp.finditer(data):
            match_span = match.span() if match else None
            size = match_span[1] - match_span[0] if match_span else 0
            results.append({'range': match_span, 'size': size, 'hexadecimal_strings\regexp': str(key)})
    return results


def chunks(dictionary, size=1000):
    """
    Split the dictionary into small parts of length 'size'
    :param dictionary: dictionary, the keys are hexadecimal strings and regex-like patterns
    :param size: int, len of sub dictionary
    :return: dictionary, 'size'-length sub dictionary
    """
    it = iter(dictionary)
    for i in range(0, len(dictionary), size):
        yield {k: dictionary[k] for k in islice(it, size)}


def matching_patterns(path, dictionary):
    """
    Get a path for a binary file and search for hexadecimal strings and regex-like patterns according to dictionary
    :param path: string, path for a binary file
    :param dictionary: dictionary, the keys are hexadecimal strings and regex-like patterns
    :return: json, patterns locations details. e.g:
            {
                "range": [98,102],
                "size": 4,
                "hexadecimal_strings\regexp": "b'\\xad(.){3}'"
            }
    """
    tic = time.time()
    with open(path, 'rb') as f:
        data = f.read()

    p = Pool(processes=cpu_count())  # num of processors
    output = p.map(functools.partial(regex, data),
                   [chunk for chunk in chunks(dictionary, 1000)])
    toc = time.time()
    print("Runtime in sec:", (toc - tic))
    return json.dumps(output, indent=2)


def main():
    path = 'latlon.bin'
    dictionary = {
        b'\x00': '',        # one byte
        b'\xbe': '',        # one byte
        b'a1': '',          # hexadecimal string
        b'27051956': '',    # hexadecimal string
        b'\x00{3,}': '',    # repeating byte is \x00, above threshold=3
        b'\xad(.){3}': ''}  # first byte is '\xad'
    print(matching_patterns(path, dictionary))


if __name__ == '__main__':
    main()

