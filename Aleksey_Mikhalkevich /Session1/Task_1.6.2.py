"""
Write a program which makes a pretty print of a part of the multiplication table.

Examples:
```
Input:
a = 2
b = 4
c = 3
d = 7

Output:
    3	4	5	6	7
2	6	8	10	12	14
3	9	12	15	18	21
4	12	16	20	24	28
```
"""

TAB = "\t"


def drawing_multiplication_table(line, column):
    print(end=TAB)
    for t in range(*column):
        print(t, end=TAB)

    print()  # line break

    for i in range(*line):
        print(i, end=TAB)

        for t in range(*column):
            print(i * t, end=TAB)
        print()  # line break


def check_data(line, column):
    if line[0] > line[1] or column[0] > column[1]:
        print("Please input correct data: first value must be more than second and third must be more than fourth!")
        return False
    return True


def get_data_for_table(list_numbers):
    line, column, temp_numbers = [], [], []
    for number in list_numbers:
        temp_numbers.append(int(number[-1]))

    line, column = temp_numbers[:2], temp_numbers[2:]

    # incrementing the second number for the correct print of the table
    line[1] += 1
    column[1] += 1

    return line, column


def main():
    list_numbers = [
        input(f"Please input data in format \"letter = number\", data received : {i} / 4 - ") for i in range(4)
    ]
    line, column = get_data_for_table(list_numbers)
    if check_data(line, column):
        drawing_multiplication_table(line, column)


if __name__ == '__main__':
    main()
