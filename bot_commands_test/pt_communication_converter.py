import re


def text_to_pt_code(text):
    bin_data = ''
    for char in bytearray(text, encoding='utf-8'):
        # convert to binary str and fill with 0 up to 8
        bin_data += format(char, 'b').zfill(8) + ' '

    # replace in pt code
    converted = bin_data.replace('0', 'P').replace('1', 'T')
    return converted


def pt_code_to_text(pt_code):

    # adjust and reconvert to binary
    bin_data = pt_code.upper().replace('P', '0').replace('T', '1').replace(' ', '')

    # split in chunks
    chuck_size = 8
    chunk_data = [bin_data[i:i + chuck_size] for i in range(0, len(bin_data), chuck_size)]

    # convert in text
    converted = ''.join(chr(int(chunk_data[idx], 2)) for idx in range(len(chunk_data)))
    return converted


if __name__ == '__main__':
    while True:
        in_text = input()

        if re.match(r'[PT]', in_text):
            print('PT CODE')
            out = pt_code_to_text(in_text)
        else:
            print('TEXT')
            out = text_to_pt_code(in_text)

        print(out)
