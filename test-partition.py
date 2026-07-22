# hash_check.py
import struct

def murmur2(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    seed = 0x9747b28c
    m = 0x5bd1e995
    r = 24
    
    length = len(data)
    h = seed ^ length
    
    index = 0
    while length >= 4:
        k = struct.unpack_from('<I', data, index)[0]
        k = (k * m) & 0xFFFFFFFF
        k ^= k >> r
        k = (k * m) & 0xFFFFFFFF
        h = (h * m) & 0xFFFFFFFF
        h ^= k
        index += 4
        length -= 4
    
    if length == 3:
        h ^= data[index + 2] << 16
    if length >= 2:
        h ^= data[index + 1] << 8
    if length >= 1:
        h ^= data[index]
        h = (h * m) & 0xFFFFFFFF
    
    h ^= h >> 13
    h = (h * m) & 0xFFFFFFFF
    h ^= h >> 15
    
    return h

num_partitions = 4
vendors = ["CMT", "LRS", "VTS", "MAHIKO"]

for vendor in vendors:
    h = murmur2(vendor)
    partition = h % num_partitions
    print(f"{vendor} → hash={h} → partition {partition}")