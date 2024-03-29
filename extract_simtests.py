'''
Use this program to iterate through the output files generated by
llm_generation.py (stored in dir_path) to isolate the generated test cases
and store them in create_dir
'''

import sys
import os

dir_path = '/home/isaacgor216/CS329M/code_contests/llm_generation'
create_dir = 'tests_only'

if __name__ == "__main__":
    for filename in os.listdir(dir_path):
        try:
            os.mkdir(os.path.join(dir_path, create_dir))
        except OSError as error:
            pass

        read_path = os.path.join(dir_path, filename)
        write_path = os.path.join(dir_path, create_dir, filename)

        # If simulated tests have already been extracted
        if os.path.isfile(write_path):
            continue

        if os.path.isfile(read_path):
            with open(write_path, 'w') as wf:
                with open(read_path) as rf:
                    line = rf.readline()
                    inputs_flag = False
                    while line:
                        if "Title:" in line:
                            inputs_flag = False
                            wf.write(rf.readline())
                        if inputs_flag:
                            wf.write(line)
                        if "Pain points:" in line:
                            inputs_flag = False
                        if "Test inputs:" in line:
                            inputs_flag = True
                        
                        line = rf.readline()

            
    
