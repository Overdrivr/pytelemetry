# From : https://en.wikipedia.org/wiki/Computation_of_cyclic_redundancy_checks

# Most significant bit first (big-endian)
# x^16+x^12+x^5+1 = (1) 0001 0000 0010 0001 = 0x1021

def crc16(data):
    rem  = 0
    n = 16
    # A popular variant complements rem here
    for d in data:
        rem  = rem ^ (d << (n-8))   # n = 16 in this example
        for j in range(1,8):
            # Assuming 8 bits per byte
            if rem & 0x8000:
            # if leftmost (most significant) bit is set
                rem  = (rem << 1) ^ 0x1021
            else:
                rem  = rem << 1
        rem  = rem & 0xffff      # Trim remainder to 16 bits
    # A popular variant complements rem here
    return rem
