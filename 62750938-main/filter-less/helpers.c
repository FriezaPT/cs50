#include "helpers.h"
#include <math.h>

int min(int a, int b);
int max(int a, int b);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // To grayscale, we need to get the mean of the RGB, and apply it to all of them

    int mean = 0;
    // iterate through lines
    for (int i = 0; i < height; i++)
    {
        // Iterate trough columns
        for (int k = 0; k < width; k++)
        {
            mean =
                round((image[i][k].rgbtBlue + image[i][k].rgbtGreen + image[i][k].rgbtRed) / 3.0);
            image[i][k].rgbtBlue = mean;
            image[i][k].rgbtGreen = mean;
            image[i][k].rgbtRed = mean;
        }
    }
    return;

    // Passes the tests, seems ok
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int sepiaRed = 0;
    int sepiaGreen = 0;
    int sepiaBlue = 0;
    for (int i = 0; i < height; i++)
    {
        for (int k = 0; k < width; k++)
        {
            sepiaRed = round(.393 * image[i][k].rgbtRed + .769 * image[i][k].rgbtGreen +
                             .189 * image[i][k].rgbtBlue);
            if (sepiaRed > 255)
                sepiaRed = 255;
            sepiaGreen = round(.349 * image[i][k].rgbtRed + .686 * image[i][k].rgbtGreen +
                               .168 * image[i][k].rgbtBlue);
            if (sepiaGreen > 255)
                sepiaGreen = 255;
            sepiaBlue = round(.272 * image[i][k].rgbtRed + .534 * image[i][k].rgbtGreen +
                              .131 * image[i][k].rgbtBlue);
            if (sepiaBlue > 255)
                sepiaBlue = 255;
            image[i][k].rgbtBlue = sepiaBlue;
            image[i][k].rgbtGreen = sepiaGreen;
            image[i][k].rgbtRed = sepiaRed;
        }
    }
    return;

    // Passes the tests, seems ok
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int redHelp = 0;
    int greenHelp = 0;
    int blueHelp = 0;
    for (int i = 0; i < height; i++)
    {
        for (int k = 0; k < round(width / 2); k++)
        {
            // Assign the values to the the helper
            blueHelp = image[i][k].rgbtBlue;
            greenHelp = image[i][k].rgbtGreen;
            redHelp = image[i][k].rgbtRed;

            // Assign the inverse values to the original values
            image[i][k].rgbtBlue = image[i][width - k - 1].rgbtBlue;
            image[i][k].rgbtGreen = image[i][width - k - 1].rgbtGreen;
            image[i][k].rgbtRed = image[i][width - k - 1].rgbtRed;

            // Assign the help values to the inverse values
            image[i][width - k - 1].rgbtBlue = blueHelp;
            image[i][width - k - 1].rgbtGreen = greenHelp;
            image[i][width - k - 1].rgbtRed = redHelp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of the original to preserve the original values for the math
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int k = 0; k < width; k++)
        {
            copy[i][k] = image[i][k];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int k = 0; k < width; k++)
        {
            int redSum = 0, greenSum = 0, blueSum = 0;
            int count = 0;

            // Iterate over the surrounding pixels within the 3x3 box, ensuring we don't go out of
            // bounds
            for (int di = max(0, i - 1); di <= min(height - 1, i + 1); di++)
            {
                for (int dk = max(0, k - 1); dk <= min(width - 1, k + 1); dk++)
                {
                    redSum += copy[di][dk].rgbtRed;
                    greenSum += copy[di][dk].rgbtGreen;
                    blueSum += copy[di][dk].rgbtBlue;
                    count++;
                }
            }

            // Calculate the average color values and assign them to the current pixel
            image[i][k].rgbtRed = round((float) redSum / count);
            image[i][k].rgbtGreen = round((float) greenSum / count);
            image[i][k].rgbtBlue = round((float) blueSum / count);
        }
    }

    return;
}

// Helper function to find the minimum of two numbers
int min(int a, int b)
{
    return (a < b) ? a : b;
}

// Helper function to find the maximum of two numbers
int max(int a, int b)
{
    return (a > b) ? a : b;
}
