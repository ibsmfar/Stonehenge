"""A game of Stonehenge"""
import math
from game import Game
from stonehenge_state import StonehengeState
from leyline import Leyline


class Stonehenge(Game):
    """
    A game of Stonehenge, a zero-sum game

    b_length: int
    p1_count: int
    p2_count: int
    current_state: StonehengeState
    hoz_lines: list
    right_lines: list
    left_lines: list

    """

    ALPHA = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
             'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
             'X', 'Y', 'Z']

    def __init__(self, is_p1: bool) -> None:
        """
        Initialize a game of Stonehenge

        """
        b_length = int(input("Enter the length of the board: "))
        p1_count = 0
        p2_count = 0
        self.hoz_lines = self.generate_hoz(b_length)
        self.right_lines = self.generate_right_diag_lines(b_length)
        self.left_lines = self.generate_left_diag_lines(b_length)
        self.current_state = StonehengeState(is_p1, b_length,
                                             p1_count, p2_count, self.hoz_lines,
                                             self.right_lines, self.left_lines)

    def get_instructions(self) -> str:
        """x`
        Overrides SuperClass method

        Returns the instructions for a game of Stonehenge
        """
        return "In Stonehenge, players take turns picking letters" \
               "that have not been captured yet. If a player claims" \
               "half of the letters in a leyline, they capture that leyline." \
               "The first one to capture half the leylines wins"

    def is_over(self, state: StonehengeState) -> bool:
        """
        Overrides SuperClass method

        Returns whether the game is over
        """
        threshold = math.ceil(3 * (state.b_length + 1) / 2)
        if state.p1_score >= threshold or state.p2_score \
                >= threshold:
            return True
        return False

    def is_winner(self, player: str) -> bool:
        """
        Overrides SuperClass method

        Return whether player is the winner
        """
        threshold = math.ceil(3 * (self.current_state.b_length + 1) / 2)

        if player == 'p1' and self.current_state.p1_score >= \
                threshold:
            return True
        elif player == 'p2' and self.current_state.p2_score >= \
                threshold:
            return True
        return False

    def str_to_move(self, string: str) -> str:
        """
        Overrides SuperClass method

        Return string as a str
        """
        return str(string)

    def generate_hoz(self, num: int) -> list:
        """
        Generate the horizontal list of leylines
        """
        hoz_lines = []
        n = num
        a = self.ALPHA[:]

        for i in range(1, n+2):
            ley = Leyline(i)
            if i <= n:
                p = 0
                while p < i + 1:
                    ley.letters.append(a.pop(0))
                    p += 1
            else:
                p = 0
                while p < n:
                    ley.letters.append(a.pop(0))
                    p += 1
            hoz_lines.append(ley)
        return hoz_lines

    def generate_right_diag_lines(self, num: int) -> list:
        """
        Generate the right diagonal list of leylines
        """
        right_lines = []
        n = num
        hl = self.hoz_lines[:]
        start = 0

        for i in range(1, n+2):
            ley = Leyline(i)

            if i == 1:
                for j in range(start, n):
                    ley.letters.append(hl[j].letters[0])
            else:
                for j in range(start, n):
                    ley.letters.append(hl[j].letters[i-1])
                start += 1
            right_lines.append(ley)

        counter = 0
        for i in range(1, len(right_lines)):
            right_lines[i].letters.append(hl[n].letters[counter])
            counter += 1

        return right_lines

    def generate_left_diag_lines(self, num: int) -> list:
        """
        Generate the left diagonal lines
        """
        left_lines = []
        n = num
        hl = self.hoz_lines[:]
        start = 0

        for i in range(1, n+2):
            ley = Leyline(i)

            for j in range(start, n):
                length = len(hl[j].letters)
                ley.letters.append(hl[j].letters[length - i])

            start += 1
            if i == 1:
                start = 0

            ley.letters.reverse()
            left_lines.append(ley)
        counter = 0
        for i in range(len(left_lines)-1, 0, -1):
            left_lines[i].letters.insert(0, hl[n].letters[counter])
            counter += 1

        return left_lines


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
