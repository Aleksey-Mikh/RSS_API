"""
Write a Python program to count the number of characters (character frequency) in a string (ignore case of letters).

Examples:
```
Input: Oh, it is python
Output: {",": 1, " ": 3, "o": 2, "h": 2, "i": 2, "t": 2, "s": 1, "p": 1, "y": 1, "n": 1}
```
"""


def get_char_frequency(string):
    dict_char = {}
    for s in string.lower():
        if s not in dict_char:
            dict_char[s] = 1
        else:
            dict_char[s] += 1

    return dict_char


def main():
    string = input("input a string: ")
    dict_char = get_char_frequency(string)
    print(dict_char)


if __name__ == "__main__":
    main()
