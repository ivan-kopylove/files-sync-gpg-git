import logging
import os
import sys

from src import utils

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


def git_status(repo_folder):
    result = utils.execute_command_string('git status', repo_folder)
    return result


def git_commit_gpg_files(repo_folder):
    logger.info("git_commit_gpg_files - start")
    utils.execute_command_string('git add *.gpg', repo_folder)
    utils.execute_command_string('git commit -m "committed by script"', repo_folder)
    logger.info("git_commit_gpg_files - end")


def git_clone(repo_folder, git_init_url):
    logger.info("git_clone - start")
    logger.info("Cloning existing repo {} to {}", git_init_url, repo_folder)
    utils.execute_command_string('git clone ' + git_init_url + " .", repo_folder)
    logger.info("git_clone - start")


def git_pull(repo_folder):
    logger.info("git_pull - start")
    utils.execute_command_string("git pull", repo_folder)
    logger.info("git_pull - end")


def git_push(repo_folder):
    logger.info("git_push - start")
    utils.execute_command_string("git push", repo_folder)
    logger.info("git_push - end")


def git_file_pre_deleted_state_commit_hash(repo_folder, path):
    history = utils.execute_command_args(['git', 'log', '-p', '--', path], repo_folder)
    lines = history.split("\n")
    commit_hash = None
    for line in lines:
        if line.startswith("commit"):
            commit_hash = line.split(" ")[1]
        if line.startswith("index"):
            if "0000000" not in line.split("..")[1]:
                return commit_hash
    logger.info(history)
    return None


def git_get_recent_file_contents(repo_folder, path) -> bytes:
    """
    Returns previous not deleted file contents
    :param repo_folder:
    :param path:
    """
    commit_hash = git_file_pre_deleted_state_commit_hash(repo_folder, path)
    if "win" in sys.platform:
        cmd = os.environ.get('COMSPEC', 'cmd')
        command = [cmd, '/c', 'git', 'show', commit_hash + ":" + path, '|gpg', '--decrypt']
        file_contents = utils.execute_command_args_bytes(command, repo_folder)
        return file_contents
    else:
        raise NotImplementedError
