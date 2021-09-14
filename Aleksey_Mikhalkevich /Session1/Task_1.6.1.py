"""
Write a Python program to convert a given tuple of positive integers into an integer.

Examples:
```
Input: (1, 2, 3, 4)
Output: 1234
```
"""


def convert_tuple_to_int(nums):
    result = int(''.join(map(str, nums)))
    return result


def main():
    tuple_int = input("input a tuple: ")
    number = convert_tuple_to_int(eval(tuple_int))
    print(number)


if __name__ == "__main__":
    main()
