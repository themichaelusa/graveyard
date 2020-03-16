import sys
from random import randint

# SOURCE: https://stackoverflow.com/questions/2673385/how-to-generate-random-number-with-the-specific-length-in-python
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return str(randint(range_start, range_end))

def decomp(int_str):
	results = []
	recursive_decomp(int_str, results)
	return ((r for r in results), len(results))

def recursive_decomp(int_str, results):
	decomp_int_str = list(int_str)
	if len(decomp_int_str) is 1:
		return 
	
	decomp_ints = [int(s) for s in decomp_int_str]
	decomp_sum = sum(decomp_ints)
	results.append((decomp_ints, decomp_sum))
		
	return recursive_decomp(str(decomp_sum), results)

if __name__ == '__main__':
	#sdecomp_int_str = list(sys.argv[1])
	cmd_or_num = sys.argv[1]

	# cmd
	if cmd_or_num == '--randn':
		#print('num len', len(sys.argv[2]))
		results, len_results = decomp(random_with_N_digits(int(sys.argv[2])))
		print(len_results)
	else:
		print('num len', len(sys.argv[1]))
		print(decomp(sys.argv[1]))
