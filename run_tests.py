#!/usr/bin/env python3
"""Simple runner to execute tests and show results."""

import subprocess
import sys

result = subprocess.run(
    [sys.executable, "test_agrolink.py"],
    cwd="c:\\Abzar\\Projects\\Agro Link"
)

sys.exit(result.returncode)
