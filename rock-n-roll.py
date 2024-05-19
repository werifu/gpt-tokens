# Original author: Tianle Cai @ctlllll (Github)
# Chinese version author: Yanyan Jiang@jiangyy (Github)
# This is just a slightly more readable copy.

from tiktoken import get_encoding
from tiktoken.model import MODEL_TO_ENCODING

encodings = list(dict.fromkeys(MODEL_TO_ENCODING.values()))


def is_japanese(ch: str):
    code_point = ord(ch)
    return (
        0x3040 <= code_point <= 0x309F  # Hiragana
        or 0x30A0 <= code_point <= 0x30FF  # Katakana
    )

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

        cn_words = []
        for token in tokens:
            chn = "".join(filter(is_japanese, token))

            # Keep this token if:
            # 1. >= 1 平仮名・カタカナ words
            # 2. Not too many other characters
            if len(chn) >= 1 and len(chn) >= len(token) - 1:
                cn_words.append(chn)

        cn_words.sort(key=lambda x: -len(x))

        cnt = 0
        for i, word in enumerate(cn_words):
            if len(word) != len(cn_words[i - 1]):
                print(f"\n\t↑({cnt})\n{len(word):4}: ", end="")
                cnt = 0
            cnt += 1
            print(word, end=" ")

        print("\n")


if __name__ == "__main__":
    main()
