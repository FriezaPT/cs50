# Create a check for the input
while True:
    try:
        number = int(input("Number: "))
        if number > 0:
            break

    except ValueError:
        pass

odd = True
checksum = 0
initials = 0
digitscount = 0

while number > 0:
    digit = number % 10

    if not odd:
        digit *= 2

        if digit < 10:
            checksum += digit
        else:
            checksum += digit // 10 + digit % 10

        odd = True
    else:
        checksum += digit
        odd = False

    number //= 10  # Use integer division

    if number >= 10 and number < 100:
        initials = number

    digitscount += 1


if checksum % 10 != 0:
    print("INVALID")
else:
    if (initials == 34 or initials == 37) and digitscount == 15:
        print("AMEX")
    elif (initials < 56 and initials > 50) and digitscount == 16:
        print("MASTERCARD")
    elif initials // 10 == 4 and (digitscount == 13 or digitscount == 16):
        print("VISA")
    else:
        print("INVALID")
