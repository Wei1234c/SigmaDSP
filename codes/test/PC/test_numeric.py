from sigma.sigma_dsp.dsp_processor import DspNumber


# float test ======================
v = -4.25
n = DspNumber(v)

n1 = DspNumber.from_bytes(n.bytes)
print(n1.value, n1.value == v)

n1 = DspNumber.from_bits(n.bits)
print(n1.value, n1.value == v)

# integer test ======================
v = 2 ** 12
n = DspNumber(v, n_bits_A = 28, n_bits_B = 0)

n1 = DspNumber.from_bytes(n.bytes, n_bits_A = 28, n_bits_B = 0)
print(n1.value, n1.value == v)

n1 = DspNumber.from_bits(n.bits, n_bits_A = 28, n_bits_B = 0)
print(n1.value, n1.value == v)

# change types ======================
v = 1.5
n = DspNumber(v)
print(n.type)
print(n.value)
print([hex(b) for b in n.bytes])

n.n_bits_A = 28
n.n_bits_B = 0
print(n.type)
print(n.value)
print([hex(b) for b in n.bytes])

n.n_bits_A = 5
n.n_bits_B = 23
print(n.type)
print(n.value)
print([hex(b) for b in n.bytes])
