#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max voters and candidates
#define MAX_VOTERS 100
#define MAX_CANDIDATES 9

// preferences[i][j] is jth preference for voter i
int preferences[MAX_VOTERS][MAX_CANDIDATES];

// Candidates have name, vote count, eliminated status
typedef struct
{
    string name;
    int votes;
    bool eliminated;
} candidate;

// Array of candidates
candidate candidates[MAX_CANDIDATES];

// Numbers of voters and candidates
int voter_count;
int candidate_count;

// Function prototypes
bool vote(int voter, int rank, string name);
void tabulate(void);
bool print_winner(void);
int find_min(void);
bool is_tie(int min);
void eliminate(int min);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: runoff [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX_CANDIDATES)
    {
        printf("Maximum number of candidates is %i\n", MAX_CANDIDATES);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
        candidates[i].eliminated = false;
    }

    voter_count = get_int("Number of voters: ");
    if (voter_count > MAX_VOTERS)
    {
        printf("Maximum number of voters is %i\n", MAX_VOTERS);
        return 3;
    }

    // Keep querying for votes
    for (int i = 0; i < voter_count; i++)
    {

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            // Record vote, unless it's invalid
            if (!vote(i, j, name))
            {
                printf("Invalid vote.\n");
                return 4;
            }
        }

        printf("\n");
    }

    // Keep holding runoffs until winner exists
    while (true)
    {
        // Calculate votes given remaining candidates
        tabulate();

        // Check if election has been won
        bool won = print_winner();
        if (won)
        {
            break;
        }

        // Eliminate last-place candidates
        int min = find_min();
        bool tie = is_tie(min);

        // If tie, everyone wins
        if (tie)
        {
            for (int i = 0; i < candidate_count; i++)
            {
                if (!candidates[i].eliminated)
                {
                    printf("%s\n", candidates[i].name);
                }
            }
            break;
        }

        // Eliminate anyone with minimum number of votes
        eliminate(min);

        // Reset vote counts back to zero
        for (int i = 0; i < candidate_count; i++)
        {
            candidates[i].votes = 0;
        }
    }
    return 0;
}

// Record preference if vote is valid
bool vote(int voter, int rank, string name)
{
    // The preferences stores the order for each voter [i], with the [rank] being the position and
    // the value being the index of the candidate that occupies that space
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i].name, name) == 0)
        {
            // candidates[i].votes++;
            preferences[voter][rank] = i;
            return true;
        }
    }
    return false;
}

// Tabulate votes for non-eliminated candidates
void tabulate(void)
{
    // look at all of the voters’ preferences and compute the current vote totals, by looking at
    // each voter’s top choice candidate who hasn’t yet been eliminated
    // Loop through the voters
    for (int i = 0; i < voter_count; i++)
    {
        // loop through the rankings of the voters to check the first candidate not eliminated
        for (int k = 0; k < candidate_count; k++)
        {
            if (candidates[preferences[i][k]].eliminated == false)
            {
                candidates[preferences[i][k]].votes++;
                break;
            }
        }
    }
    return;
}

// Print the winner of the election, if there is one
bool print_winner(void)
{
    int max_votes = 0;
    int winner_index = 0;
    // Get the highest number of votes.
    for (int j = 0; j < candidate_count; j++)
    {
        if (candidates[j].votes > max_votes)
        {
            max_votes = candidates[j].votes;
            winner_index = j;
        }
    }

    if ((float) max_votes > (float) (voter_count / 2))
    {
        printf("%s\n", candidates[winner_index].name);
        return true;
    }

    return false;
}

// Return the minimum number of votes any remaining candidate has
int find_min(void)
{
    int min_votes = voter_count;
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes < min_votes && candidates[i].eliminated == false)
        {
            min_votes = candidates[i].votes;
        }
    }
    return min_votes;
}

// Return true if the election is tied between all candidates, false otherwise
bool is_tie(int min)
{
    // int tie = 0;
    // for (int i = 0; i < candidate_count; i++)
    // {
    //     if (candidates[i].votes == min || candidates[i].eliminated == true)
    //     {
    //         tie++;
    //     }
    // }
    // // If all the scores are equal to min, the tie variable should be equal to the candidate count,
    // // meaning all the candidates had the same number of votes
    // if (tie == candidate_count)
    // {
    //     return true;
    // }
    // return false;

    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes > min)
        {
            return false;
        }
    }
    return true;

}

// Eliminate the candidate (or candidates) in last place
void eliminate(int min)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes == min)
        {
            candidates[i].eliminated = true;
        }
    }
    return;
}
