print("\n Find an algorithm to solve a generalization of Equivalent Words "
      "\n when insertions, deletions, and substitutions are allowed."
      "\n Example: To transform head into tea one can use only an intermediate: "
      "\n head → tead → tea"
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
class GeneralizedEquivalentWords:
    def __init__(self, start, goal, english_words):
        self.start = start
        self.goal = goal
        self.english_words = english_words
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.tree = {}
        self.msg = ""
        # Special cases, where a pathway cannot be found
        if type(self.english_words) == str:
            self.msg = "Sorry, the dictionary cannot be found:" + english_words
        elif start not in english_words:
            self.msg = "Sorry, but the start word is not in the dictionary"
        elif goal not in english_words:
            self.msg = "Sorry, but the goal word is not in the dictionary"
        elif goal == start:
            self.msg = "The two words are equal, so there is no pathway between them"
        else: #If there is not an error, the tree is built and we can find the path between the two words
            self.tree = self.build_tree()
            self.msg = self.find_path()

    # This function create a tree starting from the start word, every leaf differ from its root by one 1 character, added, removed or substituted
    def build_tree(self):
        goalfound = False #when the goal word is found the formation of the tree is stopped
        to_explore_words = deque() #deque of all the leaves-words that has to be analized
        to_explore_words.append(self.start) #the first word added is the start.
        del english_words[self.start] #start has to be deleted from the dictionary , it can be found again creating a loop
        while to_explore_words and not goalfound: #while there are words to check and the goal is not found
            to_check_word = to_explore_words.popleft() #the first word to control is the first one of the list that is removed
            if to_check_word == self.goal:
                goalfound = True
            else:
                self.tree[to_check_word] = self.find_neighbors(to_check_word) #If the word is not the goal, find all the possible leaves of this word
                to_explore_words.extend(self.tree[to_check_word]) #add more words to check
        if not goalfound: #If there are not any words to check and goalfound is False
            self.tree.clear() #there is no pathway between start and goal
        return self.tree

    # This function finds the neighbors(or leaves) of a word, i.e. the words that differ from a word by a character (substituted, deleted or added)
    def find_neighbors(self, word):
        neighbors = []
        for j in range(len(word)): #find all words that differ from the word by a character substituted
            for char in self.alphabet:
                newword = word[:j] + char + word[j + 1:]
                if newword in self.english_words:
                    neighbors.append(newword)
                    del english_words[newword] #newword is deleted, otherwise it can be found again
        for j in range(len(word)): #find all words that differ from the word by a character deleted
            newword = word[:j] + word[j + 1:]
            if newword in english_words:
                neighbors.append(newword)
                del english_words[newword]
        for j in range(len(word)): #find all the words that differ frome the word by a character added
            for char in self.alphabet:
                newword = word[:j] + char + word[j:]
                if newword in english_words:
                    neighbors.append(newword)
                    del english_words[newword]

        return neighbors

    # This function finds a word starting from one of its leaves or neighbors
    def find_previous(self, word):
        for previous in self.tree:
            if word in self.tree[previous]:
                return previous

    # This function finds the pathway between the start and the goal, starting from the goal
    def find_path(self):
        if self.tree.get(self.start): #if the tree of the start word is not empty, than exists a pathway between start and goal
            reversedpathway = [self.goal] #the first word of the reversed pathway is the goal itself
            child = self.goal
            while child != self.start:
                parent = self.find_previous(child) #starting from the leaf, we get its root
                reversedpathway.append(parent) #and append it to the reversed pathway
                child = parent
            pathway = reversedpathway[::-1]
            for i in pathway:
               self.msg += i + " "
        else: #if the tree of the start word is empty, there is no pathway between the two words
            self.msg = "Sorry, but there is no pathway between start and goal"
        return self.msg


start = input("Please insert the starting word:")
goal = input("Please insert the goal word:")

english_words = load_words()
c = GeneralizedEquivalentWords(start, goal, english_words)
print(c.msg)
