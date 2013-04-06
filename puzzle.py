#!/usr/bin/python3

import copy
import pprint


HEART, DIAMOND, SPADE, CLUB = range(1, 5)

CARDS = [
    [+SPADE, +DIAMOND, -HEART, -DIAMOND],
    [+DIAMOND, +CLUB, -CLUB, -DIAMOND],
    [+SPADE, +SPADE, -HEART, -CLUB],
    [+SPADE, +DIAMOND, -SPADE, -HEART],
    [+CLUB, +HEART, -DIAMOND, -CLUB],
    [+HEART, +DIAMOND, -CLUB, -CLUB],
    [+HEART, +DIAMOND, -DIAMOND, -HEART],
    [+HEART, +SPADE, -SPADE, -CLUB],
    [+CLUB, +HEART, -SPADE, -HEART],
]

EMPTY_GRID = [3 * [None] for x in range(3)]

DELTAS = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
]


def reverse_direction(direction):
    return (direction + 2) % 4


def fit(grid, card, x, y):
    candidates = [(x + dx, y + dy) for dx, dy in DELTAS]
    for direction, (other_x, other_y) in enumerate(candidates):
        if not (0 <= other_y < len(grid)):
            continue
        if not (0 <= other_x < len(grid[other_y])):
            continue
        card_connector = card[direction]
        other_card = grid[other_y][other_x]
        if other_card is None:
            continue
        other_card_connector = other_card[reverse_direction(direction)]
        if card_connector + other_card_connector:
            return False
    return True


def rotations(card):
    for delta in range(len(card)):
        yield card[delta:] + card[0:delta]


def enumerate_holes(grid):
    for y, row in enumerate(grid):
        for x, card in enumerate(row):
            if card is None:
                yield x, y


def check_grid(grid):
    for y, row in enumerate(grid):
        for x, card in enumerate(row):
            assert(fit(grid, card, x, y))
    return True


def solve_one(grid, remaining_cards):
    card = remaining_cards[0]

    for rotated_card in rotations(card):
        for hole_x, hole_y in enumerate_holes(grid):
            if fit(grid, rotated_card, hole_x, hole_y):
                new_grid = copy.deepcopy(grid)
                new_grid[hole_y][hole_x] = rotated_card
                if len(remaining_cards) == 1:
                    pprint.pprint(new_grid)
                    return True
                else:
                    if solve_one(new_grid, remaining_cards[1:]):
                        return True
    return False


if __name__ == '__main__':
    solve_one(EMPTY_GRID, CARDS)
