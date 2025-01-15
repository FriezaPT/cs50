#include <cs50.h>
#include <stdio.h>

void print(int n);
void print_right(int spaces, int bricks);


int main(void)
{
    int number = get_int("What's the size? ");
    for (int j = 0; j < number; j ++)
    {
        print_right(number - j, j);
        print(j + 1);
        printf("\n");
    }
}

void print(int n)
{
    for (int i = 0; i < n; i++ )
    {
        printf("#");
    }
    // printf("\n");
}

void print_right(int spaces, int bricks)
{
    for (int k = 0; k < spaces; k++)
    {
        printf(" ");
    }
    for (int i = 0; i < bricks; i++)
    {
        printf("#");
    }
}
