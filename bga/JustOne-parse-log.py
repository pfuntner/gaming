#! /usr/bin/env python3

import re
import os
import sys
import signal
import logging
import argparse

class Table(object):
    """
    A class the produces pretty tabular output - nicely alinged rows and columns
    """
    def __init__(self, *headings):
        """
        Constructor that initializes the Table class

        Args:
            headings: A list of objects for the headings of the columns.  The number
            of headings must match the number of cells in each row.
        """
        # `self.data` is a list that contains all the cells in the table, including the headings
        self.data = [ [str(heading) for heading in headings] ]

        # `self.widths` contains the widths of each column - the maximum width of each cell in a column
        self.widths = [len(heading) for heading in self.data[0]]

    def add(self, *columns):
        """
        Adds a row to the table

        Args:
            columns: A list of objects for the cells in the row.
        """

        # assure the number of cells matches the number of headings
        assert len(columns) == len(self.data[0]), f'Expected {len(self.data[0])} columns but got {len(columns)}'

        self.data.append(list(map(str, columns)))

        # recalculate the maximum columns widths
        for (column_number, column) in enumerate(self.data[-1]):
            self.widths[column_number] = max(self.widths[column_number], len(column))

    def close(self):
        """
        Completes the table and prints out all the rows (including headings) and columns aligned according to
        the maximum width of each column
        """

        for row_num in range(len(self.data)):
            print('  '.join([self.data[row_num][col_num].ljust(self.widths[col_num]) for col_num in range(len(self.data[0]))]))

parser = argparse.ArgumentParser(description='Convert a BGA raw text log for `Just One` into a summary')
parser.add_argument('path', help='Path to raw `Just One` text log')
parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger(sys.argv[0])
log.setLevel(logging.WARNING - (args.verbose or 0)*10)

signal.signal(signal.SIGPIPE, lambda signum, stack_frame: exit(0))

"""
  Sample relative log lines:

    $ grep -vP 'retracts|^You scored a point|^Unfortunately|^\d|finished giving clues|Active player is' 2022-12-26-JustOne-330297215.rawlog 
    It's time to reveal all clues: fish, piece, Potts, Dale, potato, Potato
    misterbruno decided to skip. The mystery word was "Chip"
    It's time to reveal all clues: cigarette, Container, milk, Milk, Cigarettes, Milk
    dazedbeam decided to skip. The mystery word was "Carton"
    It's time to reveal all clues: christmas, Mittens, Ice, January, season, Wonderland
    The mystery word was "Winter", now it's up to dazedbeam to decide if the guess was correct
    NikiLen thinks the mystery word is "Snow"
    It's time to reveal all clues: running, rally, drag, Nascar, Record, Galaxy
    A word "Race" is a perfect match, good job, mumrafan56!
    It's time to reveal all clues: shellfish, bubba, Cocktail, cocktail, Deveined, de-vein
    The mystery word was "Shrimp", now it's up to mumrafan56 to decide if the guess was correct
    Lajoie318 thinks the mystery word is "Seafood"
    It's time to reveal all clues: blown, sylph, Element, Tornado, tornado, Tornado
    A word "Wind" is a perfect match, good job, emptyset!
    It's time to reveal all clues: Burry, digging, Unearth, spade, spade, spade
    knitteddove decided to skip. The mystery word was "Shovel"

  I got this from game 330297215 and I was a little concerned that I got all the log I could but it appears to be incomplete.  Granted,
  I was grepping out a lot of stuff but the original file didn't have the usual landmarks at the start of the log.  The second line (just
  the last line) should be:

    Did you know?

  The last line is sort of a random message.  There may be more but I've seen the following:

    - If the game seems stopped or buggy, please refresh the webpage or press F5.
    - Have you found a bug? Please report it to the BGA bug reporting system, including a description and if possible a screenshot. Thank you.

  These were missing so I wonder if entire rounds were missing.  The reply of the game doesn't help very much but I was recording words & clues
  in a OCD-ish spreadsheet and the first word I recorded for this game was `shovel` so it seems complete but I'm not sure that's always going to
  be the case.
"""

# Example line showing mystery word when the guesser skips: 'knitteddove decided to skip. The mystery word was "Shovel"'
skipped_mystery_regexp = re.compile(r'decided to skip. The mystery word was "([^"]+)"')

# Example line showing wrong guess: 'Lajoie318 thinks the mystery word is "Seafood"'
wrong_clue_regexp = re.compile(r'thinks the mystery word is "([^"]+)"')

# Example line showing mystery word when the guess was wrong: 'The mystery word was "Winter", now it's up to dazedbeam to decide if the guess was correct'
wrong_mystery_regexp = re.compile(r'^The mystery word was "([^"]+)"')

# Example line showing mystery word when the guess was right: 'A word "Wind" is a perfect match, good job, emptyset!'
right_mystery_regexp = re.compile(r'^A word "([^"]+)" is a perfect match, good job, ')

# Example line showing clues: "It's time to reveal all clues: fish, piece, Potts, Dale, potato, Potato"
clues_regexp = re.compile(r'^It\'s time to reveal all clues:\s+(.+)$')

if os.path.exists(args.path):
  if not os.path.isdir(args.path):
    with open(args.path) as stream:
      lines = stream.read().splitlines()

    number_of_clues = None
    word_tuples = list()

    pos = len(lines)-1
    while pos >= 0:
      (mystery_word, guessed_word, clues) = (None, None, list())
      line = lines[pos]

      # look to see if the guesser skipped and elected to not guess what a mystery word is
      match = skipped_mystery_regexp.search(line)
      if match:
        mystery_word = match.group(1)
      else:
        # look to see if the guess was wrong about the mystery word
        match = wrong_clue_regexp.search(line)
        if match:
          guessed_word = match.group(1)
          while pos >= 0:
            line = lines[pos]
            match = wrong_mystery_regexp.search(line)
            if match:
              mystery_word = match.group(1)
              break
            pos -= 1
          assert mystery_word and pos >= 0, f'Failed to find mystery word when guess was {guessed_word!r}'
        else:
          # look to see if the guess was correct about the mystery word
          match = right_mystery_regexp.search(line)
          if match:
            mystery_word = match.group(1)
            guessed_word = match.group(1)

      if mystery_word:
        # now that we know the mystery word, find all the clues
        while pos >= 0:
          line = lines[pos]
          match = clues_regexp.search(line)
          if match:
            clues = match.group(1).split(', ')
            log.info(f'{pos:3} {line!r} mystery={mystery_word!r} guess={guessed_word!r} clues={clues}')

            number_of_clues = len(clues)
            word_tuples.append([mystery_word, guessed_word] + clues)

            break
          pos -= 1
        assert clues and pos >= 0, f'Failed to find clues when mystery word was {mystery_word!r}'

      log.debug(f'{pos:3} {line!r} mystery={mystery_word!r} guess={guessed_word!r} clues={clues}')
      pos -= 1

    if number_of_clues:
      columns = ['Word number', 'Mystery word', 'Guess']
      for num in range(number_of_clues):
        columns.append(f'Clue #{num}')
      table = Table(*columns)

      for (word_num, word_tuple) in enumerate(word_tuples):
        table.add(*([word_num+1] + word_tuple))

      table.close()
  else:
    parser.error(f'Not a regular file: {args.path!r}')
else:
  parser.error(f'Could not find {args.path!r}')
