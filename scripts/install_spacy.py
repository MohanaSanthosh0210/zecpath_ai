"""
Simple helper to install spaCy and download the English small model.
Run from the virtualenv you plan to use for this project.

Usage:
    python scripts/install_spacy.py
"""
import subprocess
import sys

def run(cmd):
    print("Running:", " ".join(cmd))
    subprocess.check_call(cmd)


def main():
    try:
        run([sys.executable, "-m", "pip", "install", "spacy"])
        run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("spaCy and model installed successfully.")
    except subprocess.CalledProcessError as e:
        print("Installation failed:", e)
        sys.exit(1)

if __name__ == '__main__':
    main()
