import os
import sys

username = os.environ.get('USER')
if not username:
    print("Could not get username")
    sys.exit(1)

PLIST_LABEL = f"com.{username}.discord_hellowork"

agents_dir = os.path.expanduser("~/Library/LaunchAgents")
LOG_DIR = os.path.expanduser("~/Library/Logs/DiscordHelloWork")

plist_filename = f"{PLIST_LABEL}.plist"
PLIST_PATH = os.path.join(agents_dir, plist_filename)

def ensure_dir_exists():
    os.makedirs(agents_dir, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
