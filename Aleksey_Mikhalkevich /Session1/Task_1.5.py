"""
Write a Python program to print all unique values of all dictionaries in a list.

Examples:
```
Input: [{"V":"S001"}, {"V": "S002"}, {"VI": "S001"}, {"VI": "S005"}, {"VII":"S005"}, {"V":"S009"},{"VIII":"S007"}]
Output: {'S005', 'S002', 'S007', 'S001', 'S009'}
```
"""


def get_unique_values(list_of_dicts):
    unique_values = set()

    for dictionary in list_of_dicts:
        for value in dictionary.values():
            unique_values.add(value)

    return unique_values


def main():
    list_of_dicts = input("input a list: ")
    unique_values = get_unique_values(eval(list_of_dicts))
    print(unique_values)


if __name__ == "__main__":
    main()
