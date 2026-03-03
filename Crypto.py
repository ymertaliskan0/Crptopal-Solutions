import base64
import sys


# Cryptopals Challange Set #1

# Question - 1 Convert hex to base64
def hex2B64(s):
    b = bytes.fromhex(s)
    return base64.b64encode(b)
# print(hex2B64("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"))


# Question 2 Fixed XOR
def fixedXOR(buffer1, buffer2):
    print(buffer1 , " XOR " , buffer2)
    return (bytes(b1 ^ b2 for b1,b2 in zip(buffer1, buffer2))).hex()
# print(fixedXOR(bytes.fromhex("1c0111001f010100061a024b53535009181c"), bytes.fromhex("686974207468652062756c6c277320657965")))



# Question 3 Frequency analysis
def frequency(s):
    common_chars = "etaoin shrdluETAOINSHRDLU"
    max = -1000;
    probable = 0
    for i in range(256):
        score = 0
        for c in s:
            t = c ^ i
            if(t < 32 and t not in (9, 10, 13)) or t > 126:
                score -= 100
                break
            if chr(t) in common_chars: score += 1
        if(score > max):
            probable = i
            max = score
    # print(i, "== ", bytes([c ^ i for c in s]).decode('ascii', errors='ignore'))
    return max, probable, bytes([c ^ probable for c in s]).decode('ascii', errors='ignore'), s
# print(frequency(bytes.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")))


# Question 4 Detect single-character XOR
def findLine(path = "4.txt"):
    max = 0
    best = ""
    scr = ""
    with open("4.txt", "r") as file:
        for line in file:
            clean_line = line.strip()
            value, key, line, scrambled = frequency(bytes.fromhex(clean_line))
            if value > max:
                max = value
                best = line
                scr = scrambled
    print("Unscrambled message: ", best)
    print("Scrmbled messge: ", scr.hex())
    # Uses the frequency analysis function from Q3
    frequency(bytes.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"))



# Question 5 repeating-key XOR
def repeatXOR(s, pattern = b"ICE"):
    index = 0
    result = bytearray()
    for c in s:
        xor = pattern[index] ^ c
        index = (index + 1) % len(pattern)
        result.append(xor)
    return bytes(result)

text = (b"Burning 'em, if you ain't quick and nimble\n"
        b"I go crazy when I hear a cymbal")

res = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
# assert repeatXOR(text).hex() == res, "Assertion failed: The output does not match!"
# print(repeatXOR(text).hex())




# Question 6 Part 1 Hamming Distance
def hammingBit(s1,s2):
    # s1 = s1.encode('utf-8')
    # s2 = s2.encode('utf-8')

    total = 0
    for b1, b2 in zip(s1, s2):
        xor = b1 ^ b2
        total += xor.bit_count()
    return total

# print(hammingBit("this is a test","wokka wokka!!!"))

# Question 6 Prt2 finding keysize
def findKEYSIZE(s):
    results = []
    for i in range(2, 41):
        total = 0
        blocks = 4
        for j in range(blocks):
            b1 = s[j * i: (j + 1) * i]
            b2 = s[(j + 1) * i: (j + 2) * i]
            total += hammingBit(b1, b2)
        total /= (i * blocks)
        results.append((total ,i))

    results.sort()
    return [r[1] for r in results[:3]]

# print(findKEYSIZE(b"0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"))

# Question 6 Part 3 group i + KEYSIZE * N bytes together
def transpose(s, keysize):
    blocks = []
    for i in range (keysize):
        blocks.append(s[i::keysize])
    return blocks

# Question 6 Part 4 find the most probable key for each block
def getKey(blocks):
    result = bytearray()
    for b in blocks:
        _, res, _, _ = frequency(b)
        result.append(res)
    return result

# Question 6 Putting it together
def decryptRepeatingKey(path, output_path="Set1_Q6.txt"):
    with open(path, "r") as file:
        string1 = file.read()
        bytes_decoded = base64.b64decode(string1)
        possibleKeys = findKEYSIZE(bytes_decoded)
        # print(possibleKeys)
        with open(output_path, "w", encoding="utf-8") as out_file:
            for p in possibleKeys:
                blocks = transpose(bytes_decoded, p)
                key = getKey(blocks)

                key_str = key.decode('ascii', errors='ignore')
                decrypted_str = repeatXOR(bytes_decoded, key).decode('ascii', errors='ignore')

                out_file.write(f'KEY = "{key_str}"\n')
                out_file.write(f'DECRYPTED TEXT = {decrypted_str}\n')
                out_file.write('-' * 50 + '\n\n')

# decryptRepeatingKey("6.txt")