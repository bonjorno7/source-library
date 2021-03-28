'''SMD utils.'''
from typing import List
from csv import reader

SMDCommand = List[str]


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
        self._commands = list(reader(lines, delimiter=' '))

    def __len__(self):
        # type () -> int
        '''The amount of remaining SMD commands.'''
        return len(self._commands)

    def __next__(self):
        # type () -> SMDCommand
        '''The next SMD command.'''
        return self._commands.pop(0)

    def peek(self, sentinel=None):
        # type (str) -> SMDCommand
        '''Peek the next SMD command if sentinel is not found there.

        Args:
            sentinel: Token to check for.

        Returns:
            The next SMD command or None.
        '''
        if self._commands:
            if sentinel not in self._commands[0]:
                return self._commands[0]
