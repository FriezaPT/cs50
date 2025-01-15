def left_side(spaces, bricks):
    for i in range(spaces):
        print(" ", end="")
    for i in range(bricks):
        print("#", end="")

    print("  ", end="")


def right_side(bricks):
    for i in range(bricks):
        print("#", end="")

    print("")


while True:
    try:
        number = int(input("Size: "))
        if number > 0 and number < 9:
            break

    except ValueError:
        pass


for i in range(number):
    left_side((number - i) - 1, i + 1)
    right_side(i + 1)
