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
VOWELS = 'aeiou'
word_lc = word.lower()
word = "h*ney"
def test_wild_card(word):
    if "*" in word: 
        for v in VOWELS:
            wild_word = word_lc.replace("*", v)
            print(wild_word)
            if wild_word in word_list:
                for letter in word_dict:
                    letter_frequency = word_dict[letter]
                    if letter in hand and letter_frequency <= hand[letter]:
                        return True
