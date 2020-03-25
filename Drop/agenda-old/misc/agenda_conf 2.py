import subprocess

KSPRAY_GIT = 'https://github.com/kubernetes-incubator/kubespray.git'

if __name__ == '__main__':
	subprocess.run(['git', 'clone', KSPRAY_GIT])