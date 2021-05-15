import subprocess
from github import Github
from dotenv import load_dotenv
from util.log import LoggerX
import schedule
import os
import time

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
    token = os.getenv("GIT_API_SECRET")
    g = None
    try:
        log_warn(f"[{repo_name}] Running script")
        last_sha_str = read_sha(repo_name)
        g = Github(token)
        print(repo_str)
        branch = g.get_repo(repo_str).get_branch(branch)

        if last_sha_str != branch.commit.sha:
            # NEW COMMIT!
            print(f"new commit! {branch.commit.sha}")
            log_info(f"{repo_name}] New commit detected.")
            write_sha(branch.commit.sha, repo_name)
            subprocess.run(f"./src/git_pull.sh {path}", shell=True, check=True)
        else:
            log_info(f"[{repo_name}] No changes detected.")

    except Exception as ex:
        log_err(repo_str, ex)
    finally:
        log_warn(f"[{repo_name}] End Script")


if __name__ == "__main__":
    schedule.every(1).minutes.do(
        check_git, "jowtro/fr-cnbase-jxtech", "fr-cnbase-jxtech", "/home/jonnas/4fun/fr-cnbase-jxtech"
    )

    schedule.every(1).minutes.do(check_git, "jowtro/bnance_jxtech", "bnance_jxtech", "/home/jonnas/4fun/bnance_jxtech")

    # Run cron
    while True:
        schedule.run_pending()
        time.sleep(2)
