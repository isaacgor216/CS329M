# Copyright 2022 DeepMind Technologies Limited
#
# This is a very basic modification of the provided
# print_names_and_sources.py to extract the provided tests as well

"""A simple tool to iterate through the dataset, printing the name, source, 
   entire set of test cases stored for each problem.

Example usage:

  print_names_and_tests /path/to/dataset/code_contests_train*
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


def _print_names_and_tests(filenames):
  """Prints the names and sources of all ContestProblems in filenames."""
  for problem in _all_problems(filenames):
    print(
        contest_problem_pb2.ContestProblem.Source.Name(problem.source),
        problem.name)
    for test in problem.public_tests:
        print(test.input)
    for test in problem.private_tests:
        print(test.input)


if __name__ == '__main__':
  _print_names_and_tests(sys.argv[1:])
