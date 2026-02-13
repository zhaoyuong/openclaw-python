#!/bin/bash
# OpenClaw Quick Run Script

# Change to project directory
cd "$(dirname "$0")"

# Run OpenClaw using virtual environment Python
.venv/bin/python -m openclaw.cli.main "$@"
