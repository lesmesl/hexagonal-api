import subprocess
import sys


def run_command(command):
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main():
    commands = [
        "poetry run isort .",
        "poetry run autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place .",
        "poetry run black .",
    ]

    for command in commands:
        run_command(command)


if __name__ == "__main__":
    main()
