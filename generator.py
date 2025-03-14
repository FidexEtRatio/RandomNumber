from system_entropy import get_hardware_seed
import hashlib

def generate(base, seed, beg, end):
    base = base.encode() if isinstance(base, str) else base
    seed = seed.encode() if isinstance(seed, str) else seed

    hw_seed = str(get_hardware_seed()).encode()
    rand = hashlib.sha3_512(base + hashlib.sha3_512(seed + hw_seed).digest()).hexdigest()

    rounds = 3
    while rounds != 0:
        hw_seed = str(get_hardware_seed()).encode()
        rand += hashlib.sha3_512(base + hashlib.sha3_512(seed + hw_seed).digest()).hexdigest()
        rounds -= 1
    rand = int(rand, 16)
    bit_len = (rand % (2048 - 128 + 1)) + 128
    rand = rand & ((1 << bit_len) - 1)
    rand = rand % (end - beg + 1) + beg
    print("\n!!! A random number has been generated !!!\n")
    return rand