# Command Line Arguments

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

- **-l or --logfile**
  - Takes no argument, the user only has to mention the flag [optional].
  - Used to create a log file of testcase/s.

- **-n or --name**
  - Takes one argument which is the name of the testcase.
  - If enabled, the script won't ask which testcase to run.
  - Returns the list of testcases if the given testcase name is incorrect.

- **-s or --status**
  - To observe the status of each testcase [pass/fail].

- **-r or --regression**
  - To merge the functional coverage .vdb files.

- **-db or --debug**
  - To debug the code (commands will be printed).
  - The log file won't be created, preferred to detect infinite loops in output.

- **-q or --questa**
  - To compile and/or run VIP on MentorGrafix's Questasim.
