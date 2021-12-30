import subprocess
from github import Github
from dotenv import load_dotenv
from util.log import LoggerX
import schedule
import os
import time
from pathlib import Path

script_path = str(Path(os.getcwd()).parent.absolute())
# reads .env file from project root ./
load_dotenv()

LoggerX().create_rotating_log("./git_hook.log", "jx-githook")
log_info = LoggerX().logger.info
log_warn = LoggerX().logger.warning
log_err = LoggerX().logger.error
log_critical = LoggerX().logger.critical


@LoggerX()
def write_sha(sha_str, repo_name):
    with open(f"{repo_name}.txt", "w") as f:
        f.write(sha_str)


@LoggerX()
def read_sha(repo_name):
    try:
        with open(f"{repo_name}.txt", "r") as f:
            sha_commit = f.read()
    except FileNotFoundError:
        with open(f"{repo_name}.txt", "w") as f:
            f.write("nada")
        return "nada"

    return sha_commit


def check_git(repo_str, repo_name, path, branch="master"):
    """Compare latest commit's sha with a stored one if is different
        does a git pull.

    Args:
        repo_str (str): repository user/repo path
        repo_name (str): repository name
        path (str): file path
        branch (str, optional): branch. Defaults to "master".
    """
    token = os.getenv("GIT_API_SECRET")  # Token necessary token for github
    git = None
    try:
        log_warn(f"[{repo_name}] ---------------- Running script")
        last_sha_str = read_sha(repo_name)  # get last commit sha
        git = Github(token)
        print(repo_str)
        # get info from branch
        branch = git.get_repo(repo_str).get_branch(branch)
        # compare commit sha strings (gets current sha > branch.commit.sha)
        if last_sha_str != branch.commit.sha:
            # NEW COMMIT!
            print(f"new commit! {branch.commit.sha}")
            log_info(f"{repo_name}] New commit detected.")

            write_sha(branch.commit.sha, repo_name)
            log_info(f"{repo_name} running bash")
            # run a script that does git pull on specific dir
            proc = subprocess.run(
                [f"./{script_path}/git_pull.sh", path], capture_output=True
            )

            log_info(f"{repo_name} {proc}")
        else:
            log_info(f"[{repo_name}] No changes detected.")

    except Exception as ex:
        log_err(repo_str, ex)
    finally:
        log_warn(f"[{repo_name}] ---------------- End Script")


if __name__ == "__main__":
    schedule.every(30).seconds.do(
        check_git,
        "jowtro/fr-cnbase-jxtech",
        "fr-cnbase-jxtech",
        "/home/pi/work/fr-cnbase-jxtech",
    )

    schedule.every(30).seconds.do(
        check_git,
        "jowtro/bnance_jxtech",
        "bnance_jxtech",
        "/home/pi/work/bnance_jxtech",
    )

    # Run cron
    while True:
        schedule.run_pending()
        time.sleep(2)
