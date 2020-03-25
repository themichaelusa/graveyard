import sys 
import subprocess 
if __name__ == '__main__':
	action, target = sys.argv[1], sys.argv[2]

	# if create cluster, generate template using gen_template.py
	if action == 'create' and target == 'cluster':
		cluster_name = sys.argv[3]
		subprocess.run()

