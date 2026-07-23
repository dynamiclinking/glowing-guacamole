import subprocess
from datetime import datetime


def get_git_info():
    def run(cmd):
        return subprocess.check_output(cmd, text=True).strip()

    try:
        commit = run(["git", "rev-parse", "HEAD"])
        dirty = run(["git", "status", "--porcelain"]) != ""
        branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])

        return {
            "commit": commit,
            "branch": branch,
            "dirty": dirty
        }

    except Exception:
        return {
            "commit": "unknown",
            "branch": "unknown",
            "dirty": True
        }


def get_timestamp():
    return datetime.utcnow().isoformat()
