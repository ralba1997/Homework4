print ("\n Transform one English word v into another word w by going"
    "\n through a series of intermediate English words, where each word"
    "\n in the sequence differs from the next by only one substitution (1 character)"
    "\n Example: To transform head into tail one can use three intermediates:"
    "\n head → tead → teal → taal → tail"
    "\n")

# A solution using a tree which is implemented with a Python dictionary: starting from the start word
# leaves are added until there are children. If the goal is found the procedure ends and the path from the start
# word to the goal word is given.

import json
import os, sys
from collections import deque

# read english_dictionary
def load_words():
    try:
        path = os.path.dirname(os.path.realpath(__file__))
        filename = path + "\words_dictionary.json"
        with open(filename, "r") as english_dictionary:
            valid_words = json.load(english_dictionary)
            return valid_words
    except Exception as e:
        return str(e)

# Creation of a class that uses as parameters the starting word, the goal word and a dictionary
class EquivalentWords:
    def __init__(self, start, goal, english_words):
        self.start = start
        self.goal = goal
        self.english_words = english_words
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.tree = {}
        self.msg = ""
        # Special cases, where a pathway cannot be found
        if type(self.english_words) == str:
            self.msg = "Sorry, the dictionary cannot be found: " + english_words
        elif start not in english_words:
            self.msg = "Sorry, but the start word is not in the dictionary"
        elif goal not in english_words:
            self.msg = "Sorry, but the goal word is not in the dictionary"
        elif goal == start:
            self.msg = "The two words are equal, so there is no pathway between them"
        elif len(start) != len(goal):
            self.msg = "The two words have different lengths, so there is no pathway between them"
        else: #If there is not an error, the tree is built and the path between the two words can be found
            self.build_tree()
            self.msg = self.find_path()

    # A tree is created with the start word as root. Every leaf differs from its parent by only one substitution (1 character)
    def build_tree(self):
        goalfound = False # when the goal word is found the construction of the tree is stopped
        to_explore_words = deque() # deque of all the leaves-words that have to be analyzed
        to_explore_words.append(self.start) # the first word added is the start.
        del english_words[self.start] # start has to be deleted from the dictionary, otherwise it can be found again creating a loop
        while to_explore_words and not goalfound: # while there are words to check and the goal is not found
            to_check_word = to_explore_words.popleft() # the first word to check is the first of the deque and it is removed from the deque
            if to_check_word == self.goal:
                goalfound = True
            else:
                self.tree[to_check_word] = self.find_neighbors(to_check_word) # If the word is not the goal, find all the possible leaves of this word
                to_explore_words.extend(self.tree[to_check_word]) # add more words to check
        if not goalfound: # If there are not any words to check and goalfound is False
            self.tree.clear() # there is no pathway between start and goal
        return self.tree

    # The neighbors (or leaves) of a word, i.e. the words that differ from a word by a character by substitution, are found 
    def find_neighbors(self, word):
        neighbors = []
        for j in range(len(word)): # find all words that differ from the word by a substituted character
            for char in self.alphabet:
                newword = word[:j] + char + word[j + 1:]
                if newword in english_words:
                    neighbors.append(newword)
                    del english_words[newword] # newword is deleted, otherwise it can be found again
        return neighbors

    # A word is found starting from one of its leaves or neighbors
    def find_previous(self,word):
        for previous in self.tree:
            if word in self.tree[previous]:
                return previous

    # The pathway between the start and the goal, starting from the goal, is found
    def find_path(self):
        if self.tree.get(self.start):  # if the tree with the start word as root is not empty, then a pathway between start and goal exists
            reversedpathway = [self.goal] # the first word of the reversed pathway is the goal itself
            child = self.goal
            while child != self.start:
                parent = self.find_previous(child) # starting from the leaf, find its parent
                reversedpathway.append(parent) # and append it to the reversed pathway
                child = parent
            pathway = reversedpathway[::-1]
            msg = ""
            for i in pathway:
                msg += i + " "
        else: # if the tree with the start word as root is empty, there is no pathway between the two words
            msg = "Sorry, but there is no pathway between start and goal"
        return msg

start = input("Please insert the starting word:")
goal = input("Please insert the goal word:")

english_words = load_words()
c = EquivalentWords(start, goal, english_words)
print(c.msg)
