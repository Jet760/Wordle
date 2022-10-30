#!/usr/bin/env python3
"""Guess-My-Word is a game where the player has to guess a word.
Author: <Jessica Turner>
Copyright: <2022>

"""

import random
from datetime import date

MISS = 0  # _-.: letter not found ⬜
MISPLACED = 1  # O, ?: letter in wrong place 🟨
EXACT = 2  # X, +: right letter, right place 🟩

MAX_ATTEMPTS = 6
WORD_LENGTH = 5

ALL_WORDS = "word-bank/all_words.txt"
TARGET_WORDS = 'word-bank/target_words.txt'

TARGET_WORD_HISTORY_FILE = "word-bank/target_word_history.txt"
GUESS_HISTORY_FILE = "word-bank/guess_history.txt"
LEADERBOARD_FILE = "word-bank/leaderboard.txt"


def play(cheat_mode=False):
    """Code that controls the interactive game play"""
    # select a word of the day:
    play_game = True
    while play_game:
        letters_not_in_word = []
        guess_list = []
        guess_counter = 0
        welcome_message()
        word_of_the_day = get_target_word()
        add_target_word_history(word_of_the_day)
        if cheat_mode:
            print(word_of_the_day)
        # build a list of valid words (words that can be entered in the UI):
        valid_words = get_valid_words()
        # do the following in an iteration construct
        while guess_counter < MAX_ATTEMPTS:
            guess = ask_for_guess(valid_words)
            guess_list.append(guess)
            score, letters = score_guess(guess, word_of_the_day)
            for i in letters:
                if i not in letters_not_in_word:
                    letters_not_in_word.append(i)
            guess_counter += 1
            print("The result of your guess is:")
            print(format_score(guess, score))
            if is_correct(score):
                print(f"You guessed {word_of_the_day} correctly after {guess_counter} tries!")
                add_guess_history(guess_list)
                add_to_leaderboard(True, word_of_the_day, guess_list, guess_counter, cheat_mode)
                letters_not_in_word = []
                play_game = play_again()
                break
            else:
                print(f"You have {MAX_ATTEMPTS - guess_counter} tries remaining")
                letters_not_in_word.sort()
                print(f"The letters that not in the word are: {', '.join(letters_not_in_word)}")
            if guess_counter == MAX_ATTEMPTS:
                print("Game Over, you ran out of tries")
                print(f"The word was: {word_of_the_day.upper()}")
                add_guess_history(guess_list)
                add_to_leaderboard(False, word_of_the_day, guess_list, guess_counter, cheat_mode)
                letters_not_in_word = []
                play_game = play_again()
                break


def is_correct(score):
    """Checks if the score is entirely correct and returns True if it is.
    Args:
        score:a tuple of numbers that represent the score
    Returns:
        bool: True if the guess was correct, False if not
    Examples:
    >>> is_correct((1,1,1,1,1))
    False
    >>> is_correct((2,2,2,2,1))
    False
    >>> is_correct((0,0,0,0,0))
    False
    >>> is_correct((2,2,2,2,2))
    True"""

    return all((s == 2 for s in score))


def get_valid_words(file_path=ALL_WORDS):
    """returns a list containing all valid words.
    Note to test that the file is read correctly, use:
    >>> get_valid_words()[0]
    'aahed'
    >>> get_valid_words()[-1]
    'zymic'
    >>> get_valid_words()[10:15]
    ['abamp', 'aband', 'abase', 'abash', 'abask']

    """
    # read words from files and return a list containing all words that can be entered as guesses
    valid_words_list = []
    file = open(file_path, "r")

    for line in file:
        valid_words_list.append(line.strip())

    file.close()
    return valid_words_list


def get_target_word(file_path=TARGET_WORDS, seed=None):
    """Picks a random word from a file of words

    Args:
        file_path (str): the path to the file containing the words
        seed: choosing the word that will be returned (not random)

    Returns:
        str: a random word from the file

    >>> get_target_word(seed='aback')
    'aback'
    >>> get_target_word(seed='zonal')
    'zonal'

    """
    # read words from a file and return a random word (word of the day)
    if seed is not None:
        return seed
    target_words_list = []
    file = open(file_path, "r")

    for line in file:
        target_words_list.append(line.strip())
    word_of_the_day = random.choice(target_words_list)
    file.close()
    return word_of_the_day


def ask_for_guess(valid_words):
    """Requests a guess from the user directly from stdout/in
    Returns:
        str: the guess chosen by the user. Ensures guess is a valid word of correct length in lowercase
    """
    while True:
        print("Please enter your guess")
        guess = input("> ")
        if len(guess) != 5:
            print("Please enter a guess that is five letters long")
        elif guess.lower() not in valid_words:
            print("Please enter a valid word")
            continue
        else:
            return guess.lower()


def score_guess(guess, target_word):
    """given two strings of equal length, returns a tuple of ints representing the score of the guess
    against the target word (MISS, MISPLACED, or EXACT)
    Args:
        guess: the word guessed by the user
        target_word: the word the program has selected to be guessed
    Returns:
        tuple: a tuple containg a tuple of numbers representing the score and a list of letters were guessed but are not in the target word
    Here are some example (will run as doctest):

    >>> score_guess('hello', 'hello')
    ((2, 2, 2, 2, 2), [])
    >>> score_guess('drain', 'float')
    ((0, 0, 1, 0, 0), ['d', 'r', 'i', 'n'])
    >>> score_guess('hello', 'spams')
    ((0, 0, 0, 0, 0), ['h', 'e', 'l', 'l', 'o'])

    Try and pass the first few tests in the doctest before passing these tests.
    >>> score_guess('gauge', 'range')
    ((0, 2, 0, 2, 2), ['g', 'u'])
    >>> score_guess('melee', 'erect')
    ((0, 1, 0, 1, 0), ['m', 'l', 'e'])
    >>> score_guess('array', 'spray')
    ((0, 0, 2, 2, 2), ['a', 'r'])
    >>> score_guess('train', 'tenor')
    ((2, 1, 0, 0, 1), ['a', 'i'])
        """

    score = [0, 0, 0, 0, 0]
    letter_list = []

    target_word_list = list(target_word)
    for i, char in enumerate(guess):
        if guess[i] == target_word_list[i]:
            score[i] = 2
            target_word_list[i] = None

    for i, char in enumerate(guess):
        if score[i] == 0:
            if char in target_word_list:
                score[i] = 1
                target_word_list[target_word_list.index(char)] = None
            else:
                letter_list.append(char)

    return tuple(score), letter_list


def help():
    """Provides help for the game"""
    print("\n", "---------------------------------------------------------------------------",
                "\n", "HOW TO PLAY WORDLE".center(75), "\n",
                "---------------------------------------------------------------------------",
                f"\nGuess the randomly generated word in {MAX_ATTEMPTS} tries.\n"
                f"Each guess must be a valid {WORD_LENGTH} letter word.\n"
                f"Hit the enter button to submit.\n"
                f"After each guess, a series of symbols will appear below your guess to \nshow how close "
                f"your guess was to the word.\n"
                "The symbols used are: \n", "+  =  the letter is in the correct position\n".center(60),
                "?  =  the letter appears in the word but is in the wrong position\n".center(60),
                "-  =  the letter does not appear in the word".center(60),
                "\n\nAn example where the target word is HUMOR and your guess was HELLO:\n",
                "H E L L O".center(75), "\n", "+ - - - ?".center(75), "\n")

    while True:
        print('\nReady to play? (please enter "yes")')
        if input(">").lower() == "yes":
            play()
            return


def format_score(guess, score):
    """Formats a guess with a given score as output to the terminal.
    The following is an example output (you can change it to meet your own creative ideas, 
    but be sure to update these examples)
    >>> print(format_score('hello', (0,0,0,0,0)))
    H E L L O
    - - - - -
    >>> print(format_score('hello', (0,0,0,1,1)))
    H E L L O
    - - - ? ?
    >>> print(format_score('hello', (1,0,0,2,1)))
    H E L L O
    ? - - + ?
    >>> print(format_score('hello', (2,2,2,2,2)))
    H E L L O
    + + + + +"""
    guess_letter_list = []
    score_symbol_list = []
    for letter in guess:
        guess_letter_list.append(letter.upper())
    for number in score:
        if number == 2:
            score_symbol_list.append("+")
        elif number == 1:
            score_symbol_list.append("?")
        else:
            score_symbol_list.append("-")
    return f"{' '.join(guess_letter_list)}\n{' '.join(score_symbol_list)}"


def play_again(testing=None):
    """Asks the user if they want to play the game again then either starts a new game or exits.
    Returns:
        Bool

        >>> play_again('y')
        Play again?
        True
        >>> play_again('Y')
        Play again?
        True
        >>> play_again('Yes')
        Play again?
        True
        >>> play_again('n')
        Play again?
        False
        >>> play_again('N')
        Play again?
        False
        >>> play_again('No')
        Play again?
        False
        >>> play_again('6')
        Play again?
        That wasn't Y or N, play by the rules next time...
        False
"""
    print("Play again?")
    if testing is None:
        answer = input("(Please enter Y or N): ")
    else:
        answer = testing
    if answer.lower() == "n" or answer.lower() == "no":
        return False
    if answer.lower() == "y" or answer.lower() == "yes":
        return True
    else:
        print("That wasn't Y or N, play by the rules next time...")
        return False


def welcome_message():
    """ Prints a welcome message for the user
    """
    print(
        "\n",
        "--------------------------------------------------------------------------------------------------".center(97),
        "\n", "Welcome to Jess' Wordle!!".center(97),
        "\n",
        "The aim is to guess the randomly selected word, "
        "you have six tries to guess the five letter word".center(97), "\n",
        "--------------------------------------------------------------------------------------------------".center(97))


def add_guess_history(guesses):
    """ Adds a list of all the guesses from a game to a file"""
    file = open(GUESS_HISTORY_FILE, "a")
    file.write(f"{date.today()}: {guesses}\n")
    file.close()


def add_target_word_history(word):
    """ Adds the target word from a game to a file"""
    file = open(TARGET_WORD_HISTORY_FILE, "a")
    file.write(f"{date.today()}: {word}\n")
    file.close()


def add_to_leaderboard(win, word, guesses, tries, cheat_mode=False):
    """ Adds to a file: the user's name, target word, number of tries, list of guesses and if cheat mode was on """
    name = input("Please enter your name for the leader board: ")
    file = open(LEADERBOARD_FILE, "a")
    if win is True:
        file.write(f"({date.today()}) {name} guessed '{word.upper()}' after {tries} tries. Guesses:{guesses} Cheat Mode: {cheat_mode}\n")
    else:
        file.write(f"({date.today()}) {name} failed to guess '{word.upper()}'. Guesses:{guesses} Cheat Mode: {cheat_mode}\n")
    file.close()



def main(test=False):
    if test:
        import doctest
        return doctest.testmod()
    play()


if __name__ == '__main__':
    #print(main(test=True))
    #play(cheat_mode=True)
    #play()
    help()


