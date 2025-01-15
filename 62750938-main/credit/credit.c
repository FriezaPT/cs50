#include <cs50.h>
#include <stdio.h>


int main(void)
{
    long number = get_long("Number: ");
    int digit = 0;
    int code = 0;
    bool odd = true;
    int initials = 0;
    int digitscount = 0;


    while (number > 0)
    {
        //selecting the last digit
        digit = number % 10;


        if(odd == false){
            digit = digit * 2;

            //Check if the double of the number is bigger than 10, and if it is sum both the algarisms
            if(digit < 10)
            {
                code += digit;
            }
            else
            {
                code += (int) digit / 10;
                code += digit % 10;
            }
            odd = true;
        }
        else
        {
            code += digit;
            odd = false;
        }

        //deleting the last digit from the number
        number = number / 10;

        if(number < 100 && number >= 10)
        {
            initials = number;
        }

        //counting the digits to check with the initials
        digitscount++;
    }


    //Checking if the checksum ends in 0
    if(code % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }

    if((initials == 34 || initials == 37) && digitscount == 15)
    {
        printf("AMEX\n");
    }
    else if((initials < 56 && initials > 50) && digitscount == 16)
    {
        printf("MASTERCARD\n");
    }
    else if(initials / 10 == 4 && (digitscount == 13 || digitscount == 16))
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}
