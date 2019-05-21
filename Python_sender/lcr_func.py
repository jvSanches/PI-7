register = 0
entrada = [1, 3, 0, 1, 0, 1]
entrada = [0, 1, 0, 3, 0, 0, 0, 1, 0, 0, 0, 1]
for character in entrada:
    register += ord(str(character))

lrc = ((register ^ 0xFF) + 1) & 0xFF

""""lrcString = _numToOneByteString(lrc)"""
lrcString = lrc
print(lrc)
print(hex(lrc))

