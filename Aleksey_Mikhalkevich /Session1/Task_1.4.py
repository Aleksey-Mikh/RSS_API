"""
Write a Python program to sort a dictionary by key.


Examples:
```
Input: {"b": 9, 1: 3, "c": 7, "a": "7", False: 7}
Output: {1: 3, False: 7, "a": "7", "b": 9, "c": 7}
```
"""


def get_sorted_dict(unsorted_dict):
    """
    Getting key and value from the dictionary for sorting by key. Key is converting to the string to avoid errors.
    At the output "sorted" we get a list of tuples.
    :return sorted_tuples converting to the dict.
    """
    sorted_tuples = sorted(unsorted_dict.items(), key=lambda x: str(x[0]))
    return dict(sorted_tuples)


def main():
    unsorted_dict = input("input a dictionary: ")
    sorted_dict = get_sorted_dict(eval(unsorted_dict))
    print(sorted_dict)


if __name__ == "__main__":
    main()
