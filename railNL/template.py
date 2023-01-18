"""
Template to run files for a long time
Replace "99999" with desired total seconds if to be run for x amount of time
Insert filename at [insert_filename].py
Run in terminal and append a textfile by using ">> [name_of_textfile].txt"
"""


import subprocess
import time

start = time.time()
n_runs = 0

print("total runs @ EOF")

while time.time() - start < 99999:
    subprocess.run(["python3", "[insert_filename].py"])
    n_runs += 1

print(f"runs completed: {n_runs}")
