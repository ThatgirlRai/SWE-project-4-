import re
import sys
import json
from .randomGen import *
from .readJSONFile import *


class Boggle:
    def __init__(self, grid, dictionary):
        self.grid = grid
        self.dictionary = []
        self.solutions = []

        if isinstance(dictionary, list):
            self.dictionary = dictionary
        else:
            self.dictionary = self.read_json_to_list(dictionary)

    def getDictionary(self):
        return self.dictionary

    def is_grid_valid(self):
        regex = r'(st|qu|ie)|[a-hj-prt-z]'

        for row in self.grid:
            for cell in row:
                if not re.search(regex, cell.lower()):
                    return False

        return True

    def getSolution(self):
        # Check inputs
        if self.grid is None or self.dictionary is None:
            return self.solutions

        # Check if grid is NxN
        N = len(self.grid)

        for row in self.grid:
            if len(row) != N:
                return self.solutions

        # Convert everything uppercase
        self.grid = [[x.upper() for x in a] for a in self.grid]
        self.dictionary = [x.upper() for x in self.dictionary]

        # Validate grid
        if not self.is_grid_valid():
            return self.solutions

        # Setup structures
        self.solution_set = set()
        self.hash_map = self.create_hash_map()

        # Search board
        for y in range(N):
            for x in range(N):
                word = ""
                visited = [[False for _ in range(N)] for _ in range(N)]

                self.find_words(
                    word,
                    y,
                    x,
                    self.grid,
                    visited,
                    self.hash_map,
                    self.solution_set
                )

        self.solutions = list(self.solution_set)
        return self.solutions

    def find_words(
        self,
        word,
        y,
        x,
        grid,
        visited,
        hash_map,
        solution_set
    ):
        adj_matrix = [
            [-1, -1],
            [-1, 0],
            [-1, 1],
            [0, 1],
            [1, 1],
            [1, 0],
            [1, -1],
            [0, -1]
        ]

        # Out of bounds / visited
        if (
            y < 0 or
            x < 0 or
            y >= len(grid) or
            x >= len(grid) or
            visited[y][x]
        ):
            return

        # Add letter
        word += grid[y][x]

        # Check prefix
        if self.is_prefix_or_word(word, hash_map):

            visited[y][x] = True

            # Check actual word
            if self.is_word(word, hash_map):
                if len(word) >= 3:
                    self.solution_set.add(word)

            # Explore neighbors
            for i in range(8):
                self.find_words(
                    word,
                    y + adj_matrix[i][0],
                    x + adj_matrix[i][1],
                    grid,
                    visited,
                    hash_map,
                    solution_set
                )

        visited[y][x] = False

    def is_prefix_or_word(self, word, hash_map):
        return word in hash_map

    def is_word(self, word, hash_map):
        return self.hash_map.get(word) == 1

    def create_hash_map(self):
        dict_map = {}

        for word in self.dictionary:
            dict_map[word] = 1

            for i in range(1, len(word)):
                prefix = word[:i]

                if prefix not in dict_map:
                    dict_map[prefix] = 0

        return dict_map