# IMPORTS
import sys
import subprocess 

# CONSTANTS
DARWIN_STR = 'Darwin'
DARWIN_MAX_NICE = '-20'
LINUX_MAX_NICE = '-20'

def is_macos():
	stdout = str(subprocess.check_output(['uname', '-a']))
	os_str = stdout.split(' ')[0]
	return os_str == DARWIN_STR

def exec_nice(nice_val, prog_args):
	subprocess.call(['sudo', 'nice', nice_val, *prog_args])

def run_program(prog_args):
	if is_macos():
		exec_nice(DARWIN_MAX_NICE, prog_args)
	else:
		exec_nice(LINUX_MAX_NICE, prog_args)

if __name__ == '__main__':
	run_program(sys.argv[1:])
	