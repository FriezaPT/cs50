#include <stdio.h>
#include <cs50.h>

void meow(int n);

int main(void)
{
    // int i = 3;
    // while (i > 0)
    // {
    //     printf("meow\n");
    //     i--;
    // }

    meow(3);
}

void meow(int n)
{
    for(int i = 0; i < n; i++)
    {
        printf("meow\n");
    }

}
