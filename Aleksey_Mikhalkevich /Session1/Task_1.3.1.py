"""
Write a Python program that accepts a comma separated sequence of words as input and prints the unique words in
sorted form.

Examples:
```
Input: red,white,black,red,green,black
Output: ["black", "green", "red", "white"]
```
"""


def get_sorted_unique_sequence(string):
    sequence = string.split(",")
    return sorted(list(set(sequence)))


def main():
    string = input("input a comma separated sequence of words: ")
    sorted_sequence = get_sorted_unique_sequence(string)
    print(sorted_sequence)


if __name__ == "__main__":
    main()
