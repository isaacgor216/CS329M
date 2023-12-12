# Created by Isaac Gorelik and Aaron Li for the CS 329M Competitive Testing project
# 
'''
This program parses a text file (passed in as the first argument)
containing CodeContests problem names and their full problem specifications

For each problem, PaLM is queried in an attempt to generate useful test cases
which capture a potential pain point that a programmer might experience when 
attempting to solve the problem.

To generate the text file inputs, use the script get_all_specs.sh
'''

import sys
import google.generativeai as palm
import asyncio

API_KEY = "your-palm-api-key-goes-here"
palm.configure(api_key=API_KEY)

# This is required to circumvent getting rate limited by the PaLM API.
# This delay is conservative (makes this script take roughly 8 min per file),
# but it is still considerably faster than the serialized version
AVG_PAUSE_BETWEEN_REQUESTS = 5

SOURCES = [
    "UNKNOWN_SOURCE ",
    "CODECHEF ",
    "CODEFORCES ",
    "HACKEREARTH ",
    "CODEJAM ",
    "ATCODER ",
    "AIZU ",
]

def is_prob_name(line):
    for source in SOURCES:
        if line.startswith(source):
            return True
    return False

def palm_pipeline(title, problem_dict):

    # Uncomment these block to process code_contests_train_00002.txt and 
    # code_contests_train_00057.txt which contains specs entirely in Latin:

    # if "CODEFORCES 409_C." in title:
    #     problem_dict[title].append("April fools problem")
    #     problem_dict[title].append("No test cases")
    #     return

    # if "CODEFORCES 1331_G." in title:
    #     problem_dict[title].append("April fools problem")
    #     problem_dict[title].append("No test cases")
    #     return
    
    spec = problem_dict[title][0]
    print(title)
    prompt = "I would like you to list the most important possible problems and bugs that a developer may encounter when solving this problem:\n"
    prompt += spec

    response = palm.generate_text(prompt=prompt)
    pain_points = response.result
    
    problem_dict[title].append(pain_points)

    new_prompt = "I will now give you a problem spec and a list of important problems a developer needs to consider when solving it.\n"
    new_prompt += "Given this information, please generate program inputs that will validate whether an implementation meets each of these requirements:\n"
    new_prompt += spec
    new_prompt += "\nKey potential problems:\n"
    new_prompt += pain_points if pain_points else "Pain points missing."
    new_prompt += "\nIn your response, include ONLY the program inputs and nothing else.\n"

    response = palm.generate_text(prompt=new_prompt)
    candidate_inputs = response.result
    problem_dict[title].append(candidate_inputs)
    return

async def async_wrapper(title, problem_dict, delay):
    await asyncio.sleep(delay)
    loop = asyncio.get_running_loop()

    result = await loop.run_in_executor(None, palm_pipeline, title, problem_dict)
    return result

async def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("usage: llm_pipeline source_file [dest_file]")
        quit()

    specs = []
    titles = []
    with open(sys.argv[1], "r") as f:
        spec = ""
        line = ""
        title = ""
        while line := f.readline():
            if is_prob_name(line):
                titles.append(line)
                if spec != "":
                    specs.append(title + spec)
                    spec = ""
                title = line
            else:
                spec += line
        specs.append(title + spec)

    problem_dict = {}
    for title, spec in zip(titles, specs):
        problem_dict[title] = [spec]

    tasks = [async_wrapper(title, problem_dict, AVG_PAUSE_BETWEEN_REQUESTS * i) for i, title in enumerate(titles)]
    await asyncio.gather(*tasks)
    
    if len(sys.argv) == 3:
        with open(sys.argv[2], "w") as f:
            for key, val in problem_dict.items():
                f.write("\nTitle:\n" + key)
                f.write("\nPain points:\n" + (val[1] if val[1] else ""))
                f.write("\nTest inputs:\n" + (val[2] if val[2] else ""))

    else:
        for key, val in problem_dict.items():
            print("\nTitle:\n" + key)
            print("\nPain points:\n" + (val[1] if val[1] else ""))
            print("\nTest inputs:\n" + (val[2] if val[2] else ""))

if __name__ == "__main__":
    asyncio.run(main())
