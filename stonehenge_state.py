"""A state of a game of Stonehenge"""
from typing import Any, List
import copy
import math
from leyline import Leyline
from game_state import GameState


class StonehengeState(GameState):
    """
    A StonehengeState for use in the game Stonehenge
    """

    ALPHA = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
             'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
             'X', 'Y', 'Z']

    def __init__(self, is_p1: bool, b_length: int, p1_score, p2_score, h_lines,
                 r_lines, l_lines) -> None:
        """
        Initialize a StonehengeState

        p1_turn: the current player
        b_length: the board length
        p1_score: number of leylines captured by p1
        p2_score: number of leylines captured by p2
        h_lines: list of horizontal leylines
        r_lines: list of right_diagonal leylines
        l_lines: list of left_diagonal leylines
        possible_moves: the possible moves

        Extends class GameState

        >>> h_lines = [Leyline(), Leyline()]
        >>> h_lines[0].letters = ['A', 'B']
        >>> h_lines[1].letters = ['C']
        >>> l_lines = [Leyline(), Leyline()]
        >>> l_lines[0].letters = ['B']
        >>> l_lines[0].letters = ['C', 'A']
        >>> r_lines = [Leyline(), Leyline()]
        >>> r_lines[0].letters = ['A']
        >>> r_lines[0].letters = ['B', 'C']
        >>> s = StonehengeState(True, 1, 0, 0, h_lines, \
        r_lines, l_lines)
        >>> s.threshold
        3
        >>> s.p1_turn
        True
        >>> s.p1_score
        0

        """
        self.p1_turn = is_p1
        self.b_length = b_length
        self.p1_score = p1_score
        self.p2_score = p2_score
        self.h_lines = h_lines
        self.r_lines = r_lines
        self.l_lines = l_lines
        num = int(0.5*(b_length**2 + 5*b_length))
        self.possible_moves = self.ALPHA[:num]

    def __repr__(self) -> str:
        """
        Return a representation of self

        >>> h_lines = [Leyline(), Leyline()]
        >>> h_lines[0].letters = ['A', 'B']
        >>> h_lines[1].letters = ['C']
        >>> l_lines = [Leyline(), Leyline()]
        >>> l_lines[0].letters = ['B']
        >>> l_lines[0].letters = ['C', 'A']
        >>> r_lines = [Leyline(), Leyline()]
        >>> r_lines[0].letters = ['A']
        >>> r_lines[0].letters = ['B', 'C']
        >>> s = StonehengeState(True, 1, 0, 0, h_lines, \
        r_lines, l_lines)
        >>> string = s.__repr__()
        >>> '0' in string
        True
        >>> s1 = s.__str__()
        >>> s1 in string
        True
        """

        s = self.__str__()
        s += '\n'
        s += 'p1 {} - {} p2'.format(self.p1_score, self.p2_score)
        s += '\n'
        if self.p1_turn:
            s += 'The current player is p1'
        else:
            s += 'The current player is p2'

        return s

    def __str__(self) -> str:
        """
        Return a string representation of self

        >>> h_lines = [Leyline(), Leyline()]
        >>> h_lines[0].letters = ['A', 'B']
        >>> h_lines[1].letters = ['C']
        >>> l_lines = [Leyline(), Leyline()]
        >>> l_lines[0].letters = ['B']
        >>> l_lines[0].letters = ['C', 'A']
        >>> r_lines = [Leyline(), Leyline()]
        >>> r_lines[0].letters = ['A']
        >>> r_lines[0].letters = ['B', 'C']
        >>> s = StonehengeState(True, 1, 0, 0, h_lines, \
        r_lines, l_lines)
        >>> one = s.one()
        >>> 'A' in one and 'B' in one and 'C' in one and '@' in one
        True
        """

        if self.b_length == 1:
            return self.one()
        elif self.b_length == 2:
            return self.two()
        elif self.b_length == 3:
            return self.three()
        elif self.b_length == 4:
            return self.four()
        return self.five()
        # s = ''
        # for ley in self.h_lines:
        #     s += "{} \n".format(ley.letters)
        #
        # s += "{},{},{}".format(self.p1_turn, self.p1_score, self.p2_score)

    def get_possible_moves(self) -> list:
        """
        Overrides SuperClass method

        Return the possible moves

        >>> h_lines = [Leyline(), Leyline()]
        >>> h_lines[0].letters = ['A', 'B']
        >>> h_lines[1].letters = ['C']
        >>> l_lines = [Leyline(), Leyline()]
        >>> l_lines[0].letters = ['B']
        >>> l_lines[0].letters = ['C', 'A']
        >>> r_lines = [Leyline(), Leyline()]
        >>> r_lines[0].letters = ['A']
        >>> r_lines[0].letters = ['B', 'C']
        >>> s = StonehengeState(True, 1, 0, 0, h_lines, \
        r_lines, l_lines)
        >>> s.get_possible_moves()
        ['A', 'B', 'C']
        """
        return self.possible_moves[:]

    def change_leyline(self, ley: Leyline) -> None:
        """
        Check and change the status of a leyline if a
        player has captured it

        >>> h_lines = [Leyline(), Leyline()]
        >>> h_lines[0].letters = ['A', 'B']
        >>> h_lines[1].letters = ['C']
        >>> l_lines = [Leyline(), Leyline()]
        >>> l_lines[0].letters = ['B']
        >>> l_lines[0].letters = ['C', 'A']
        >>> r_lines = [Leyline(), Leyline()]
        >>> r_lines[0].letters = ['A']
        >>> r_lines[0].letters = ['B', 'C']
        >>> s = StonehengeState(True, 1, 0, 0, h_lines, \
        r_lines, l_lines)
        >>> s.change_leyline(s.h_lines[0])
        >>> s.h_lines[0].letters == ['A', 'B']
        True
        >>> s.h_lines[1].letters == ['C']
        True

        """
        threshold = math.ceil(0.5*(len(ley.letters)))

        if ley.letters.count('1') >= threshold and type(ley.value) == int:
            ley.value = '1'
            self.p1_score += 1

        if ley.letters.count('2') >= threshold and type(ley.value) == int:
            ley.value = '2'
            self.p2_score += 1

    def change_letter(self, move: str, line_list: List[Leyline]) -> None:
        """
        Change the letter in line_list

        >>> h_lines = [Leyline(), Leyline()]
        >>> h_lines[0].letters = ['A', 'B']
        >>> h_lines[1].letters = ['C']
        >>> l_lines = [Leyline(), Leyline()]
        >>> l_lines[0].letters = ['B']
        >>> l_lines[0].letters = ['C', 'A']
        >>> r_lines = [Leyline(), Leyline()]
        >>> r_lines[0].letters = ['A']
        >>> r_lines[0].letters = ['B', 'C']
        >>> s = StonehengeState(True, 1, 0, 0, h_lines, \
        r_lines, l_lines)
        >>> s.change_letter('A', s.h_lines)
        >>> s.h_lines[0].letters[0] == '1'
        True
        """

        if self.p1_turn:
            player = '1'
        else:
            player = '2'

        for leyline in line_list:
            for i in range(len(leyline.letters)):
                if leyline.letters[i] == move:
                    leyline.letters.insert(i, player)
                    leyline.letters.pop(i + 1)
                    self.change_leyline(leyline)
                    break
            else:
                continue
            break

    def make_move(self, move: Any) -> "StonehengeState":

        """
        Return a StonehengeState after applying move

        Overrides SuperClass method

        >>> h_lines = [Leyline(), Leyline()]
        >>> h_lines[0].letters = ['A', 'B']
        >>> h_lines[1].letters = ['C']
        >>> l_lines = [Leyline(), Leyline()]
        >>> l_lines[0].letters = ['B']
        >>> l_lines[0].letters = ['C', 'A']
        >>> r_lines = [Leyline(), Leyline()]
        >>> r_lines[0].letters = ['A']
        >>> r_lines[0].letters = ['B', 'C']
        >>> s = StonehengeState(True, 1, 0, 0, h_lines, \
        r_lines, l_lines)
        >>> s1 = s.make_move('A')
        >>> s1.h_lines[0].letters[0] == '1'
        True
        >>> s1.p1_turn
        false
        """
        h_lines = copy.deepcopy(self.h_lines)
        l_lines = copy.deepcopy(self.l_lines)
        r_lines = copy.deepcopy(self.r_lines)

        ss = StonehengeState(self.p1_turn, self.b_length, self.p1_score,
                             self.p2_score, h_lines, r_lines,
                             l_lines)

        ss.change_letter(move, ss.h_lines[:])
        ss.change_letter(move, ss.r_lines[:])
        ss.change_letter(move, ss.l_lines[:])

        moves = self.get_possible_moves()[:]
        ss.possible_moves = moves
        ss.possible_moves.remove(move)
        ss.p1_turn = not ss.p1_turn

        threshold = math.ceil(3 * (ss.b_length + 1) / 2)

        if ss.p1_score >= threshold or ss.p2_score >= threshold:
            ss.possible_moves = []

        return ss

    def get_leyline_value(self, lst: List[Leyline]) -> List:
        """
        Return the values of the leylines of L.
        @ if no one has captured it and 1 or 2 depending
        on who captured it

        >>> h_lines = [Leyline(), Leyline()]
        >>> h_lines[0].letters = ['A', 'B']
        >>> h_lines[1].letters = ['C']
        >>> l_lines = [Leyline(), Leyline()]
        >>> l_lines[0].letters = ['B']
        >>> l_lines[0].letters = ['C', 'A']
        >>> r_lines = [Leyline(), Leyline()]
        >>> r_lines[0].letters = ['A']
        >>> r_lines[0].letters = ['B', 'C']
        >>> s = StonehengeState(True, 1, 0, 0, h_lines, \
        r_lines, l_lines)
        >>> s.get_leyline_value(s.h_lines)
        ['@', '@', '@']

        """
        leylist = []
        for ley in lst:
            if type(ley.value) == int:
                leylist.append("@")
            else:
                leylist.append(ley.value)

        return leylist

    def rough_outcome(self) -> Any:
        """
        Look 1-2 states ahead and return a rough estimate of
        the current state's score

        >>> h_lines = [Leyline(), Leyline()]
        >>> h_lines[0].letters = ['A', 'B']
        >>> h_lines[1].letters = ['C']
        >>> l_lines = [Leyline(), Leyline()]
        >>> l_lines[0].letters = ['B']
        >>> l_lines[0].letters = ['C', 'A']
        >>> r_lines = [Leyline(), Leyline()]
        >>> r_lines[0].letters = ['A']
        >>> r_lines[0].letters = ['B', 'C']
        >>> s = StonehengeState(True, 1, 0, 0, h_lines, \
        r_lines, l_lines)
        >>> s.rough_outcome()
        1
        """
        threshold = math.ceil(3 * (self.b_length + 1) / 2)
        if self.p1_score >= threshold or self.p1_score >= threshold:
            return -1
        elif any([self.check_good_move(m) for m in self.possible_moves]):
            return 1
        elif all([s.check_good_move(m) for m in s.possible_moves] for
                 s in self.list_states()):
            return -1

        return 0

    def list_states(self) -> list:
        """
        return a list of all the states
        reachable from self

        >>> h_lines = [Leyline(), Leyline()]
        >>> h_lines[0].letters = ['A', 'B']
        >>> h_lines[1].letters = ['C']
        >>> l_lines = [Leyline(), Leyline()]
        >>> l_lines[0].letters = ['B']
        >>> l_lines[0].letters = ['C', 'A']
        >>> r_lines = [Leyline(), Leyline()]
        >>> r_lines[0].letters = ['A']
        >>> r_lines[0].letters = ['B', 'C']
        >>> s = StonehengeState(True, 1, 0, 0, h_lines, \
        r_lines, l_lines)
        >>> lst = s.list_states()
        >>> lst[0].p1_score == lst[1].p1_score == lst[2].p1_score
        True

        """
        l = []
        for move in self.possible_moves:
            l.append(self.give_copy(move))

        return l

    def give_copy(self, move: Any) -> "StonehengeState":
        """
        make a copy of self, apply a move,
        and return it

        >>> h_lines = [Leyline(), Leyline()]
        >>> h_lines[0].letters = ['A', 'B']
        >>> h_lines[1].letters = ['C']
        >>> l_lines = [Leyline(), Leyline()]
        >>> l_lines[0].letters = ['B']
        >>> l_lines[0].letters = ['C', 'A']
        >>> r_lines = [Leyline(), Leyline()]
        >>> r_lines[0].letters = ['A']
        >>> r_lines[0].letters = ['B', 'C']
        >>> s = StonehengeState(True, 1, 0, 0, h_lines, \
        r_lines, l_lines)
        >>> copy = s.give_copy('A')
        >>> copy.p1_score == 3
        True
        """
        s = copy.deepcopy(self)
        new_state = s.make_move(move)

        return new_state

    def check_good_move(self, move: Any) -> bool:
        """
        Check if move leads to a state where either
        p1 or p2 have won

        >>> h_lines = [Leyline(), Leyline()]
        >>> h_lines[0].letters = ['A', 'B']
        >>> h_lines[1].letters = ['C']
        >>> l_lines = [Leyline(), Leyline()]
        >>> l_lines[0].letters = ['B']
        >>> l_lines[0].letters = ['C', 'A']
        >>> r_lines = [Leyline(), Leyline()]
        >>> r_lines[0].letters = ['A']
        >>> r_lines[0].letters = ['B', 'C']
        >>> s = StonehengeState(True, 1, 0, 0, h_lines, \
        r_lines, l_lines)
        >>> s.check_good_move('A')
        True

        """
        new_state = self.give_copy(move)
        threshold = math.ceil(3 * (new_state.b_length + 1) / 2)
        return new_state.p1_score >= threshold \
               or new_state.p2_score >= threshold

    def one(self) -> str:
        """
        Return the string representation of
        a StonehengeState with a board length of one

        >>> h_lines = [Leyline(), Leyline()]
        >>> h_lines[0].letters = ['A', 'B']
        >>> h_lines[1].letters = ['C']
        >>> l_lines = [Leyline(), Leyline()]
        >>> l_lines[0].letters = ['B']
        >>> l_lines[0].letters = ['C', 'A']
        >>> r_lines = [Leyline(), Leyline()]
        >>> r_lines[0].letters = ['A']
        >>> r_lines[0].letters = ['B', 'C']
        >>> s = StonehengeState(True, 1, 0, 0, h_lines, \
        r_lines, l_lines)
        >>> string = s.one()
        >>> 'A' in string and 'B' in string and 'C' in string
        """
        h = self.get_leyline_value(self.h_lines)
        r = self.get_leyline_value(self.r_lines)
        l = self.get_leyline_value(self.l_lines)
        h_l = self.h_lines[:]

        s = """\
              {}   {}
             /   /
        {} - {} - {}
             \\ / \\
          {} - {}   {}
               \\
                {}""".format(r[0], r[1], h[0], h_l[0].letters[0],
                             h_l[0].letters[1], h[1], h_l[1].letters[0],
                             l[0], l[1])

        return s

    def two(self) -> str:
        """
        Return the string representation of a Stonehenge game
        with board length of two

        >>> h_lines = [Leyline(), Leyline(), Leyline()]
        >>> h_lines[0].letters = ['A', 'B']
        >>> h_lines[1].letters = ['C', 'D', 'E']
        >>> h_lines[2].letters = ['F', 'G']
        >>> l_lines = [Leyline(), Leyline(), Leyline()]
        >>> l_lines[0].letters = ['E', 'B']
        >>> l_lines[1].letters = ['G', 'D', 'A']
        >>> l_lines[2].letters = ['F', 'C']
        >>> r_lines = [Leyline(), Leyline(), Leyline()]
        >>> r_lines[0].letters = ['A', 'C']
        >>> r_lines[1].letters = ['B ', 'D', 'F']
        >>> r_lines[2].letters = ['E', 'G']
        >>> s = StonehengeState(True, 2, 0, 0, h_lines, \
        r_lines, l_lines)
        >>> string = s.two()
        >>> 'A' in string and 'B' in string and 'C' in string and 'D' in string
        True
        """
        h = self.get_leyline_value(self.h_lines)
        r = self.get_leyline_value(self.r_lines)
        l = self.get_leyline_value(self.l_lines)
        h_l = self.h_lines[:]

        s = """\
                {}   {}
               /   /
          {} - {} - {}   {}
             / \\ / \\ /
        {} - {} - {} - {}
             \\ / \\ / \\
          {} - {} - {}   {}
               \\   \\
                {}   {}""".format(r[0], r[1], h[0], h_l[0].letters[0],
                                  h_l[0].letters[1], r[2], h[1],
                                  h_l[1].letters[0],
                                  h_l[1].letters[1], h_l[1].letters[2], h[2],
                                  h_l[2].letters[0], h_l[2].letters[1], l[0],
                                  l[2], l[1])

        return s

    def three(self) -> str:
        """
        Return the string representation of
        a StonehengeState with a board length of three

        >>> h_lines = [Leyline(), Leyline(), Leyline(), Leyline()]
        >>> h_lines[0].letters = ['A', 'B']
        >>> h_lines[1].letters = ['C', 'D', 'E']
        >>> h_lines[2].letters = ['F', 'G', 'H', 'I']
        >>> h_lines[3].letters = ['J', 'K', 'L']
        >>> l_lines = [Leyline(), Leyline(), Leyline(), Leyline()]
        >>> l_lines[0].letters = ['I', 'E', 'B']
        >>> l_lines[1].letters = ['L', 'H', 'D', 'A']
        >>> l_lines[2].letters = ['K', 'G', 'C']
        >>> l_lines[3].letters = ['I', 'F']
        >>> r_lines = [Leyline(), Leyline(), Leyline(), Leyline()]
        >>> r_lines[0].letters = ['A', 'C', 'F']
        >>> r_lines[1].letters = ['B ', 'D', 'G', 'I']
        >>> r_lines[2].letters = ['E', 'H', 'K']
        >>> r_lines[3].letters = ['I', 'L']
        >>> s = StonehengeState(True, 3, 0, 0, h_lines, \
        r_lines, l_lines)
        >>> string = s.three()
        >>> 'A' in string and 'I' in string and 'G' in string and 'D' in string
        """
        h = self.get_leyline_value(self.h_lines)
        r = self.get_leyline_value(self.r_lines)
        l = self.get_leyline_value(self.l_lines)
        h_l = self.h_lines[:]

        s = """\
                        {}   {}
                       /   /
                  {} - {} - {}   {}
                     / \\ / \\ /
                {} - {} - {} - {}    {}
                    / \\ / \\ / \\ /     
               {} - {} - {} - {} - {}
                    \\ / \\ / \\ / \\
                 {} - {} - {} - {}   {}
                       \\   \\   \\
                        {}   {}   {}""".format(r[0], r[1], h[0],
                                               h_l[0].letters[0],
                                               h_l[0].letters[1],
                                               r[2], h[1], h_l[1].letters[0],
                                               h_l[1].letters[1],
                                               h_l[1].letters[2], r[3], h[2],
                                               h_l[2].letters[0],
                                               h_l[2].letters[1],
                                               h_l[2].letters[2],
                                               h_l[2].letters[3],
                                               h[3], h_l[3].letters[0],
                                               h_l[3].letters[1],
                                               h_l[3].letters[2], l[0],
                                               l[3], l[2], l[1])

        return s

    def four(self) -> str:
        """
        Return the string representation of
        a StonehengeState with a board length of four

        >>> h_lines = [Leyline(), Leyline(), Leyline(), Leyline(), Leyline()]
        >>> h_lines[0].letters = ['A', 'B']
        >>> h_lines[1].letters = ['C', 'D', 'E']
        >>> h_lines[2].letters = ['F', 'G', 'H', 'I']
        >>> h_lines[3].letters = ['J', 'K', 'L', 'M', 'N']
        >>> h_lines[4].letters = ['O', 'P', 'Q', 'R']
        >>> l_lines = [Leyline(), Leyline(), Leyline(), Leyline(), Leyline()]
        >>> l_lines[0].letters = ['N', 'I', 'E', 'B']
        >>> l_lines[1].letters = ['R', 'M', 'H', 'D', 'A']
        >>> l_lines[2].letters = ['Q', 'L', 'G', 'C']
        >>> l_lines[3].letters = ['P', 'K', 'F']
        >>> l_lines[4].letters = ['J', 'O']
        >>> r_lines = [Leyline(), Leyline(), Leyline(), Leyline(), Leyline()]
        >>> r_lines[0].letters = ['A', 'C', 'F', 'J']
        >>> r_lines[1].letters = ['B ', 'D', 'G', 'K', 'O']
        >>> r_lines[2].letters = ['E', 'H', 'L', 'P']
        >>> r_lines[3].letters = ['I', 'M', 'Q']
        >>> r_lines[4].letters = ['N', 'R']
        >>> s = StonehengeState(True, 4, 0, 0, h_lines, \
        r_lines, l_lines)
        >>> string = s.four()
        >>> 'Q' in string and 'P' in string
        True

        """

        h = self.get_leyline_value(self.h_lines)
        r = self.get_leyline_value(self.r_lines)
        l = self.get_leyline_value(self.l_lines)
        h_l = self.h_lines[:]

        s = """\
                               {}   {}
                              /   /
                         {} - {} - {}   {}
                            / \\ / \\ /
                       {} - {} - {} - {}   {}
                          / \\ / \\ / \\ /     
                    {} - {} - {} - {} - {}   {}
                       / \\ / \\ / \\ / \\ /
                  {} - {} - {} - {} - {} - {}
                       \\ / \\ / \\ / \\ / \\     
                    {} - {} - {} - {} - {}   {}                 
                         \\   \\   \\   \\
                          {}   {}   {}   {}""".format(r[0], r[1], h[0],
                                                      h_l[0].letters[0],
                                                      h_l[0].letters[1],
                                                      r[2], h[1],
                                                      h_l[1].letters[0],
                                                      h_l[1].letters[1],
                                                      h_l[1].letters[2], r[3],
                                                      h[2], h_l[2].letters[0],
                                                      h_l[2].letters[1],
                                                      h_l[2].letters[2],
                                                      h_l[2].letters[3],
                                                      r[4], h[3],
                                                      h_l[3].letters[0],
                                                      h_l[3].letters[1],
                                                      h_l[3].letters[2],
                                                      h_l[3].letters[3],
                                                      h_l[3].letters[4],
                                                      h[4], h_l[4].letters[0],
                                                      h_l[4].letters[1],
                                                      h_l[4].letters[2],
                                                      h_l[4].letters[3], l[0],
                                                      l[4], l[3], l[2], l[1])

        return s

    def five(self) -> str:
        """
        Return the string representation of
        a StonehengeState with a board length of five

        >>> h_lines = [Leyline(), Leyline(), Leyline(), Leyline(), Leyline(), \
        Leyline()]
        >>> h_lines[0].letters = ['A', 'B']
        >>> h_lines[1].letters = ['C', 'D', 'E']
        >>> h_lines[2].letters = ['F', 'G', 'H', 'I']
        >>> h_lines[3].letters = ['J', 'K', 'L', 'M', 'N']
        >>> h_lines[4].letters = ['O', 'P', 'Q', 'R', 'S', 'T']
        >>> h_lines[5].letters = ['U', 'V', 'W', 'X', 'Y']
        >>> l_lines = [Leyline(), Leyline(), Leyline(), Leyline(), Leyline(), \
        Leyline()]
        >>> l_lines[0].letters = ['T', 'N', 'I', 'E', 'B']
        >>> l_lines[1].letters = ['Y','S', 'M', 'H', 'D', 'A']
        >>> l_lines[2].letters = ['X', 'R', 'L', 'G', 'C']
        >>> l_lines[3].letters = ['W', 'Q', 'K', 'F']
        >>> l_lines[4].letters = ['V', 'P', 'J']
        >>> l_lines[5].letters = ['U', 'O']
        >>> r_lines = [Leyline(), Leyline(), Leyline(), Leyline(), Leyline(), \
        Leyline()]
        >>> r_lines[0].letters = ['A', 'C', 'F', 'J', 'O']
        >>> r_lines[1].letters = ['B ', 'D', 'G', 'K', 'P', 'U']
        >>> r_lines[2].letters = ['E', 'H', 'L', 'Q', 'V']
        >>> r_lines[3].letters = ['I', 'M', 'R', 'W']
        >>> r_lines[4].letters = ['N', 'S', 'X']
        >>> r_lines[4].letters = ['T', 'Y']
        >>> s = StonehengeState(True, 5, 0, 0, h_lines, \
        r_lines, l_lines)
        >>> string = s.five()
        >>> 'Y' in string and 'X' in string
        True
        """

        h = self.get_leyline_value(self.h_lines)
        r = self.get_leyline_value(self.r_lines)
        l = self.get_leyline_value(self.l_lines)
        h_l = self.h_lines[:]

        s = """\
                                      {}   {}
                                     /   /
                                {} - {} - {}   {}
                                   / \\ / \\ /
                              {} - {} - {} - {}   {}
                                 / \\ / \\ / \\ /     
                           {} - {} - {} - {} - {}   {}
                              / \\ / \\ / \\ / \\ /
                         {} - {} - {} - {} - {} - {}   {}
                            / \\ / \\ / \\ / \\ / \\ /
                       {} - {} - {} - {} - {} - {} - {}  
                            \\ / \\ / \\ / \\ / \\ / \\ 
                         {} - {} - {} - {} - {} - {}   {}
                              \\   \\   \\   \\   \\
                               {}   {}   {}   {}   {}
                         
                       """.format(r[0], r[1], h[0], h_l[0].letters[0],
                                  h_l[0].letters[1],
                                  r[2], h[1], h_l[1].letters[0],
                                  h_l[1].letters[1],
                                  h_l[1].letters[2], r[3],
                                  h[2], h_l[2].letters[0], h_l[2].letters[1],
                                  h_l[2].letters[2], h_l[2].letters[3],
                                  r[4], h[3], h_l[3].letters[0],
                                  h_l[3].letters[1], h_l[3].letters[2],
                                  h_l[3].letters[3], h_l[3].letters[4],
                                  r[5], h[4],
                                  h_l[4].letters[0],
                                  h_l[4].letters[1],
                                  h_l[4].letters[2],
                                  h_l[4].letters[3],
                                  h_l[4].letters[4],
                                  h_l[4].letters[5],
                                  h[5], h_l[5].letters[0],
                                  h_l[5].letters[1], h_l[5].letters[2],
                                  h_l[5].letters[3], h_l[5].letters[4],
                                  l[0], l[5], l[4], l[3], l[2], l[1])
        return s

if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
