from Crypto.Random import get_random_bytes

# Generate the first key
key1 = get_random_bytes(16)  # 16 bytes = 128 bits

# Generate the second key
key2 = get_random_bytes(16)  # 16 bytes = 128 bits

# Print the keys (in hexadecimal format)
print("Key 1:", key1.hex())
print("Key 2:", key2.hex())