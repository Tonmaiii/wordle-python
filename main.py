from __future__ import annotations
from dataclasses import dataclass
import json
import random
from typing import Literal
from unittest import result


with open('data/answers.json', encoding='utf-8') as f:
    answers: list[str] = json.load(f)

with open('data/words.json', encoding='utf-8') as f:
    words: list[str] = json.load(f)


def main():
    answer = random.choice(answers)

    while True:
        guess = get_input()
        if guess == answer:
            print('yay')
            return
        result = validate_guess(answer, guess)
        print(''.join(COLORS[state] for state in result))


State = Literal['Usused', 'Incorrect', 'Present', 'Correct']
COLORS = {
    'Usused': '', 'Incorrect': '⬛', 'Present': '🟨', 'Correct': '🟩'
}


def get_input():
    while True:
        guess = input('Enter your guess: ').lower()
        if guess in words:
            return guess


@dataclass
class GuessedLetter:
    letter: str
    state: State


@dataclass
class SolutionLetter:
    letter: str
    included_in_guess: bool


def validate_guess(answer: str, guess: str):
    guessed_letters = [GuessedLetter(letter, 'Incorrect') for letter in guess]
    solution_letters = [SolutionLetter(letter, False) for letter in answer]

    # First pass: correct letters in the correct place
    for guessed_letter, solution_letter in zip(guessed_letters, solution_letters):
        if (guessed_letter.letter == solution_letter.letter):
            guessed_letter.state = 'Correct'
            solution_letter.included_in_guess = True

    # Second pass: correct letters in the wrong places
    for guessed_letter in guessed_letters:
        if guessed_letter.state == 'Correct':
            continue

        letter_found_elsewhere = None
        for solution_letter in solution_letters:
            matches_letter = solution_letter.letter == guessed_letter.letter
            if matches_letter and not solution_letter.included_in_guess:
                letter_found_elsewhere = solution_letter
                break

        if letter_found_elsewhere:
            guessed_letter.state = 'Present'
            letter_found_elsewhere.included_in_guess = True

    result: list[State] = [letter.state for letter in guessed_letters]
    return result


main()
