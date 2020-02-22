5# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
n = HAND_SIZE

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#

def get_word_score(word, n):
    lc_word = word.lower()
    first_comp = 0
    for letter in lc_word:
        first_comp += SCRABBLE_LETTER_VALUES[letter]
    second_comp = 0
    word_length = len(lc_word)
    x = 7 * word_length - 3 * (n - word_length)
    if x >= 1:
        second_comp += x
    else: 
        second_comp += 1
    word_score = first_comp * second_comp 
    return word_score
#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    d_hand = []
    for letter in hand.keys():
        for j in range(hand[letter]):
            d_hand.append(letter)     # adds letter then space into dict
            d_hand.append(' ')
    str_d_hand = ''.join(str(e) for e in d_hand) #takes dictionary and makes into string
    return str_d_hand
    print(str_d_hand) 

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))
    hand["*"] = 1
    for i in range(num_vowels - 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(current_hand, word):
    
    word_lc = word.lower()
    word_dict = get_frequency_dict(word_lc)
    new_hand = {}
    for letter in word_dict:
       if letter in current_hand: 
            x = int(current_hand[letter]) - int(word_dict[letter])
            if x >= 0:
                new_hand[letter] = x
    for lett in current_hand:
        if lett not in word_dict:
           new_hand[lett] = current_hand[lett]
    return new_hand

    #we need to interate through the word dictionary and if the letter in the word appears in the hand remove the letter from teh orginal hand creating a new_hand which has
    #the left over letters in. Need to decrease the VALUE in the dictionary NOT gget rid of the letter. Once value is equal to 0 we can remove.

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
     
    word_lc = word.lower()
    word_dict = get_frequency_dict(word_lc) 
    all_vowels_tried = 0
    if '*' in word_lc: 
        for v in VOWELS:
            wild_word = word_lc.replace('*', v)
            if wild_word in word_list:
                for letter in word_dict:
                    letter_frequency = word_dict[letter]
                    if letter in hand and letter_frequency <= hand[letter]:
                        return True
            else:
                all_vowels_tried += 1
    elif all_vowels_tried == 5:
        return False
    elif not all(c in hand for c in word_lc):
        return False
    elif word_lc in word_list:
       for letter in word_dict:
           letter_frequency = word_dict[letter]
           if letter in hand and letter_frequency <= hand[letter]:
               return True
           else:
               return False
    else:
       return False
       #function checks if wildcard is in word. iterates through the vowel list, replaces star with vowel from list and checks if that word is in word_list 
   
     


        

    

#
# Problem #5: Playing a hand
#
def calculate_handlen(current_hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    hand_length = 0
    for x in current_hand:
        if current_hand[x] > 0:
            hand_length += current_hand[x]
    return hand_length
    print(hand_length)
    
       

def play_hand(hand, word_list):
    total_score_this_hand = 0
    current_hand = hand
    n = calculate_handlen(current_hand)
    word = ""
    while all(current_hand[x] < 1 for x in current_hand) == False:
        print("Current hand is: %s" % display_hand(current_hand))
        word = input("Enter word, or '!!' to indicate that you are finished:")
        if word == "!!":
            print( "Ended hand. Total score: %s" % total_score_this_hand)
            return total_score_this_hand
        if is_valid_word(word, current_hand, word_list) is True:
            total_score_this_hand += get_word_score(word, n)
            print("'%s' earned %s points. Total %s" % (word, get_word_score(word, n), total_score_this_hand))
            current_hand = update_hand(current_hand, word)
            n = calculate_handlen(current_hand)
            print(" ")          
        else:
            current_hand = update_hand(current_hand, word)
            n = calculate_handlen(current_hand)
            print("Not a Valid word")
            print(" ")            
    print( "Ran out of letters. Total score: %s" % total_score_this_hand)
    return total_score_this_hand


def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    subd_hand = hand
    letter_frequency = hand[letter] 
    l = random.choice(VOWELS + CONSONANTS)
    while (l in hand and l == letter) == True:
        l = random.choice(VOWELS + CONSONANTS)
    subd_hand[l] = letter_frequency
    del subd_hand[letter]
    return subd_hand
       
def break_out_loop(word, total_score_this_hand):
    if word == "!!":
            print( "Ended hand. Total score: %s" % total_score_this_hand)
            return total_score_this_hand

def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.


            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    total_number_of_hands = int(input("Enter total number of hands: "))
    game_complete = 0
    total_score_game = 0
    substituted_hand_played = 0
    subd_hand_q = ""
    while game_complete < total_number_of_hands:
        hand = deal_hand(HAND_SIZE)
        print(display_hand(hand))
        if substituted_hand_played == 0:
            subd_hand_q = input("Would you like to substitute a letter? ")
            if subd_hand_q == "yes":
                letter = input("What letter would you like to substitute? ")
                hand = substitute_hand(hand, letter)
                display_hand(hand)
                substituted_hand_played += 1
                total_score_game += play_hand(hand, word_list) 
                game_complete += 1
            elif subd_hand_q == "no":
                    total_score_game += play_hand(hand, word_list)
                    game_complete += 1
        else:
            total_score_game += play_hand(hand, word_list)
            game_complete += 1
    print("game complete total score is: %s" % total_score_game)

if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
