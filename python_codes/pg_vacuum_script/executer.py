'''
Short Description:
        This script will execute VACUUM Script.

Parameter Details:
        1) Git Repo Name to clone 
        2) Git Branch Name 
        3) R53 Host Name of RDS Instance
        4) detailsFile
        5) script

# Step 1 : Importing require modules
        module gitpython                        : to do all git commands usjing python
	module os                               : to pass arguments from environment
	module json                             : to read JSON file
	module argparse                         : to reading command line arguments
	module subprocess       		: to run the python script inside this script

# Step 2 : Difining classes CloneProgress and GitCloneExecuter

# Step 3 : Class : CloneProgress
        Method update           : Will display the progress of the git clone

# Step 4 : Class : GitCloneExecuter
        Method Constructor      : Initialize all the Class objects
        Method gitClone         : Git Clone if new Repo
                                : Git Pull if repo already exsists
                                : Call CloneProgress.update for progress
                                : Reads the JSON file to get Job details
        Method jobExecuter      :Will execute the python script to run the job against Host details provided
'''
import git
import os
import json
import argparse
import subprocess
from subprocess import PIPE
#from git import RemoteProgress
#from getpass import getpass


class CloneProgress(git.RemoteProgress):
        def update(self, op_code, cur_count, max_count=None, message=''):
                if message:
                        print(message)

class GitCloneExecuter(object):
        def __init__(self,gitRepo,gitBranch):
                self.gitURL                             = 'https://github.com/vigneshpalanivelr/' + gitRepo + '.git'
                self.gitDIR                             = '/root/' + gitRepo
                self.gitBranch                          = gitBranch
                self.scriptDIR                          = self.gitDIR + '/python_codes/pg_vacuum_script/'
                project_dir                             = os.path.dirname(os.path.abspath(__file__))
                os.environ['GIT_ASKPASS']               = ''.join((project_dir, '/askpass.py'))
                os.environ['GIT_USERNAME']              = "vigneshpalanivelr"
                os.environ['GIT_PASSWORD']              = "Vicky@03"
                #os.environ['GIT_PASSWORD']             = getpass()

        def gitClone(self,host,detailsFile,script):
                try:
                        git.Repo.clone_from(self.gitURL, self.gitDIR, branch=self.gitBranch, progress=CloneProgress())
                except Exception as e:
                        git.Repo(self.gitDIR).remotes.origin.pull()

                with open(self.scriptDIR + detailsFile, 'r') as json_data:
                        all_data             = json.load(json_data)
                        self.database        = all_data[host]["database"]
                        self.username        = all_data[host]["username"]
                        self.password        = all_data[host]["password"]
                        self.job             = all_data[host]["job"]
                        self.schema          = all_data[host]["schema"]
                        self.table           = all_data[host]["table"]
                exe.jobExecuter(host,script)

        def jobExecuter(self,host,script):
                try:
                        sub_proc        = subprocess.Popen(["python", self.scriptDIR + script, host, self.database, self.username, self.password, "--job", self.job, "--schema", self.schema, "--table", self.table])
                        stdout, stderr  = sub_proc.communicate()
                except Exception as e:
                        print e
                except JobTimeoutException:
                        raise
                finally:
                        if sub_proc.poll() is None:
                                sub_proc.kill()
                                stdout, stderr = sub_proc.communicate()

if __name__ == '__main__':
        parser          = argparse.ArgumentParser(description = 'Fetching DB details')
        parser.add_argument('gitRepo',          action='store', help='Git Repo Name')
        parser.add_argument('gitBranch',        action='store', help='Git Branch')
        parser.add_argument('host',             action='store', help='R53 Host Address')
        parser.add_argument('detailsFile',      action='store', help='DB / Host details JSON File')
        parser.add_argument('script',           action='store', help='Name of the script to execute')
        args            = parser.parse_args()
        gitRepo         = args.gitRepo
        gitBranch       = args.gitBranch
        host            = args.host
        detailsFile     = args.detailsFile
        script          = args.script
        
        exe             = GitCloneExecuter(gitRepo,gitBranch)
        exe.gitClone(host,detailsFile,script)
