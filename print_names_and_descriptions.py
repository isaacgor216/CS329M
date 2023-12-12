# Copyright 2022 DeepMind Technologies Limited
#
# This is a very basic modification of the provided
# print_names_and_sources.py to extract the full problem specs as well

"""A simple tool to iterate through the dataset, printing the name, source, 
   and full problem description.

Example usage:

  print_names_and_descriptions /path/to/dataset/code_contests_train*
"""

import io
import sys

import riegeli

import contest_problem_pb2


def _all_problems(filenames):
  """Iterates through all ContestProblems in filenames."""
  for filename in filenames:
    reader = riegeli.RecordReader(io.FileIO(filename, mode='rb'),)
    for problem in reader.read_messages(contest_problem_pb2.ContestProblem):
      yield problem


def _print_names_and_descriptions(filenames):
  """Prints the names and sources of all ContestProblems in filenames."""
  for problem in _all_problems(filenames):
    print(
        contest_problem_pb2.ContestProblem.Source.Name(problem.source),
        problem.name)
    print(problem.description)


if __name__ == '__main__':
  _print_names_and_descriptions(sys.argv[1:])
