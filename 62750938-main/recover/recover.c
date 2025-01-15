#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./recover filename.raw\n");
        return 1;
    }

    // Open file
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    int filenumber = 0;
    uint8_t photo[512];
    FILE *output = NULL;
    int foundjpg = 0;

    while (fread(&photo, sizeof(uint8_t), 512, input) == 512)
    {
        if (photo[0] == 0xff && photo[1] == 0xd8 && photo[2] == 0xff)
        {

            foundjpg = 1;

            // If a jpg is already open, need to close it before proceeding
            if (output != NULL)
            {
                fclose(output);
            }

            // 3 digits for the number, 1 for the ., 3 for the jpg and 1 for the null terminator
            char filename[8];

            // Put the actual value in the filename string
            sprintf(filename, "%03i.jpg", filenumber);

            // Open the file with the filename (W for writing in it)
            output = fopen(filename, "w");

            // Increase the number so the file is not the same everytime
            filenumber++;
        }

        if (foundjpg == 1)
        {
            fwrite(&photo, sizeof(uint8_t), 512, output);
        }
    }

    // After being read untill the end, close the input and output files
    if (output != NULL)
    {
        fclose(output);
    }
    fclose(input);
    return 0;
}
