from pathlib import Path
from subprocess import call

if __name__ == "__main__":
    for day in range(1, 26):
        daydir = (Path.cwd() / f"{day:02d}")
        if daydir.exists():
            call(f"echo === Day {day:02d} ===", shell=True)
            for pyfile in daydir.glob("*.py"):
                call(f"python {pyfile.name}", shell=True, cwd=daydir)
            call("echo", shell=True)
