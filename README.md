# CodeContests

CodeContests is a competitive programming dataset for machine-learning. This
dataset was used when training
[AlphaCode](https://deepmind.com/blog/article/Competitive-programming-with-AlphaCode). AlphaCode has been published in [Science](https://www.science.org/doi/10.1126/science.abq1158), with a preprint on [arXiv](https://arxiv.org/abs/2203.07814).

It consists of programming problems, from a variety of sources:

Site        | URL                         | Source
----------- | --------------------------- | ------
Aizu        | https://judge.u-aizu.ac.jp  | [CodeNet](https://github.com/IBM/Project_CodeNet)
AtCoder     | https://atcoder.jp          | [CodeNet](https://github.com/IBM/Project_CodeNet)
CodeChef    | https://www.codechef.com    | [description2code](https://github.com/ethancaballero/description2code)
Codeforces  | https://codeforces.com      | [description2code](https://github.com/ethancaballero/description2code) and Codeforces
HackerEarth | https://www.hackerearth.com | [description2code](https://github.com/ethancaballero/description2code)

Problems include test cases in the form of paired inputs and outputs, as well as
both correct and incorrect human solutions in a variety of languages.

## Install bazel

First [install bazel](https://docs.bazel.build/versions/main/install.html)
and verify it builds correctly (we only support Linux with clang, but other
platforms might work):

```sh
bazel build -c opt :print_names_and_sources
```

## Downloading the dataset

[Install the Cloud SDK](https://cloud.google.com/sdk/docs/quickstart), which
provides the `gsutil` utility. You can then download the full data (~3GiB) with,
e.g:

```
gsutil -m cp -r gs://dm-code_contests /tmp
```

The data consists of `ContestProblem` protocol buffers in
[Riegeli](https://github.com/google/riegeli) format. See `contest_problem.proto`
for the protocol buffer definition and documentation of its fields.

The dataset contains three splits:

Split      | Filename
---------- | ----------------------------------------
Training   | `code_contests_train.riegeli-*-of-00128`
Validation | `code_contests_valid.riegeli`
Test       | `code_contests_test.riegeli`

There is example code for iterating over the dataset in C++ (in
`print_names.cc`) and Python (in `print_names_and_sources.py`). For example, you
can print the source and name of each problem in the validation data by
[installing bazel](https://docs.bazel.build/versions/main/install.html) and then
running:

```
bazel run -c opt \
  :print_names_and_sources /tmp/dm-code_contests/code_contests_valid.riegeli
```

Or do the same for the training data with the following command (which will
print around 13000 lines of output):

```
bazel run -c opt \
  :print_names_and_sources /tmp/dm-code_contests/code_contests_train.riegeli*
```

## Executing and evaluating solutions

The `execution` subdirectory contains code for executing a solution and
evaluating whether it solves a problem. `solve_example` demonstrates this
functionality, and can be run with e.g.

```
bazel run -c opt execution:solve_example -- \
  --valid_path=/tmp/dm-code_contests/code_contests_valid.riegeli
```

Note, for the last command you should see one `Compilation failed` and two
`Compilation succeeded`, if you see three `Compilation failed` then there is
likely an issue with the Python version used, please install and try several
ones before reporting a bug.

The execution code defaults to using Python 3.9 and 2.7, located at
`/usr/bin/python3.9` and `/usr/bin/python2.7`, with standard libraries at
`/usr/lib/python3.9` and `/usr/lib/python2.7`. These can be changed with the
flags defined in `py_locations.cc`, for example:

```
bazel run -c opt execution:solve_example -- \
  --valid_path=/tmp/dm-code_contests/code_contests_valid.riegeli \
  --python3_path=/usr/bin/python3.10 --python3_library_paths=/usr/lib/python3.10
```

In Debian/Ubuntu you can install specific Python versions with

```
sudo apt install python3.9 python3.10 python3.11
```

and you can check if you have some version installed by `which` provides output:

```
which python3.11
```

Note that the Python used for building with bazel and for executing inside the sandbox can be different.

### Note on data and sandbox consistency

The incorrect and correct solutions attached to problems are not guaranteed to compile and execute in the exact same way as in their original contest website (for example different compiler versions or flags or different library versions). Some of the solutions will fail compilation, or will produce sandbox violations, especially if they are incorrect.

### FAQ

We recommend running the following before reporting bugs, which wipes out the
bazel state and sometimes fixes transient errors.

```
bazel clean --expunge
rm -rf ~/.cache/bazel
```

## Supported platforms

This repository is supported on Linux, compiled with clang.

People on MacOS have reported this error:
https://github.com/deepmind/code_contests/issues/5

Windows have reported this error:
https://github.com/deepmind/code_contests/issues/9

## Citing this work

If you use this dataset or code, please cite this paper:

```
@article{
  doi:10.1126/science.abq1158,
  author = {Yujia Li  and David Choi  and Junyoung Chung  and Nate Kushman  and Julian Schrittwieser  and R{\'e}mi Leblond  and Tom Eccles  and James Keeling  and Felix Gimeno  and Agustin Dal Lago  and Thomas Hubert  and Peter Choy  and Cyprien de Masson d’Autume  and Igor Babuschkin  and Xinyun Chen  and Po-Sen Huang  and Johannes Welbl  and Sven Gowal  and Alexey Cherepanov  and James Molloy  and Daniel J. Mankowitz  and Esme Sutherland Robson  and Pushmeet Kohli  and Nando de Freitas  and Koray Kavukcuoglu  and Oriol Vinyals },
  title = {Competition-level code generation with AlphaCode},
  journal = {Science},
  volume = {378},
  number = {6624},
  pages = {1092-1097},
  year = {2022},
  doi = {10.1126/science.abq1158},
  URL = {https://www.science.org/doi/abs/10.1126/science.abq1158},
  eprint = {https://www.science.org/doi/pdf/10.1126/science.abq1158},
  abstract = {Programming is a powerful and ubiquitous problem-solving tool. Systems that can assist programmers or even generate programs themselves could make programming more productive and accessible. Recent transformer-based neural network models show impressive code generation abilities yet still perform poorly on more complex tasks requiring problem-solving skills, such as competitive programming problems. Here, we introduce AlphaCode, a system for code generation that achieved an average ranking in the top 54.3\% in simulated evaluations on recent programming competitions on the Codeforces platform. AlphaCode solves problems by generating millions of diverse programs using specially trained transformer-based networks and then filtering and clustering those programs to a maximum of just 10 submissions. This result marks the first time an artificial intelligence system has performed competitively in programming competitions. Computer programming competitions are popular tests among programmers that require critical thinking informed by experience and creating solutions to unforeseen problems, both of which are key aspects of human intelligence but challenging to mimic by machine learning models. Using self-supervised learning and an encoder-decoder transformer architecture, Li et al. developed AlphaCode, a deep-learning model that can achieve approximately human-level performance on the Codeforces platform, which regularly hosts these competitions and attracts numerous participants worldwide (see the Perspective by Kolter). The development of such coding platforms could have a huge impact on programmers’ productivity. It may even change the culture of programming by shifting human work to formulating problems, with machine learning being the main one responsible for generating and executing codes. —YS Modern machine learning systems can achieve average human-level performance in popular competitive programming contests.}}
```

## License

The code is licensed under the
[Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).

All non-code materials provided are made available under the terms of the CC BY
4.0 license
([Creative Commons Attribution 4.0 International license](https://creativecommons.org/licenses/by/4.0/legalcode)).

We gratefully acknowledge the contributions of the following:

*   Codeforces materials are sourced from http://codeforces.com.
*   Description2Code materials are sourced from:
    [Description2Code Dataset](https://github.com/ethancaballero/description2code),
    licensed under the
    [MIT open source license](https://opensource.org/licenses/MIT), copyright
    not specified.
*   CodeNet materials are sourced from:
    [Project_CodeNet](https://github.com/IBM/Project_CodeNet), licensed under
    [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0), copyright not
    specified.

Use of the third-party software, libraries code or data may be governed by
separate terms and conditions or license provisions. Your use of the third-party
software, libraries or code may be subject to any such terms. We make no
representations here with respect to rights or abilities to use any such
materials.

## Disclaimer

This is not an official Google product.

-------------------------------------------------------------------------------

# Setup and Configuration for CS 329M:

## Introduction

First and foremost we would like to thank the team responsible for this dataset 
for their contributions.

The purpose of this project is to automate useful test case generation. 
Competitive programming problems are a natural place to start, given their 
structured and precise problem specifications, restrictions on input and output, 
and -- thanks to this dataset -- the presence of successful and unsuccessful 
attempts to solve the problem. Our ultimate goal is to build a tool that
composes useful test cases on the fly given a problem specification and
an attempt to solve the problem. A "useful" test case is one that either 
isolates a particular aspect of the problem specification or targets a
pain point that a programmer might be likely to encounter when solving the problem.

## Setup and Installation

### Configure CodeContests dataset

Firstly, follow the provided installation instructions provided by CodeContests.
Verify that you have properly downloaded the dataset and configured the bazel
workspace by (minimally) running:

```
bazel run -c opt \
  :print_names_and_sources /tmp/dm-code_contests/code_contests_valid.riegeli
```

We have added two (very similar) scripts that were needed for the dataset generation. Verify that these run with 

```
bazel run -c opt \
  :print_names_and_tests /tmp/dm-code_contests/code_contests_valid.riegeli
```

```
bazel run -c opt \
  :print_names_and_descriptions /tmp/dm-code_contests/code_contests_valid.riegeli
```

### Dataset Generation

The provided dataset consists of 130 Riegeli files:
 - 128 files in the training set, each called `code_contests_train.riegeli-00xxx-of-00128` 
where `xxx` is between `000` and `127`.
 - one file in the test set, called `code_contests_test.riegeli`
 - one file in the validation set, called `code_contests_valid.riegeli`

Each file contains roughly 110 problems' worth of data.

The first component of our pipeline involves using few-shot prompting with PaLM 
to generate candidate useful test cases for each problem, meant to target certain
components of the spec or potential pain points a developer might encounter.

Some preprocessing is required to efficiently make use of the data in text form:
Execute the bash scripts in the `bash_scripts` directory called 
`get_all_specs.sh` and `get_provided_tests.sh` to extract the problem specs 
and provided test cases from the provided .riegeli files.

Make sure to adjust the destination directory for each script!

These scripts automate the processing of the 128 training data files. To do the
same for the validation and test data files, run the following four commands:
```
bazel run -c opt   :print_names_and_descriptions /your/path/to/dm-code_contests/code_contests_valid.riegeli > /your/path/to/problem_specs/code_contests_valid_specs.txt
```
```
bazel run -c opt   :print_names_and_descriptions /your/path/to/dm-code_contests/code_contests_test.riegeli > /your/path/to/probelm_specs/code_contests_test_specs.txt
```
```
bazel run -c opt   :print_names_and_tests /your/path/to/dm-code_contests/code_contests_valid.riegeli > /your/path/to/provided_tests/code_contests_valid_tests.txt
```
```
bazel run -c opt   :print_names_and_tests /your/path/to/dm-code_contests/code_contests_test.riegeli > /your/path/to/provided_tests/code_contests_test_tests.txt
```

Once these scripts execute, you will be able to run the `llm_pipeline.py` program to 
create the candidate LLM-generate test cases. For the entire dataset, this will take 
several hours, as we must be conservatively slow to not get rate limited.

Examples for test and validation sets:
```
python3 llm_pipeline.py /path/to/problem_specs/code_contests_test.txt /path/to/llm_generation/test.txt
```
```
python3 llm_pipeline.py /path/to/problem_specs/code_contests_valid.txt /path/to/llm_generation/valid.txt
```
The bash script `generate_tests.sh` executes this command for each problem spec in the 
training set, and stores the generated test cases in a file called `train_num.txt`.

The program `extract_simtests.py` is used to parse the LLM output files and extract
the generated test cases only -- this makes it easier to isolate the test cases
and evaluate their quality.

### Funny notes

Two CodeForces April Fools challenge problems (problem 409C -- 2014 and 
1331G -- 2020) bamboozled the LLM! The problem specs were pranks, and they
were written entirely in Latin, which caused an InvalidArgument exception: 
"The requested language is not supported by models/text-bison-001".


## Contributions and Resulting Data

The resulting data is stored in three new folders:
 - `problem_specs`: This folder contains the text files with the names problem descriptions of each corresponding file in the dataset.
 - `provided_tests`: This folder contains the text files with the names and build-in test cases for each file in the CodeContests dataset.
 - `llm_generation`: This folder contains the text files with the problem names, LLM generated pain points, and LLM generated test cases for each file in the dataset. This folder also contains the subdirectory `tests_only`, which contains the text same files, omitting the pain points for easier comparison. These files can be readile compared with the provided built-in tests stored in `provided_tests`.

## Acknowledgements

Again, many thanks to the CodeContests team for their work in compiling this dataset and the software packages necesary to extract useful information.

Lastly, huge thank you to Dr. Justin Gottschlich and TA Tathagat Verma for outstanding instruction, inspiration, and guidance over the course of this quarter.
