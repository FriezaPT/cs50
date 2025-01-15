// Implements a dictionary's functionality

#include "dictionary.h"
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Chose 142,933 because it's a prime number (wich will reduce the number of collisions) near the
// max number of the bigger dictionary In terms of memory, it will ocupy about 1.2Mb, seems like ok
const unsigned int N = 142933;

// Hash table
node *table[N];

// Global to count the words loaded in the dictionary
int word_count = 0;

// Declaring the function prototype
void destroy_list(node *current);

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Get the hash and a pointer to iterate through the possible single linked list
    int hash_result = hash(word);
    node *pointer = table[hash_result];

    // Iterate untill the pointer is null
    while (pointer != NULL)
    {
        if (strcasecmp(word, pointer->word) == 0)
        {
            return true;
        }
        else
        {
            pointer = pointer->next;
        }
    }

    // If no match is found, return false
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Assign a weighted value for each char contained in the string
    int sum = 0;
    for (int i = 0; word[i] != '\0'; i++)
    {
        sum += tolower(word[i]) * (i + 1);
    }
    // Returns the modulo of the weighted value for the number of cells in the hash table so it
    // doesn't get place outside
    return sum % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // *dictionary is the path for the dictionary
    FILE *input = fopen(dictionary, "r");
    if (input == NULL)
    {
        printf("Unable to load dictionary.\n");
        return false;
    }

    // +1 to allow for the null char
    char buffer[LENGTH + 1];

    // Reinitiate to 0 the word_count variable
    word_count = 0;

    while (fgets(buffer, LENGTH + 1, input) != NULL)
    {
        // check for edge case of word being LENGHT size, which was causing the \n to be counted as
        // a different word and creating another entry in the hash table
        if (buffer[strlen(buffer) - 1] != '\n' && !feof(input))
        {
            // Read char by char until it reaches the end of the line or file
            // Not great but the max lenght is hard coded so this should work
            int ch;
            while ((ch = fgetc(input)) != '\n' && ch != EOF)
                ;
        }

        // Substitute the \n for the string end char
        buffer[strcspn(buffer, "\n")] = '\0';

        // Create a new node to store the string to be passed to the table
        node *new_word = malloc(sizeof(node));
        if (new_word == NULL)
        {
            printf("Memory allocation failed.\n");
            fclose(input);
            return false;
        }

        // Put the string in the node and initialize next as null
        strcpy(new_word->word, buffer);
        new_word->next = NULL;

        // Pass the string through the hash function, and get the result
        int hash_result = hash(buffer);

        // Put the node pointer in the correct hash cell, in the first position of the single linked
        // list
        new_word->next = table[hash_result];
        table[hash_result] = new_word;

        // Increase the count of the global word_count
        word_count++;
    }

    // Close the file
    fclose(input);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // Use the global variable word_count to
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Iterate through all the cells in table
    for (int i = 0; i < N; i++)
    {
        // Inside each cell, go through each link of the single linked list, get the pointer to the
        // next link and free the memory of the current link, repeat untill all links are free
        // (until pointer is null)

        destroy_list(table[i]);
    }

    return true;
}

void destroy_list(node *current)
{
    if (current == NULL)
    {
        return;
    }

    // Free the rest of the list recursively
    destroy_list(current->next);

    // Free the current node
    free(current);
}
