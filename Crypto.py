import base64

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
    max = 0;
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
    return max, bytes([c ^ probable for c in s]).decode('ascii', errors='ignore'), s

# Question 4 Detect single-character XOR
def findLine(path = "4.txt"):
    max = 0
    best = ""
    scr = ""
    with open("4.txt", "r") as file:
        for line in file:
            clean_line = line.strip()
            value, line, scrambled = frequency(bytes.fromhex(clean_line))
            if value > max:
                max = value
                best = line
                scr = scrambled
    print("Unscrambled message: ", best)
    print("Scrmbled messge: ", scr.hex())
    # Uses the frequency analysis function from Q3
    frequency(bytes.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"))



# Question 5 