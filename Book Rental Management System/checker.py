import re


def is_validName(string: str, count: int) -> bool:
    char_count = 0
    for char in string:
        if char.isalpha():
            char_count += 1
    return char_count >= count


def is_validBookName(string, count):
    char_count = 0
    for char in string:
        if char.isalnum():
            char_count += 1
    return char_count >= count


def is_validPhone(number: str) -> bool:
    pattern = r'^(09\d{9}|(\+639)\d{9})$'
    return True if re.match(pattern, number) else False


def is_validEmail(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return True if re.match(pattern, email) else False


def main():
    # print(is_validName("James*-/-*/-*/@@@*"))
    # print(is_validPhone("09205360159"))
    # print(is_validEmail("1@gmail.com"))
    print("Done")


if __name__ == "__main__":
    main()