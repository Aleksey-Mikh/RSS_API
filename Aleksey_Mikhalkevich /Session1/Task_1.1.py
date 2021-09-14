"""
Write a Python program to calculate the length of a string without using the `len` function.

Examples:
```
Input: Oh, it is python
Output: 16
```
"""


def calculate_len(string):
    if string:
        string_len = string.rindex(string[-1]) + 1
    else:
        string_len = 0
    return string_len


def main():
    string = input("input a string: ")
    string_len = calculate_len(string)
    print(string_len)


if __name__ == "__main__":
    main()
