"""
Create a program that asks the user for a number and then prints out a list of all the [divisors]
(https://en.wikipedia.org/wiki/Divisor) of that number.

Examples:
```
Input: 60
Output: {1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60}
```
"""
from math import ceil, sqrt


def get_divisors_of_number(number):
    result = list()

    for i in range(1, ceil(sqrt(number))):
        if number % i == 0:
            result.append(i)
            result.append(number // i)

    return sorted(result)


def main():
    number = int(input("input a number: "))
    result = get_divisors_of_number(number)
    print(result)


if __name__ == "__main__":
    main()
