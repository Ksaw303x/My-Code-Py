def b2_shift(x):
    _x1 = (x & 1) << 7 | \
          (x & 2) << 5 | \
           (x & 4) << 3 | \
           (x & 8) << 1 | \
           (x & 16) >> 1 | \
           (x & 32) >> 3 | \
           (x & 64) >> 5 | \
           (x & 128) >> 7
    return _x1


def convert_stamping_to_hex(stamping_in):
    raw_in = hex(stamping_in)
    byte_string = int(raw_in, 16)
    converted_byte_string = \
        b2_shift(byte_string & 0xFF) | \
        b2_shift((byte_string & 0xFF00) >> 8) << 8 | \
        b2_shift((byte_string & 0xFF0000) >> 16) << 16 | \
        b2_shift((byte_string & 0xFF000000) >> 24) << 24 | \
        b2_shift((byte_string & 0xFF00000000) >> 32) << 32
    return hex(converted_byte_string)


original = '4b'
int_string = int(original, 16)

print(int_string)

a0 = int_string & 0xFF
b0 = b2_shift(a0)

a1 = int_string & 0xFF00
b1 = a1 >> 8
c1 = b2_shift(b1)

a2 = int_string & 0xFF0000
b2 = a2 >> 16
c2 = b2_shift(b2)

a3 = int_string & 0xFF000000
b3 = a3 >> 24
c3 = b2_shift(b3)

a4 = int_string & 0xFF00000000
b4 = a4 >> 32
c4 = b2_shift(b4)

r1 = c1 << 8
r2 = c2 << 16
r3 = c3 << 24
r4 = c4 << 32

out1 = b0 | r1
out2 = out1 | r2
out3 = out2 | r3
out4 = out3 | r4
print(out4)

value_in = 6080910
out = convert_stamping_to_hex(value_in)
print(out)






