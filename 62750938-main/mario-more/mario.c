#include <cs50.h>
#include <stdio.h>

void left_side(int spaces, int bricks);
void right_side(int bricks);

int main(void)
{

    int number = 0;
    do
    {
        number = get_int("What's the size? ");
    }
    while (number < 1 || number > 8);

    for (int j = 1; j <= number; j++)
    {
        left_side(number - j, j);
        right_side(j);
    }
}

void left_side(int spaces, int bricks)
{
    for (int i = 0; i < spaces; i++)
    {
        printf(" ");
    }
    for (int k = 0; k < bricks; k++)
    {
        printf("#");
    }
    printf("  ");
}

void right_side(int bricks)
{
    for (int b = 0; b < bricks; b++)
    {
        printf("#");
    }
    printf("\n");
}
