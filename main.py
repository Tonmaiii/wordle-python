from __future__ import annotations
from dataclasses import dataclass
import json
import random
from typing import Literal


with open("data/answers.json", encoding="utf-8") as f:
    answers: list[str] = json.load(f)

with open("data/words.json", encoding="utf-8") as f:
    words: list[str] = json.load(f)


def main():
    answer = random.choice(answers)
    guesses: list[str] = []
    results: list[list[State]] = []

    rounds = 1
    while True:
        guess = get_input(rounds)
        guesses.append(guess)

        result = validate_guess(answer, guess)
        results.append(result)
        print_game(guesses, results)

        if guess == answer:
            print(f"{rounds} guessed used.")
            return
        rounds += 1


def print_game(guesses: list[str], results: list[list[State]]):
    print("\n" * 10)
    for guess, result in zip(guesses, results):
        print()
        print(" ".join(guess.upper()))
        print("".join(COLORS[state] for state in result))


State = Literal["Usused", "Incorrect", "Present", "Correct"]
COLORS = {"Usused": "", "Incorrect": "⬛", "Present": "🟨", "Correct": "🟩"}


def get_input(round: int):
    while True:
        guess = input(f"Enter your guess ({round}): ").lower()
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
    guessed_letters = [GuessedLetter(letter, "Incorrect") for letter in guess]
    solution_letters = [SolutionLetter(letter, False) for letter in answer]

    # First pass: correct letters in the correct place
    for guessed_letter, solution_letter in zip(guessed_letters, solution_letters):
        if guessed_letter.letter == solution_letter.letter:
            guessed_letter.state = "Correct"
            solution_letter.included_in_guess = True

    # Second pass: correct letters in the wrong places
    for guessed_letter in guessed_letters:
        if guessed_letter.state == "Correct":
            continue

        letter_found_elsewhere = None
        for solution_letter in solution_letters:
            matches_letter = solution_letter.letter == guessed_letter.letter
            if matches_letter and not solution_letter.included_in_guess:
                letter_found_elsewhere = solution_letter
                break

        if letter_found_elsewhere:
            guessed_letter.state = "Present"
            letter_found_elsewhere.included_in_guess = True

    result: list[State] = [letter.state for letter in guessed_letters]
    return result


main()
