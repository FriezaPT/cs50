#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
{
    // Check if one argument was passed, if not abort the program
    if (argc != 2)
    {
        printf("Unexcpeted number of arguments.\n");
        return 1;
    }

    // Check if the argument is 26 chars long
    if (strlen(argv[1]) != 26)
    {
        printf("Argument not with 26 characters.\n");
        return 1;
    }

    // Get an array with 26 spaces
    int cyphercheck[26] = {0};

    // Iterate the string passed to confirm it only contains characters
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (((int) argv[1][i] >= 'A' && (int) argv[1][i] <= 'Z'))
        {
            cyphercheck[argv[1][i] - 'A'] += 1;

            // Check if there is already that char in the check.
            if (cyphercheck[argv[1][i] - 'A'] > 1)
            {
                printf("Cypher contains a duplicate character.\n");
                return 1;
            }
        }
        else if ((int) argv[1][i] >= 'a' && (int) argv[1][i] <= 'z')
        {
            cyphercheck[argv[1][i] - 'a'] += 1;

            // Check if there is already that char in the check.
            if (cyphercheck[argv[1][i] - 'a'] > 1)
            {
                printf("Cypher contains a duplicate character.\n");
                return 1;
            }
        }
        else
        {
            printf("The cypher contains invalid characters.\n");
            return 1;
        }
    }

    string input = get_string("plaintext: ");
    char output[strlen(input) + 1];
    output[strlen(input)] = '\0';

    // Iterate through the input string to create the output string
    for (int k = 0, f = strlen(input); k < f; k++)
    {
        if (input[k] >= 'A' && input[k] <= 'Z')
        {
            output[k] = toupper(argv[1][input[k] - 'A']);
        }
        else if (input[k] >= 'a' && input[k] <= 'z')
        {
            output[k] = tolower(argv[1][input[k] - 'a']);
        }
        else
        {
            output[k] = input[k];
        }
    }
    printf("ciphertext: %s\n", output);
    return 0;
}
