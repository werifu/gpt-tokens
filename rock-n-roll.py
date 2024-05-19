# Original author: Tianle Cai @ctlllll (Github)
# Chinese version author: Yanyan Jiang@jiangyy (Github)
# This is just a slightly more readable copy.

from tiktoken import get_encoding
from tiktoken.model import MODEL_TO_ENCODING

encodings = list(dict.fromkeys(MODEL_TO_ENCODING.values()))


def is_japanese(ch: str):
    code_point = ord(ch)
    return (
        is_kana(ch)
        # Chinese or Kanji
        or 0x4E00 <= code_point <= 0x9FFF
        or 0x3400 <= code_point <= 0x4DBF
        or 0x20000 <= code_point <= 0x2A6DF
        or 0x2A700 <= code_point <= 0x2B73F
        or 0x2B740 <= code_point <= 0x2B81F
        or 0x2B820 <= code_point <= 0x2CEAF
        or 0x2CEB0 <= code_point <= 0x2EBEF
        or 0xF900 <= code_point <= 0xFAFF
    )

def is_kana(ch: str):
    code_point = ord(ch)
    return (
        0x3040 <= code_point <= 0x309F  # Hiragana
        or 0x30A0 <= code_point <= 0x30FF  # Katakana
    )

def contains_kana(s: str):
    for ch in s:
        if is_kana(ch):
            return True
    return False

def main():
    for enc_name in encodings:
        encoder = get_encoding(enc_name)
        models = [model for model, enc in MODEL_TO_ENCODING.items() if enc == enc_name]

        print(f'Encoding "{enc_name}", {encoder.max_token_value=}')
        print("  Used by:", ", ".join(models), end="")

        tokens = []
        for i in range(encoder.max_token_value + 1):
            try:
                tokens.append(
                    # Try to decode all tokens.
                    encoder.decode([i])
                )
            except:
                pass

        jp_words = []
        for token in tokens:
            cj = "".join(filter(is_japanese, token))

            # Keep this token if:
            # 1. Includes 平仮名 or カタカナ words
            # 2. Not too many other characters
            if contains_kana(cj) and len(cj) >= 1 and len(cj) >= len(token) - 1:
                jp_words.append(cj)

        jp_words.sort(key=lambda x: -len(x))

        cnt = 0
        for i, word in enumerate(jp_words):
            if len(word) != len(jp_words[i - 1]):
                print(f"\n\t↑({cnt})", end="")
                print(f"\n{len(word):4}: ", end="")
                cnt = 0
            cnt += 1
            print(word, end=" ")
        print(f"\n\t↑({cnt})", end="")
        print("\n")


if __name__ == "__main__":
    main()
