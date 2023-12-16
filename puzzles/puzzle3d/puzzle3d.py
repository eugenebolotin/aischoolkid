import hashlib

import numpy as np


class Puzzle:
    def __init__(self, cells=None):
        self.cells = np.array(np.zeros((3, 3, 3)), dtype=int) if cells is None else cells.copy()

    def place_piece(self, piece):
        puzzle = Puzzle(self.cells)
        for (z, y, x), value in np.ndenumerate(piece.cells):
            if value:
                if self.cells[z, y, x]:
                    return None
                puzzle.cells[z, y, x] = value
        return puzzle


class PuzzlePiece:
    def __init__(self, cells=None):
        self.cells = np.array(np.zeros((3, 3, 3)), dtype=int) if (cells is None) else cells.copy()

    def __hash__(self):
        return int(hashlib.sha256(self.cells.tobytes()).hexdigest(), 16)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def rotate_z(self):
        return PuzzlePiece(np.rot90(self.cells, axes=(1, 2)))

    def rotate_y(self):
        return PuzzlePiece(np.rot90(self.cells, axes=(0, 2)))

    def rotate_x(self):
        return PuzzlePiece(np.rot90(self.cells, axes=(0, 1)))

    def translate(self, dx, dy, dz):
        piece = PuzzlePiece()
        for (z, y, x), value in np.ndenumerate(self.cells):
            if value:
                new_x, new_y, new_z = x + dx, y + dy, z + dz
                if 0 <= new_x < 3 and 0 <= new_y < 3 and 0 <= new_z < 3:
                    piece.cells[new_z, new_y, new_x] = value
                else:
                    return None
        return piece


def generate_piece_variations(piece):
    pieces = set([piece])

    for z in range(5):
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                for dz in range(-2, 3):
                    piece_new = piece.translate(dx, dy, dz)
                    if not piece_new:
                        continue

                    pieces.add(piece_new)

                    for az in range(3):
                        piece_new = piece_new.rotate_z()
                        pieces.add(piece_new)
                        for ay in range(3):
                            piece_new = piece_new.rotate_y()
                            pieces.add(piece_new)
                            for ax in range(3):
                                piece_new = piece_new.rotate_x()
                                pieces.add(piece_new)

    return pieces


def solve(puzzle, piece_variants, index=0):
    if index >= len(piece_variants):
        print(puzzle.cells)
        return True

    for piece in piece_variants[index]:
        puzzle_updated = puzzle.place_piece(piece)
        if puzzle_updated:
            if solve(puzzle_updated, piece_variants, index + 1):
                return True

    return False

piece1 = PuzzlePiece()
piece1.cells[0, 0, 0] = 1
piece1.cells[0, 0, 1] = 1
piece1.cells[0, 1, 1] = 1
piece1.cells[0, 1, 2] = 1
piece1.cells[1, 0, 1] = 1

piece2 = PuzzlePiece()
piece2.cells[0, 0, 0] = 2
piece2.cells[0, 0, 1] = 2
piece2.cells[0, 0, 2] = 2
piece2.cells[0, 1, 1] = 2
piece2.cells[1, 0, 0] = 2

piece3 = PuzzlePiece()
piece3.cells[0, 0, 0] = 3
piece3.cells[0, 0, 1] = 3
piece3.cells[0, 0, 2] = 3
piece3.cells[0, 1, 1] = 3

piece4 = PuzzlePiece()
piece4.cells[0, 0, 0] = 4
piece4.cells[0, 0, 1] = 4
piece4.cells[0, 0, 2] = 4
piece4.cells[0, 1, 0] = 4

piece5 = PuzzlePiece()
piece5.cells[0, 0, 0] = 5
piece5.cells[0, 0, 1] = 5
piece5.cells[0, 0, 2] = 5
piece5.cells[0, 1, 1] = 5
piece5.cells[1, 1, 1] = 5

piece6 = PuzzlePiece()
piece6.cells[0, 0, 0] = 6
piece6.cells[0, 0, 1] = 6
piece6.cells[1, 0, 0] = 6
piece6.cells[1, 1, 0] = 6

puzzle = Puzzle()
solve(puzzle, [generate_piece_variations(piece) for piece in (piece1, piece2, piece3, piece4, piece5, piece6)])