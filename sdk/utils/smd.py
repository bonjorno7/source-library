'''SMD utils.'''
from typing import List
from csv import reader

SMDLine = List[str]


class SMDIterator(object):
    '''SMD iterator.'''

    def __init__(self, string) -> None:
        # type: (str) -> None
        '''Initialize SMD iterator.

        Args:
            string: SMD contents.
        '''
        lines = string.splitlines()
        # TODO: Remove comments and empty lines
        self._lines = list(reader(lines, delimiter=' '))

    def __len__(self):
        # type () -> int
        '''The amount of remaining SMD lines.'''
        return len(self._lines)

    def __next__(self):
        # type () -> SMDLine
        '''The next SMD line.'''
        return self._lines.pop(0)

    def peek(self, sentinel=None):
        # type (str) -> SMDLine
        '''Peek the next SMD line if sentinel is not found there.

        Args:
            sentinel: Token to check for.

        Returns:
            The next SMD line or None.
        '''
        if self._lines:
            if sentinel not in self._lines[0]:
                return self._lines[0]
