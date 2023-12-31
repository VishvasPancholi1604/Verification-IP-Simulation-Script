# How to Use the script??
-----------------

- It is mendatory to set-up 3 variables in the script before using it:
  -  project_name          : Top-module Prefix
  -  working_sim_directory : path to your simulation directory
  -  testcase_directory    : path to your testcases directory

# Command Line Arguments
-------------------------

Get command line arguments from the user. Each CLArgument is optional.

## Argument Options

- **-e or --execute**
  - Options are:
    1. compile
    2. run
    3. both
    4. waveform
  - Example: `python run.py -e compile`
  - Default is 'both' if no argument is given.

- **-v or --verbosity**
  - Options are:
    1. NONE
    2. LOW
    3. MEDIUM
    4. HIGH
    5. FULL
    6. DEBUG
  - Example: `python run.py -v medium`
  - Default is 'HIGH' if no argument is given.

- **-w or --waveform**
  - Takes no argument, the user only has to mention the flag [optional].
  - If only 1 testcase is selected by the user to run, the waveform will open by default.
  - Example: `python run.py -e run -w`

- **-l or --logfile**
  - Takes no argument, the user only has to mention the flag [optional].
  - Used to create a log file of testcase/s.
  - Example: `python run.py -e run -l`

- **-n or --name**
  - Takes one argument which is the name of the testcase.
  - If enabled, the script won't ask which testcase to run.
  - Returns the list of testcases if the given testcase name is incorrect.
  - Example: `python run.py -e run -n i2c_multimaster_arbitration_test_c`

- **-db or --debug**
  - To debug the code (commands will be printed).
  - preferred to detect infinite loops in output, will print some extra debugging-info as wekk.
  - Example: `python run.py -e run -db`

- **-q or --questa**
  - To compile and/or run VIP on MentorGrafix's Questasim.
  - Example: `python run.py -e run -q`

## Work in Progress

- **-s or --status**
  - To observe the status of each testcase [pass/fail].
  - Example: `python run.py -e run -s`

- **-r or --regression**
  - To merge the functional coverage .vdb files.
  - Example: `python run.py -e run -r`
