#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
int calculate_score(string word);

int main(void)
{
    string player1 = get_string("Player one: ");
    string player2 = get_string("Player two: ");
    int score1 = calculate_score(player1);
    int score2 = calculate_score(player2);

    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int calculate_score(string word)
{
    int score = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        if (((int) word[i] >= 'A' && (int) word[i] <= 'Z'))
        {
            score += POINTS[word[i] - 'A'];
        }
        else if ((int) word[i] >= 'a' && (int) word[i] <= 'z')
        {
            score += POINTS[word[i] - 'a'];
        }
    }

    return score;
}
