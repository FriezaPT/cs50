#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    string input = get_string("Text: ");
    int letters = 0;
    int words = 1;
    int sentences = 0;

    for (int i = 0, n = strlen(input); i < n; i++)
    {
        if (isalpha(input[i])) // Count alphabetic characters as letters
        {
            letters++;
        }
        else if (input[i] == ' ') // Count spaces as word separators
        {
            words++;
        }
        else if (input[i] == '.' || input[i] == '!' || input[i] == '?') // Sentence terminators
        {
            sentences++;
        }
    }

    float l = ((float) letters / words) * 100;
    float s = ((float) sentences / words) * 100;

    float index = (0.0588 * l) - (0.296 * s) - 15.8;

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", (int) round(index));
    }
}
