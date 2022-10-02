#!/bin/bash
# echo "Running Cron Task"

# chmod +x cron-task.sh
# to make this .sh file executable
# crontab -e
# to edit the crontab

# Load virtualenv and run the script
source /Users/your/path/to/folder/venv-py3.10-mac/bin/activate
export PYTHONPATH="${PYTHONPATH}:/Users/your/path/to/folder"
cd /Users/your/path/to/folder || return
python main.py
