import os
import sys
import subprocess
import argparse
import plistlib

from launchctl_config import PLIST_LABEL, PLIST_PATH, LOG_DIR

def check_service_status():
    try:
        result = subprocess.run(
            ["launchctl", "list"], stdout=subprocess.PIPE, check=True
        )
        for line in result.stdout.decode("utf-8").splitlines():
            if PLIST_LABEL not in line:
                continue
            parts = line.split()
            if len(parts) < 3:
                return False, f"Service {PLIST_LABEL} is found (Status: {line})"
            pid = parts[0]
            status = parts[1]
            service_label = parts[2]
            if pid == "-":
                return False, f"Service {service_label} is loaded but not running"
            else:
                return (
                    True,
                    f"Service {service_label} is running(PID: {pid}, Status: {status})",
                )

        if os.path.exists(PLIST_PATH):
            return False, f"Service {PLIST_LABEL} is exist but not loaded"
        else:
            return False, f"Service {PLIST_LABEL} is not found"
    except subprocess.CalledProcessError as e:
        return False, f"Failed to check service status: {e}"


def show_service_status():
    is_running, status = check_service_status()
    mark = "OK" if is_running else "NG"
    print(f"{mark}: {status}")


def get_log_paths():
    with open(PLIST_PATH, "rb") as f:
        plist = plistlib.load(f)

    stdlog = plist.get("StandardOutPath", "")
    errlog = plist.get("StandardErrorPath", "")
    return stdlog, errlog


def show_logs(lines):
    stdlog, errlog = get_log_paths()
    if os.path.exists(stdlog):
        print(f"StandardOutPath: {stdlog}")
        subprocess.run(["tail", "-n", f"{lines}", stdlog])
    else:
        print(f"StandardOutPath: {stdlog} is not found")

    if os.path.exists(errlog):
        print(f"StandardErrorPath: {errlog}")
        subprocess.run(["tail", "-n", f"{lines}", errlog])
    else:
        print(f"StandardErrorPath: {errlog} is not found")


def main():
    parser = argparse.ArgumentParser(
        description="script to manage Discord Hellowork launchctl service"
    )

    subparsers = parser.add_subparsers(dest="command", help="run command")

    status_parser = subparsers.add_parser("status", help="status of the service")
    log_parser = subparsers.add_parser("log", help="show log of the service")
    log_parser.add_argument(
        "--lines", type=int, default=10, help="number of lines to show(default: 10)"
    )

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    elif args.command == "status":
        show_service_status()
    elif args.command == "log":
        show_logs(args.lines)


if __name__ == "__main__":
    main()

