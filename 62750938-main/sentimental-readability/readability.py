import cs50

input = cs50.get_string("Text: ")

letters = 0
words = 1  # to add the first word, that doesnt have a space before
sentences = 0


for char in input:
    if char.isalpha():
        letters += 1

    if char == ' ':
        words += 1

    if char == '.' or char == '!' or char == '?':
        sentences += 1

l = (letters / words) * 100
s = (sentences / words) * 100

cli = (0.0588 * l) - (0.296 * s) - 15.8

if cli < 1:
    print("Before Grade 1")
elif cli > 16:
    print("Grade 16+")
else:
    print(f"Grade {round(cli)}")
