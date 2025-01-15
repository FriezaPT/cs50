#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int x = get_int("What's x? ");
    int y = get_int("What's y? ");
    if(x < y)
    {
        printf("x is lass than y\n");
    } else if (y < x)
    {
        printf("x is more than y\n");
    } else
    {
        printf("x and y are equal\n");
    }
}
