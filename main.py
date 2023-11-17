import os, argparse, subprocess, time, json

# prints commands getting fired on
# terminal if debug mode is on
debug_mode = True

# do not execute the simulation file
# if compilation failed..
# holds the status of compilation for VIP
compilation_status = True

# defaults
project_name  = 'i2c'
top_name      = f'ei_{project_name}_top.sv'
verbosity     = 'HIGH'
timescale     = '1ns/1ps'
exec_command  = 'both'
log_output    = 'outputs'
database_path = 'database'
vdb_path      = 'vdb_files'
wavepath      = 'wave_files'
json_directory = 'DATABASE'
testcases_status_file = 'testcases_status_database.json'

# setting up paths
working_sim_directory = '/home/vishvas.pancholi/Desktop/UVM/VIPs/I2C_NEW/GIT/UVM_I2C/DEVELOPMENT/SIM'
testcase_directory    = '/home/vishvas.pancholi/Desktop/UVM/VIPs/I2C_NEW/GIT/UVM_I2C/DEVELOPMENT/TEST'

# testcase database path
# testcase database dictionary
testDB_path = os.path.join(working_sim_directory, json_directory, testcases_status_file)
testDB_json = {}

# ignore testcases during simulation
# testcases present in below list will be 
# ignored in regression
ignore_testcases = ['ei_i2c_10bit_addressing_repeated_start_test_c']

# list for passed and failed testcases
passed_testcases = failed_testcases = []

# synopsys VCS commands
vcs_commands = {
    'compile'   : 'vcs -full64 -debug_access+r -sverilog -debug_access+r+w+nomemcbk -debug_region+cell +vpi +incdir+/home/hitesh.patel/UVM/UVM_1.2/src /home/hitesh.patel/UVM/UVM_1.2/src/uvm.sv /home/hitesh.patel/UVM/UVM_1.2/src/dpi/uvm_dpi.cc -CFLAGS -DVCS -assert svaext '
                  + f'-timescale={timescale} '
                  + '+incdir+../RTL/ +incdir+../ENV/ +incdir+../TEST/ +incdir+../SRC ../TOP/'
                  + f'{top_name}'
                  + ' +vcs+lic+wait',
    'simulate'  : './simv'
}

# MentorGraphics Questasim commands
questa_commands = {
    'compile'  : 'vlog ..\SRC\ei_i2c_package.sv ..\TOP\ei_i2c_top.sv +incdir+..\SRC +incdir+..\ENV +incdir+..\TEST',
    'simulate' : f'vsim {top_name[:-3]} -32 -do \"run -all; exit\" '
}

# Get command line arguments from user [each CLArguments are optional]
# argument options are [NOTE- any switch can be used with eachother]:
#   -e or --execute
#     - Options are
#       1. compile
#       2. run
#       3. both
#       4. waveform
#     - i.e. for compilation command is 'python run.py -e compile'
#     - default is 'both' if no argument is given
#   -v or --verbosity
#     - Options are
#       1. NONE
#       2. LOW
#       3. MEDIUM
#       4. HIGH
#       5. FULL
#       6. DEBUG
#     - i.e. for Medium verbosity command is 'python run.py -v medium'
#     - default is 'HIGH' if no argument is given
#   -w  or --waveform
#     - takes no argument, user only has to mention the flag [optional]
#     - if only 1 testcase is selected by user to run, waveform will open by default
#   -l  or --logfile
#     - takes no argument, user only has to mention the flag [optional]
#     - used to create log file of testcase/s
#   -n  or --name
#     - takes one argument which is the name of the testcase
#     - if enabled, script won't ask which testcase to run.
#     - returns the list of testcases if given testcase name is incorrect
#   -s  or --status
#     - to observe the status of each testcase [pass/fail]
#   -r  or --regression
#     - to merge the functional coverage .vdb files
#   -db or --debug
#     - to debug the code (commands will be printed)
#     - log file won't be created, preffered to detect infinite loops in output
#   -q  or --questa
#     - to compile and/or run VIP on MentorGrafix's Questasim
def get_args():
    global args
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-e', '--execute',
                        help='type of execution (enter number): \n1. compile\n2. run\n3. compile & '
                             'run\n4. waveform')
    parser.add_argument('-v', '--verbosity',
                        help='Verboisty type: \n1. NONE\n2. LOW\n3. MEDIUM\n4. HIGH\n5. FULL\n6. DEBUG')
    parser.add_argument('-w', '--waveform', action='store_true',
                        help='to open waveform (can only run one testcase at a time)')
    parser.add_argument('-l', '--logfile', action='store_true', help='to create log files of output')
    parser.add_argument('-n', '--testname',
                        help='to give testname from CLI input')
    parser.add_argument('-s', '--status', action='store_true',
                        help='to see the status of each selected testcase at the end of simulation')
    parser.add_argument('-r', '--regression', action='store_true',
                        help='to merge the functional coverage of each testcases')
    parser.add_argument('-db', '--debug', action='store_true',
                        help='debug mode prints commands')
    parser.add_argument('-q', '--questa', action='store_true', help='to compile/run in questasim')
    args = parser.parse_args()

# fire command to terminal
def fire_cmd(execute_this = '', logFile = '', testStatus = False):
    global debug_mode
    testcase_state = 'None'

    if debug_mode == True:
        print(execute_this)
    if logFile == '':
        process = subprocess.Popen(execute_this, shell=True, cwd=working_sim_directory, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
        for line in process.stdout:
            print(line, end='')
            if testStatus == True:
                if 'TEST PASS' in line:
                    testcase_state = 'PASS'
                elif 'TEST FAIL' in line:
                    testcase_state = 'FAIL'
        process.wait()
        return process, testcase_state
    else:
        logPath = os.path.join(working_sim_directory, log_output, logFile)
        with open(logPath, 'w') as logOutput:
            process = subprocess.Popen(execute_this, shell=True, cwd=working_sim_directory, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
            for line in process.stdout:
                if args.debug == True:
                    print(line, end='')
                if testStatus == True:
                    if 'TEST PASS' in line:
                        testcase_state = 'PASS'
                    elif 'TEST FAIL' in line:
                        testcase_state = 'FAIL'
                logOutput.write(line)
            process.wait()
            return process, testcase_state

# creates compilation command
# based on simulator selected and
# and executes on terminal
def compile():
    global compilation_status
    if args.questa == False:
        output, _ = fire_cmd(vcs_commands['compile'])
    else:
        output, _ = fire_cmd(questa_commands['compile'])
    if output.returncode == 0:
        compilation_status = True
    else:
        print()
        print('*********************')
        print('Compilation failed!!')
        compilation_status = False

# creates simulation command
# based on simulator selected, testcase name, verbosity
# and other commandline argument provided and
# executes on the terminal
def simulate_test(testname, verbosity, clargs = ''):
    global testDB_path, testDB_json

    uvm_runtime_command =  f' +UVM_TESTNAME={testname} +UVM_VERBOSITY={verbosity} {clargs}'
    logFile = '' if args.logfile == False else f"{testname[:-len('_c')]}.log"
    testStatus = 'NONE'

    print(f'Running Testcase : {testname},\t', end='')

    start_time = time.time()
    if args.questa == False:
        output, testStatus = fire_cmd(vcs_commands['simulate'] + uvm_runtime_command, logFile, testStatus=True)
    else:
        output, testStatus = fire_cmd(questa_commands['simulate'] + ' -c' + uvm_runtime_command, logFile, testStatus=True)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f'Test status : {testStatus},\t', end='')
    print(f'Elapsed time : {elapsed_time}')

    # update json database and json file
    testDB_json.update({testname : {'test status' : testStatus,'execution time' : elapsed_time}})

    writeJSONfile(testDB_path, testDB_json)

# creates waveform command
# based on simulator selected, testcase name, verbosity
# and other commandline argument provided and
# executes on the terminal
def waveform(testname, verbosity = verbosity, clargs = ''):
    uvm_runtime_command = f' +UVM_TESTNAME={testname} +UVM_VERBOSITY={verbosity} ' \
                          f'{clargs}'
    print(f'Opening waveforms for \'{testname}\'')
    if args.questa == False:
        output, _ = fire_cmd(vcs_commands['simulate'] + uvm_runtime_command + ' -gui &')
    else:
        output, _ = fire_cmd(questa_commands['simulate'] + uvm_runtime_command)

# prints the list of testcases
def print_testcases(testcase_list):
    print()
    print('Written Testcases are:')
    for i in range(0, len(testcase_list)):
        print(str(i + 1) + '. ' + testcase_list[i])
    print()

# extracts testcase names from 'TEST'
# directory provided in the argument
# appends '_c' at last and removes .sv extension
# class name must be same as file name
# (excluding '_c')
def extract_testcases(folder_path):
    testcase_list = []
    for file in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file)):
            testname = file.split('.')[0]
            if testname not in ignore_testcases and 'base_test' not in testname:
                testcase_list.append(testname + '_c')
    if len(testcase_list) == 0:
        testcase_list.append(f'ei_{project_name}_base_test_c')
    return testcase_list

# load data from json file
def readJSONfile(testDB_path):
    testDB_json = {}
    if os.path.isfile(testDB_path) and os.path.getsize(testDB_path):
        with open(testDB_path, 'r') as jsonFile:
            testDB_json = json.load(jsonFile)
    return testDB_json

# dump testcases data into json file
def writeJSONfile(testDB_path, testDB_json):
    with open(testDB_path, 'w') as jsonFile:
        json.dump(testDB_json, jsonFile, indent=2)

# asks user which waveform to observe to
# if multiple testcases are simulated
# only one testcase waveform should be opened
# at a time to prevent liscencing issues
def ask_for_wave_selection():
    if args.waveform == True:
        print_testcases(testcases)
        run_test_input = input('select any testcase from above to observe waveform: ')
        if run_test_input != '':
            waveform(testcases[int(run_test_input) - 1])

# defines which testcases to run and
# runs each testcases selected sequentially
def test_selection_method():
    global verbosity
    verbosity = str(args.verbosity).upper() if str(args.verbosity).upper() != 'NONE' else 'HIGH'
    test_name = str(args.testname)
    if args.testname == None:
        print_testcases(testcases)
        run_test_input = input('Enter Testcase number seperated by comma to run '
                               '(\'all\' to run each testcase): ')
        if run_test_input != '':
            if run_test_input == 'all':
                for testname in testcases:
                    simulate_test(testname, verbosity)
            else:
                run_test_input = run_test_input.split(',')
                for test in run_test_input:
                    if ':' in test:
                        test = test.split(':')
                        for idx in range(int(test[0]), int(test[1])+1):
                            simulate_test(testcases[idx - 1], verbosity)
                    else:
                        simulate_test(testcases[int(test) - 1], verbosity)
            ask_for_wave_selection()
        else:
            simulate_test(f'ei_{project_name}_base_test_c', verbosity)
            if args.waveform == True:
                waveform(f'ei_{project_name}_base_test_c')
    else:
        if test_name in testcases:
            simulate_test(test_name, verbosity)
            if args.waveform == True:
                waveform(test_name)
        else:
            print(f'Invalid testcase name {test_name}. '
                  f'Valid testcases are listed below: ')
            print_testcases(testcases)

# main method
# decides which commands to fire on higher level
# i.e. compile, simulate, observe waves etc
def main_execution_method():
    global exec_command, debug_mode
    global json_directory, testDB_path, testDB_json

    exec_command = str(args.execute) if str(args.execute) != 'None' else 'both'
    debug_mode = True if args.debug == True else False

    os.makedirs(os.path.join(working_sim_directory, log_output), exist_ok=True)

    json_directory = os.path.join(working_sim_directory, json_directory)
    os.makedirs(json_directory, exist_ok=True)

    # load data from json file
    testDB_json = readJSONfile(testDB_path)

    if exec_command == 'compile':
        compile()
    elif exec_command == 'run':
        test_selection_method()
    elif exec_command == 'both':
        compile()
        if compilation_status != False:
            test_selection_method()
    elif exec_command == 'waveform':
        print_testcases(testcases)
        run_test_input = input('select any testcase from above to observe waveform: ')
        if run_test_input != '':
            waveform(testcases[int(run_test_input) - 1])
    else:
        print('Invalid Command. use \'-help\' for help regarding optional arguments and commands')

# get command line arguments
get_args()

# extract testcases from test directory
testcases = extract_testcases(testcase_directory)

# main execution phase
main_execution_method()

