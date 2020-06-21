# matching-binary-patterns


Get a path for a binary file and a dictionary and search for hexadecimal strings and regex-like patterns according to this dictionary.
The dictionary can include:

    dictionary = {
        b'\x00': '',        # one byte
        b'\xbe': '',        # one byte
        b'a1': '',          # hexadecimal string
        b'27051956': '',    # hexadecimal string
        b'\x00{3,}': '',    # repeating byte is \x00, above threshold=3
        b'\xad(.){3}': ''}  # first byte is '\xad'

The function output will contain patterns locations details in Json format    
 e.g for an output:
        {
            "range": [98,102],
            "size": 4,
            "hexadecimal_strings\regexp": "b'\\xad(.){3}'"
        }

