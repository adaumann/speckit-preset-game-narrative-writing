import glob, os

# CP1252 byte -> replacement character map for bytes undefined or problematic in strict cp1252
CP1252_EXTRAS = {
    0x80: '\u20ac', 0x82: '\u201a', 0x83: '\u0192', 0x84: '\u201e',
    0x85: '\u2026', 0x86: '\u2020', 0x87: '\u2021', 0x88: '\u02c6',
    0x89: '\u2030', 0x8a: '\u0160', 0x8b: '\u2039', 0x8c: '\u0152',
    0x8e: '\u017d', 0x91: '\u2018', 0x92: '\u2019', 0x93: '\u201c',
    0x94: '\u201d', 0x95: '\u2022', 0x96: '\u2013', 0x97: '\u2014',
    0x98: '\u02dc', 0x99: '\u2122', 0x9a: '\u0161', 0x9b: '\u203a',
    0x9c: '\u0153', 0x9d: '\u009d', 0x9e: '\u017e', 0x9f: '\u0178',
}

def decode_mixed(raw):
    chars = []
    for b in raw:
        if b in CP1252_EXTRAS:
            chars.append(CP1252_EXTRAS[b])
        else:
            chars.append(chr(b))
    return ''.join(chars)

paths = glob.glob(r"c:\Users\Andreas.Daumann\OneDrive\Source\speckit-preset-game-narrative-writing\game-rpg-narrative-writing\commands\speckit.*.md")
paths += glob.glob(r"c:\Users\Andreas.Daumann\OneDrive\Source\speckit-preset-game-narrative-writing\game-narrative-writing\commands\speckit.*.md")

for path in paths:
    with open(path, "rb") as f:
        raw = f.read()
    # Check if any non-UTF-8 bytes are present
    try:
        raw.decode("utf-8")
        print("Already UTF-8:", os.path.basename(path))
        continue
    except UnicodeDecodeError:
        pass
    text = decode_mixed(raw)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Fixed:", os.path.basename(path))
