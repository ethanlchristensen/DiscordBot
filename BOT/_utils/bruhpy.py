import sys
import time
import contextlib
import python_weather
import multiprocessing
from io import StringIO

@contextlib.contextmanager
def stdoutIO(stdout=None):
    """
    Function to route stdout to a new stdout and
    capture the output
    """
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

def execute_processed_command(program, results, debug):
    """
    Function for executing the code and capturing any output to 
    stdout
    :param program: the code to execute
    :param results: multiprocessing Manager Dict to store the stdout to
    :param debug  : to show debug messages
    """
    if debug: print(f"\nEPC called with\n{program}\n")
    with stdoutIO() as s:
        try:
            exec(f"""\n{program}\n""")
            if s.getvalue() != '': results['POST'] = ('NORMAL', '[OUTPUT]\n'+s.getvalue())
            else:results['POST'] =  ('INFO', '[INFO]: no output produced')
        except Exception as exception:
            results['POST'] = ('ERROR', "-[ERROR]: " + str(exception))

class BruhPy:
    """
    Class responsible for processing of incoming python code from the /bruh command
    """
    def __init__(self, debug=False):
        self._debug     = debug
        self._responses = [] 
        self._manager   = multiprocessing.Manager()
        self._results   = self._manager.dict()
    
    def run(self, arg, argvs):
        """
        Parse, prepare and execute the code passed in
        :param arg  : second word in the command
        :param argvs: every other word in the command
        """
        if arg == '-s':
            pre_process = f"{' '.join(argvs) if argvs else ''}".replace('#', '\n').replace('\\t', '\t').replace("“", "\"").replace("”", "\"")
            self._responses.append(('PY', pre_process))
        else: pre_process = f"{arg + ' ' + (' '.join(argvs) if argvs else '')}".replace('#', '\n').replace('\\t', '\t').replace("“", "\"").replace("”", "\"")

        # Execute the code 
        process = multiprocessing.Process(target=execute_processed_command, args=(pre_process, self._results, self._debug))
        process.start()

        # sleep while code is running
        time.sleep(2)

        # timeout after the two seconds
        if process.is_alive():
            process.terminate()
            self._responses.append(('ERROR', '-[ERROR]: valid runtime exceeded!'))
        else: self._responses.append(self._results['POST'])

        return self._responses
