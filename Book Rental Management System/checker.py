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
    if len(number) == 13 or len(number) == 11:
        for num in number:
            if not num.isnumeric():
                if not num == '+':
                    return False
        return True
    return False


def is_validEmail(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False


def split_name(name: str) -> list:
    # Holds the last name, first name, middle intial
    names = []
    # Define the regex pattern for splitting the name
    pattern = r"(\w+\s*\w*)\s*(\w*\.+)?\s+(\w+\-*\w*)"
    # Perform the regex matching
    matches = re.match(pattern, name)
    # Extract the components of the name
    names.append(matches.group(3))
    names.append(matches.group(1))
    names.append(matches.group(2))

    return names


def main():
    # print(is_validName("James*-/-*/-*/@@@*"))
    # print(is_validPhone("09205360159"))
    # print(is_validEmail("1@gmail.com"))
    print("Done")


if __name__ == "__main__":
    main()