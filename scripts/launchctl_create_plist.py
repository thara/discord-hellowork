import os
import sys
import plistlib
import subprocess
from pathlib import Path

# Add the parent directory to the sys.path so we can import env.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env import DISCORD_TOKEN

from launchctl_config import PLIST_LABEL, PLIST_PATH, LOG_DIR


def create_plist(
    working_dir, program_path, program_args, stdout_path, stderr_path, environment_vars
):
    plist_dict = {
        "Label": PLIST_LABEL,
        "WorkingDirectory": working_dir or "/tmp",
        "ProgramArguments": [program_path] + (program_args or []),
        "RunAtLoad": True,
        "KeepAlive": True,
        "StandardOutPath": stdout_path,
        "StandardErrorPath": stderr_path,
        "EnvironmentVariables": environment_vars or {},
    }
    return plistlib.dumps(plist_dict)


def main():
    python_path = (
        input("Enter the path to the python executable: ") or "/usr/bin/python3"
    )
    bot_script = input("Enter the path to the bot script: ")
    if not os.path.exists(bot_script):
        print(f"error: {bot_script} does not exist")
        sys.exit(1)

    working_dir = os.path.dirname(os.path.abspath(bot_script))

    stdout_path = os.path.join(LOG_DIR, "{}-stdout.log".format(PLIST_LABEL))
    stderr_path = os.path.join(LOG_DIR, "{}-stderr.log".format(PLIST_LABEL))

    plist_content = create_plist(
        working_dir,
        python_path,
        [bot_script],
        stdout_path,
        stderr_path,
        {"DISCORD_TOKEN": DISCORD_TOKEN},
    )

    with open(PLIST_PATH, "wb") as f:
        f.write(plist_content)
    print(f"Created {PLIST_PATH}")


if __name__ == "__main__":
    main()
