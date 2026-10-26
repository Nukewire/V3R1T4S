#!/bin/sh
# Runs the standalone stdlib checker (2-4 minutes). Last line: PASS or FAIL.
cd "$(dirname "$0")"
python verify_standalone.py 2>&1
