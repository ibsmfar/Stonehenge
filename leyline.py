"""A Leyline to be used in a game of Stonehenge"""
from typing import Union
class Leyline:
    """
    A Leyline has a value, either the number of the leyline
    or the number (as a string) of the player who captured it.
    Its letters are a list of letters that are to be captured
    or letters denoted by the number (as a string) of the player who
    captured it

    value: Union[int, str]
    letters: Union[int, str]

    """
    def __init__(self, value: Union[int, str]) -> None:
        """
        Initialize a leyline with value and an empty list of letters

        >>> ley = Leyline(1)
        >>> ley.value
        1
        >>> ley.letters
        []

        """

        self.value = value
        self.letters = []


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
