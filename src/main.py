import subprocess
from github import Github
from dotenv import load_dotenv
import os
load_dotenv()

def write_sha(sha_str):
    with open("commit_sha.txt", "w") as f:
        f.write(sha_str)

def read_sha():
    try:
        with open("commit_sha.txt", "r") as f:
            sha_commit = f.read()
    except FileNotFoundError:
        with open("commit_sha.txt", "w") as f:
            f.write("nada")
        return "nada"
    
    return sha_commit

if __name__ == '__main__':
    token = os.getenv("GIT_API_SECRET")
    try:
        last_sha_str = read_sha()
        g = Github(token)
        branch = g.get_repo("jowtro/fr-cnbase-jxtech").get_branch("master")
        #NEW COMMIT!
        if last_sha_str != branch.commit.sha: 
            write_sha(branch.commit.sha)
            process = subprocess.run("./git_pull.sh".split(),
                shell=True, check=True)
        else:
            print("No changes detected.")
    except Exception as ex:
        print(ex)
    